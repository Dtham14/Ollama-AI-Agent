from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.document import DocumentMetadata, DocumentListResponse
from ..services.document_service import document_service
from ..config import settings

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentMetadata)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("Music Theory"),
    tags: str = Form(""),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload a new document"""

    # Validate file size
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    # Validate file extension
    file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if f".{file_ext}" not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    try:
        # Parse tags
        tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []

        # Save file
        document = await document_service.save_uploaded_file(
            file_content=content,
            original_filename=file.filename,
            db=db,
            category=category,
            tags=tag_list,
            description=description
        )

        # Process document asynchronously (in background)
        # For now, we'll do it synchronously
        await document_service.process_document(document, db)

        # Refresh to get updated data
        db.refresh(document)

        return DocumentMetadata.from_orm(document)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    limit: Optional[int] = 50,
    db: Session = Depends(get_db)
):
    """List all uploaded documents"""
    try:
        documents = document_service.list_documents(db, limit=limit)
        doc_metadata = [DocumentMetadata.from_orm(doc) for doc in documents]

        return DocumentListResponse(
            documents=doc_metadata,
            total=len(doc_metadata)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentMetadata)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific document by ID"""
    document = document_service.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentMetadata.from_orm(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Delete a document"""
    success = document_service.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}


@router.post("/{document_id}/reembed")
async def reembed_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Re-process and re-embed a document"""
    try:
        chunk_count = await document_service.reembed_document(db, document_id)
        return {
            "message": "Document re-embedded successfully",
            "chunk_count": chunk_count
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
