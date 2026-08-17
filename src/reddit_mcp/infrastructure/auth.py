import asyncio
import base64
import logging
import time

import httpx

from reddit_mcp.infrastructure.settings import get_settings

logger = logging.getLogger(__name__)


class RedditAuthError(Exception):
    """Exception raised for errors during Reddit authentication."""


class RedditAuthManager:
    """
    Manages OAuth 2.0 Access Tokens for Reddit via the client_credentials flow.
    Automatically fetches and caches the token, refreshing it before it expires.
    """

    def __init__(self, user_agent: str):
        settings = get_settings()
        self.client_id = settings.reddit_client_id
        self.client_secret = settings.reddit_client_secret
        self.user_agent = user_agent

        self._token: str | None = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    @property
    def has_credentials(self) -> bool:
        """Check if OAuth credentials are provided."""
        return bool(self.client_id and self.client_secret)

    async def get_token(self) -> str | None:
        """
        Get a valid access token, refreshing it if necessary. Returns None if unauthenticated.
        """
        if not self.has_credentials:
            return None

        async with self._lock:
            # Refresh if token is missing or expires within the next 30 seconds
            if not self._token or time.time() >= (self._expires_at - 30):
                await self._refresh_token()

            return self._token

    def invalidate(self) -> None:
        """Clear the cached token, forcing a refresh on the next get_token call."""
        self._token = None
        self._expires_at = 0.0

    async def _refresh_token(self) -> None:
        """
        Fetch a new token from Reddit API using client credentials.
        """
        logger.info("Fetching new Reddit OAuth access token...")

        auth_string = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "User-Agent": self.user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"grant_type": "client_credentials"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://www.reddit.com/api/v1/access_token",
                    headers=headers,
                    data=data,
                    timeout=10.0,
                )
                response.raise_for_status()

                token_data = response.json()
                self._token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)

                if not self._token:
                    raise RedditAuthError(
                        "Token response did not contain an access_token"
                    )

                self._expires_at = time.time() + expires_in
                logger.info("Successfully acquired new Reddit OAuth access token.")

            except httpx.HTTPStatusError as e:
                logger.error(
                    f"Failed to fetch token. HTTP Status: {e.response.status_code}. Body: {e.response.text}"
                )
                raise RedditAuthError(
                    f"HTTP {e.response.status_code} during token refresh"
                ) from e
            except httpx.RequestError as e:
                logger.error(f"Network error during token refresh: {e}")
                raise RedditAuthError(f"Network error: {e}") from e
            except Exception as e:
                logger.error(f"Unexpected error during token refresh: {e}")
                raise RedditAuthError(f"Unexpected error: {e}") from e
