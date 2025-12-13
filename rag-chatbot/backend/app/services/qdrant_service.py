from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class QdrantService:
    """Service for managing Qdrant vector database operations"""

    def __init__(self):
        """Initialize Qdrant client"""
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    async def initialize(self):
        """Initialize Qdrant client"""
        try:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                timeout=30
            )
            # Test connection
            collections = self.client.get_collections()
            logger.info(f"Connected to Qdrant. Available collections: {[c.name for c in collections.collections]}")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    async def create_collection_if_not_exists(self):
        """Create collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(
                collection.name == self.collection_name
                for collection in collections.collections
            )

            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise

    async def insert_vectors(self, points: List[Dict[str, Any]]):
        """Insert vectors into collection"""
        try:
            # Prepare points for Qdrant
            qdrant_points = []
            for point_data in points:
                point = models.PointStruct(
                    id=point_data["id"],
                    vector=point_data["vector"],
                    payload=point_data["payload"]
                )
                qdrant_points.append(point)

            # Batch insert
            batch_size = 100
            for i in range(0, len(qdrant_points), batch_size):
                batch = qdrant_points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                logger.info(f"Inserted batch {i//batch_size + 1} of {len(qdrant_points)//batch_size + 1}")

            logger.info(f"Successfully inserted {len(points)} vectors")

        except Exception as e:
            logger.error(f"Failed to insert vectors: {e}")
            raise

    async def search(
        self,
        query_vector: List[float],
        limit: int = None,
        score_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            if limit is None:
                limit = settings.MAX_RETRIEVED_DOCUMENTS
            if score_threshold is None:
                score_threshold = settings.SIMILARITY_THRESHOLD

            # Search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=None,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True,
                with_vectors=False
            )

            # Format results
            results = []
            for hit in search_result:
                result = {
                    "id": str(hit.id),
                    "score": hit.score,
                    "payload": hit.payload
                }
                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    async def delete_by_filter(self, filter_dict: Dict[str, Any]):
        """Delete vectors by filter"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                        for key, value in filter_dict.items()
                    ]
                )
            )
            logger.info(f"Deleted vectors matching filter: {filter_dict}")
        except Exception as e:
            logger.error(f"Delete operation failed: {e}")
            raise

    async def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "indexed_vectors_count": info.indexed_vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise

    async def ensure_connection(self):
        """Ensure Qdrant connection is active"""
        try:
            if not self.client:
                await self.initialize()

            # Test connection
            self.client.get_collections()

        except Exception as e:
            logger.error(f"Qdrant connection check failed: {e}")
            await self.initialize()