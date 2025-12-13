from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from app.services.ingestion_service import ingestion_service
from app.services.qdrant_service import QdrantService
from app.main import get_qdrant_service

logger = logging.getLogger(__name__)
router = APIRouter()

class IngestionStatus(BaseModel):
    status: str
    total_files: int
    processed_files: int
    total_chunks: int
    completion_percentage: float

class IngestionResponse(BaseModel):
    message: str
    status: str

@router.get("/status", response_model=IngestionStatus)
async def get_ingestion_status():
    """Get current ingestion status"""
    try:
        status = await ingestion_service.get_ingestion_status()
        return IngestionStatus(
            status="completed" if status["completion_percentage"] == 100 else "in_progress",
            **status
        )
    except Exception as e:
        logger.error(f"Failed to get ingestion status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start", response_model=IngestionResponse)
async def start_ingestion(
    background_tasks: BackgroundTasks,
    qdrant_service: QdrantService = Depends(get_qdrant_service)
):
    """Start content ingestion process"""
    try:
        # Add ingestion to background tasks
        background_tasks.add_task(run_full_ingestion, qdrant_service)

        return IngestionResponse(
            message="Content ingestion started in background",
            status="started"
        )

    except Exception as e:
        logger.error(f"Failed to start ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reindex", response_model=IngestionResponse)
async def reindex_content(
    background_tasks: BackgroundTasks,
    qdrant_service: QdrantService = Depends(get_qdrant_service)
):
    """Reindex all content (clear and re-ingest)"""
    try:
        # Add reindexing to background tasks
        background_tasks.add_task(run_reindexing, qdrant_service)

        return IngestionResponse(
            message="Content reindexing started in background",
            status="started"
        )

    except Exception as e:
        logger.error(f"Failed to start reindexing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear", response_model=IngestionResponse)
async def clear_content(qdrant_service: QdrantService = Depends(get_qdrant_service)):
    """Clear all ingested content"""
    try:
        # Clear Qdrant collection
        await qdrant_service.delete_by_filter({})

        # Clear database
        from app.core.database import DatabaseManager
        await DatabaseManager.execute_command("TRUNCATE TABLE content_chunks")

        return IngestionResponse(
            message="All content cleared successfully",
            status="completed"
        )

    except Exception as e:
        logger.error(f"Failed to clear content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_full_ingestion(qdrant_service: QdrantService):
    """Run full ingestion process in background"""
    try:
        logger.info("Starting full content ingestion...")

        # Ingest content and get chunks
        chunks = await ingestion_service.ingest_all_content()

        # Prepare vectors for Qdrant
        vector_points = []
        for chunk_data in chunks:
            vector_points.append({
                "id": chunk_data["vector_id"],
                "vector": chunk_data["vector"],
                "payload": {
                    "content": chunk_data["content"],
                    "metadata": chunk_data["metadata"]
                }
            })

        # Insert into Qdrant
        if vector_points:
            await qdrant_service.insert_vectors(vector_points)
            logger.info(f"Successfully inserted {len(vector_points)} vectors into Qdrant")

        logger.info("Full ingestion completed successfully")

    except Exception as e:
        logger.error(f"Background ingestion failed: {e}")
        raise

async def run_reindexing(qdrant_service: QdrantService):
    """Run reindexing process in background"""
    try:
        logger.info("Starting content reindexing...")

        # Clear existing content
        await qdrant_service.delete_by_filter({})
        from app.core.database import DatabaseManager
        await DatabaseManager.execute_command("TRUNCATE TABLE content_chunks")

        # Run full ingestion
        await run_full_ingestion(qdrant_service)

        logger.info("Reindexing completed successfully")

    except Exception as e:
        logger.error(f"Background reindexing failed: {e}")
        raise