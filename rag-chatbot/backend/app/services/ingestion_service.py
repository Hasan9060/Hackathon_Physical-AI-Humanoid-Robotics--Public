import asyncio
import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import aiofiles
import markdown
from bs4 import BeautifulSoup
import re
import logging
from app.core.config import settings, BOOK_CONTENT_DIR
from app.core.database import DatabaseManager
from app.services.openai_service import openai_service

logger = logging.getLogger(__name__)

class ContentIngestionService:
    """Service for ingesting book content into the RAG system"""

    def __init__(self):
        """Initialize ingestion service"""
        self.processed_files = set()
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    async def ingest_all_content(self):
        """Ingest all content from the book"""
        logger.info("Starting content ingestion...")

        try:
            # Scan for all markdown files
            md_files = self._scan_for_markdown_files()
            logger.info(f"Found {len(md_files)} markdown files to process")

            # Process each file
            for file_path in md_files:
                await self._process_file(file_path)

            logger.info("Content ingestion completed successfully")
            return {"status": "success", "processed_files": len(self.processed_files)}

        except Exception as e:
            logger.error(f"Content ingestion failed: {e}")
            raise

    def _scan_for_markdown_files(self) -> List[Path]:
        """Scan for markdown files in the content directory"""
        md_files = []

        if not BOOK_CONTENT_DIR.exists():
            logger.error(f"Book content directory not found: {BOOK_CONTENT_DIR}")
            return []

        # Recursively find all .md files
        for file_path in BOOK_CONTENT_DIR.rglob("*.md"):
            if file_path.is_file():
                # Skip certain files/directories
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                md_files.append(file_path)

        return sorted(md_files)

    async def _process_file(self, file_path: Path):
        """Process a single markdown file"""
        try:
            logger.info(f"Processing file: {file_path}")

            # Read file content
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()

            # Extract metadata and content
            metadata = self._extract_metadata(content, file_path)
            clean_content = self._extract_content(content)

            # Parse HTML structure
            html_content = markdown.markdown(clean_content, extensions=['extra', 'codehilite'])
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract structured content
            sections = self._extract_sections(soup, str(file_path))

            # Create chunks
            chunks = await self._create_chunks(sections, metadata)

            # Store chunks in database
            await self._store_chunks(chunks, str(file_path))

            self.processed_files.add(str(file_path))
            logger.info(f"Successfully processed file: {file_path}")

        except Exception as e:
            logger.error(f"Failed to process file {file_path}: {e}")
            raise

    def _extract_metadata(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract frontmatter metadata from markdown file"""
        metadata = {
            "file_path": str(file_path.relative_to(BOOK_CONTENT_DIR)),
            "file_name": file_path.name,
            "section": "Unknown"
        }

        # Extract frontmatter if present
        if content.startswith('---'):
            try:
                frontmatter_end = content.find('---', 3)
                if frontmatter_end != -1:
                    frontmatter = content[3:frontmatter_end].strip()
                    # Parse YAML-like frontmatter
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip().strip('"\'')
            except Exception as e:
                logger.warning(f"Failed to parse frontmatter: {e}")

        # Infer section from file path
        path_parts = file_path.relative_to(BOOK_CONTENT_DIR).parts
        if len(path_parts) > 1:
            metadata["section"] = path_parts[0].replace('-', ' ').title()

        return metadata

    def _extract_content(self, content: str) -> str:
        """Extract content without frontmatter"""
        if content.startswith('---'):
            frontmatter_end = content.find('---', 3)
            if frontmatter_end != -1:
                return content[frontmatter_end + 3:].strip()
        return content

    def _extract_sections(self, soup: BeautifulSoup, file_path: str) -> List[Dict[str, Any]]:
        """Extract structured sections from HTML content"""
        sections = []

        # Find all headers
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        if not headers:
            # No headers, treat entire content as one section
            content_text = self._clean_text(soup.get_text())
            if content_text.strip():
                sections.append({
                    "level": 0,
                    "title": "Content",
                    "content": content_text,
                    "html": str(soup)
                })
        else:
            current_section = None
            current_content = []

            for i, element in enumerate(soup.find_all()):
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    # Save previous section
                    if current_section and current_content:
                        current_section["content"] = "\n".join(current_content)
                        current_section["html"] = "\n".join(str(c) for c in current_content)
                        sections.append(current_section)

                    # Start new section
                    current_section = {
                        "level": int(element.name[1]),
                        "title": element.get_text().strip(),
                        "content": "",
                        "html": ""
                    }
                    current_content = []

                elif current_section:
                    # Add content to current section
                    if element.get_text().strip():
                        current_content.append(str(element))

                else:
                    # Content before first header
                    pass

            # Save last section
            if current_section and current_content:
                current_section["content"] = "\n".join(current_content)
                current_section["html"] = "\n".join(str(c) for c in current_content)
                sections.append(current_section)

        # Filter sections with meaningful content
        filtered_sections = []
        for section in sections:
            content_text = self._clean_text(section["content"])
            if len(content_text.strip()) > 50:  # Only keep sections with substantial content
                section["content"] = content_text
                section["word_count"] = len(content_text.split())
                filtered_sections.append(section)

        return filtered_sections

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\?\!\;\:\-\(\)\[\]\{\}\"\'\/\\]', '', text)
        # Normalize spacing around punctuation
        text = re.sub(r'\s*([.,;:!?])\s*', r'\1 ', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    async def _create_chunks(self, sections: List[Dict[str, Any]], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create chunks from sections"""
        chunks = []
        chunk_id = 0

        for section in sections:
            content = section["content"]
            if len(content) < self.chunk_size:
                # Small content, create single chunk
                chunk = {
                    "id": f"{metadata['file_path']}_chunk_{chunk_id}",
                    "content": content,
                    "metadata": {
                        **metadata,
                        "section_title": section["title"],
                        "section_level": section["level"],
                        "word_count": section["word_count"],
                        "chunk_index": chunk_id
                    }
                }
                chunks.append(chunk)
                chunk_id += 1
            else:
                # Large content, split into multiple chunks
                words = content.split()
                start_pos = 0

                while start_pos < len(words):
                    end_pos = min(start_pos + self.chunk_size, len(words))
                    chunk_words = words[start_pos:end_pos]
                    chunk_content = " ".join(chunk_words)

                    chunk = {
                        "id": f"{metadata['file_path']}_chunk_{chunk_id}",
                        "content": chunk_content,
                        "metadata": {
                            **metadata,
                            "section_title": section["title"],
                            "section_level": section["level"],
                            "word_count": len(chunk_words),
                            "chunk_index": chunk_id,
                            "total_chunks": (len(words) + self.chunk_size - 1) // self.chunk_size
                        }
                    }
                    chunks.append(chunk)
                    chunk_id += 1

                    # Move to next chunk with overlap
                    start_pos = end_pos - self.chunk_overlap

        return chunks

    async def _store_chunks(self, chunks: List[Dict[str, Any]], file_path: str):
        """Store chunks in database and prepare for vectorization"""
        try:
            # Clear existing chunks for this file
            await DatabaseManager.execute_command(
                "DELETE FROM content_chunks WHERE file_path = $1",
                file_path
            )

            # Insert new chunks
            for chunk in chunks:
                # Create vector embedding
                embedding = await openai_service.create_embedding(chunk["content"])

                # Generate vector ID
                vector_id = hashlib.md5(
                    f"{chunk['id']}_{chunk['content'][:100]}".encode()
                ).hexdigest()

                # Store in database
                await DatabaseManager.execute_command(
                    """
                    INSERT INTO content_chunks (id, file_path, chunk_index, content, metadata, vector_id)
                    VALUES (gen_random_uuid(), $1, $2, $3, $4, $5)
                    """,
                    file_path,
                    chunk["metadata"]["chunk_index"],
                    chunk["content"],
                    json.dumps(chunk["metadata"]),
                    vector_id
                )

                # Prepare for Qdrant
                chunk["vector"] = embedding
                chunk["vector_id"] = vector_id

            logger.info(f"Stored {len(chunks)} chunks from {file_path}")
            return chunks

        except Exception as e:
            logger.error(f"Failed to store chunks: {e}")
            raise

    async def get_ingestion_status(self) -> Dict[str, Any]:
        """Get current ingestion status"""
        try:
            # Get total files
            md_files = self._scan_for_markdown_files()
            total_files = len(md_files)

            # Get processed files from database
            result = await DatabaseManager.execute_query(
                """
                SELECT COUNT(DISTINCT file_path) as processed_files,
                       COUNT(*) as total_chunks
                FROM content_chunks
                """
            )

            processed_files = result[0]["processed_files"] if result else 0
            total_chunks = result[0]["total_chunks"] if result else 0

            return {
                "total_files": total_files,
                "processed_files": processed_files,
                "total_chunks": total_chunks,
                "completion_percentage": (processed_files / total_files * 100) if total_files > 0 else 0
            }

        except Exception as e:
            logger.error(f"Failed to get ingestion status: {e}")
            raise

# Create global service instance
ingestion_service = ContentIngestionService()