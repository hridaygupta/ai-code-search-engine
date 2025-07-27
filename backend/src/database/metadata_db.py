"""
Metadata database layer for storing repository and snippet metadata.
"""

import asyncio
from typing import List, Dict, Any, Optional
import asyncpg
import logging
from datetime import datetime

from ..config.settings import settings
from ..models.repository import Repository, RepositoryCreate, RepositoryUpdate
from ..models.code_snippet import CodeSnippet, CodeSnippetCreate, CodeSnippetUpdate
from ..models.user import User, UserCreate, UserUpdate


class MetadataDB:
    """Metadata database for storing repository and snippet information."""
    
    def __init__(self):
        """Initialize the metadata database."""
        self.pool = None
        self.logger = logging.getLogger(__name__)
    
    async def connect(self):
        """Connect to the database."""
        try:
            self.pool = await asyncpg.create_pool(settings.DATABASE_URL)
            await self._create_tables()
            self.logger.info("Connected to metadata database")
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise
    
    async def _create_tables(self):
        """Create database tables if they don't exist."""
        async with self.pool.acquire() as conn:
            # Users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(255) PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    full_name VARCHAR(255),
                    role VARCHAR(50) DEFAULT 'user',
                    status VARCHAR(50) DEFAULT 'active',
                    is_verified BOOLEAN DEFAULT FALSE,
                    is_premium BOOLEAN DEFAULT FALSE,
                    hashed_password VARCHAR(255) NOT NULL,
                    salt VARCHAR(255) NOT NULL,
                    avatar_url TEXT,
                    bio TEXT,
                    location VARCHAR(255),
                    website VARCHAR(255),
                    company VARCHAR(255),
                    preferred_languages JSONB DEFAULT '[]',
                    search_preferences JSONB DEFAULT '{}',
                    notification_settings JSONB DEFAULT '{}',
                    theme_preference VARCHAR(50) DEFAULT 'light',
                    total_searches INTEGER DEFAULT 0,
                    total_bookmarks INTEGER DEFAULT 0,
                    total_contributions INTEGER DEFAULT 0,
                    api_key VARCHAR(255),
                    api_quota INTEGER DEFAULT 1000,
                    api_usage INTEGER DEFAULT 0,
                    two_factor_enabled BOOLEAN DEFAULT FALSE,
                    github_username VARCHAR(255),
                    gitlab_username VARCHAR(255),
                    bitbucket_username VARCHAR(255),
                    external_id VARCHAR(255),
                    tags JSONB DEFAULT '[]',
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Repositories table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS repositories (
                    id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    description TEXT,
                    url TEXT NOT NULL,
                    clone_url TEXT NOT NULL,
                    ssh_url TEXT,
                    api_url TEXT,
                    repository_type VARCHAR(50) NOT NULL,
                    visibility VARCHAR(50) NOT NULL,
                    owner VARCHAR(255) NOT NULL,
                    owner_type VARCHAR(50) DEFAULT 'User',
                    stars INTEGER DEFAULT 0,
                    forks INTEGER DEFAULT 0,
                    watchers INTEGER DEFAULT 0,
                    open_issues INTEGER DEFAULT 0,
                    size INTEGER DEFAULT 0,
                    primary_language VARCHAR(100),
                    languages JSONB DEFAULT '{}',
                    topics JSONB DEFAULT '[]',
                    license VARCHAR(255),
                    default_branch VARCHAR(100) DEFAULT 'main',
                    branches JSONB DEFAULT '[]',
                    tags JSONB DEFAULT '[]',
                    last_commit_hash VARCHAR(255),
                    last_commit_message TEXT,
                    last_commit_author VARCHAR(255),
                    last_commit_date TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'pending',
                    indexed_branches JSONB DEFAULT '[]',
                    total_files INTEGER DEFAULT 0,
                    indexed_files INTEGER DEFAULT 0,
                    total_snippets INTEGER DEFAULT 0,
                    indexed_snippets INTEGER DEFAULT 0,
                    indexing_progress FLOAT DEFAULT 0.0,
                    indexing_started_at TIMESTAMP,
                    indexing_completed_at TIMESTAMP,
                    indexing_duration FLOAT,
                    indexing_errors JSONB DEFAULT '[]',
                    quality_score FLOAT DEFAULT 0.0,
                    documentation_score FLOAT DEFAULT 0.0,
                    test_coverage FLOAT DEFAULT 0.0,
                    code_quality_score FLOAT DEFAULT 0.0,
                    is_private BOOLEAN DEFAULT FALSE,
                    has_wiki BOOLEAN DEFAULT FALSE,
                    has_issues BOOLEAN DEFAULT TRUE,
                    has_projects BOOLEAN DEFAULT FALSE,
                    has_downloads BOOLEAN DEFAULT FALSE,
                    webhook_url TEXT,
                    webhook_secret VARCHAR(255),
                    integration_token VARCHAR(255),
                    indexing_config JSONB DEFAULT '{}',
                    search_config JSONB DEFAULT '{}',
                    exclude_patterns JSONB DEFAULT '[]',
                    include_patterns JSONB DEFAULT '[]',
                    tags JSONB DEFAULT '[]',
                    annotations JSONB DEFAULT '{}',
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    pushed_at TIMESTAMP
                )
            """)
            
            # Code snippets table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS code_snippets (
                    id VARCHAR(255) PRIMARY KEY,
                    repository_id VARCHAR(255) NOT NULL REFERENCES repositories(id),
                    file_path TEXT NOT NULL,
                    file_name VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    start_line INTEGER NOT NULL,
                    end_line INTEGER NOT NULL,
                    start_column INTEGER NOT NULL,
                    end_column INTEGER NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    code_type VARCHAR(50) NOT NULL,
                    name VARCHAR(255),
                    signature TEXT,
                    parameters JSONB DEFAULT '[]',
                    return_type VARCHAR(255),
                    docstring TEXT,
                    parent_class VARCHAR(255),
                    imports JSONB DEFAULT '[]',
                    dependencies JSONB DEFAULT '[]',
                    called_functions JSONB DEFAULT '[]',
                    variables_used JSONB DEFAULT '[]',
                    complexity_score FLOAT DEFAULT 0.0,
                    complexity_level VARCHAR(50) DEFAULT 'low',
                    quality_score FLOAT DEFAULT 0.0,
                    quality_level VARCHAR(50) DEFAULT 'fair',
                    readability_score FLOAT DEFAULT 0.0,
                    keywords JSONB DEFAULT '[]',
                    topics JSONB DEFAULT '[]',
                    intent TEXT,
                    algorithm VARCHAR(255),
                    embedding JSONB,
                    embedding_model VARCHAR(100),
                    branch VARCHAR(100) DEFAULT 'main',
                    commit_hash VARCHAR(255),
                    commit_message TEXT,
                    author VARCHAR(255),
                    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    search_score FLOAT DEFAULT 0.0,
                    popularity_score FLOAT DEFAULT 0.0,
                    usage_count INTEGER DEFAULT 0,
                    tags JSONB DEFAULT '[]',
                    annotations JSONB DEFAULT '{}',
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Search queries table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS search_queries (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) REFERENCES users(id),
                    query TEXT NOT NULL,
                    search_type VARCHAR(50) DEFAULT 'hybrid',
                    intent VARCHAR(100),
                    languages JSONB DEFAULT '[]',
                    repositories JSONB DEFAULT '[]',
                    file_types JSONB DEFAULT '[]',
                    complexity_levels JSONB DEFAULT '[]',
                    date_range JSONB,
                    min_stars INTEGER,
                    min_forks INTEGER,
                    max_results INTEGER DEFAULT 50,
                    similarity_threshold FLOAT DEFAULT 0.7,
                    include_documentation BOOLEAN DEFAULT TRUE,
                    include_comments BOOLEAN DEFAULT TRUE,
                    use_semantic_search BOOLEAN DEFAULT TRUE,
                    use_keyword_search BOOLEAN DEFAULT TRUE,
                    use_pattern_search BOOLEAN DEFAULT FALSE,
                    expand_query BOOLEAN DEFAULT TRUE,
                    context TEXT,
                    session_id VARCHAR(255),
                    query_embedding JSONB,
                    query_keywords JSONB DEFAULT '[]',
                    query_topics JSONB DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Search results table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS search_results (
                    id VARCHAR(255) PRIMARY KEY,
                    query_id VARCHAR(255) REFERENCES search_queries(id),
                    snippet_id VARCHAR(255) REFERENCES code_snippets(id),
                    repository_id VARCHAR(255) REFERENCES repositories(id),
                    similarity_score FLOAT NOT NULL,
                    keyword_score FLOAT DEFAULT 0.0,
                    pattern_score FLOAT DEFAULT 0.0,
                    relevance_score FLOAT NOT NULL,
                    quality_boost FLOAT DEFAULT 1.0,
                    popularity_boost FLOAT DEFAULT 1.0,
                    recency_boost FLOAT DEFAULT 1.0,
                    documentation_boost FLOAT DEFAULT 1.0,
                    match_highlights JSONB DEFAULT '[]',
                    context_lines JSONB DEFAULT '[]',
                    matched_keywords JSONB DEFAULT '[]',
                    matched_patterns JSONB DEFAULT '[]',
                    explanation TEXT,
                    suggestions JSONB DEFAULT '[]',
                    similar_snippets JSONB DEFAULT '[]',
                    click_count INTEGER DEFAULT 0,
                    view_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_snippets_repository ON code_snippets(repository_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_snippets_language ON code_snippets(language)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_snippets_code_type ON code_snippets(code_type)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_snippets_created_at ON code_snippets(created_at)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_repositories_status ON repositories(status)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_repositories_owner ON repositories(owner)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_search_queries_user ON search_queries(user_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_search_results_query ON search_results(query_id)")
    
    async def close(self):
        """Close the database connection."""
        if self.pool:
            await self.pool.close()
    
    # Repository operations
    async def create_repository(self, repo: RepositoryCreate) -> Optional[Repository]:
        """Create a new repository."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO repositories (
                    id, name, full_name, description, url, clone_url, ssh_url, api_url,
                    repository_type, visibility, owner, owner_type, stars, forks, watchers,
                    open_issues, size, primary_language, languages, topics, license,
                    default_branch, branches, tags, is_private, has_wiki, has_issues,
                    has_projects, has_downloads, indexing_config, search_config,
                    exclude_patterns, include_patterns, tags, metadata
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                         $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29,
                         $30, $31, $32, $33, $34, $35)
                RETURNING *
            """, repo.id, repo.name, repo.full_name, repo.description, repo.url, repo.clone_url,
                 repo.ssh_url, repo.api_url, repo.repository_type.value, repo.visibility.value,
                 repo.owner, repo.owner_type, repo.stars, repo.forks, repo.watchers, repo.open_issues,
                 repo.size, repo.primary_language, repo.languages, repo.topics, repo.license,
                 repo.default_branch, repo.branches, repo.tags, repo.is_private, repo.has_wiki,
                 repo.has_issues, repo.has_projects, repo.has_downloads, repo.indexing_config,
                 repo.search_config, repo.exclude_patterns, repo.include_patterns, repo.tags, repo.metadata)
            
            return Repository(**dict(row)) if row else None
    
    async def get_repository(self, repo_id: str) -> Optional[Repository]:
        """Get a repository by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM repositories WHERE id = $1", repo_id)
            return Repository(**dict(row)) if row else None
    
    async def update_repository(self, repo_id: str, update_data: RepositoryUpdate) -> Optional[Repository]:
        """Update a repository."""
        async with self.pool.acquire() as conn:
            # Build dynamic update query
            set_clauses = []
            values = []
            param_count = 1
            
            for field, value in update_data.dict(exclude_unset=True).items():
                if value is not None:
                    set_clauses.append(f"{field} = ${param_count}")
                    values.append(value)
                    param_count += 1
            
            if not set_clauses:
                return await self.get_repository(repo_id)
            
            set_clauses.append(f"updated_at = ${param_count}")
            values.append(datetime.utcnow())
            values.append(repo_id)
            
            query = f"""
                UPDATE repositories 
                SET {', '.join(set_clauses)}
                WHERE id = ${param_count + 1}
                RETURNING *
            """
            
            row = await conn.fetchrow(query, *values)
            return Repository(**dict(row)) if row else None
    
    async def list_repositories(self, limit: int = 100, offset: int = 0) -> List[Repository]:
        """List repositories."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM repositories 
                ORDER BY created_at DESC 
                LIMIT $1 OFFSET $2
            """, limit, offset)
            
            return [Repository(**dict(row)) for row in rows]
    
    # Code snippet operations
    async def create_snippet(self, snippet: CodeSnippetCreate) -> Optional[CodeSnippet]:
        """Create a new code snippet."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO code_snippets (
                    id, repository_id, file_path, file_name, content, start_line, end_line,
                    start_column, end_column, language, code_type, name, signature, parameters,
                    return_type, docstring, parent_class, imports, dependencies, called_functions,
                    variables_used, complexity_score, complexity_level, quality_score, quality_level,
                    readability_score, keywords, topics, intent, algorithm, embedding, embedding_model,
                    branch, commit_hash, commit_message, author, tags, metadata
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17,
                         $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32,
                         $33, $34, $35, $36, $37, $38, $39)
                RETURNING *
            """, snippet.id, snippet.repository_id, snippet.file_path, snippet.file_name,
                 snippet.content, snippet.start_line, snippet.end_line, snippet.start_column,
                 snippet.end_column, snippet.language, snippet.code_type.value, snippet.name,
                 snippet.signature, snippet.parameters, snippet.return_type, snippet.docstring,
                 snippet.parent_class, snippet.imports, snippet.dependencies, snippet.called_functions,
                 snippet.variables_used, snippet.complexity_score, snippet.complexity_level.value,
                 snippet.quality_score, snippet.quality_level.value, snippet.readability_score,
                 snippet.keywords, snippet.topics, snippet.intent, snippet.algorithm, snippet.embedding,
                 snippet.embedding_model, snippet.branch, snippet.commit_hash, snippet.commit_message,
                 snippet.author, snippet.tags, snippet.metadata)
            
            return CodeSnippet(**dict(row)) if row else None
    
    async def get_snippet(self, snippet_id: str) -> Optional[CodeSnippet]:
        """Get a code snippet by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM code_snippets WHERE id = $1", snippet_id)
            return CodeSnippet(**dict(row)) if row else None
    
    async def update_snippet(self, snippet_id: str, update_data: CodeSnippetUpdate) -> Optional[CodeSnippet]:
        """Update a code snippet."""
        async with self.pool.acquire() as conn:
            # Build dynamic update query
            set_clauses = []
            values = []
            param_count = 1
            
            for field, value in update_data.dict(exclude_unset=True).items():
                if value is not None:
                    set_clauses.append(f"{field} = ${param_count}")
                    values.append(value)
                    param_count += 1
            
            if not set_clauses:
                return await self.get_snippet(snippet_id)
            
            set_clauses.append(f"updated_at = ${param_count}")
            values.append(datetime.utcnow())
            values.append(snippet_id)
            
            query = f"""
                UPDATE code_snippets 
                SET {', '.join(set_clauses)}
                WHERE id = ${param_count + 1}
                RETURNING *
            """
            
            row = await conn.fetchrow(query, *values)
            return CodeSnippet(**dict(row)) if row else None
    
    async def list_snippets(self, repository_id: str = None, limit: int = 100, offset: int = 0) -> List[CodeSnippet]:
        """List code snippets."""
        async with self.pool.acquire() as conn:
            if repository_id:
                rows = await conn.fetch("""
                    SELECT * FROM code_snippets 
                    WHERE repository_id = $1
                    ORDER BY created_at DESC 
                    LIMIT $2 OFFSET $3
                """, repository_id, limit, offset)
            else:
                rows = await conn.fetch("""
                    SELECT * FROM code_snippets 
                    ORDER BY created_at DESC 
                    LIMIT $1 OFFSET $2
                """, limit, offset)
            
            return [CodeSnippet(**dict(row)) for row in rows] 