"""
IMSLP (International Music Score Library Project) composer scraper.
"""

from typing import Dict, Any, List
import re
from .base_scraper import BaseScraper, ComposerData, NotFoundError
from ..config import settings


class IMSLPScraper(BaseScraper):
    """
    Scraper for IMSLP composer pages.

    Extracts:
    - Composer overview
    - List of compositions (categorized)
    - Work categories
    """

    def __init__(self):
        super().__init__(rate_limit=settings.RATE_LIMIT_IMSLP)
        self.base_url = "https://imslp.org"

    def _get_domain(self) -> str:
        return "imslp.org"

    async def scrape_composer(self, composer_data: Dict[str, Any]) -> ComposerData:
        """
        Scrape composer information from IMSLP.

        Args:
            composer_data: Dict with 'name' and optionally 'imslp_url'

        Returns:
            ComposerData object with scraped content
        """
        composer_name = composer_data.get("name")
        imslp_url = composer_data.get("imslp_url")

        if not imslp_url:
            # Try to construct URL from name
            # Format: "Bach, Johann Sebastian" -> "Category:Bach,_Johann_Sebastian"
            normalized_name = composer_data.get("normalized_name", composer_name)
            imslp_url = f"{self.base_url}/wiki/Category:{normalized_name.replace(' ', '_')}"

        try:
            # Fetch page
            html = await self.fetch_with_retry(imslp_url)
            soup = self.parse_html(html)

            # Extract content
            overview = self._extract_overview(soup)
            works = self._extract_works_list(soup)

            # Compose biography from overview
            biography = f"IMSLP Overview:\n{overview}" if overview else ""

            return ComposerData(
                source="imslp",
                success=True,
                biography=biography,
                works=works,
                metadata={"url": imslp_url},
            )

        except NotFoundError:
            return ComposerData(
                source="imslp",
                success=False,
                error=f"IMSLP page not found for {composer_name}",
            )
        except Exception as e:
            return ComposerData(
                source="imslp", success=False, error=f"IMSLP error: {str(e)}"
            )

    def _extract_overview(self, soup) -> str:
        """Extract composer overview text"""
        # IMSLP uses MediaWiki format similar to Wikipedia
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return ""

        paragraphs = []
        for p in content_div.find_all("p", limit=5):
            text = self.extract_text_from_element(p)
            if text and len(text) > 50:
                paragraphs.append(text)

        return "\n\n".join(paragraphs)

    def _extract_works_list(self, soup) -> List[str]:
        """Extract list of works"""
        works = []

        # Look for composition lists
        # IMSLP organizes by category (Symphonies, Concertos, etc.)
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return works

        # Find category links
        links = content_div.find_all("a", limit=100)
        for link in links:
            text = self.extract_text_from_element(link)
            href = link.get("href", "")

            # Filter for composition links
            if "/wiki/" in href and text and len(text) < 150:
                # Skip navigation links
                if any(
                    skip in text.lower()
                    for skip in ["category", "help", "special", "imslp"]
                ):
                    continue
                works.append(text)

        return works[:50]  # Limit to first 50
