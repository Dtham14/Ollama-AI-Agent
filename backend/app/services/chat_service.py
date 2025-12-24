from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from .vector_service import vector_service
from ..models.session import Session as ChatSession
from ..models.message import Message
from ..schemas.chat import ChatResponse, MessageSchema, SourceCitation
from ..config import settings


class ChatService:
    """Service for handling chat interactions with LLM"""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.DEFAULT_MODEL
        self.model = OllamaLLM(
            model=self.model_name,
            base_url=settings.OLLAMA_BASE_URL
        )

        # Prompt template from original main.py
        self.template = """
You are an expert in answering questions about Music Theory.
Here are some facts: {facts}
Here is the question to answer: {question}
"""
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    def get_or_create_session(
        self,
        db: Session,
        session_id: Optional[str] = None
    ) -> ChatSession:
        """Get existing session or create a new one"""
        if session_id:
            session = db.query(ChatSession).filter(
                ChatSession.id == session_id
            ).first()
            if session:
                return session

        # Create new session
        new_session = ChatSession(model_name=self.model_name)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    async def get_response(
        self,
        question: str,
        db: Session,
        session_id: Optional[str] = None,
        include_sources: bool = True
    ) -> ChatResponse:
        """Get chat response for a question"""

        # Get or create session
        session = self.get_or_create_session(db, session_id)

        # Save user message
        user_message = Message(
            session_id=session.id,
            role="user",
            content=question
        )
        db.add(user_message)
        db.commit()

        # Retrieve relevant facts from vector store
        if include_sources:
            sources = vector_service.get_source_citations(question)
            facts_text = "\n".join([s.content for s in sources])
        else:
            docs = vector_service.search(question)
            facts_text = "\n".join([doc.page_content for doc in docs])
            sources = None

        # Get LLM response
        result = self.chain.invoke({
            "facts": facts_text,
            "question": question
        })

        # Save assistant message
        assistant_message = Message(
            session_id=session.id,
            role="assistant",
            content=result,
            sources=[s.model_dump() for s in sources] if sources else None
        )
        db.add(assistant_message)

        # Update session
        session.message_count += 2  # user + assistant
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(assistant_message)

        # Convert to schema
        message_schema = MessageSchema(
            id=assistant_message.id,
            role=assistant_message.role,
            content=assistant_message.content,
            created_at=assistant_message.created_at,
            sources=sources if include_sources else None
        )

        return ChatResponse(
            session_id=session.id,
            message=message_schema,
            model_used=self.model_name
        )

    def get_session_history(
        self,
        db: Session,
        session_id: str,
        limit: int = None
    ) -> List[MessageSchema]:
        """Get chat history for a session"""
        limit = limit or settings.MAX_HISTORY_LENGTH

        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at).limit(limit).all()

        return [
            MessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
                sources=[SourceCitation(**s) for s in msg.sources] if msg.sources else None
            )
            for msg in messages
        ]

    def delete_session_history(self, db: Session, session_id: str) -> bool:
        """Delete all messages in a session"""
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()

        if not session:
            return False

        db.delete(session)  # Cascade will delete messages
        db.commit()
        return True

    def delete_message(self, db: Session, message_id: str) -> bool:
        """Delete an individual message"""
        message = db.query(Message).filter(
            Message.id == message_id
        ).first()

        if not message:
            return False

        # Update the session's message count
        session = db.query(ChatSession).filter(
            ChatSession.id == message.session_id
        ).first()

        if session and session.message_count > 0:
            session.message_count -= 1
            session.updated_at = datetime.utcnow()

        db.delete(message)
        db.commit()
        return True


# Create singleton with default model
chat_service = ChatService()
