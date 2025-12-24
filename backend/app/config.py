from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Music Theory Q&A"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./data/chat.db"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "llama3.2"
    EMBEDDING_MODEL: str = "mxbai-embed-large"

    # Vector Store
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "music-theory-knowledge"

    # Document Upload
    UPLOAD_DIR: str = "./data/documents"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".txt", ".csv", ".docx", ".md"}

    # Chat
    MAX_HISTORY_LENGTH: int = 50
    RETRIEVAL_K: int = 3  # Number of docs to retrieve

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:3000"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
