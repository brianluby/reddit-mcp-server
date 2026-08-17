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
    """

    def __init__(self, auth_manager: RedditAuthManager, user_agent: str):
        self.auth_manager = auth_manager
        self.user_agent = user_agent
        self.client = httpx.AsyncClient(timeout=15.0)

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def get(
        self, url: str, params: dict[str, Any] | None = None, max_retries: int = 3
    ) -> httpx.Response:
        """
        Perform a GET request with automatic token injection and rate limit retries.
        """
        auth_retry_done = False
        for attempt in range(max_retries):
            headers = {"User-Agent": self.user_agent}
            token = await self.auth_manager.get_token()

            if token:
                headers["Authorization"] = f"Bearer {token}"

            try:
                response = await self.client.get(url, params=params, headers=headers)

                # Check for rate limit (429) or Server Errors (500, 502, 503, 504)
                if response.status_code == 429 or response.status_code >= 500:
                    retry_after = response.headers.get("Retry-After")

                    if (
                        response.status_code == 429
                        and retry_after
                        and retry_after.isdigit()
                    ):
                        wait_seconds = int(retry_after)
                    else:
                        # Exponential backoff for 5xx or missing Retry-After
                        wait_seconds = 2**attempt

                    logger.warning(
                        f"HTTP {response.status_code} on {url}. Retrying in {wait_seconds} seconds. "
                        f"(Attempt {attempt + 1}/{max_retries})"
                    )

                    if attempt < max_retries - 1:
                        await asyncio.sleep(wait_seconds)
                        continue
                    else:
                        if response.status_code == 429:
                            raise RedditRateLimitError(
                                "Max retries exceeded due to rate limiting."
                            )
                        else:
                            response.raise_for_status()

                # Stale token: invalidate and retry once with a fresh token
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
                    continue
                raise

        raise RuntimeError("Failed to complete request (should not reach here)")
