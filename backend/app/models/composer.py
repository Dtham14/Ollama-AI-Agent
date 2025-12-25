"""
Composer model for tracking classical music composers and scraping status.
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from ..database import Base


class Composer(Base):
    """Database model for classical music composers"""

    __tablename__ = "composers"

    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Composer Information
    name = Column(String, nullable=False, unique=True)  # "Johann Sebastian Bach"
    normalized_name = Column(String, nullable=False)  # "Bach, Johann Sebastian"
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)
    era = Column(String, nullable=True)  # "Baroque", "Classical", "Romantic", etc.
    nationality = Column(String, nullable=True)  # "German", "Austrian", etc.

    # Scraping Status Tracking
    scrape_status = Column(
        String, default="pending"
    )  # pending/in_progress/completed/failed
    wikipedia_scraped = Column(Boolean, default=False)
    imslp_scraped = Column(Boolean, default=False)
    allmusic_scraped = Column(Boolean, default=False)

    # Source URLs
    wikipedia_url = Column(String, nullable=True)
    imslp_url = Column(String, nullable=True)
    allmusic_url = Column(String, nullable=True)

    # Output File Information
    output_file = Column(String, nullable=True)  # Path to generated markdown file
    file_size = Column(Integer, nullable=True)  # Size in bytes

    # Error Tracking
    error_count = Column(Integer, default=0)
    last_error = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    scraped_at = Column(DateTime, nullable=True)  # When scraping completed
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<Composer(name={self.name}, era={self.era}, status={self.scrape_status})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "normalized_name": self.normalized_name,
            "birth_year": self.birth_year,
            "death_year": self.death_year,
            "era": self.era,
            "nationality": self.nationality,
            "scrape_status": self.scrape_status,
            "sources_scraped": {
                "wikipedia": self.wikipedia_scraped,
                "imslp": self.imslp_scraped,
                "allmusic": self.allmusic_scraped,
            },
            "output_file": self.output_file,
            "file_size": self.file_size,
            "error_count": self.error_count,
            "last_error": self.last_error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
