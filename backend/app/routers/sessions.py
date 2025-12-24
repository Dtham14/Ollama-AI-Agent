from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from ..database import get_db
from ..models.session import Session as ChatSession

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


class SessionResponse(BaseModel):
    id: str
    title: str | None
    created_at: str
    updated_at: str
    message_count: int
    model_name: str

    class Config:
        from_attributes = True


class CreateSessionRequest(BaseModel):
    title: str | None = None
    model_name: str | None = None


@router.post("", response_model=SessionResponse)
async def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    new_session = ChatSession(
        title=request.title,
        model_name=request.model_name or "llama3.2"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return SessionResponse(
        id=new_session.id,
        title=new_session.title,
        created_at=new_session.created_at.isoformat(),
        updated_at=new_session.updated_at.isoformat(),
        message_count=new_session.message_count,
        model_name=new_session.model_name
    )


@router.get("", response_model=List[SessionResponse])
async def list_sessions(
    db: Session = Depends(get_db),
    limit: int = 50
):
    """List all chat sessions"""
    sessions = db.query(ChatSession).order_by(
        ChatSession.updated_at.desc()
    ).limit(limit).all()

    return [
        SessionResponse(
            id=s.id,
            title=s.title,
            created_at=s.created_at.isoformat(),
            updated_at=s.updated_at.isoformat(),
            message_count=s.message_count,
            model_name=s.model_name
        )
        for s in sessions
    ]


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get details of a specific session"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
        message_count=session.message_count,
        model_name=session.model_name
    )
