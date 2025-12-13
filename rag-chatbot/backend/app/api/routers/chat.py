from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import logging
from app.core.database import DatabaseManager
from app.services.openai_service import openai_service
from app.services.qdrant_service import QdrantService
from app.main import get_qdrant_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context_sources: Optional[List[str]] = None
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[Dict[str, Any]]
    context_used: bool

class SelectedTextRequest(BaseModel):
    selected_text: str
    question: str

class SelectedTextResponse(BaseModel):
    answer: str
    context_sources: List[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    qdrant_service: QdrantService = Depends(get_qdrant_service)
):
    """Handle chat message with RAG context"""
    try:
        # Create or get session
        session_id = request.session_id or str(uuid.uuid4())

        # Store user message
        await DatabaseManager.execute_command(
            """
            INSERT INTO chat_messages (session_id, role, content, metadata)
            VALUES ($1, $2, $3, $4)
            """,
            session_id,
            "user",
            request.message,
            "{}"
        )

        # Handle selected text case
        if request.selected_text:
            response_content = await openai_service.analyze_selected_text(
                selected_text=request.selected_text,
                user_question=request.message
            )
            sources = [{"type": "selected_text", "content": request.selected_text}]
            context_used = True

        else:
            # RAG pipeline
            # 1. Create embedding for user query
            query_embedding = await openai_service.create_embedding(request.message)

            # 2. Search for relevant documents
            search_results = await qdrant_service.search(
                query_vector=query_embedding,
                limit=5
            )

            # 3. Get conversation history
            history = await get_conversation_history(session_id)

            # 4. Generate response with context
            if search_results:
                response_content = await openai_service.create_rag_response(
                    query=request.message,
                    context_documents=search_results,
                    conversation_history=history
                )
                sources = [
                    {
                        "file_path": result["payload"]["metadata"]["file_path"],
                        "section": result["payload"]["metadata"]["section_title"],
                        "score": result["score"],
                        "snippet": result["payload"]["content"][:200] + "..."
                    }
                    for result in search_results
                ]
                context_used = True
            else:
                # No relevant context found
                response_content = await openai_service.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant for a robotics textbook. No relevant context was found for the user's question. Provide a general helpful response suggesting they ask about specific topics covered in the textbook."
                        },
                        {"role": "user", "content": request.message}
                    ]
                )
                sources = []
                context_used = False

        # Store assistant response
        await DatabaseManager.execute_command(
            """
            INSERT INTO chat_messages (session_id, role, content, context_sources, metadata)
            VALUES ($1, $2, $3, $4, $5)
            """,
            session_id,
            "assistant",
            response_content,
            json.dumps(sources),
            json.dumps({"context_used": context_used})
        )

        return ChatResponse(
            response=response_content,
            session_id=session_id,
            sources=sources,
            context_used=context_used
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/selected-text", response_model=SelectedTextResponse)
async def analyze_selected_text(request: SelectedTextRequest):
    """Analyze selected text and answer question about it"""
    try:
        # Get answer based on selected text
        answer = await openai_service.analyze_selected_text(
            selected_text=request.selected_text,
            user_question=request.question
        )

        return SelectedTextResponse(
            answer=answer,
            context_sources=["selected_text"]
        )

    except Exception as e:
        logger.error(f"Selected text analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Get all messages for a session"""
    try:
        messages = await DatabaseManager.execute_query(
            """
            SELECT role, content, context_sources, created_at, metadata
            FROM chat_messages
            WHERE session_id = $1
            ORDER BY created_at ASC
            """,
            session_id
        )

        return {
            "session_id": session_id,
            "messages": [
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "sources": json.loads(msg["context_sources"]) if msg["context_sources"] else [],
                    "timestamp": msg["created_at"].isoformat(),
                    "metadata": json.loads(msg["metadata"]) if msg["metadata"] else {}
                }
                for msg in messages
            ]
        }

    except Exception as e:
        logger.error(f"Failed to get session messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    try:
        # Delete messages and session
        await DatabaseManager.execute_command(
            "DELETE FROM chat_messages WHERE session_id = $1",
            session_id
        )

        return {"message": "Session deleted successfully"}

    except Exception as e:
        logger.error(f"Failed to delete session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
async def get_sessions():
    """Get all chat sessions"""
    try:
        sessions = await DatabaseManager.execute_query(
            """
            SELECT DISTINCT cm.session_id,
                   MAX(cm.created_at) as last_message_at,
                   COUNT(*) as message_count,
                   cs.session_metadata
            FROM chat_messages cm
            LEFT JOIN chat_sessions cs ON cm.session_id = cs.id
            GROUP BY cm.session_id, cs.session_metadata
            ORDER BY last_message_at DESC
            """
        )

        return {
            "sessions": [
                {
                    "session_id": session["session_id"],
                    "last_message_at": session["last_message_at"].isoformat(),
                    "message_count": session["message_count"],
                    "metadata": json.loads(session["session_metadata"]) if session["session_metadata"] else {}
                }
                for session in sessions
            ]
        }

    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_conversation_history(session_id: str, limit: int = 10) -> List[Dict[str, str]]:
    """Get conversation history for a session"""
    try:
        messages = await DatabaseManager.execute_query(
            """
            SELECT role, content
            FROM chat_messages
            WHERE session_id = $1
            ORDER BY created_at DESC
            LIMIT $2
            """,
            session_id,
            limit * 2  # Get more to have context
        )

        # Convert to chat format (newest first, so reverse)
        history = [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in reversed(messages)
        ]

        return history

    except Exception as e:
        logger.error(f"Failed to get conversation history: {e}")
        return []