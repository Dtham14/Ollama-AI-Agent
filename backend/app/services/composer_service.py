"""
Service for managing composer database operations and scraping lifecycle.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

from ..models.composer import Composer
from ..config import settings


class ComposerService:
    """Service to manage composer database and scraping lifecycle"""

    def load_seed_data(self, db: Session, seed_file: str = None) -> int:
        """
        Load composers from seed JSON file into database.

        Args:
            db: Database session
            seed_file: Path to JSON seed file (defaults to settings.COMPOSER_SEED_FILE)

        Returns:
            Number of composers loaded
        """
        seed_path = Path(seed_file or settings.COMPOSER_SEED_FILE)

        if not seed_path.exists():
            raise FileNotFoundError(f"Seed file not found: {seed_path}")

        with open(seed_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        composers_data = data.get("composers", [])
        loaded_count = 0

        for composer_data in composers_data:
            # Check if composer already exists
            existing = (
                db.query(Composer)
                .filter(Composer.name == composer_data["name"])
                .first()
            )

            if existing:
                continue  # Skip if already in database

            # Create new composer
            composer = Composer(
                name=composer_data["name"],
                normalized_name=composer_data.get(
                    "normalized_name", composer_data["name"]
                ),
                birth_year=composer_data.get("birth_year"),
                death_year=composer_data.get("death_year"),
                era=composer_data.get("era"),
                nationality=composer_data.get("nationality"),
                wikipedia_url=composer_data.get("wikipedia_url"),
                imslp_url=composer_data.get("imslp_url"),
                allmusic_url=composer_data.get("allmusic_url"),
            )

            db.add(composer)
            loaded_count += 1

        db.commit()
        return loaded_count

    def add_composer(
        self,
        db: Session,
        name: str,
        era: Optional[str] = None,
        birth_year: Optional[int] = None,
        death_year: Optional[int] = None,
        nationality: Optional[str] = None,
        **kwargs,
    ) -> Composer:
        """
        Add a new composer to the database.

        Args:
            db: Database session
            name: Composer's full name
            era: Musical era (e.g., "Baroque", "Romantic")
            birth_year: Year of birth
            death_year: Year of death
            nationality: Composer's nationality
            **kwargs: Additional composer attributes

        Returns:
            Created Composer object
        """
        # Generate normalized name if not provided
        normalized_name = kwargs.get("normalized_name")
        if not normalized_name:
            # Simple normalization: "Johann Sebastian Bach" -> "Bach, Johann Sebastian"
            parts = name.split()
            if len(parts) > 1:
                normalized_name = f"{parts[-1]}, {' '.join(parts[:-1])}"
            else:
                normalized_name = name

        composer = Composer(
            name=name,
            normalized_name=normalized_name,
            era=era,
            birth_year=birth_year,
            death_year=death_year,
            nationality=nationality,
            **{k: v for k, v in kwargs.items() if k != "normalized_name"},
        )

        db.add(composer)
        db.commit()
        db.refresh(composer)
        return composer

    def get_composer(self, db: Session, composer_id: str) -> Optional[Composer]:
        """Get composer by ID"""
        return db.query(Composer).filter(Composer.id == composer_id).first()

    def get_composer_by_name(self, db: Session, name: str) -> Optional[Composer]:
        """Get composer by name"""
        return db.query(Composer).filter(Composer.name == name).first()

    def get_all_composers(self, db: Session) -> List[Composer]:
        """Get all composers"""
        return db.query(Composer).order_by(Composer.era, Composer.name).all()

    def get_pending_composers(self, db: Session) -> List[Composer]:
        """Get composers with status='pending'"""
        return (
            db.query(Composer)
            .filter(Composer.scrape_status == "pending")
            .order_by(Composer.era, Composer.name)
            .all()
        )

    def get_composers_by_era(self, db: Session, era: str) -> List[Composer]:
        """Get composers filtered by era"""
        return (
            db.query(Composer)
            .filter(Composer.era == era)
            .order_by(Composer.name)
            .all()
        )

    def get_failed_composers(self, db: Session) -> List[Composer]:
        """Get composers with status='failed'"""
        return (
            db.query(Composer)
            .filter(Composer.scrape_status == "failed")
            .order_by(Composer.era, Composer.name)
            .all()
        )

    def update_scrape_status(
        self, db: Session, composer_id: str, status: str
    ) -> Composer:
        """
        Update composer's overall scraping status.

        Args:
            db: Database session
            composer_id: Composer ID
            status: New status (pending/in_progress/completed/failed)

        Returns:
            Updated Composer object
        """
        composer = self.get_composer(db, composer_id)
        if not composer:
            raise ValueError(f"Composer not found: {composer_id}")

        composer.scrape_status = status
        composer.updated_at = datetime.utcnow()

        if status == "completed":
            composer.scraped_at = datetime.utcnow()

        db.commit()
        db.refresh(composer)
        return composer

    def mark_source_scraped(
        self, db: Session, composer_id: str, source: str, scraped: bool = True
    ) -> Composer:
        """
        Mark a specific source as scraped for a composer.

        Args:
            db: Database session
            composer_id: Composer ID
            source: Source name ('wikipedia', 'imslp', 'allmusic')
            scraped: Whether the source was successfully scraped

        Returns:
            Updated Composer object
        """
        composer = self.get_composer(db, composer_id)
        if not composer:
            raise ValueError(f"Composer not found: {composer_id}")

        source = source.lower()
        if source == "wikipedia":
            composer.wikipedia_scraped = scraped
        elif source == "imslp":
            composer.imslp_scraped = scraped
        elif source == "allmusic":
            composer.allmusic_scraped = scraped
        else:
            raise ValueError(f"Unknown source: {source}")

        composer.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(composer)
        return composer

    def update_output_file(
        self, db: Session, composer_id: str, file_path: str, file_size: int
    ) -> Composer:
        """
        Update composer's output file information.

        Args:
            db: Database session
            composer_id: Composer ID
            file_path: Path to the generated markdown file
            file_size: Size of the file in bytes

        Returns:
            Updated Composer object
        """
        composer = self.get_composer(db, composer_id)
        if not composer:
            raise ValueError(f"Composer not found: {composer_id}")

        composer.output_file = file_path
        composer.file_size = file_size
        composer.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(composer)
        return composer

    def record_error(
        self, db: Session, composer_id: str, error_message: str
    ) -> Composer:
        """
        Record an error for a composer.

        Args:
            db: Database session
            composer_id: Composer ID
            error_message: Error message

        Returns:
            Updated Composer object
        """
        composer = self.get_composer(db, composer_id)
        if not composer:
            raise ValueError(f"Composer not found: {composer_id}")

        composer.error_count += 1
        composer.last_error = error_message
        composer.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(composer)
        return composer

    def get_statistics(self, db: Session) -> dict:
        """
        Get overall statistics about composer scraping progress.

        Returns:
            Dictionary with statistics
        """
        total = db.query(Composer).count()
        pending = (
            db.query(Composer).filter(Composer.scrape_status == "pending").count()
        )
        in_progress = (
            db.query(Composer).filter(Composer.scrape_status == "in_progress").count()
        )
        completed = (
            db.query(Composer).filter(Composer.scrape_status == "completed").count()
        )
        failed = db.query(Composer).filter(Composer.scrape_status == "failed").count()

        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "failed": failed,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
        }


# Singleton instance
composer_service = ComposerService()
