"""
Main FastAPI application for the Contextual Code Search Engine.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import logging
from contextlib import asynccontextmanager

from ..config.settings import settings
from .routes import search, indexing, repositories, analytics
from ..database.vector_store import VectorStore
from ..database.metadata_db import MetadataDB


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Contextual Code Search Engine...")
    
    # Initialize databases
    try:
        app.state.vector_store = VectorStore()
        app.state.metadata_db = MetadataDB()
        logger.info("Databases initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Contextual Code Search Engine...")
    if hasattr(app.state, 'vector_store'):
        await app.state.vector_store.close()
    if hasattr(app.state, 'metadata_db'):
        await app.state.metadata_db.close()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered contextual code search engine with semantic understanding",
    docs_url="/docs" if settings.ENABLE_SWAGGER else None,
    redoc_url="/redoc" if settings.ENABLE_SWAGGER else None,
    lifespan=lifespan
)

# Security
security = HTTPBearer(auto_error=False)


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure appropriately for production
    )


# Dependency injection
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: Implement proper JWT token validation
    # For now, return a mock user
    return {"user_id": "mock_user", "username": "test_user"}


async def get_vector_store():
    """Get vector store instance."""
    return app.state.vector_store


async def get_metadata_db():
    """Get metadata database instance."""
    return app.state.metadata_db


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Contextual Code Search Engine",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Manifest endpoint for frontend
@app.get("/manifest.json")
async def manifest():
    """Manifest endpoint for frontend."""
    return {
        "name": "Contextual Code Search Engine",
        "short_name": "CodeSearch",
        "description": "AI-powered contextual code search engine",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#3b82f6",
        "icons": []
    }


# Basic endpoints for frontend compatibility
@app.get("/api/v1/repositories")
async def get_repositories():
    """Get repositories endpoint."""
    return {
        "repositories": [],
        "total": 0,
        "page": 1,
        "page_size": 20
    }


@app.get("/api/v1/analytics/search")
async def get_search_analytics():
    """Get search analytics endpoint."""
    return {
        "total_queries": 0,
        "unique_queries": 0,
        "average_query_length": 0,
        "most_common_queries": []
    }


@app.get("/api/v1/search/suggestions")
async def get_search_suggestions(q: str = "", limit: int = 10):
    """Get search suggestions endpoint."""
    return {
        "query": q,
        "suggestions": ["sorting algorithm", "binary search", "quick sort", "machine learning"]
    }


# Include routers
app.include_router(
    search.router,
    prefix="/api/v1/search",
    tags=["Search"]
)

app.include_router(
    indexing.router,
    prefix="/api/v1/index",
    tags=["Indexing"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    repositories.router,
    prefix="/api/v1/repositories",
    tags=["Repositories"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)]
)


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.AUTO_RELOAD,
        workers=settings.WORKERS
    ) 