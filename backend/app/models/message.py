from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Store source citations as JSON
    sources = Column(JSON, nullable=True)  # List of {source, content, score}

    # Relationship to session
    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, session_id={self.session_id})>"
