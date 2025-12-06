"""
Simple and robust content uploader
"""

import asyncio
import os
from pathlib import Path
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from dotenv import load_dotenv
import re

load_dotenv()

# Initialize clients
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "robotics_book_embeddings")

def clean_content(content: str) -> str:
    """Remove MDX syntax"""
    # Remove imports
    content = re.sub(r'^import\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^export\s+.*$', '', content, flags=re.MULTILINE)
    
    # Remove JSX tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Remove comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'{/\*.*?\*/}', '', content, flags=re.DOTALL)
    
    # Clean up whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content.strip()

def chunk_text(text: str, size: int = 1000) -> list[str]:
    """Simple chunking"""
    chunks = []
    words = text.split()
    current = []
    current_size = 0
    
    for word in words:
        current.append(word)
        current_size += len(word) + 1
        
        if current_size >= size:
            chunks.append(' '.join(current))
            current = []
            current_size = 0
    
    if current:
        chunks.append(' '.join(current))
    
    return chunks

async def upload_file(file_path: Path):
    """Upload one file"""
    print(f"\n📄 {file_path.name}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        cleaned = clean_content(content)
        
        if len(cleaned) < 50:
            print(f"   ⚠️  Too short, skipped")
            return 0
        
        chunks = chunk_text(cleaned)
        print(f"   📊 {len(chunks)} chunks")
        
        points = []
        for i, chunk in enumerate(chunks):
            # Create embedding
            response = await openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            )
            embedding = response.data[0].embedding
            
            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "doc_id": file_path.stem,
                    "file": file_path.name,
                    "chunk_index": i
                }
            )
            points.append(point)
            
            # Show progress
            if (i + 1) % 5 == 0:
                print(f"   ... {i + 1}/{len(chunks)}")
        
        # Upload
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        print(f"   ✅ Uploaded {len(points)} chunks")
        return len(points)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0

async def main():
    print("=" * 60)
    print("📚 UPLOADING CONTENT")
    print("=" * 60)
    
    # Find all MDX files
    docs_dir = Path(__file__).parent.parent / "docs"
    files = list(docs_dir.rglob("*.mdx"))
    
    print(f"\n📁 Found {len(files)} files")
    
    total = 0
    for file in sorted(files):
        count = await upload_file(file)
        total += count
    
    # Final count
    info = qdrant_client.get_collection(COLLECTION_NAME)
    
    print("\n" + "=" * 60)
    print("✅ DONE!")
    print("=" * 60)
    print(f"📊 Uploaded: {total} chunks")
    print(f"📚 Total in DB: {info.points_count}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
