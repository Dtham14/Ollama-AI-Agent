"""
Base scraper class with rate limiting, retries, and error handling.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .rate_limiter import global_rate_limiter
from ..config import settings


class ScraperError(Exception):
    """Base exception for scraper errors"""

    pass


class RateLimitError(ScraperError):
    """Raised when rate limit is exceeded"""

    pass


class NotFoundError(ScraperError):
    """Raised when resource not found (404)"""

    pass


class BaseScraper(ABC):
    """
    Abstract base class for all web scrapers.

    Features:
    - Rate limiting with token bucket algorithm
    - Exponential backoff retry logic
    - User-agent rotation
    - robots.txt compliance checking (optional)
    - Error handling and logging
    """

    def __init__(
        self,
        rate_limit: float = 1.0,
        max_retries: int = None,
        timeout: int = None,
        verify_ssl: bool = True,
    ):
        """
        Initialize base scraper.

        Args:
            rate_limit: Requests per second (default: 1.0)
            max_retries: Maximum retry attempts (default: from settings)
            timeout: Request timeout in seconds (default: from settings)
            verify_ssl: Verify SSL certificates (default: True)
        """
        self.rate_limit = rate_limit
        self.max_retries = max_retries or settings.MAX_RETRIES
        self.timeout = timeout or settings.REQUEST_TIMEOUT
        self.verify_ssl = verify_ssl

        # User agent rotation
        self.ua = UserAgent()

        # Setup rate limiter for this scraper's domain
        self.domain = self._get_domain()
        if self.domain:
            global_rate_limiter.set_rate(self.domain, rate_limit)

    @abstractmethod
    def _get_domain(self) -> str:
        """
        Get the domain this scraper targets.
        Must be implemented by subclasses.

        Returns:
            Domain name (e.g., "wikipedia.org")
        """
        pass

    @abstractmethod
    async def scrape_composer(self, composer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape composer information.
        Must be implemented by subclasses.

        Args:
            composer_data: Dictionary with composer info (name, urls, etc.)

        Returns:
            Dictionary with scraped content
        """
        pass

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate headers with rotated user agent.

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    async def fetch_with_retry(self, url: str) -> str:
        """
        Fetch URL with rate limiting and retry logic.

        Args:
            url: URL to fetch

        Returns:
            HTML content as string

        Raises:
            NotFoundError: If resource not found (404)
            ScraperError: For other errors after retries exhausted
        """
        # Wait for rate limit
        global_rate_limiter.wait_if_needed(self.domain)

        retry_count = 0
        last_error = None

        while retry_count <= self.max_retries:
            try:
                async with httpx.AsyncClient(
                    timeout=self.timeout, verify=self.verify_ssl
                ) as client:
                    response = await client.get(url, headers=self._get_headers())

                    # Handle specific status codes
                    if response.status_code == 404:
                        raise NotFoundError(f"Resource not found: {url}")

                    if response.status_code == 429:
                        # Rate limit exceeded - wait longer
                        wait_time = self._get_backoff_time(retry_count) * 2
                        print(
                            f"Rate limit hit for {url}, waiting {wait_time:.1f}s..."
                        )
                        await asyncio.sleep(wait_time)
                        retry_count += 1
                        continue

                    response.raise_for_status()
                    return response.text

            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code == 404:
                    raise NotFoundError(f"Resource not found: {url}")

                print(
                    f"HTTP error {e.response.status_code} for {url}, retry {retry_count}/{self.max_retries}"
                )

            except httpx.RequestError as e:
                last_error = e
                print(f"Network error for {url}: {e}, retry {retry_count}/{self.max_retries}")

            except Exception as e:
                last_error = e
                print(
                    f"Unexpected error for {url}: {e}, retry {retry_count}/{self.max_retries}"
                )

            # Exponential backoff
            if retry_count < self.max_retries:
                wait_time = self._get_backoff_time(retry_count)
                print(f"Waiting {wait_time:.1f}s before retry...")
                await asyncio.sleep(wait_time)

            retry_count += 1

        # All retries exhausted
        raise ScraperError(
            f"Failed to fetch {url} after {self.max_retries} retries: {last_error}"
        )

    def _get_backoff_time(self, retry_count: int) -> float:
        """
        Calculate exponential backoff time.

        Args:
            retry_count: Current retry attempt number

        Returns:
            Seconds to wait
        """
        # Exponential backoff: 1s, 2s, 4s, 8s, 16s
        return min(2**retry_count, 16)

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup.

        Args:
            html: HTML string

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "lxml")

    def check_robots_txt(self, url: str) -> bool:
        """
        Check if URL is allowed by robots.txt.
        (Simplified implementation - basic check)

        Args:
            url: URL to check

        Returns:
            True if allowed (currently always True - can be enhanced)
        """
        # TODO: Implement proper robots.txt checking
        # For now, we rely on respectful rate limiting
        return True

    def clean_text(self, text: str) -> str:
        """
        Clean scraped text (remove extra whitespace, etc.)

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace
        lines = [line.strip() for line in text.split("\n")]
        lines = [line for line in lines if line]
        return "\n".join(lines)

    def extract_text_from_element(self, element) -> str:
        """
        Extract and clean text from BeautifulSoup element.

        Args:
            element: BeautifulSoup element

        Returns:
            Cleaned text
        """
        if not element:
            return ""

        text = element.get_text(separator="\n", strip=True)
        return self.clean_text(text)


class ComposerData:
    """Data class for scraped composer information"""

    def __init__(
        self,
        source: str,
        success: bool = True,
        biography: str = "",
        works: list = None,
        musical_style: str = "",
        legacy: str = "",
        metadata: dict = None,
        error: str = None,
    ):
        self.source = source
        self.success = success
        self.biography = biography
        self.works = works or []
        self.musical_style = musical_style
        self.legacy = legacy
        self.metadata = metadata or {}
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source": self.source,
            "success": self.success,
            "biography": self.biography,
            "works": self.works,
            "musical_style": self.musical_style,
            "legacy": self.legacy,
            "metadata": self.metadata,
            "error": self.error,
        }
