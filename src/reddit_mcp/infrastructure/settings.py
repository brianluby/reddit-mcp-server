from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    """
    Centralized configuration for the Reddit MCP Server.
    Validates environment variables at startup (Fail-Fast).
    """
    reddit_client_id: str = Field(..., description="Reddit App Client ID")
    reddit_client_secret: str = Field(..., description="Reddit App Client Secret")
    reddit_user_agent: str = Field(
        default="reddit-mcp-server/0.1.0 (by /u/reddit-mcp-server-dev)", 
        description="User-Agent string for HTTP requests"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> AppConfig:
    """
    Returns a cached instance of the application settings.
    Will raise a ValidationError immediately if required vars are missing.
    """
    return AppConfig()