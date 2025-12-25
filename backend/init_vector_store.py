"""Initialize vector store from composer markdown files on startup"""
import os
import asyncio
from pathlib import Path
from app.database import SessionLocal
from app.services.document_service import document_service

async def initialize_vector_store():
    """Load all composer files into vector store if empty"""
    print("Checking vector store...")

    composer_dir = Path("data/composer_sources")

    if not composer_dir.exists():
        print("No composer source files found. Skipping vector store initialization.")
        return

    # Check if vector store is already populated
    from app.services.vector_service import vector_service
    try:
        collection = vector_service.vector_store._collection
        count = collection.count()

        if count > 0:
            print(f"Vector store already has {count} chunks. Skipping initialization.")
            return
    except Exception as e:
        print(f"Error checking vector store: {e}")

    print("Vector store is empty. Initializing from composer files...")

    db = SessionLocal()
    total_chunks = 0

    try:
        # Find all markdown files
        md_files = list(composer_dir.glob("**/*.md"))
        print(f"Found {len(md_files)} composer files to process...")

        for i, md_file in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] Processing {md_file.name}...")

            try:
                # Read file content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract metadata from filename (e.g., "Bach_Johann_Sebastian.md")
                composer_name = md_file.stem.replace('_', ' ')
                era = md_file.parent.name if md_file.parent != composer_dir else "Unknown"

                # Save to database and process
                document = await document_service.save_uploaded_file(
                    file_content=content.encode('utf-8'),
                    original_filename=md_file.name,
                    db=db,
                    category="Composer Biography",
                    tags=["composer", era.lower(), "biography"],
                    description=f"{composer_name} - {era} period composer biography"
                )

                # Process into vector store
                chunk_count = await document_service.process_document(document, db)
                total_chunks += chunk_count
                print(f"  ✓ Added {chunk_count} chunks")

            except Exception as e:
                print(f"  ✗ Error processing {md_file.name}: {e}")
                continue

        print(f"\n✓ Vector store initialized with {total_chunks} total chunks from {len(md_files)} composers")

    except Exception as e:
        print(f"Error during initialization: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(initialize_vector_store())
