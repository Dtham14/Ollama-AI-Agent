"""
Vercel serverless entry point for FastAPI app
Uses Mangum to adapt ASGI app for serverless environment

Note: For Vercel serverless deployment:
- Database (SQLite) is ephemeral and resets on cold starts
- Vector store needs to be rebuilt from composer markdown files
- First request after cold start will be slower (30-60 seconds)
"""
from mangum import Mangum
from app.main import app
from app.database import init_db
import os

# Initialize database tables on cold start
# Note: Database is ephemeral and will reset on each deployment
try:
    init_db()
    print("✓ Database initialized for serverless")
except Exception as e:
    print(f"⚠ Database initialization warning: {e}")

# Initialize vector store with composer data on cold start
# This makes first cold start slow (30-60s) but ensures data is available
try:
    import asyncio
    from init_vector_store import initialize_vector_store

    # Run async initialization
    asyncio.run(initialize_vector_store())

    # Verify initialization
    from app.services.vector_service import vector_service
    collection = vector_service.vector_store._collection
    count = collection.count()
    print(f"✓ Vector store initialized with {count} chunks")
except Exception as e:
    print(f"⚠ Vector store initialization: {e}")
    print("  Vector store will be empty - upload documents via /api/documents/upload")

# Wrap FastAPI app for Vercel serverless
# lifespan="auto" allows the app's lifespan manager to run if needed
handler = Mangum(app, lifespan="auto")
