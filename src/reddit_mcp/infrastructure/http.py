import asyncio
import logging
from typing import Any

import httpx

from reddit_mcp.infrastructure.auth import RedditAuthManager

logger = logging.getLogger(__name__)


class RedditRateLimitError(Exception):
    """Exception raised when the maximum number of rate limit retries is exceeded."""


class ResilientHTTPClient:
    """
    HTTP client wrapper using httpx with built-in resilience.
    Automatically injects Reddit OAuth tokens, enforces User-Agent,
    and handles rate limits (429) using exponential backoff.

    Bearer tokens are only attached to Reddit API hosts, so shared use with
    third-party clients (e.g. Arctic Shift) never leaks credentials.
    """

    MAX_RETRY_AFTER_SECONDS = 5
    TOTAL_BUDGET_SECONDS = 14.0

    def __init__(self, auth_manager: RedditAuthManager, user_agent: str):
        self.auth_manager = auth_manager
        self.user_agent = user_agent
        # httpx timeouts are per network phase, not per request; the aggregate
        # TOTAL_BUDGET_SECONDS deadline enforced in get() bounds the whole
        # attempt/retry flow (token fetch is a separate call with its own 10s).
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(5.0))

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()

    @staticmethod
    def _is_reddit_url(url: str) -> bool:
        host = httpx.URL(url).host or ""
        return host == "reddit.com" or host.endswith(".reddit.com")

    async def get(
        self, url: str, params: dict[str, Any] | None = None, max_retries: int = 2
    ) -> httpx.Response:
        """
        Perform a GET request with automatic token injection and rate limit retries.
        The one-shot 401 token-refresh retry does not consume the retry budget.
        The whole flow is bounded by TOTAL_BUDGET_SECONDS; expiry raises
        TimeoutError (callers wrap it into their error handling).
        """
        is_reddit = self._is_reddit_url(url)
        attempt = 0
        auth_retry_done = False
        async with asyncio.timeout(self.TOTAL_BUDGET_SECONDS):
            while True:
                headers = {"User-Agent": self.user_agent}
                token = await self.auth_manager.get_token() if is_reddit else None

                if token:
                    headers["Authorization"] = f"Bearer {token}"

                try:
                    response = await self.client.get(
                        url, params=params, headers=headers
                    )

                    # Check for rate limit (429) or Server Errors (500, 502, 503, 504)
                    if response.status_code == 429 or response.status_code >= 500:
                        retry_after = response.headers.get("Retry-After")

                        if (
                            response.status_code == 429
                            and retry_after
                            and retry_after.isdigit()
                        ):
                            requested = int(retry_after)
                            wait_seconds = min(requested, self.MAX_RETRY_AFTER_SECONDS)
                            if requested > self.MAX_RETRY_AFTER_SECONDS:
                                logger.warning(
                                    f"Retry-After {requested}s exceeds cap of "
                                    f"{self.MAX_RETRY_AFTER_SECONDS}s; waiting "
                                    f"{wait_seconds}s instead."
                                )
                        else:
                            # Exponential backoff for 5xx or missing Retry-After
                            wait_seconds = 2**attempt

                        logger.warning(
                            f"HTTP {response.status_code} on {url}. Retrying in {wait_seconds} seconds. "
                            f"(Attempt {attempt + 1}/{max_retries})"
                        )

                        if attempt < max_retries - 1:
                            await asyncio.sleep(wait_seconds)
                            attempt += 1
                            continue
                        else:
                            if response.status_code == 429:
                                raise RedditRateLimitError(
                                    "Max retries exceeded due to rate limiting."
                                )
                            else:
                                response.raise_for_status()

                    # Stale token: invalidate and retry once with a fresh token.
                    # This retry is independent of the general retry budget.
                    if response.status_code == 401 and token and not auth_retry_done:
                        auth_retry_done = True
                        logger.warning(
                            f"HTTP 401 on {url}. Invalidating token and retrying."
                        )
                        self.auth_manager.invalidate()
                        continue

                    # Raise for other HTTP errors (4xx)
                    response.raise_for_status()
                    return response

                except httpx.HTTPStatusError:
                    # Handled retries above, raise if we get here
                    raise
                except httpx.RequestError as e:
                    logger.error(f"Network error on {url}: {e}")
                    if attempt < max_retries - 1:
                        wait_seconds = 2**attempt
                        await asyncio.sleep(wait_seconds)
                        attempt += 1
                        continue
                    raise
