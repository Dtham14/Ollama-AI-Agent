import os
import uuid
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

from langchain_core.documents import Document as LangChainDocument
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..models.document import Document
from ..config import settings
from .vector_service import vector_service


class DocumentService:
    """Service for handling document upload, processing, and embedding"""

    LOADERS = {
        '.pdf': PyPDFLoader,
        '.txt': TextLoader,
        '.csv': CSVLoader,
        '.docx': Docx2txtLoader,
        '.md': UnstructuredMarkdownLoader,
    }

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    async def save_uploaded_file(
        self,
        file_content: bytes,
        original_filename: str,
        db: Session,
        category: str = "Music Theory",
        tags: List[str] = None,
        description: Optional[str] = None
    ) -> Document:
        """Save uploaded file and create database record"""

        # Generate unique filename
        file_ext = Path(original_filename).suffix.lower()
        if file_ext not in self.LOADERS:
            raise ValueError(f"Unsupported file type: {file_ext}")

        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = self.upload_dir / unique_filename

        # Save file to disk
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Create database record
        document = Document(
            filename=unique_filename,
            original_filename=original_filename,
            file_type=file_ext[1:],  # Remove the dot
            file_size=len(file_content),
            file_path=str(file_path),
            category=category,
            tags=tags or [],
            description=description,
            embedded="pending"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    async def process_document(
        self,
        document: Document,
        db: Session
    ) -> int:
        """Process document: load, chunk, and embed into vector store"""

        try:
            # Update status
            document.embedded = "processing"
            db.commit()

            # Load document based on file type
            file_ext = f".{document.file_type}"
            loader_class = self.LOADERS[file_ext]

            if file_ext == '.csv':
                # Special handling for CSV - treat each row as a document
                df = pd.read_csv(document.file_path)
                langchain_docs = []

                for idx, row in df.iterrows():
                    # Combine all columns into content
                    content = " ".join([f"{col}: {row[col]}" for col in df.columns])
                    langchain_docs.append(
                        LangChainDocument(
                            page_content=content,
                            metadata={
                                "source": document.original_filename,
                                "source_type": document.file_type,
                                "category": document.category,
                                "row_index": idx,
                                "document_id": document.id,
                                "user_uploaded": True
                            }
                        )
                    )
            else:
                # Load document
                loader = loader_class(document.file_path)
                loaded_docs = loader.load()

                # Split into chunks
                langchain_docs = self.text_splitter.split_documents(loaded_docs)

                # Add metadata to each chunk
                for idx, doc in enumerate(langchain_docs):
                    doc.metadata.update({
                        "source": document.original_filename,
                        "source_type": document.file_type,
                        "category": document.category,
                        "chunk_index": idx,
                        "total_chunks": len(langchain_docs),
                        "document_id": document.id,
                        "user_uploaded": True,
                        "tags": document.tags
                    })

            # Add to vector store
            ids = [f"{document.id}_{i}" for i in range(len(langchain_docs))]
            vector_service.add_documents(langchain_docs, ids=ids)

            # Update document record
            document.chunk_count = len(langchain_docs)
            document.embedded = "completed"
            document.processed_at = datetime.utcnow()
            db.commit()

            return len(langchain_docs)

        except Exception as e:
            document.embedded = "failed"
            db.commit()
            raise e

    def list_documents(
        self,
        db: Session,
        limit: Optional[int] = None
    ) -> List[Document]:
        """List all uploaded documents"""
        query = db.query(Document).order_by(Document.uploaded_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_document(
        self,
        db: Session,
        document_id: str
    ) -> Optional[Document]:
        """Get a specific document by ID"""
        return db.query(Document).filter(Document.id == document_id).first()

    def delete_document(
        self,
        db: Session,
        document_id: str
    ) -> bool:
        """Delete a document and its embeddings"""
        document = self.get_document(db, document_id)
        if not document:
            return False

        # Delete file from disk
        try:
            os.remove(document.file_path)
        except OSError:
            pass  # File might not exist

        # Delete from vector store (would need to implement delete by metadata in vector_service)
        # For now, we'll just delete the database record

        db.delete(document)
        db.commit()
        return True

    async def reembed_document(
        self,
        db: Session,
        document_id: str
    ) -> int:
        """Re-process and re-embed a document"""
        document = self.get_document(db, document_id)
        if not document:
            raise ValueError("Document not found")

        return await self.process_document(document, db)


# Singleton instance
document_service = DocumentService()
