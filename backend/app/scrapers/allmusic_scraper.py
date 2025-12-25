"""
AllMusic database scraper for composer information.
"""

from typing import Dict, Any
from .base_scraper import BaseScraper, ComposerData, NotFoundError
from ..config import settings


class AllMusicScraper(BaseScraper):
    """
    Scraper for AllMusic composer pages.

    Extracts:
    - Artist biography
    - Musical characteristics
    - Historical context
    """

    def __init__(self):
        super().__init__(rate_limit=settings.RATE_LIMIT_ALLMUSIC)
        self.base_url = "https://www.allmusic.com"

    def _get_domain(self) -> str:
        return "allmusic.com"

    async def scrape_composer(self, composer_data: Dict[str, Any]) -> ComposerData:
        """
        Scrape composer information from AllMusic.

        Args:
            composer_data: Dict with 'name' and optionally 'allmusic_url'

        Returns:
            ComposerData object with scraped content
        """
        composer_name = composer_data.get("name")
        allmusic_url = composer_data.get("allmusic_url")

        # AllMusic requires specific artist URLs which we may not have
        # For now, mark as not available if URL not provided
        if not allmusic_url:
            return ComposerData(
                source="allmusic",
                success=False,
                error="AllMusic URL not provided (search not implemented)",
            )

        try:
            # Fetch page
            html = await self.fetch_with_retry(allmusic_url)
            soup = self.parse_html(html)

            # Extract biography
            biography = self._extract_biography(soup)

            # Extract characteristics/style
            style = self._extract_style(soup)

            return ComposerData(
                source="allmusic",
                success=True,
                biography=biography,
                musical_style=style,
                metadata={"url": allmusic_url},
            )

        except NotFoundError:
            return ComposerData(
                source="allmusic",
                success=False,
                error=f"AllMusic page not found for {composer_name}",
            )
        except Exception as e:
            return ComposerData(
                source="allmusic", success=False, error=f"AllMusic error: {str(e)}"
            )

    def _extract_biography(self, soup) -> str:
        """Extract artist biography"""
        # AllMusic biography is typically in a specific div
        bio_div = soup.find("div", {"class": "biography"})
        if not bio_div:
            # Try alternate selectors
            bio_div = soup.find("section", {"class": "biography"})

        if bio_div:
            paragraphs = bio_div.find_all("p")
            texts = [self.extract_text_from_element(p) for p in paragraphs if p]
            return "\n\n".join(texts)

        return ""

    def _extract_style(self, soup) -> str:
        """Extract musical style/characteristics"""
        # Look for style/genre information
        style_section = soup.find("section", {"class": "genre"}) or soup.find(
            "div", {"class": "styles"}
        )

        if style_section:
            return self.extract_text_from_element(style_section)

        return ""
