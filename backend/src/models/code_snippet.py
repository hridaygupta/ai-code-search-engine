"""
Code snippet model for storing parsed and analyzed code fragments.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class CodeType(str, Enum):
    """Types of code elements."""
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    MODULE = "module"
    VARIABLE = "variable"
    CONSTANT = "constant"
    IMPORT = "import"
    COMMENT = "comment"
    DOCSTRING = "docstring"
    SNIPPET = "snippet"


class ComplexityLevel(str, Enum):
    """Code complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class CodeQuality(str, Enum):
    """Code quality indicators."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class CodeSnippet(BaseModel):
    """Model representing a code snippet with comprehensive metadata."""
    
    # Basic identification
    id: str = Field(..., description="Unique identifier for the code snippet")
    repository_id: str = Field(..., description="ID of the repository containing this snippet")
    file_path: str = Field(..., description="Path to the file containing the snippet")
    file_name: str = Field(..., description="Name of the file")
    
    # Code content
    content: str = Field(..., description="The actual code content")
    start_line: int = Field(..., description="Starting line number")
    end_line: int = Field(..., description="Ending line number")
    start_column: int = Field(..., description="Starting column number")
    end_column: int = Field(..., description="Ending column number")
    
    # Language and type information
    language: str = Field(..., description="Programming language")
    code_type: CodeType = Field(..., description="Type of code element")
    
    # Function/class specific fields
    name: Optional[str] = Field(None, description="Name of the function, class, or variable")
    signature: Optional[str] = Field(None, description="Function signature or class definition")
    parameters: Optional[List[str]] = Field(None, description="Function parameters")
    return_type: Optional[str] = Field(None, description="Return type for functions")
    docstring: Optional[str] = Field(None, description="Documentation string")
    
    # Context and relationships
    parent_class: Optional[str] = Field(None, description="Parent class if this is a method")
    imports: List[str] = Field(default_factory=list, description="Import statements")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies and imports")
    called_functions: List[str] = Field(default_factory=list, description="Functions called within this snippet")
    variables_used: List[str] = Field(default_factory=list, description="Variables used in the snippet")
    
    # Analysis results
    complexity_score: float = Field(default=0.0, description="Cyclomatic complexity score")
    complexity_level: ComplexityLevel = Field(default=ComplexityLevel.LOW, description="Complexity level")
    quality_score: float = Field(default=0.0, description="Code quality score")
    quality_level: CodeQuality = Field(default=CodeQuality.FAIR, description="Code quality level")
    readability_score: float = Field(default=0.0, description="Readability score")
    
    # Semantic information
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords")
    topics: List[str] = Field(default_factory=list, description="Identified topics")
    intent: Optional[str] = Field(None, description="Code intent or purpose")
    algorithm: Optional[str] = Field(None, description="Algorithm or pattern used")
    
    # Embeddings and vectors
    embedding: Optional[List[float]] = Field(None, description="Semantic embedding vector")
    embedding_model: Optional[str] = Field(None, description="Model used for embedding")
    
    # Repository metadata
    branch: str = Field(default="main", description="Git branch")
    commit_hash: Optional[str] = Field(None, description="Git commit hash")
    commit_message: Optional[str] = Field(None, description="Git commit message")
    author: Optional[str] = Field(None, description="Code author")
    last_modified: datetime = Field(default_factory=datetime.utcnow, description="Last modification time")
    
    # Search and ranking
    search_score: float = Field(default=0.0, description="Search relevance score")
    popularity_score: float = Field(default=0.0, description="Popularity score")
    usage_count: int = Field(default=0, description="Number of times this snippet was accessed")
    
    # Additional metadata
    tags: List[str] = Field(default_factory=list, description="User-defined tags")
    annotations: Dict[str, Any] = Field(default_factory=dict, description="Additional annotations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    indexed_at: datetime = Field(default_factory=datetime.utcnow, description="Indexing timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CodeSnippetCreate(BaseModel):
    """Model for creating a new code snippet."""
    repository_id: str
    file_path: str
    content: str
    start_line: int
    end_line: int
    language: str
    code_type: CodeType
    name: Optional[str] = None
    signature: Optional[str] = None
    parameters: Optional[List[str]] = None
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    parent_class: Optional[str] = None
    imports: List[str] = []
    dependencies: List[str] = []
    called_functions: List[str] = []
    variables_used: List[str] = []
    keywords: List[str] = []
    topics: List[str] = []
    intent: Optional[str] = None
    algorithm: Optional[str] = None
    branch: str = "main"
    commit_hash: Optional[str] = None
    commit_message: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class CodeSnippetUpdate(BaseModel):
    """Model for updating an existing code snippet."""
    content: Optional[str] = None
    complexity_score: Optional[float] = None
    complexity_level: Optional[ComplexityLevel] = None
    quality_score: Optional[float] = None
    quality_level: Optional[CodeQuality] = None
    readability_score: Optional[float] = None
    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    search_score: Optional[float] = None
    popularity_score: Optional[float] = None
    usage_count: Optional[int] = None
    tags: Optional[List[str]] = None
    annotations: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class CodeSnippetSearch(BaseModel):
    """Model for code snippet search results."""
    snippet: CodeSnippet
    similarity_score: float = Field(..., description="Similarity score with query")
    relevance_score: float = Field(..., description="Overall relevance score")
    match_highlights: List[Dict[str, Any]] = Field(default_factory=list, description="Highlighted matches")
    context_lines: List[str] = Field(default_factory=list, description="Context lines around the snippet")


class CodeSnippetBatch(BaseModel):
    """Model for batch processing of code snippets."""
    snippets: List[CodeSnippet]
    total_count: int
    processed_count: int
    failed_count: int
    errors: List[str] = Field(default_factory=list) 