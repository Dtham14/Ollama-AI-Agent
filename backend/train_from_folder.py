"""
Bulk training script to process PDFs from a folder.

This script:
1. Scans the training_docs folder for PDF files
2. Processes each PDF (extracts text, chunks it, and embeds into vector store)
3. Tracks which files have been processed to avoid duplicates

Usage:
    python train_from_folder.py

You can put your music theory PDFs in: backend/data/training_docs/
"""

import os
import sys
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.services.document_service import document_service
from app.config import settings


class FolderTrainingService:
    """Service to bulk process documents from a folder"""

    def __init__(self, training_folder: str = None):
        self.training_folder = Path(training_folder or "./data/training_docs")
        self.training_folder.mkdir(parents=True, exist_ok=True)
        print(f"Training folder: {self.training_folder.absolute()}")

    async def process_all_documents(self, force_reprocess: bool = False):
        """Process all documents in the training folder"""

        # Get all supported files
        supported_extensions = settings.ALLOWED_EXTENSIONS
        files_to_process = []

        for ext in supported_extensions:
            files_to_process.extend(self.training_folder.glob(f"*{ext}"))

        if not files_to_process:
            print(f"WARNING: No documents found in {self.training_folder}")
            print(f"   Supported formats: {', '.join(supported_extensions)}")
            return

        print(f"\nFound {len(files_to_process)} documents to process\n")

        db: Session = SessionLocal()
        try:
            processed_count = 0
            skipped_count = 0
            error_count = 0

            for file_path in files_to_process:
                try:
                    # Check if already processed
                    from app.models.document import Document

                    existing_doc = db.query(Document).filter(
                        Document.original_filename == file_path.name
                    ).first()

                    if existing_doc and not force_reprocess:
                        print(f"[SKIP] Already processed: {file_path.name}")
                        skipped_count += 1
                        continue

                    print(f"Processing: {file_path.name}")

                    # Read file
                    with open(file_path, 'rb') as f:
                        file_content = f.read()

                    # Check file size
                    if len(file_content) > settings.MAX_UPLOAD_SIZE:
                        print(f"   [ERROR] File too large (max {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB)")
                        error_count += 1
                        continue

                    # Save and process document
                    if existing_doc and force_reprocess:
                        # Delete existing and reprocess
                        document_service.delete_document(db, existing_doc.id)
                        print(f"   [REPROCESS] Reprocessing existing document...")

                    document = await document_service.save_uploaded_file(
                        file_content=file_content,
                        original_filename=file_path.name,
                        db=db,
                        category="Music Theory",
                        tags=["bulk_import"],
                        description=f"Imported from {self.training_folder.name}"
                    )

                    # Process (chunk and embed)
                    chunk_count = await document_service.process_document(document, db)
                    print(f"   [SUCCESS] Processed! ({chunk_count} chunks)")
                    processed_count += 1

                except Exception as e:
                    print(f"   [ERROR] {file_path.name}: {str(e)}")
                    error_count += 1
                    continue

            print(f"\n{'='*60}")
            print(f"Summary:")
            print(f"   Processed: {processed_count}")
            print(f"   Skipped: {skipped_count}")
            print(f"   Errors: {error_count}")
            print(f"   Total: {len(files_to_process)}")
            print(f"{'='*60}\n")

        finally:
            db.close()


async def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("Music Theory Knowledge Base - Bulk Training Tool")
    print("="*60 + "\n")

    service = FolderTrainingService()

    # Check if user wants to force reprocess
    force_reprocess = False
    if len(sys.argv) > 1 and sys.argv[1] in ['--force', '-f', '--reprocess']:
        force_reprocess = True
        print("WARNING: Force reprocess mode enabled - will reprocess all files\n")

    await service.process_all_documents(force_reprocess=force_reprocess)

    print("Training complete!\n")


if __name__ == "__main__":
    asyncio.run(main())
