"""
RAG Service - Core Retrieval-Augmented Generation logic
Handles vector search and answer generation
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import AsyncOpenAI
import os
from typing import List, Dict, Optional
import uuid
from .embedding_service import EmbeddingService

class RAGService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "robotics_book_embeddings")
        self.chat_model = os.getenv("CHAT_MODEL", "gpt-4-turbo-preview")
        self.max_tokens = int(os.getenv("MAX_TOKENS", 1000))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))
        
        self.client = None
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def initialize(self):
        """Initialize Qdrant client and create collection if needed"""
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )
        
        # Create collection if it doesn't exist
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created Qdrant collection: {self.collection_name}")
    
    async def add_text_chunk(
        self,
        text: str,
        embedding: List[float],
        metadata: Dict = {},
        doc_id: Optional[str] = None
    ) -> str:
        """Add a text chunk with its embedding to Qdrant"""
        chunk_id = str(uuid.uuid4())
        
        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "text": text,
                "doc_id": doc_id or "unknown",
                **metadata
            }
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
        return chunk_id
    
    async def search_similar(
        self,
        query_embedding: List[float],
        limit: int = 5
    ) -> List[Dict]:
        """Search for similar text chunks using vector similarity"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        return [
            {
                "id": hit.id,
                "score": hit.score,
                "text": hit.payload.get("text", ""),
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            }
            for hit in results
        ]
    
    async def query(
        self,
        question: str,
        max_results: int = 5,
        additional_context: Optional[str] = None
    ) -> Dict:
        """
        Query the RAG system with a question
        
        Returns:
            Dictionary with answer, sources, and confidence
        """
        
        # Create embedding service
        embedding_service = EmbeddingService()
        
        # Get question embedding
        question_embedding = await embedding_service.create_embedding(question)
        
        # Search for relevant chunks
        similar_chunks = await self.search_similar(question_embedding, max_results)
        
        # Build context from retrieved chunks
        context_parts = []
        for i, chunk in enumerate(similar_chunks, 1):
            context_parts.append(f"[Source {i}]: {chunk['text']}")
        
        context = "\n\n".join(context_parts)
        
        # Add selected text if provided
        if additional_context:
            context = f"Selected Text:\n{additional_context}\n\n{context}"
        
        # Generate answer using OpenAI
        system_prompt = """You are an expert AI assistant for the Physical AI & Humanoid Robotics Lab textbook.
Your role is to answer questions accurately based on the provided context from the book.

Guidelines:
- Answer based ONLY on the provided context
- Be precise and technical when appropriate
- If the context doesn't contain enough information, say so
- Cite sources when possible
- Use clear, educational language"""

        user_prompt = f"""Context from the textbook:
{context}

Question: {question}

Please provide a detailed answer based on the context above."""

        response = await self.openai_client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        answer = response.choices[0].message.content
        
        # Calculate confidence based on similarity scores
        avg_score = sum(chunk["score"] for chunk in similar_chunks) / len(similar_chunks) if similar_chunks else 0
        
        return {
            "answer": answer,
            "sources": similar_chunks,
            "confidence": round(avg_score, 2)
        }
    
    async def clear_collection(self):
        """Clear all vectors from the collection"""
        self.client.delete_collection(collection_name=self.collection_name)
        await self.initialize()  # Recreate empty collection
