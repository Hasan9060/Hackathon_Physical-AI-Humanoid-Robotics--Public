import openai
import tiktoken
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for OpenAI operations including embeddings and chat completions"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.encoding = tiktoken.encoding_for_model(settings.EMBEDDING_MODEL)

    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text"""
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to create embedding: {e}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts"""
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"Failed to create embeddings batch: {e}")
            raise

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """Create chat completion"""
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise

    async def create_rag_response(
        self,
        query: str,
        context_documents: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """Create a RAG-enhanced response using context documents"""

        # Prepare context
        context_text = self._prepare_context(context_documents)

        # Prepare system message
        system_message = self._create_system_message(context_text)

        # Prepare conversation
        messages = [system_message]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-5:])  # Last 5 messages

        # Add current query
        messages.append({
            "role": "user",
            "content": query
        })

        # Create response
        response = await self.chat_completion(
            messages=messages,
            temperature=0.3,  # Lower temperature for more factual responses
            max_tokens=1000
        )

        return response

    def _prepare_context(self, documents: List[Dict[str, Any]]) -> str:
        """Prepare context text from retrieved documents"""
        if not documents:
            return "No relevant context found in the textbook."

        context_parts = []
        for i, doc in enumerate(documents, 1):
            payload = doc.get("payload", {})
            content = payload.get("content", "")
            metadata = payload.get("metadata", {})

            # Format context with source information
            source_info = f"Source: {metadata.get('file_path', 'Unknown')}"
            section_info = metadata.get('section', 'Unknown section')

            context_part = f"""
Context Document {i}:
{source_info}
Section: {section_info}
Content: {content}
---
"""
            context_parts.append(context_part)

        return "\n".join(context_parts)

    def _create_system_message(self, context_text: str) -> Dict[str, str]:
        """Create system message for RAG response"""
        system_prompt = f"""
You are an expert AI assistant specializing in Physical AI and Humanoid Robotics.
Your role is to help users understand the textbook content by providing accurate,
context-aware answers based on the provided context.

CONTEXT FROM TEXTBOOK:
{context_text}

INSTRUCTIONS:
1. Use only the provided context to answer questions
2. If the context doesn't contain the answer, say "I don't have enough information in the textbook to answer that question"
3. Provide clear, educational responses that help users learn
4. Reference specific sections or concepts from the textbook when relevant
5. Keep responses focused on robotics, AI, and related technical topics
6. When explaining concepts, use examples from the textbook when available
7. Always prioritize accuracy and educational value

Remember: You are a helpful assistant for this specific robotics textbook, not a general chatbot.
"""

        return {
            "role": "system",
            "content": system_prompt
        }

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            logger.error(f"Token counting failed: {e}")
            return len(text.split())  # Fallback to word count

    def truncate_text(self, text: str, max_tokens: int = 8000) -> str:
        """Truncate text to maximum token limit"""
        try:
            tokens = self.encoding.encode(text)
            if len(tokens) <= max_tokens:
                return text

            truncated_tokens = tokens[:max_tokens]
            return self.encoding.decode(truncated_tokens)
        except Exception as e:
            logger.error(f"Text truncation failed: {e}")
            # Fallback to character truncation
            max_chars = max_tokens * 4  # Rough estimate
            return text[:max_chars]

    async def analyze_selected_text(
        self,
        selected_text: str,
        user_question: str
    ) -> str:
        """Analyze selected text and answer question about it"""

        system_prompt = f"""
You are analyzing a specific excerpt from the Physical AI & Humanoid Robotics textbook.
The user has selected the following text from the book:

SELECTED TEXT:
{selected_text}

Please answer the user's question based ONLY on this selected text. Do not use any external knowledge.
If the selected text doesn't contain information to answer the question, say so clearly.

User Question: {user_question}

Provide a focused, accurate answer based on the selected text.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ]

        response = await self.chat_completion(
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )

        return response

# Create global service instance
openai_service = OpenAIService()