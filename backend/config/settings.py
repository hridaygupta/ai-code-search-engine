"""
Configuration settings for the Contextual Code Search Engine.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "Contextual Code Search Engine"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    
    # Database
    DATABASE_URL: str = Field(env="DATABASE_URL")
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    NEO4J_URI: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    NEO4J_USER: str = Field(default="neo4j", env="NEO4J_USER")
    NEO4J_PASSWORD: str = Field(default="password", env="NEO4J_PASSWORD")
    
    # Vector Database
    QDRANT_URL: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = Field(default="http://localhost:9200", env="ELASTICSEARCH_URL")
    ELASTICSEARCH_USERNAME: Optional[str] = Field(default=None, env="ELASTICSEARCH_USERNAME")
    ELASTICSEARCH_PASSWORD: Optional[str] = Field(default=None, env="ELASTICSEARCH_PASSWORD")
    
    # AI/ML Models
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    
    # Model Configuration
    EMBEDDING_MODEL: str = Field(default="microsoft/codebert-base", env="EMBEDDING_MODEL")
    SIMILARITY_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", env="SIMILARITY_MODEL")
    CODE_GENERATION_MODEL: str = Field(default="Salesforce/codet5-base", env="CODE_GENERATION_MODEL")
    
    # GitHub Integration
    GITHUB_CLIENT_ID: Optional[str] = Field(default=None, env="GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: Optional[str] = Field(default=None, env="GITHUB_CLIENT_SECRET")
    GITHUB_ACCESS_TOKEN: Optional[str] = Field(default=None, env="GITHUB_ACCESS_TOKEN")
    
    # GitLab Integration
    GITLAB_CLIENT_ID: Optional[str] = Field(default=None, env="GITLAB_CLIENT_ID")
    GITLAB_CLIENT_SECRET: Optional[str] = Field(default=None, env="GITLAB_CLIENT_SECRET")
    GITLAB_URL: str = Field(default="https://gitlab.com", env="GITLAB_URL")
    
    # Bitbucket Integration
    BITBUCKET_CLIENT_ID: Optional[str] = Field(default=None, env="BITBUCKET_CLIENT_ID")
    BITBUCKET_CLIENT_SECRET: Optional[str] = Field(default=None, env="BITBUCKET_CLIENT_SECRET")
    
    # Authentication
    SECRET_KEY: str = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:3000"], env="ALLOWED_ORIGINS")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Indexing
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    BATCH_SIZE: int = Field(default=100, env="BATCH_SIZE")
    INDEXING_WORKERS: int = Field(default=4, env="INDEXING_WORKERS")
    
    # Search
    MAX_SEARCH_RESULTS: int = Field(default=100, env="MAX_SEARCH_RESULTS")
    SIMILARITY_THRESHOLD: float = Field(default=0.7, env="SIMILARITY_THRESHOLD")
    
    # Caching
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    SEARCH_CACHE_TTL: int = Field(default=1800, env="SEARCH_CACHE_TTL")  # 30 minutes
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    TEMP_DIR: str = Field(default="./temp", env="TEMP_DIR")
    
    # Security
    ENABLE_HTTPS: bool = Field(default=False, env="ENABLE_HTTPS")
    SSL_CERT_FILE: Optional[str] = Field(default=None, env="SSL_CERT_FILE")
    SSL_KEY_FILE: Optional[str] = Field(default=None, env="SSL_KEY_FILE")
    
    # Development
    AUTO_RELOAD: bool = Field(default=False, env="AUTO_RELOAD")
    ENABLE_SWAGGER: bool = Field(default=True, env="ENABLE_SWAGGER")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Language-specific configurations
SUPPORTED_LANGUAGES = {
    "python": {
        "extensions": [".py", ".pyx", ".pyi"],
        "parser": "python",
        "keywords": ["def", "class", "import", "from", "if", "for", "while", "try", "except"],
        "complexity_threshold": 10
    },
    "javascript": {
        "extensions": [".js", ".jsx", ".mjs"],
        "parser": "javascript",
        "keywords": ["function", "const", "let", "var", "if", "for", "while", "try", "catch"],
        "complexity_threshold": 8
    },
    "typescript": {
        "extensions": [".ts", ".tsx"],
        "parser": "typescript",
        "keywords": ["function", "const", "let", "var", "interface", "type", "class"],
        "complexity_threshold": 8
    },
    "java": {
        "extensions": [".java"],
        "parser": "java",
        "keywords": ["public", "private", "class", "interface", "method", "static"],
        "complexity_threshold": 12
    },
    "cpp": {
        "extensions": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
        "parser": "cpp",
        "keywords": ["class", "struct", "template", "namespace", "public", "private"],
        "complexity_threshold": 15
    },
    "go": {
        "extensions": [".go"],
        "parser": "go",
        "keywords": ["func", "type", "struct", "interface", "package", "import"],
        "complexity_threshold": 10
    },
    "rust": {
        "extensions": [".rs"],
        "parser": "rust",
        "keywords": ["fn", "struct", "enum", "impl", "trait", "mod"],
        "complexity_threshold": 12
    }
}

# File patterns to exclude from indexing
EXCLUDED_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "__pycache__",
    "*.so",
    "*.dll",
    "*.dylib",
    "*.exe",
    "node_modules",
    ".git",
    ".svn",
    ".hg",
    "*.log",
    "*.tmp",
    "*.temp",
    ".DS_Store",
    "Thumbs.db",
    "*.min.js",
    "*.min.css",
    "dist",
    "build",
    "target",
    "bin",
    "obj"
]

# Search ranking weights
SEARCH_WEIGHTS = {
    "semantic_similarity": 0.4,
    "keyword_match": 0.2,
    "code_quality": 0.15,
    "popularity": 0.1,
    "recency": 0.1,
    "documentation": 0.05
}

# Complexity thresholds
COMPLEXITY_THRESHOLDS = {
    "low": 5,
    "medium": 15,
    "high": 30
} 