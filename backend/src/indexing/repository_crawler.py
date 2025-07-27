"""
Repository crawler for cloning and crawling repositories from various sources.
"""

import os
import shutil
import tempfile
from typing import List, Dict, Any, Optional, Generator
from pathlib import Path
import git
from git import Repo, GitCommandError
import requests
from urllib.parse import urlparse
import logging

from ..config.settings import settings
from ..models.repository import Repository, RepositoryType, RepositoryStatus
from ..integrations.github_api import GitHubAPI
from ..integrations.gitlab_api import GitLabAPI
from ..integrations.bitbucket_api import BitbucketAPI


class RepositoryCrawler:
    """Crawler for cloning and managing repositories."""
    
    def __init__(self):
        """Initialize the repository crawler."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.github_api = GitHubAPI()
        self.gitlab_api = GitLabAPI()
        self.bitbucket_api = BitbucketAPI()
        self.logger = logging.getLogger(__name__)
    
    def clone_repository(self, repository: Repository, branch: str = None) -> Optional[Path]:
        """Clone a repository to a temporary directory."""
        try:
            # Create repository directory
            repo_name = repository.name
            repo_path = self.temp_dir / repo_name
            
            if repo_path.exists():
                shutil.rmtree(repo_path)
            
            repo_path.mkdir(parents=True, exist_ok=True)
            
            # Clone repository
            clone_url = repository.clone_url
            if repository.is_private and repository.integration_token:
                # Use token for private repositories
                parsed_url = urlparse(clone_url)
                clone_url = f"{parsed_url.scheme}://{repository.integration_token}@{parsed_url.netloc}{parsed_url.path}"
            
            self.logger.info(f"Cloning repository: {clone_url}")
            
            # Clone with specific branch if provided
            if branch:
                repo = Repo.clone_from(clone_url, repo_path, branch=branch, depth=1)
            else:
                repo = Repo.clone_from(clone_url, repo_path, depth=1)
            
            self.logger.info(f"Successfully cloned repository to {repo_path}")
            return repo_path
            
        except GitCommandError as e:
            self.logger.error(f"Git error cloning repository: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error cloning repository: {e}")
            return None
    
    def crawl_repository(self, repo_path: Path) -> Generator[Path, None, None]:
        """Crawl a repository and yield file paths."""
        try:
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Check if file should be processed
                    if self._should_process_file(file_path, repo_path):
                        yield file_path
                        
        except Exception as e:
            self.logger.error(f"Error crawling repository: {e}")
    
    def _should_process_file(self, file_path: Path, repo_path: Path) -> bool:
        """Check if a file should be processed."""
        # Skip files that are too large
        try:
            if file_path.stat().st_size > settings.MAX_FILE_SIZE:
                return False
        except OSError:
            return False
        
        # Skip binary files
        if self._is_binary_file(file_path):
            return False
        
        # Skip excluded patterns
        relative_path = file_path.relative_to(repo_path)
        for pattern in settings.EXCLUDED_PATTERNS:
            if pattern.startswith('*'):
                if str(relative_path).endswith(pattern[1:]):
                    return False
            elif pattern in str(relative_path):
                return False
        
        return True
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except Exception:
            return True
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get repository information from various sources."""
        try:
            parsed_url = urlparse(repo_url)
            
            if 'github.com' in parsed_url.netloc:
                return self._get_github_repo_info(repo_url)
            elif 'gitlab.com' in parsed_url.netloc or 'gitlab' in parsed_url.netloc:
                return self._get_gitlab_repo_info(repo_url)
            elif 'bitbucket.org' in parsed_url.netloc:
                return self._get_bitbucket_repo_info(repo_url)
            else:
                return self._get_generic_repo_info(repo_url)
                
        except Exception as e:
            self.logger.error(f"Error getting repository info: {e}")
            return None
    
    def _get_github_repo_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get GitHub repository information."""
        try:
            # Extract owner and repo name from URL
            parts = repo_url.rstrip('/').split('/')
            if len(parts) >= 2:
                owner = parts[-2]
                repo_name = parts[-1]
                
                repo_info = self.github_api.get_repository(owner, repo_name)
                if repo_info:
                    return {
                        'name': repo_info['name'],
                        'full_name': repo_info['full_name'],
                        'description': repo_info.get('description'),
                        'url': repo_info['html_url'],
                        'clone_url': repo_info['clone_url'],
                        'ssh_url': repo_info['ssh_url'],
                        'api_url': repo_info['url'],
                        'repository_type': RepositoryType.GITHUB,
                        'visibility': RepositoryVisibility.PUBLIC if not repo_info['private'] else RepositoryVisibility.PRIVATE,
                        'owner': repo_info['owner']['login'],
                        'owner_type': repo_info['owner']['type'],
                        'stars': repo_info['stargazers_count'],
                        'forks': repo_info['forks_count'],
                        'watchers': repo_info['watchers_count'],
                        'open_issues': repo_info['open_issues_count'],
                        'size': repo_info['size'],
                        'primary_language': repo_info.get('language'),
                        'topics': repo_info.get('topics', []),
                        'license': repo_info.get('license', {}).get('name') if repo_info.get('license') else None,
                        'default_branch': repo_info['default_branch'],
                        'has_wiki': repo_info['has_wiki'],
                        'has_issues': repo_info['has_issues'],
                        'has_projects': repo_info['has_projects'],
                        'has_downloads': repo_info['has_downloads'],
                        'created_at': repo_info['created_at'],
                        'updated_at': repo_info['updated_at'],
                        'pushed_at': repo_info['pushed_at']
                    }
        except Exception as e:
            self.logger.error(f"Error getting GitHub repo info: {e}")
        
        return None
    
    def _get_gitlab_repo_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get GitLab repository information."""
        try:
            repo_info = self.gitlab_api.get_repository_info(repo_url)
            if repo_info:
                return {
                    'name': repo_info['name'],
                    'full_name': repo_info['path_with_namespace'],
                    'description': repo_info.get('description'),
                    'url': repo_info['web_url'],
                    'clone_url': repo_info['http_url_to_repo'],
                    'ssh_url': repo_info['ssh_url_to_repo'],
                    'api_url': repo_info['_links']['self'],
                    'repository_type': RepositoryType.GITLAB,
                    'visibility': repo_info['visibility'],
                    'owner': repo_info['namespace']['name'],
                    'owner_type': repo_info['namespace']['kind'],
                    'stars': repo_info.get('star_count', 0),
                    'forks': repo_info.get('forks_count', 0),
                    'open_issues': repo_info.get('open_issues_count', 0),
                    'size': repo_info.get('statistics', {}).get('repository_size', 0),
                    'default_branch': repo_info['default_branch'],
                    'has_wiki': repo_info.get('wiki_enabled', False),
                    'has_issues': repo_info.get('issues_enabled', False),
                    'created_at': repo_info['created_at'],
                    'updated_at': repo_info['last_activity_at']
                }
        except Exception as e:
            self.logger.error(f"Error getting GitLab repo info: {e}")
        
        return None
    
    def _get_bitbucket_repo_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get Bitbucket repository information."""
        try:
            repo_info = self.bitbucket_api.get_repository_info(repo_url)
            if repo_info:
                return {
                    'name': repo_info['name'],
                    'full_name': repo_info['full_name'],
                    'description': repo_info.get('description'),
                    'url': repo_info['links']['html']['href'],
                    'clone_url': repo_info['links']['clone'][0]['href'],
                    'ssh_url': repo_info['links']['clone'][1]['href'],
                    'api_url': repo_info['links']['self']['href'],
                    'repository_type': RepositoryType.BITBUCKET,
                    'visibility': 'private' if repo_info['is_private'] else 'public',
                    'owner': repo_info['owner']['display_name'],
                    'owner_type': repo_info['owner']['type'],
                    'size': repo_info.get('size', 0),
                    'default_branch': repo_info['mainbranch']['name'],
                    'created_at': repo_info['created_on'],
                    'updated_at': repo_info['updated_on']
                }
        except Exception as e:
            self.logger.error(f"Error getting Bitbucket repo info: {e}")
        
        return None
    
    def _get_generic_repo_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get generic repository information."""
        try:
            parsed_url = urlparse(repo_url)
            repo_name = Path(parsed_url.path).stem
            
            return {
                'name': repo_name,
                'full_name': repo_name,
                'description': None,
                'url': repo_url,
                'clone_url': repo_url,
                'repository_type': RepositoryType.GIT,
                'visibility': RepositoryVisibility.PUBLIC,
                'owner': parsed_url.netloc,
                'owner_type': 'Unknown',
                'stars': 0,
                'forks': 0,
                'watchers': 0,
                'open_issues': 0,
                'size': 0,
                'default_branch': 'main',
                'has_wiki': False,
                'has_issues': False,
                'has_projects': False,
                'has_downloads': False
            }
        except Exception as e:
            self.logger.error(f"Error getting generic repo info: {e}")
            return None
    
    def get_repository_branches(self, repo_path: Path) -> List[str]:
        """Get list of branches in a repository."""
        try:
            repo = Repo(repo_path)
            branches = []
            
            for branch in repo.branches:
                branches.append(branch.name)
            
            return branches
        except Exception as e:
            self.logger.error(f"Error getting repository branches: {e}")
            return []
    
    def get_repository_tags(self, repo_path: Path) -> List[str]:
        """Get list of tags in a repository."""
        try:
            repo = Repo(repo_path)
            tags = []
            
            for tag in repo.tags:
                tags.append(tag.name)
            
            return tags
        except Exception as e:
            self.logger.error(f"Error getting repository tags: {e}")
            return []
    
    def get_repository_languages(self, repo_path: Path) -> Dict[str, int]:
        """Analyze repository to determine language distribution."""
        try:
            language_stats = {}
            
            for file_path in self.crawl_repository(repo_path):
                language = self._detect_language_from_file(file_path)
                if language:
                    language_stats[language] = language_stats.get(language, 0) + 1
            
            return language_stats
        except Exception as e:
            self.logger.error(f"Error analyzing repository languages: {e}")
            return {}
    
    def _detect_language_from_file(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension."""
        ext = file_path.suffix.lower()
        
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.cc': 'C++',
            '.cxx': 'C++',
            '.hpp': 'C++',
            '.h': 'C++',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.r': 'R',
            '.m': 'Objective-C',
            '.mm': 'Objective-C++',
            '.pl': 'Perl',
            '.sh': 'Shell',
            '.bash': 'Shell',
            '.zsh': 'Shell',
            '.fish': 'Shell',
            '.sql': 'SQL',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.sass': 'Sass',
            '.less': 'Less',
            '.vue': 'Vue',
            '.svelte': 'Svelte',
            '.dart': 'Dart',
            '.lua': 'Lua',
            '.groovy': 'Groovy',
            '.clj': 'Clojure',
            '.hs': 'Haskell',
            '.ml': 'OCaml',
            '.fs': 'F#',
            '.elm': 'Elm',
            '.ex': 'Elixir',
            '.exs': 'Elixir',
            '.erl': 'Erlang',
            '.beam': 'Erlang',
            '.cr': 'Crystal',
            '.nim': 'Nim',
            '.zig': 'Zig',
            '.v': 'V',
            '.d': 'D',
            '.pas': 'Pascal',
            '.f90': 'Fortran',
            '.f95': 'Fortran',
            '.f03': 'Fortran',
            '.f08': 'Fortran',
            '.ada': 'Ada',
            '.adb': 'Ada',
            '.ads': 'Ada',
            '.cob': 'COBOL',
            '.cbl': 'COBOL',
            '.asm': 'Assembly',
            '.s': 'Assembly',
            '.S': 'Assembly',
            '.nasm': 'Assembly',
            '.yasm': 'Assembly',
            '.masm': 'Assembly',
            '.gas': 'Assembly'
        }
        
        return language_map.get(ext)
    
    def cleanup_repository(self, repo_path: Path):
        """Clean up a cloned repository."""
        try:
            if repo_path.exists():
                shutil.rmtree(repo_path)
                self.logger.info(f"Cleaned up repository: {repo_path}")
        except Exception as e:
            self.logger.error(f"Error cleaning up repository: {e}")
    
    def cleanup_all(self):
        """Clean up all temporary repositories."""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                self.logger.info("Cleaned up all temporary repositories")
        except Exception as e:
            self.logger.error(f"Error cleaning up temporary directories: {e}")
    
    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup_all() 