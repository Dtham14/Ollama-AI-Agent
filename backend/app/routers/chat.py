from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.chat import ChatRequest, ChatResponse, MessageSchema
from ..services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get a response"""
    try:
        response = await chat_service.get_response(
            question=request.message,
            db=db,
            session_id=request.session_id,
            include_sources=request.include_sources
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=List[MessageSchema])
async def get_history(
    session_id: str,
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get chat history for a session"""
    try:
        messages = chat_service.get_session_history(db, session_id, limit)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{session_id}")
async def delete_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Delete a chat session and its history"""
    success = chat_service.delete_session_history(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@router.delete("/message/{message_id}")
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """Delete an individual message"""
    success = chat_service.delete_message(db, message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}
