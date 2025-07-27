"""
Bitbucket API integration for repository management.
"""

import logging
from typing import List, Dict, Any, Optional
import requests

from ..config.settings import settings


class BitbucketAPI:
    """Bitbucket API client for repository operations."""
    
    def __init__(self):
        """Initialize Bitbucket API client."""
        self.logger = logging.getLogger(__name__)
        self.token = settings.BITBUCKET_TOKEN
        self.base_url = "https://api.bitbucket.org/2.0"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "CodeSearch-Engine"
        }
        
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get repository information from Bitbucket."""
        try:
            # Extract workspace and repo from URL
            workspace, repo = self._extract_workspace_repo(repo_url)
            if not workspace or not repo:
                return None
            
            url = f"{self.base_url}/repositories/{workspace}/{repo}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"Failed to get repo info: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting repository info: {e}")
            return None
    
    def _extract_workspace_repo(self, repo_url: str) -> tuple[Optional[str], Optional[str]]:
        """Extract workspace and repo from Bitbucket URL."""
        try:
            parts = repo_url.rstrip('/').split('/')
            if len(parts) >= 2:
                return parts[-2], parts[-1]
            return None, None
        except Exception:
            return None, None 