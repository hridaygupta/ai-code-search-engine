"""
Vector store database layer for managing embeddings and similarity search.
"""

from typing import List, Dict, Any, Optional, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, Range, MatchValue
import numpy as np
import logging
from datetime import datetime

from ..config.settings import settings


class VectorStore:
    """Vector store for managing code embeddings and similarity search."""
    
    def __init__(self):
        """Initialize the vector store."""
        self.client = QdrantClient(settings.QDRANT_URL)
        self.logger = logging.getLogger(__name__)
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Initialize Qdrant collections."""
        collections = {
            'codebert': 768,
            'graphcodebert': 768,
            'sentence': 384,
            'hybrid': 768
        }
        
        for collection_name, vector_size in collections.items():
            try:
                collections_info = self.client.get_collections()
                collection_names = [col.name for col in collections_info.collections]
                
                if collection_name not in collection_names:
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=vector_size,
                            distance=Distance.COSINE
                        )
                    )
                    self.logger.info(f"Created collection: {collection_name}")
            except Exception as e:
                self.logger.error(f"Error initializing collection {collection_name}: {e}")
    
    async def add_embedding(self, collection: str, point_id: str, vector: List[float], 
                          payload: Dict[str, Any]) -> bool:
        """Add an embedding to the vector store."""
        try:
            point = PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
            
            self.client.upsert(
                collection_name=collection,
                points=[point]
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error adding embedding: {e}")
            return False
    
    async def search_similar(self, collection: str, query_vector: List[float], 
                           limit: int = 10, filter_conditions: Dict[str, Any] = None) -> List[Tuple[str, float]]:
        """Search for similar vectors."""
        try:
            search_filter = None
            if filter_conditions:
                search_filter = self._build_filter(filter_conditions)
            
            results = self.client.search(
                collection_name=collection,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=limit,
                with_payload=False
            )
            
            return [(result.id, result.score) for result in results]
        except Exception as e:
            self.logger.error(f"Error searching similar vectors: {e}")
            return []
    
    async def get_embedding(self, collection: str, point_id: str) -> Optional[List[float]]:
        """Get an embedding by ID."""
        try:
            results = self.client.retrieve(
                collection_name=collection,
                ids=[point_id],
                with_vectors=True
            )
            
            if results:
                return results[0].vector
            return None
        except Exception as e:
            self.logger.error(f"Error getting embedding: {e}")
            return None
    
    async def delete_embedding(self, collection: str, point_id: str) -> bool:
        """Delete an embedding."""
        try:
            self.client.delete(
                collection_name=collection,
                points_selector=[point_id]
            )
            return True
        except Exception as e:
            self.logger.error(f"Error deleting embedding: {e}")
            return False
    
    async def delete_by_filter(self, collection: str, filter_conditions: Dict[str, Any]) -> bool:
        """Delete embeddings by filter conditions."""
        try:
            search_filter = self._build_filter(filter_conditions)
            self.client.delete(
                collection_name=collection,
                points_selector=search_filter
            )
            return True
        except Exception as e:
            self.logger.error(f"Error deleting by filter: {e}")
            return False
    
    def _build_filter(self, conditions: Dict[str, Any]) -> Filter:
        """Build Qdrant filter from conditions."""
        filter_conditions = []
        
        for key, value in conditions.items():
            if isinstance(value, list):
                filter_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(any=value)
                    )
                )
            elif isinstance(value, dict) and 'range' in value:
                range_conditions = []
                if 'gte' in value['range']:
                    range_conditions.append(Range(gte=value['range']['gte']))
                if 'lte' in value['range']:
                    range_conditions.append(Range(lte=value['range']['lte']))
                if range_conditions:
                    filter_conditions.append(
                        FieldCondition(
                            key=key,
                            range=range_conditions[0] if len(range_conditions) == 1 else range_conditions
                        )
                    )
            else:
                filter_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
        
        return Filter(must=filter_conditions)
    
    async def get_collection_stats(self, collection: str) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            info = self.client.get_collection(collection)
            return {
                'name': info.name,
                'vector_size': info.config.params.vectors.size,
                'distance': info.config.params.vectors.distance.value,
                'points_count': info.points_count,
                'segments_count': info.segments_count,
                'status': info.status.value
            }
        except Exception as e:
            self.logger.error(f"Error getting collection stats: {e}")
            return {}
    
    async def optimize_collection(self, collection: str) -> bool:
        """Optimize collection for better performance."""
        try:
            self.client.update_collection(
                collection_name=collection,
                optimizer_config={
                    'default_segment_number': 2,
                    'memmap_threshold': 20000
                }
            )
            return True
        except Exception as e:
            self.logger.error(f"Error optimizing collection: {e}")
            return False
    
    async def close(self):
        """Close the vector store connection."""
        try:
            self.client.close()
        except Exception as e:
            self.logger.error(f"Error closing vector store: {e}") 