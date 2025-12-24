from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DocumentUpload(BaseModel):
    category: str = "Music Theory"
    tags: List[str] = []
    description: Optional[str] = None


class DocumentMetadata(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    category: str
    tags: List[str]
    description: Optional[str]
    chunk_count: int
    embedded: str
    uploaded_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: List[DocumentMetadata]
    total: int
