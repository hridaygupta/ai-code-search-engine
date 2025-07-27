"""
Search result models for handling search queries and results.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

from .code_snippet import CodeSnippet
from .repository import Repository


class SearchType(str, Enum):
    """Types of search queries."""
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    PATTERN = "pattern"
    FUNCTION = "function"
    CLASS = "class"
    ALGORITHM = "algorithm"
    API = "api"
    ERROR = "error"
    EXAMPLE = "example"


class SearchIntent(str, Enum):
    """Search intent classification."""
    FIND_FUNCTION = "find_function"
    FIND_CLASS = "find_class"
    FIND_ALGORITHM = "find_algorithm"
    FIND_EXAMPLE = "find_example"
    FIND_PATTERN = "find_pattern"
    FIND_API = "find_api"
    DEBUG_ERROR = "debug_error"
    LEARN_CONCEPT = "learn_concept"
    COMPARE_IMPLEMENTATIONS = "compare_implementations"


class SearchQuery(BaseModel):
    """Model representing a search query."""
    
    # Query information
    query: str = Field(..., description="The search query text")
    search_type: SearchType = Field(default=SearchType.HYBRID, description="Type of search")
    intent: Optional[SearchIntent] = Field(None, description="Detected search intent")
    
    # Filters
    languages: List[str] = Field(default_factory=list, description="Programming languages to search in")
    repositories: List[str] = Field(default_factory=list, description="Repository IDs to search in")
    file_types: List[str] = Field(default_factory=list, description="File types to include")
    complexity_levels: List[str] = Field(default_factory=list, description="Complexity levels to include")
    date_range: Optional[Dict[str, datetime]] = Field(None, description="Date range filter")
    min_stars: Optional[int] = Field(None, description="Minimum repository stars")
    min_forks: Optional[int] = Field(None, description="Minimum repository forks")
    
    # Search parameters
    max_results: int = Field(default=50, description="Maximum number of results")
    similarity_threshold: float = Field(default=0.7, description="Minimum similarity threshold")
    include_documentation: bool = Field(default=True, description="Include documentation in search")
    include_comments: bool = Field(default=True, description="Include comments in search")
    
    # Advanced options
    use_semantic_search: bool = Field(default=True, description="Enable semantic search")
    use_keyword_search: bool = Field(default=True, description="Enable keyword search")
    use_pattern_search: bool = Field(default=False, description="Enable pattern search")
    expand_query: bool = Field(default=True, description="Expand query with synonyms")
    
    # Context
    context: Optional[str] = Field(None, description="Additional context for the search")
    user_id: Optional[str] = Field(None, description="User ID for personalized results")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")
    
    # Metadata
    query_embedding: Optional[List[float]] = Field(None, description="Query embedding vector")
    query_keywords: List[str] = Field(default_factory=list, description="Extracted keywords")
    query_topics: List[str] = Field(default_factory=list, description="Identified topics")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchResult(BaseModel):
    """Model representing a single search result."""
    
    # Result identification
    id: str = Field(..., description="Unique result identifier")
    query_id: str = Field(..., description="Associated query ID")
    
    # Content
    snippet: CodeSnippet = Field(..., description="The code snippet")
    repository: Repository = Field(..., description="The repository containing the snippet")
    
    # Relevance scores
    similarity_score: float = Field(..., description="Semantic similarity score")
    keyword_score: float = Field(..., description="Keyword matching score")
    pattern_score: float = Field(default=0.0, description="Pattern matching score")
    relevance_score: float = Field(..., description="Overall relevance score")
    
    # Ranking factors
    quality_boost: float = Field(default=1.0, description="Quality-based boost")
    popularity_boost: float = Field(default=1.0, description="Popularity-based boost")
    recency_boost: float = Field(default=1.0, description="Recency-based boost")
    documentation_boost: float = Field(default=1.0, description="Documentation-based boost")
    
    # Match information
    match_highlights: List[Dict[str, Any]] = Field(default_factory=list, description="Highlighted matches")
    context_lines: List[str] = Field(default_factory=list, description="Context lines around the snippet")
    matched_keywords: List[str] = Field(default_factory=list, description="Matched keywords")
    matched_patterns: List[str] = Field(default_factory=list, description="Matched patterns")
    
    # Additional information
    explanation: Optional[str] = Field(None, description="AI-generated explanation of relevance")
    suggestions: List[str] = Field(default_factory=list, description="Related search suggestions")
    similar_snippets: List[str] = Field(default_factory=list, description="IDs of similar snippets")
    
    # Usage tracking
    click_count: int = Field(default=0, description="Number of times this result was clicked")
    view_count: int = Field(default=0, description="Number of times this result was viewed")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Result creation time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchResponse(BaseModel):
    """Model representing a complete search response."""
    
    # Query information
    query: SearchQuery = Field(..., description="The original search query")
    query_id: str = Field(..., description="Unique query identifier")
    
    # Results
    results: List[SearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results found")
    returned_results: int = Field(..., description="Number of results returned")
    
    # Performance metrics
    search_time_ms: float = Field(..., description="Search execution time in milliseconds")
    indexing_time_ms: Optional[float] = Field(None, description="Time spent on indexing operations")
    embedding_time_ms: Optional[float] = Field(None, description="Time spent on embedding generation")
    
    # Search statistics
    languages_found: List[str] = Field(default_factory=list, description="Languages found in results")
    repositories_found: List[str] = Field(default_factory=list, description="Repositories found in results")
    complexity_distribution: Dict[str, int] = Field(default_factory=dict, description="Complexity distribution")
    quality_distribution: Dict[str, int] = Field(default_factory=dict, description="Quality distribution")
    
    # Suggestions and improvements
    query_suggestions: List[str] = Field(default_factory=list, description="Query improvement suggestions")
    filter_suggestions: List[Dict[str, Any]] = Field(default_factory=list, description="Filter suggestions")
    related_queries: List[str] = Field(default_factory=list, description="Related search queries")
    
    # Pagination
    page: int = Field(default=1, description="Current page number")
    page_size: int = Field(default=50, description="Results per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next_page: bool = Field(..., description="Whether there are more results")
    has_previous_page: bool = Field(..., description="Whether there are previous results")
    
    # Metadata
    search_engine_version: str = Field(default="1.0.0", description="Search engine version")
    model_versions: Dict[str, str] = Field(default_factory=dict, description="AI model versions used")
    cache_hit: bool = Field(default=False, description="Whether result was served from cache")
    
    # Timestamps
    search_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Search execution timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchAnalytics(BaseModel):
    """Model for search analytics and insights."""
    
    # Query analytics
    total_queries: int = Field(..., description="Total number of queries")
    unique_queries: int = Field(..., description="Number of unique queries")
    average_query_length: float = Field(..., description="Average query length")
    most_common_queries: List[Dict[str, Any]] = Field(default_factory=list, description="Most common queries")
    
    # Result analytics
    total_results_clicked: int = Field(..., description="Total results clicked")
    average_click_position: float = Field(..., description="Average position of clicked results")
    click_through_rate: float = Field(..., description="Click-through rate")
    most_clicked_results: List[Dict[str, Any]] = Field(default_factory=list, description="Most clicked results")
    
    # Performance analytics
    average_search_time: float = Field(..., description="Average search time in milliseconds")
    cache_hit_rate: float = Field(..., description="Cache hit rate")
    search_time_distribution: Dict[str, int] = Field(default_factory=dict, description="Search time distribution")
    
    # User analytics
    active_users: int = Field(..., description="Number of active users")
    average_queries_per_user: float = Field(..., description="Average queries per user")
    user_satisfaction_score: float = Field(..., description="User satisfaction score")
    
    # Language and repository analytics
    language_popularity: Dict[str, int] = Field(default_factory=dict, description="Language popularity")
    repository_popularity: Dict[str, int] = Field(default_factory=dict, description="Repository popularity")
    search_intent_distribution: Dict[str, int] = Field(default_factory=dict, description="Search intent distribution")
    
    # Time-based analytics
    queries_by_hour: Dict[int, int] = Field(default_factory=dict, description="Queries by hour of day")
    queries_by_day: Dict[str, int] = Field(default_factory=dict, description="Queries by day of week")
    queries_by_month: Dict[str, int] = Field(default_factory=dict, description="Queries by month")
    
    # Quality metrics
    result_relevance_score: float = Field(..., description="Average result relevance score")
    user_feedback_score: float = Field(..., description="Average user feedback score")
    search_quality_score: float = Field(..., description="Overall search quality score")
    
    # Timestamps
    analytics_period_start: datetime = Field(..., description="Analytics period start")
    analytics_period_end: datetime = Field(..., description="Analytics period end")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Analytics generation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchSuggestion(BaseModel):
    """Model for search suggestions and autocomplete."""
    
    suggestion: str = Field(..., description="The suggested query")
    type: str = Field(..., description="Type of suggestion (query, filter, etc.)")
    relevance_score: float = Field(..., description="Relevance score for the suggestion")
    frequency: int = Field(default=0, description="Frequency of this suggestion")
    context: Optional[str] = Field(None, description="Context for the suggestion")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata") 