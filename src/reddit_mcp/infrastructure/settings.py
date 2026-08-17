import uuid
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_user_agent() -> str:
    return (
        f"reddit-mcp-server/0.2.0 "
        f"(by /u/reddit-mcp-server-dev; install:{uuid.uuid4().hex[:8]})"
    )


class AppConfig(BaseSettings):
    """
    Centralized configuration for the Reddit MCP Server.
    Validates environment variables at startup (Fail-Fast).
    """

    reddit_client_id: str | None = Field(
        default=None, description="Reddit App Client ID"
    )
    reddit_client_secret: str | None = Field(
        default=None, description="Reddit App Client Secret"
    )
    reddit_user_agent: str = Field(
        default_factory=_default_user_agent,
        description="User-Agent string for HTTP requests",
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> AppConfig:
    """
    Returns a cached instance of the application settings.
    Will raise a ValidationError immediately if required vars are missing.
    """
    return AppConfig()
