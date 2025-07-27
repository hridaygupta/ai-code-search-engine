"""
Repository model for managing repository metadata and indexing information.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class RepositoryStatus(str, Enum):
    """Repository indexing status."""
    PENDING = "pending"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"
    UPDATING = "updating"


class RepositoryType(str, Enum):
    """Types of repositories."""
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"
    LOCAL = "local"
    GIT = "git"


class RepositoryVisibility(str, Enum):
    """Repository visibility levels."""
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"


class Repository(BaseModel):
    """Model representing a repository with comprehensive metadata."""
    
    # Basic identification
    id: str = Field(..., description="Unique identifier for the repository")
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/repo)")
    description: Optional[str] = Field(None, description="Repository description")
    
    # Repository source information
    url: str = Field(..., description="Repository URL")
    clone_url: str = Field(..., description="Git clone URL")
    ssh_url: Optional[str] = Field(None, description="SSH clone URL")
    api_url: Optional[str] = Field(None, description="API URL for the repository")
    
    # Repository type and visibility
    repository_type: RepositoryType = Field(..., description="Type of repository")
    visibility: RepositoryVisibility = Field(..., description="Repository visibility")
    
    # Owner information
    owner: str = Field(..., description="Repository owner")
    owner_type: str = Field(default="User", description="Owner type (User/Organization)")
    
    # Repository statistics
    stars: int = Field(default=0, description="Number of stars")
    forks: int = Field(default=0, description="Number of forks")
    watchers: int = Field(default=0, description="Number of watchers")
    open_issues: int = Field(default=0, description="Number of open issues")
    size: int = Field(default=0, description="Repository size in bytes")
    
    # Language and technology information
    primary_language: Optional[str] = Field(None, description="Primary programming language")
    languages: Dict[str, int] = Field(default_factory=dict, description="Language statistics")
    topics: List[str] = Field(default_factory=list, description="Repository topics")
    license: Optional[str] = Field(None, description="Repository license")
    
    # Git information
    default_branch: str = Field(default="main", description="Default branch")
    branches: List[str] = Field(default_factory=list, description="Available branches")
    tags: List[str] = Field(default_factory=list, description="Available tags")
    last_commit_hash: Optional[str] = Field(None, description="Last commit hash")
    last_commit_message: Optional[str] = Field(None, description="Last commit message")
    last_commit_author: Optional[str] = Field(None, description="Last commit author")
    last_commit_date: Optional[datetime] = Field(None, description="Last commit date")
    
    # Indexing information
    status: RepositoryStatus = Field(default=RepositoryStatus.PENDING, description="Indexing status")
    indexed_branches: List[str] = Field(default_factory=list, description="Indexed branches")
    total_files: int = Field(default=0, description="Total number of files")
    indexed_files: int = Field(default=0, description="Number of indexed files")
    total_snippets: int = Field(default=0, description="Total number of code snippets")
    indexed_snippets: int = Field(default=0, description="Number of indexed snippets")
    
    # Indexing progress and errors
    indexing_progress: float = Field(default=0.0, description="Indexing progress (0-100)")
    indexing_started_at: Optional[datetime] = Field(None, description="Indexing start time")
    indexing_completed_at: Optional[datetime] = Field(None, description="Indexing completion time")
    indexing_duration: Optional[float] = Field(None, description="Indexing duration in seconds")
    indexing_errors: List[str] = Field(default_factory=list, description="Indexing errors")
    
    # Quality metrics
    quality_score: float = Field(default=0.0, description="Repository quality score")
    documentation_score: float = Field(default=0.0, description="Documentation quality score")
    test_coverage: float = Field(default=0.0, description="Test coverage percentage")
    code_quality_score: float = Field(default=0.0, description="Overall code quality score")
    
    # Access and permissions
    is_private: bool = Field(default=False, description="Whether the repository is private")
    has_wiki: bool = Field(default=False, description="Whether the repository has a wiki")
    has_issues: bool = Field(default=True, description="Whether the repository has issues enabled")
    has_projects: bool = Field(default=False, description="Whether the repository has projects enabled")
    has_downloads: bool = Field(default=False, description="Whether the repository has downloads enabled")
    
    # Webhook and integration information
    webhook_url: Optional[str] = Field(None, description="Webhook URL for updates")
    webhook_secret: Optional[str] = Field(None, description="Webhook secret")
    integration_token: Optional[str] = Field(None, description="Integration access token")
    
    # Configuration
    indexing_config: Dict[str, Any] = Field(default_factory=dict, description="Indexing configuration")
    search_config: Dict[str, Any] = Field(default_factory=dict, description="Search configuration")
    exclude_patterns: List[str] = Field(default_factory=list, description="Patterns to exclude from indexing")
    include_patterns: List[str] = Field(default_factory=list, description="Patterns to include in indexing")
    
    # Metadata and annotations
    tags: List[str] = Field(default_factory=list, description="User-defined tags")
    annotations: Dict[str, Any] = Field(default_factory=dict, description="Additional annotations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    pushed_at: Optional[datetime] = Field(None, description="Last push timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RepositoryCreate(BaseModel):
    """Model for creating a new repository."""
    name: str
    full_name: str
    url: str
    clone_url: str
    repository_type: RepositoryType
    visibility: RepositoryVisibility
    owner: str
    description: Optional[str] = None
    ssh_url: Optional[str] = None
    api_url: Optional[str] = None
    owner_type: str = "User"
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    open_issues: int = 0
    size: int = 0
    primary_language: Optional[str] = None
    languages: Dict[str, int] = {}
    topics: List[str] = []
    license: Optional[str] = None
    default_branch: str = "main"
    branches: List[str] = []
    tags: List[str] = []
    is_private: bool = False
    has_wiki: bool = False
    has_issues: bool = True
    has_projects: bool = False
    has_downloads: bool = False
    indexing_config: Dict[str, Any] = {}
    search_config: Dict[str, Any] = {}
    exclude_patterns: List[str] = []
    include_patterns: List[str] = []
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class RepositoryUpdate(BaseModel):
    """Model for updating an existing repository."""
    description: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    watchers: Optional[int] = None
    open_issues: Optional[int] = None
    size: Optional[int] = None
    primary_language: Optional[str] = None
    languages: Optional[Dict[str, int]] = None
    topics: Optional[List[str]] = None
    license: Optional[str] = None
    branches: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    last_commit_hash: Optional[str] = None
    last_commit_message: Optional[str] = None
    last_commit_author: Optional[str] = None
    last_commit_date: Optional[datetime] = None
    status: Optional[RepositoryStatus] = None
    indexed_branches: Optional[List[str]] = None
    total_files: Optional[int] = None
    indexed_files: Optional[int] = None
    total_snippets: Optional[int] = None
    indexed_snippets: Optional[int] = None
    indexing_progress: Optional[float] = None
    indexing_started_at: Optional[datetime] = None
    indexing_completed_at: Optional[datetime] = None
    indexing_duration: Optional[float] = None
    indexing_errors: Optional[List[str]] = None
    quality_score: Optional[float] = None
    documentation_score: Optional[float] = None
    test_coverage: Optional[float] = None
    code_quality_score: Optional[float] = None
    pushed_at: Optional[datetime] = None
    indexing_config: Optional[Dict[str, Any]] = None
    search_config: Optional[Dict[str, Any]] = None
    exclude_patterns: Optional[List[str]] = None
    include_patterns: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    annotations: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class RepositorySearch(BaseModel):
    """Model for repository search results."""
    repository: Repository
    relevance_score: float = Field(..., description="Relevance score")
    match_highlights: List[Dict[str, Any]] = Field(default_factory=list, description="Highlighted matches")


class RepositoryStats(BaseModel):
    """Model for repository statistics."""
    total_repositories: int
    indexed_repositories: int
    total_files: int
    total_snippets: int
    languages_distribution: Dict[str, int]
    repository_types_distribution: Dict[str, int]
    indexing_status_distribution: Dict[str, int]
    average_quality_score: float
    average_documentation_score: float
    average_test_coverage: float 