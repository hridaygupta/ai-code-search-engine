"""
Search API routes for code search functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import logging
from pathlib import Path

from ...models.search_result import SearchQuery, SearchResponse, SearchType, SearchIntent
from ...search.semantic_search import SemanticSearch
from ...search.query_processor import QueryProcessor
from ...search.ranking_engine import RankingEngine

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def search_code(
    q: Optional[str] = Query(None, description="Search query"),
    query: Optional[str] = Query(None, description="Search query (alternative parameter name)"),
    search_type: SearchType = Query(SearchType.HYBRID, description="Type of search"),
    languages: Optional[List[str]] = Query(None, description="Programming languages to search in"),
    repositories: Optional[List[str]] = Query(None, description="Repository IDs to search in"),
    max_results: int = Query(50, description="Maximum number of results"),
    similarity_threshold: float = Query(0.7, description="Minimum similarity threshold"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(20, description="Results per page")
):
    """Search for code snippets using semantic and keyword matching."""
    try:
        # Handle both parameter names for compatibility
        search_query = q or query
        if not search_query:
            raise HTTPException(status_code=422, detail="Search query is required")
        
        logger.info(f"Search request received: {search_query}")
        
        # Perform real search
        from ...search.semantic_search import SemanticSearch
        semantic_search = SemanticSearch()
        
        # Apply language filter if specified
        filtered_languages = None
        if languages:
            filtered_languages = [lang.lower() for lang in languages]
        
        # Perform search
        search_results = semantic_search.search(
            query=search_query,
            max_results=max_results,
            similarity_threshold=similarity_threshold
        )
        
        # Filter by language if specified
        if filtered_languages:
            search_results = [
                result for result in search_results 
                if result.snippet.language.lower() in filtered_languages
            ]
        
        # Convert to response format
        results = []
        for result in search_results:
            snippet = result.snippet
            
            # Create repository info from file path
            file_path = Path(snippet.file_path)
            repo_name = file_path.parent.name if file_path.parent.name else "local"
            
            results.append({
                "id": snippet.id,
                "title": snippet.name,
                "content": snippet.content,
                "language": snippet.language,
                "repository": {
                    "name": repo_name,
                    "url": f"file://{snippet.file_path}",
                    "owner": "local"
                },
                "file_path": snippet.file_path,
                "line_start": snippet.line_start,
                "line_end": snippet.line_end,
                "complexity": snippet.complexity,
                "quality_score": snippet.quality_score,
                "stars": 0,  # Not available for local files
                "views": 0,  # Not available for local files
                "created_at": "2024-01-01T00:00:00Z",  # Not available for local files
                "updated_at": "2024-01-01T00:00:00Z",  # Not available for local files
                "tags": snippet.tags,
                "description": snippet.description,
                "score": result.score,
                "match_type": result.match_type,
                "highlighted_content": result.highlighted_content
            })
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = results[start_idx:end_idx]
        
        response = {
            "query": search_query,
            "results": paginated_results,
            "total_results": len(results),
            "search_time": 0.1,  # Could be measured in real implementation
            "page": page,
            "page_size": page_size,
            "total_pages": (len(results) + page_size - 1) // page_size,
            "has_next_page": end_idx < len(results),
            "has_previous_page": page > 1
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error in search: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="Partial search query"),
    limit: int = Query(10, description="Number of suggestions")
):
    """Get search suggestions based on partial query."""
    try:
        query_processor = QueryProcessor()
        suggestions = query_processor.get_suggestions(q, limit)
        
        return {
            "query": q,
            "suggestions": suggestions
        }
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get suggestions")


@router.get("/similar/{snippet_id}")
async def find_similar_snippets(
    snippet_id: str,
    limit: int = Query(10, description="Number of similar snippets"),
    threshold: float = Query(0.7, description="Similarity threshold")
):
    """Find similar code snippets to a given snippet."""
    try:
        semantic_search = SemanticSearch()
        similar_snippets = semantic_search.find_similar_snippets(
            snippet_id, 
            top_k=limit, 
            threshold=threshold
        )
        
        return {
            "snippet_id": snippet_id,
            "similar_snippets": similar_snippets
        }
        
    except Exception as e:
        logger.error(f"Error finding similar snippets: {e}")
        raise HTTPException(status_code=500, detail="Failed to find similar snippets")


@router.post("/explain")
async def explain_code_snippet(
    snippet_id: str,
    context: Optional[str] = None
):
    """Generate explanation for a code snippet."""
    try:
        # TODO: Implement code explanation using AI models
        explanation = f"Explanation for snippet {snippet_id}"
        
        return {
            "snippet_id": snippet_id,
            "explanation": explanation,
            "context": context
        }
        
    except Exception as e:
        logger.error(f"Error explaining snippet: {e}")
        raise HTTPException(status_code=500, detail="Failed to explain snippet")


@router.get("/trends")
async def get_search_trends(
    days: int = Query(7, description="Number of days to analyze")
):
    """Get search trends and popular queries."""
    try:
        # TODO: Implement search trends analysis
        trends = {
            "popular_queries": [
                {"query": "sorting algorithm", "count": 150},
                {"query": "binary search", "count": 120},
                {"query": "quick sort", "count": 100}
            ],
            "popular_languages": [
                {"language": "Python", "count": 500},
                {"language": "JavaScript", "count": 400},
                {"language": "Java", "count": 300}
            ],
            "trending_topics": [
                {"topic": "machine learning", "growth": 25},
                {"topic": "web development", "growth": 15},
                {"topic": "data structures", "growth": 10}
            ]
        }
        
        return trends
        
    except Exception as e:
        logger.error(f"Error getting search trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to get search trends")


@router.get("/filters")
async def get_available_filters():
    """Get available search filters."""
    try:
        filters = {
            "languages": [
                "Python", "JavaScript", "TypeScript", "Java", 
                "C++", "Go", "Rust", "PHP", "Ruby", "C#"
            ],
            "code_types": [
                "function", "class", "method", "variable", 
                "import", "comment", "snippet"
            ],
            "complexity_levels": [
                "low", "medium", "high", "very_high"
            ],
            "quality_levels": [
                "excellent", "good", "fair", "poor"
            ]
        }
        
        return filters
        
    except Exception as e:
        logger.error(f"Error getting filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to get filters") 