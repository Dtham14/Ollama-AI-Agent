"""
Wikipedia composer scraper using Wikipedia API and HTML parsing.
"""

from typing import Dict, Any, List
import re
from .base_scraper import BaseScraper, ComposerData, NotFoundError
from ..config import settings


class WikipediaComposerScraper(BaseScraper):
    """
    Scraper for Wikipedia composer pages.

    Extracts:
    - Biography (lead section + early life + career)
    - Musical style and characteristics
    - Notable works
    - Legacy and influence
    - Infobox data (birth/death, nationality, era)
    """

    def __init__(self):
        super().__init__(rate_limit=settings.RATE_LIMIT_WIKIPEDIA)
        self.api_endpoint = "https://en.wikipedia.org/w/api.php"
        self.base_url = "https://en.wikipedia.org"

    def _get_domain(self) -> str:
        return "wikipedia.org"

    def _get_headers(self) -> Dict[str, str]:
        """
        Override to use Wikipedia-compliant User-Agent.

        Wikipedia API requires a descriptive User-Agent with contact info.
        See: https://www.mediawiki.org/wiki/API:Etiquette
        """
        return {
            "User-Agent": "ClassicalMusicAI/1.0 (Educational music theory training bot; https://github.com/classical-music-ai)",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
        }

    async def scrape_composer(self, composer_data: Dict[str, Any]) -> ComposerData:
        """
        Scrape composer information from Wikipedia.

        Args:
            composer_data: Dict with 'name' and optionally 'wikipedia_url'

        Returns:
            ComposerData object with scraped content
        """
        composer_name = composer_data.get("name")
        wikipedia_url = composer_data.get("wikipedia_url")

        try:
            # Get page title from URL or search for composer
            if wikipedia_url:
                page_title = self._extract_title_from_url(wikipedia_url)
            else:
                page_title = await self._search_composer(composer_name)
                if not page_title:
                    return ComposerData(
                        source="wikipedia",
                        success=False,
                        error=f"Could not find Wikipedia page for {composer_name}",
                    )

            # Fetch page content using API
            page_data = await self._fetch_page_data(page_title)

            if not page_data:
                return ComposerData(
                    source="wikipedia",
                    success=False,
                    error=f"Could not fetch Wikipedia data for {page_title}",
                )

            # Parse HTML content
            # Wikipedia API returns text as {'*': '<html>...'}
            text_data = page_data.get("text", {})
            if isinstance(text_data, dict):
                html = text_data.get("*", "")
            else:
                html = text_data
            soup = self.parse_html(html)

            # Extract components
            infobox = self._extract_infobox(soup)
            biography = self._extract_biography(soup)
            style = self._extract_style_section(soup)
            works = self._extract_works(soup)
            legacy = self._extract_legacy(soup)

            return ComposerData(
                source="wikipedia",
                success=True,
                biography=biography,
                works=works,
                musical_style=style,
                legacy=legacy,
                metadata={
                    "url": f"{self.base_url}/wiki/{page_title}",
                    "page_title": page_title,
                    "infobox": infobox,
                },
            )

        except NotFoundError as e:
            return ComposerData(
                source="wikipedia", success=False, error=f"Not found: {str(e)}"
            )
        except Exception as e:
            return ComposerData(
                source="wikipedia", success=False, error=f"Error: {str(e)}"
            )

    def _extract_title_from_url(self, url: str) -> str:
        """Extract page title from Wikipedia URL"""
        # Extract from URL like https://en.wikipedia.org/wiki/Johann_Sebastian_Bach
        match = re.search(r"/wiki/(.+)$", url)
        if match:
            return match.group(1)
        return url

    async def _search_composer(self, name: str) -> str:
        """
        Search for composer page using Wikipedia API.

        Args:
            name: Composer name

        Returns:
            Page title or empty string if not found
        """
        params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{name} composer",
            "format": "json",
            "srlimit": 1,
        }

        # Build URL
        url = f"{self.api_endpoint}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

        try:
            html = await self.fetch_with_retry(url)
            import json

            data = json.loads(html)

            search_results = data.get("query", {}).get("search", [])
            if search_results:
                return search_results[0]["title"]

        except Exception as e:
            print(f"Wikipedia search error for {name}: {e}")

        return ""

    async def _fetch_page_data(self, page_title: str) -> Dict[str, Any]:
        """
        Fetch page content using Wikipedia API.

        Args:
            page_title: Wikipedia page title

        Returns:
            Dictionary with page data
        """
        params = {
            "action": "parse",
            "page": page_title,
            "format": "json",
            "prop": "text",
        }

        url = f"{self.api_endpoint}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

        try:
            html = await self.fetch_with_retry(url)
            import json

            data = json.loads(html)
            return data.get("parse", {})

        except Exception as e:
            print(f"Error fetching Wikipedia page {page_title}: {e}")
            return {}

    def _extract_infobox(self, soup) -> Dict[str, str]:
        """Extract data from infobox"""
        infobox = {}
        infobox_table = soup.find("table", {"class": "infobox"})

        if not infobox_table:
            return infobox

        rows = infobox_table.find_all("tr")
        for row in rows:
            th = row.find("th")
            td = row.find("td")

            if th and td:
                key = self.extract_text_from_element(th)
                value = self.extract_text_from_element(td)
                infobox[key] = value

        return infobox

    def _extract_biography(self, soup) -> str:
        """
        Extract biography sections.

        Looks for:
        - Lead section (before first heading)
        - Early life / Biography sections
        - Career sections
        """
        biography_parts = []

        # Get lead section (first paragraphs before any h2)
        content_div = soup.find("div", {"class": "mw-parser-output"})
        if content_div:
            # Collect paragraphs until first h2
            for elem in content_div.children:
                if elem.name == "h2":
                    break
                if elem.name == "p":
                    text = self.extract_text_from_element(elem)
                    if text and len(text) > 50:  # Skip short paragraphs
                        biography_parts.append(text)

        # Look for specific biography sections
        bio_keywords = [
            "Early life",
            "Biography",
            "Life and career",
            "Career",
            "Youth",
        ]

        for keyword in bio_keywords:
            section = self._find_section_by_heading(soup, keyword)
            if section:
                biography_parts.append(section)
                break  # Take first match

        return "\n\n".join(biography_parts)

    def _extract_style_section(self, soup) -> str:
        """Extract musical style and characteristics"""
        style_keywords = [
            "Musical style",
            "Style",
            "Compositional style",
            "Musical characteristics",
            "Music",
        ]

        for keyword in style_keywords:
            section = self._find_section_by_heading(soup, keyword)
            if section:
                return section

        return ""

    def _extract_works(self, soup) -> List[str]:
        """Extract list of notable works"""
        works = []

        # Look for works section
        works_keywords = ["Works", "Compositions", "Notable works", "Output"]

        for keyword in works_keywords:
            section_html = self._find_section_html(soup, keyword)
            if section_html:
                # Extract lists
                lists = section_html.find_all(["ul", "ol"])
                for list_elem in lists:
                    items = list_elem.find_all("li")
                    for item in items[:50]:  # Limit to first 50 works
                        text = self.extract_text_from_element(item)
                        if text and len(text) < 200:  # Skip overly long items
                            works.append(text)

                if works:
                    break  # Take first section that has works

        return works

    def _extract_legacy(self, soup) -> str:
        """Extract legacy and influence section"""
        legacy_keywords = ["Legacy", "Influence", "Reception", "Impact"]

        for keyword in legacy_keywords:
            section = self._find_section_by_heading(soup, keyword)
            if section:
                return section

        return ""

    def _find_section_by_heading(self, soup, heading_text: str) -> str:
        """
        Find section content by heading text.

        Args:
            soup: BeautifulSoup object
            heading_text: Heading text to search for (case-insensitive)

        Returns:
            Section text or empty string
        """
        section_html = self._find_section_html(soup, heading_text)
        if section_html:
            paragraphs = section_html.find_all("p")
            texts = [
                self.extract_text_from_element(p)
                for p in paragraphs
                if len(self.extract_text_from_element(p)) > 50
            ]
            return "\n\n".join(texts)

        return ""

    def _find_section_html(self, soup, heading_text: str):
        """Find section HTML by heading text"""
        # Find all headings
        for heading_level in ["h2", "h3"]:
            headings = soup.find_all(heading_level)
            for heading in headings:
                span = heading.find("span", {"class": "mw-headline"})
                if span:
                    heading_content = self.extract_text_from_element(span)
                    if heading_text.lower() in heading_content.lower():
                        # Collect content until next heading of same or higher level
                        content = []
                        for sibling in heading.find_next_siblings():
                            if sibling.name in ["h2", "h3"] and sibling.name <= heading_level:
                                break
                            content.append(sibling)

                        # Create a temporary div with content
                        if content:
                            from bs4 import BeautifulSoup

                            temp_div = BeautifulSoup("<div></div>", "lxml").div
                            for elem in content:
                                temp_div.append(elem)
                            return temp_div

        return None
