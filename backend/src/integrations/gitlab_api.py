"""
GitLab API integration for repository management.
"""

import logging
from typing import List, Dict, Any, Optional
import requests

from ..config.settings import settings


class GitLabAPI:
    """GitLab API client for repository operations."""
    
    def __init__(self):
        """Initialize GitLab API client."""
        self.logger = logging.getLogger(__name__)
        self.token = settings.GITLAB_TOKEN
        self.base_url = "https://gitlab.com/api/v4"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "CodeSearch-Engine"
        }
        
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get repository information from GitLab."""
        try:
            # Extract project ID from URL
            project_id = self._extract_project_id(repo_url)
            if not project_id:
                return None
            
            url = f"{self.base_url}/projects/{project_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"Failed to get repo info: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting repository info: {e}")
            return None
    
    def _extract_project_id(self, repo_url: str) -> Optional[str]:
        """Extract project ID from GitLab URL."""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd need to handle various GitLab URL formats
            parts = repo_url.rstrip('/').split('/')
            if len(parts) >= 2:
                return f"{parts[-2]}/{parts[-1]}"
            return None
        except Exception:
            return None 