from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SourceCitation(BaseModel):
    source: str
    content: str
    score: float
    metadata: Optional[dict] = None


class MessageSchema(BaseModel):
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime
    sources: Optional[List[SourceCitation]] = None

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    include_sources: bool = True


class ChatResponse(BaseModel):
    session_id: str
    message: MessageSchema
    model_used: str
