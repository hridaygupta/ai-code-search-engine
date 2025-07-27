"""
User model for authentication and user management.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    """User roles and permissions."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"


class UserStatus(str, Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User(BaseModel):
    """Model representing a user account."""
    
    # Basic information
    id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, description="Full name")
    
    # Account information
    role: UserRole = Field(default=UserRole.USER, description="User role")
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="Account status")
    is_verified: bool = Field(default=False, description="Email verification status")
    is_premium: bool = Field(default=False, description="Premium account status")
    
    # Authentication
    hashed_password: str = Field(..., description="Hashed password")
    salt: str = Field(..., description="Password salt")
    password_changed_at: datetime = Field(default_factory=datetime.utcnow, description="Password change timestamp")
    
    # Profile information
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    bio: Optional[str] = Field(None, description="User biography")
    location: Optional[str] = Field(None, description="User location")
    website: Optional[str] = Field(None, description="Personal website")
    company: Optional[str] = Field(None, description="Company or organization")
    
    # Preferences
    preferred_languages: List[str] = Field(default_factory=list, description="Preferred programming languages")
    search_preferences: Dict[str, Any] = Field(default_factory=dict, description="Search preferences")
    notification_settings: Dict[str, bool] = Field(default_factory=dict, description="Notification settings")
    theme_preference: str = Field(default="light", description="UI theme preference")
    
    # Usage statistics
    total_searches: int = Field(default=0, description="Total number of searches performed")
    total_bookmarks: int = Field(default=0, description="Total number of bookmarked snippets")
    total_contributions: int = Field(default=0, description="Total contributions made")
    last_active: datetime = Field(default_factory=datetime.utcnow, description="Last activity timestamp")
    
    # Repository access
    accessible_repositories: List[str] = Field(default_factory=list, description="Repository IDs user can access")
    owned_repositories: List[str] = Field(default_factory=list, description="Repository IDs user owns")
    starred_repositories: List[str] = Field(default_factory=list, description="Starred repository IDs")
    
    # API access
    api_key: Optional[str] = Field(None, description="API access key")
    api_quota: int = Field(default=1000, description="API request quota")
    api_usage: int = Field(default=0, description="API requests used")
    api_quota_reset: datetime = Field(default_factory=datetime.utcnow, description="API quota reset date")
    
    # Security
    two_factor_enabled: bool = Field(default=False, description="Two-factor authentication status")
    two_factor_secret: Optional[str] = Field(None, description="Two-factor authentication secret")
    login_attempts: int = Field(default=0, description="Failed login attempts")
    locked_until: Optional[datetime] = Field(None, description="Account lock expiration")
    
    # External integrations
    github_username: Optional[str] = Field(None, description="GitHub username")
    gitlab_username: Optional[str] = Field(None, description="GitLab username")
    bitbucket_username: Optional[str] = Field(None, description="Bitbucket username")
    external_id: Optional[str] = Field(None, description="External service user ID")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="User tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None
    preferred_languages: List[str] = []
    search_preferences: Dict[str, Any] = {}
    notification_settings: Dict[str, bool] = {}
    theme_preference: str = "light"
    github_username: Optional[str] = None
    gitlab_username: Optional[str] = None
    bitbucket_username: Optional[str] = None
    external_id: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_verified: Optional[bool] = None
    is_premium: Optional[bool] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None
    preferred_languages: Optional[List[str]] = None
    search_preferences: Optional[Dict[str, Any]] = None
    notification_settings: Optional[Dict[str, bool]] = None
    theme_preference: Optional[str] = None
    github_username: Optional[str] = None
    gitlab_username: Optional[str] = None
    bitbucket_username: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class UserLogin(BaseModel):
    """Model for user login."""
    username: str
    password: str
    remember_me: bool = False
    two_factor_code: Optional[str] = None


class UserPasswordChange(BaseModel):
    """Model for password change."""
    current_password: str
    new_password: str
    confirm_password: str


class UserPasswordReset(BaseModel):
    """Model for password reset."""
    email: EmailStr


class UserPasswordResetConfirm(BaseModel):
    """Model for password reset confirmation."""
    token: str
    new_password: str
    confirm_password: str


class UserProfile(BaseModel):
    """Model for user profile information."""
    id: str
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole
    status: UserStatus
    is_verified: bool
    is_premium: bool
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None
    preferred_languages: List[str]
    search_preferences: Dict[str, Any]
    notification_settings: Dict[str, bool]
    theme_preference: str
    total_searches: int
    total_bookmarks: int
    total_contributions: int
    last_active: datetime
    accessible_repositories: List[str]
    owned_repositories: List[str]
    starred_repositories: List[str]
    api_quota: int
    api_usage: int
    api_quota_reset: datetime
    two_factor_enabled: bool
    github_username: Optional[str] = None
    gitlab_username: Optional[str] = None
    bitbucket_username: Optional[str] = None
    tags: List[str]
    created_at: datetime
    last_login: Optional[datetime] = None


class UserStats(BaseModel):
    """Model for user statistics."""
    user_id: str
    total_searches: int
    total_bookmarks: int
    total_contributions: int
    searches_this_month: int
    searches_this_week: int
    searches_today: int
    average_search_time: float
    favorite_languages: List[str]
    favorite_repositories: List[str]
    search_patterns: Dict[str, int]
    activity_heatmap: Dict[str, int]
    last_active: datetime
    created_at: datetime


class UserSession(BaseModel):
    """Model for user session information."""
    session_id: str
    user_id: str
    ip_address: str
    user_agent: str
    is_active: bool
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class UserToken(BaseModel):
    """Model for user authentication tokens."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None 