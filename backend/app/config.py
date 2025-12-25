from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Classical Music AI Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/chat.db")

    # LLM API (HuggingFace Inference API)
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

    # Embeddings (HuggingFace)
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

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

    # Composer Scraping
    COMPOSER_SOURCES_DIR: str = "./data/composer_sources"
    COMPOSER_SEED_FILE: str = "./data/composers_seed.json"
    SCRAPE_CACHE_DIR: str = "./data/scrape_cache"

    # Rate Limiting (requests per second)
    RATE_LIMIT_WIKIPEDIA: float = 1.0  # 1 request per second
    RATE_LIMIT_IMSLP: float = 0.5  # 1 request per 2 seconds
    RATE_LIMIT_ALLMUSIC: float = 0.33  # 1 request per 3 seconds

    # Scraper Settings
    MAX_RETRIES: int = 5
    REQUEST_TIMEOUT: int = 30  # seconds
    DEDUP_SIMILARITY_THRESHOLD: float = 0.85
    COMPOSER_FILE_SIZE_TARGET: int = 5 * 1024 * 1024  # 5MB
    COMPOSER_FILE_SIZE_MAX: int = 8 * 1024 * 1024  # 8MB

    # CORS
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176,http://localhost:3000"
    ).split(",")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
