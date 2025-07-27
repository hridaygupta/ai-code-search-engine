from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://code_search_user:code_search_password@postgres:5432/code_search"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # Qdrant Vector Database
    QDRANT_URL: str = "http://qdrant:6333"
    
    # Neo4j Graph Database
    NEO4J_URL: str = "bolt://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "code_search_password"
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    
    # API Keys
    GITHUB_TOKEN: Optional[str] = None
    GITLAB_TOKEN: Optional[str] = None
    BITBUCKET_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Application Info
    APP_NAME: str = "Contextual Code Search Engine"
    APP_VERSION: str = "1.0.0"
    ENABLE_SWAGGER: bool = True
    
    # Supported Languages
    SUPPORTED_LANGUAGES: list = [
        "python", "javascript", "typescript", "java", "cpp", "c", "go", 
        "rust", "php", "ruby", "swift", "kotlin", "scala", "r", "matlab"
    ]
    
    # Search Weights
    SEARCH_WEIGHTS: dict = {
        "semantic_similarity": 0.4,
        "keyword_match": 0.3,
        "code_quality": 0.1,
        "popularity": 0.1,
        "recency": 0.05,
        "documentation": 0.05
    }
    
    # Excluded Patterns
    EXCLUDED_PATTERNS: list = [
        "**/node_modules/**",
        "**/__pycache__/**",
        "**/.git/**",
        "**/dist/**",
        "**/build/**",
        "**/.venv/**",
        "**/venv/**",
        "**/.env/**",
        "**/*.log",
        "**/*.tmp",
        "**/*.cache"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings() 