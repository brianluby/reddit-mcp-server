import pytest
import os
from unittest.mock import AsyncMock, patch
import httpx
from pydantic import ValidationError
from reddit_mcp.infrastructure.auth import RedditAuthManager, RedditAuthError
from reddit_mcp.infrastructure.settings import get_settings

@pytest.fixture
def auth_env(monkeypatch):
    monkeypatch.setenv("REDDIT_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "dummy_secret")
    get_settings.cache_clear()

@pytest.mark.asyncio
async def test_auth_manager_missing_env():
    # Ensure env is clear to test the missing credentials error
    with patch.dict(os.environ, clear=True):
        get_settings.cache_clear()
        # Force pydantic-settings to believe the .env file does not exist
        with patch("pathlib.Path.is_file", return_value=False):
            with pytest.raises(ValidationError, match="reddit_client_id"):
                RedditAuthManager(user_agent="test")

from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_auth_manager_success(auth_env):
    manager = RedditAuthManager(user_agent="test")
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "mock_token", "expires_in": 3600}
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        token = await manager.get_token()
        
    assert token == "mock_token"

@pytest.mark.asyncio
async def test_auth_manager_http_error(auth_env):
    manager = RedditAuthManager(user_agent="test")
    
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Unauthorized", request=MagicMock(), response=mock_response
    )
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        with pytest.raises(RedditAuthError, match="HTTP 401"):
            await manager.get_token()