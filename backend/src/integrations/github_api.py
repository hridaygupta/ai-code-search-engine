"""
GitHub API integration for repository management.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import requests
from datetime import datetime

from ..config.settings import settings


class GitHubAPI:
    """GitHub API client for repository operations."""
    
    def __init__(self):
        """Initialize GitHub API client."""
        self.logger = logging.getLogger(__name__)
        self.token = settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeSearch-Engine"
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get repository information from GitHub."""
        try:
            # Extract owner and repo from URL
            parts = repo_url.rstrip('/').split('/')
            if len(parts) < 2:
                return None
            
            owner = parts[-2]
            repo = parts[-1]
            
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"Failed to get repo info: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting repository info: {e}")
            return None
    
    def get_repository_files(self, repo_url: str, path: str = "") -> List[Dict[str, Any]]:
        """Get files from repository."""
        try:
            # Extract owner and repo from URL
            parts = repo_url.rstrip('/').split('/')
            if len(parts) < 2:
                return []
            
            owner = parts[-2]
            repo = parts[-1]
            
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"Failed to get files: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting repository files: {e}")
            return []
    
    def get_file_content(self, repo_url: str, file_path: str) -> Optional[str]:
        """Get file content from repository."""
        try:
            # Extract owner and repo from URL
            parts = repo_url.rstrip('/').split('/')
            if len(parts) < 2:
                return None
            
            owner = parts[-2]
            repo = parts[-1]
            
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                import base64
                content = response.json().get('content', '')
                return base64.b64decode(content).decode('utf-8')
            else:
                self.logger.warning(f"Failed to get file content: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting file content: {e}")
            return None 