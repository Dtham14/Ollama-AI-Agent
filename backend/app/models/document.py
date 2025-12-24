from sqlalchemy import Column, String, DateTime, Integer, JSON
from datetime import datetime
import uuid
from ..database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, txt, csv, docx, md
    file_size = Column(Integer, nullable=False)  # bytes
    file_path = Column(String, nullable=False)  # path to stored file

    # Metadata
    category = Column(String, default="Music Theory")
    tags = Column(JSON, default=list)  # List of tags
    description = Column(String, nullable=True)

    # Processing info
    chunk_count = Column(Integer, default=0)
    embedded = Column(String, default="pending")  # pending, processing, completed, failed

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, embedded={self.embedded})>"
