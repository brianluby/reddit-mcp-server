import os
import uuid
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_INSTALL_ID_LENGTH = 8
_HEX_DIGITS = set("0123456789abcdef")


@lru_cache(maxsize=1)
def _process_install_id() -> str:
    """One ID per process, used both for persisting and as the in-memory
    fallback when the state directory is unreadable or unwritable (e.g.
    locked-down containers); never regenerated per instance."""
    return uuid.uuid4().hex[:_INSTALL_ID_LENGTH]


def _install_id_path() -> Path:
    base = os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state"
    return Path(base) / "reddit-mcp-server" / "install-id"


def _is_valid_install_id(value: str) -> bool:
    return len(value) == _INSTALL_ID_LENGTH and set(value) <= _HEX_DIGITS


@lru_cache(maxsize=1)
def _install_id() -> str:
    """Per-install identifier persisted in the user's state directory so the
    default User-Agent stays stable across process restarts."""
    try:
        path = _install_id_path()
    except (OSError, RuntimeError):
        # No determinable home directory (e.g. minimal containers).
        return _process_install_id()
    try:
        existing = path.read_text(encoding="utf-8").strip()
        if _is_valid_install_id(existing):
            return existing
    except OSError:
        pass
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_process_install_id(), encoding="utf-8")
    except OSError:
        pass
    return _process_install_id()


def _default_user_agent() -> str:
    return (
        f"reddit-mcp-server/0.2.0 "
        f"(by /u/reddit-mcp-server-dev; install:{_install_id()})"
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
