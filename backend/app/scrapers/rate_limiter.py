"""
Token bucket rate limiter for web scraping with per-domain tracking.
"""

import time
from typing import Dict
from threading import Lock
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    """Token bucket for rate limiting"""

    capacity: float  # Maximum tokens (requests)
    rate: float  # Tokens added per second (requests per second)
    tokens: float = field(init=False)  # Current tokens available
    last_update: float = field(init=False)  # Last time tokens were added

    def __post_init__(self):
        self.tokens = self.capacity
        self.last_update = time.time()

    def _add_tokens(self):
        """Add tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

    def consume(self, tokens: float = 1.0) -> bool:
        """
        Try to consume tokens from the bucket.

        Args:
            tokens: Number of tokens to consume (default 1)

        Returns:
            True if tokens were consumed, False if not enough tokens
        """
        self._add_tokens()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def wait_time(self, tokens: float = 1.0) -> float:
        """
        Calculate time to wait until tokens are available.

        Args:
            tokens: Number of tokens needed

        Returns:
            Seconds to wait (0 if tokens available now)
        """
        self._add_tokens()

        if self.tokens >= tokens:
            return 0.0

        # Calculate how long until we have enough tokens
        tokens_needed = tokens - self.tokens
        return tokens_needed / self.rate


class RateLimiter:
    """
    Per-domain rate limiter using token bucket algorithm.

    Features:
    - Separate rate limits for different domains
    - Thread-safe
    - Configurable rates per second

    Example:
        limiter = RateLimiter()
        limiter.set_rate("wikipedia.org", 1.0)  # 1 req/sec
        limiter.wait_if_needed("wikipedia.org")  # Blocks until allowed
    """

    def __init__(self):
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()

    def set_rate(self, domain: str, rate: float, capacity: float = None):
        """
        Set rate limit for a domain.

        Args:
            domain: Domain name (e.g., "wikipedia.org")
            rate: Requests per second (e.g., 1.0 for 1 req/sec, 0.5 for 1 req/2sec)
            capacity: Maximum burst capacity (defaults to rate)
        """
        with self.lock:
            capacity = capacity or rate
            self.buckets[domain] = TokenBucket(capacity=capacity, rate=rate)

    def can_proceed(self, domain: str) -> bool:
        """
        Check if request can proceed without waiting.

        Args:
            domain: Domain name

        Returns:
            True if request can proceed now, False if need to wait
        """
        with self.lock:
            if domain not in self.buckets:
                return True  # No limit set, allow

            return self.buckets[domain].consume()

    def wait_time(self, domain: str) -> float:
        """
        Get time to wait before next request.

        Args:
            domain: Domain name

        Returns:
            Seconds to wait (0 if can proceed now)
        """
        with self.lock:
            if domain not in self.buckets:
                return 0.0

            return self.buckets[domain].wait_time()

    def wait_if_needed(self, domain: str):
        """
        Block until request is allowed for domain.

        Args:
            domain: Domain name
        """
        while True:
            wait_time = self.wait_time(domain)
            if wait_time == 0:
                # Try to consume token
                if self.can_proceed(domain):
                    break
                # If consumption failed, recalculate wait time
                continue

            # Wait the required time
            time.sleep(wait_time)

    def get_bucket_status(self, domain: str) -> dict:
        """
        Get status of rate limiter for a domain.

        Args:
            domain: Domain name

        Returns:
            Dictionary with rate limit status
        """
        with self.lock:
            if domain not in self.buckets:
                return {"rate": None, "tokens_available": None, "wait_time": 0.0}

            bucket = self.buckets[domain]
            bucket._add_tokens()  # Update tokens before reporting

            return {
                "rate": bucket.rate,
                "capacity": bucket.capacity,
                "tokens_available": bucket.tokens,
                "wait_time": bucket.wait_time(),
            }


# Global singleton
global_rate_limiter = RateLimiter()
