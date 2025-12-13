from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.core.config import settings
from app.core.database import init_database
from app.api.routers import chat, ingestion, health
from app.services.qdrant_service import QdrantService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global services
qdrant_service: QdrantService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting RAG Chatbot API...")

    # Initialize database
    await init_database()
    logger.info("Database initialized successfully")

    # Initialize Qdrant service
    global qdrant_service
    qdrant_service = QdrantService()
    await qdrant_service.initialize()
    logger.info("Qdrant service initialized successfully")

    # Create collection if it doesn't exist
    await qdrant_service.create_collection_if_not_exists()

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot API...")

# Create FastAPI application
app = FastAPI(
    title="Robotics Textbook RAG Chatbot",
    description="A RAG-powered chatbot for answering questions about the Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(ingestion.router, prefix="/api/v1", tags=["ingestion"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Robotics Textbook RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Dependency to get Qdrant service
def get_qdrant_service() -> QdrantService:
    """Get Qdrant service instance"""
    return qdrant_service

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_ENVIRONMENT == "development"
    )