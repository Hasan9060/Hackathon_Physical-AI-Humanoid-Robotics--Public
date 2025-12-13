from fastapi import APIRouter
from typing import Dict, Any
import logging
from datetime import datetime
from app.services.qdrant_service import QdrantService
from app.main import get_qdrant_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check(qdrant_service: QdrantService = Depends(get_qdrant_service)) -> Dict[str, Any]:
    """Comprehensive health check for all services"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }

    try:
        # Check Qdrant service
        try:
            collection_info = await qdrant_service.get_collection_info()
            health_status["services"]["qdrant"] = {
                "status": "healthy",
                "collection_name": collection_info["name"],
                "vectors_count": collection_info["vectors_count"],
                "points_count": collection_info["points_count"]
            }
        except Exception as e:
            health_status["services"]["qdrant"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"

        # Check OpenAI service
        try:
            from app.services.openai_service import openai_service
            # Test embedding creation
            test_embedding = await openai_service.create_embedding("health check")
            health_status["services"]["openai"] = {
                "status": "healthy",
                "model": openai_service.client.models.retrieve("gpt-4-turbo-preview").id
            }
        except Exception as e:
            health_status["services"]["openai"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"

        # Check Database
        try:
            from app.core.database import DatabaseManager
            result = await DatabaseManager.execute_query("SELECT 1 as test")
            health_status["services"]["database"] = {
                "status": "healthy",
                "connection": "ok"
            }
        except Exception as e:
            health_status["services"]["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"

    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)

    return health_status

@router.get("/ready")
async def readiness_check():
    """Simple readiness check for Kubernetes/container orchestration"""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/live")
async def liveness_check():
    """Simple liveness check for Kubernetes/container orchestration"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }