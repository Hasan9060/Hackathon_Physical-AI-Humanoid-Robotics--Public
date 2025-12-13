from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_ENVIRONMENT: str = "development"
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8000", "*"]

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # Neon Database Configuration
    NEON_DATABASE_URL: str

    # Qdrant Configuration
    QDRANT_API_KEY: str
    QDRANT_URL: str
    QDRANT_COLLECTION_NAME: str = "robotics_textbook"

    # Book Content Configuration
    BOOK_CONTENT_PATH: str = "../../docs"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Embedding Configuration
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    VECTOR_SIZE: int = 1536

    # RAG Configuration
    MAX_RETRIEVED_DOCUMENTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # Processing Configuration
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Path configurations
BASE_DIR = Path(__file__).parent.parent.parent
BOOK_CONTENT_DIR = BASE_DIR / settings.BOOK_CONTENT_PATH

# Database URL
DATABASE_URL = settings.NEON_DATABASE_URL