"""
Scraper orchestrator to coordinate multi-source scraping.
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime

from .wikipedia_scraper import WikipediaComposerScraper
from .imslp_scraper import IMSLPScraper
from .allmusic_scraper import AllMusicScraper
from .base_scraper import ComposerData


class ScraperOrchestrator:
    """
    Orchestrates scraping from multiple sources.

    Features:
    - Parallel scraping from Wikipedia, IMSLP, AllMusic
    - Aggregates results from all sources
    - Handles partial failures gracefully
    """

    def __init__(self):
        self.wikipedia_scraper = WikipediaComposerScraper()
        self.imslp_scraper = IMSLPScraper()
        self.allmusic_scraper = AllMusicScraper()

    async def scrape_composer(
        self, composer_data: Dict[str, Any], sources: List[str] = None
    ) -> Dict[str, ComposerData]:
        """
        Scrape composer from multiple sources in parallel.

        Args:
            composer_data: Dictionary with composer info (name, urls, etc.)
            sources: List of sources to scrape (default: all)
                    Options: ['wikipedia', 'imslp', 'allmusic']

        Returns:
            Dictionary mapping source name to ComposerData
        """
        if sources is None:
            sources = ["wikipedia", "imslp", "allmusic"]

        tasks = {}

        if "wikipedia" in sources:
            tasks["wikipedia"] = self.wikipedia_scraper.scrape_composer(composer_data)

        if "imslp" in sources:
            tasks["imslp"] = self.imslp_scraper.scrape_composer(composer_data)

        if "allmusic" in sources:
            tasks["allmusic"] = self.allmusic_scraper.scrape_composer(composer_data)

        # Run all scrapers in parallel
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        # Map results back to source names
        scraped_data = {}
        for (source, _), result in zip(tasks.items(), results):
            if isinstance(result, Exception):
                # Handle exception
                scraped_data[source] = ComposerData(
                    source=source, success=False, error=str(result)
                )
            else:
                scraped_data[source] = result

        return scraped_data

    def get_summary(self, scraped_data: Dict[str, ComposerData]) -> Dict[str, Any]:
        """
        Get summary of scraping results.

        Args:
            scraped_data: Dictionary of scraped data by source

        Returns:
            Summary dictionary
        """
        total = len(scraped_data)
        successful = sum(1 for data in scraped_data.values() if data.success)
        failed = total - successful

        sources_scraped = {
            source: data.success for source, data in scraped_data.items()
        }

        return {
            "total_sources": total,
            "successful": successful,
            "failed": failed,
            "sources": sources_scraped,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Singleton instance
scraper_orchestrator = ScraperOrchestrator()
