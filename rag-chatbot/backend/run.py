#!/usr/bin/env python3
"""
Entry point for the RAG Chatbot backend service
"""

import uvicorn
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    # Get configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    environment = os.getenv("API_ENVIRONMENT", "development")

    logger.info(f"Starting RAG Chatbot API on {host}:{port} in {environment} mode")

    # Run the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=environment == "development",
        log_level="info"
    )

if __name__ == "__main__":
    main()