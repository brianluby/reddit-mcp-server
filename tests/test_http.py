import pytest
from unittest.mock import AsyncMock, MagicMock
from reddit_mcp.infrastructure.http import ResilientHTTPClient, RedditRateLimitError
from reddit_mcp.infrastructure.auth import RedditAuthManager

@pytest.fixture
def mock_auth_manager():
    manager = MagicMock(spec=RedditAuthManager)
    manager.get_token = AsyncMock(return_value="mock_token")
    return manager

@pytest.mark.asyncio
async def test_http_client_success(mock_auth_manager):
    client = ResilientHTTPClient(auth_manager=mock_auth_manager, user_agent="test")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    
    client.client.get = AsyncMock(return_value=mock_response)
    
    response = await client.get("http://test.com")
    assert response.status_code == 200
    assert client.client.get.call_count == 1
    await client.close()

@pytest.mark.asyncio
async def test_http_client_429_retry_success(mock_auth_manager, monkeypatch):
    # Skip actual asyncio.sleep during tests to make them fast
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    
    client = ResilientHTTPClient(auth_manager=mock_auth_manager, user_agent="test")
    
    fail_response = MagicMock()
    fail_response.status_code = 429
    fail_response.headers = {"Retry-After": "1"}
    
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.raise_for_status = MagicMock()
    
    # First call returns 429, second call returns 200
    client.client.get = AsyncMock(side_effect=[fail_response, success_response])
    
    response = await client.get("http://test.com", max_retries=3)
    assert response.status_code == 200
    assert client.client.get.call_count == 2
    await client.close()

@pytest.mark.asyncio
async def test_http_client_429_max_retries(mock_auth_manager, monkeypatch):
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    client = ResilientHTTPClient(auth_manager=mock_auth_manager, user_agent="test")
    
    fail_response = MagicMock()
    fail_response.status_code = 429
    fail_response.headers = {"Retry-After": "1"}
    
    # Always return 429
    client.client.get = AsyncMock(return_value=fail_response)
    
    with pytest.raises(RedditRateLimitError, match="Max retries exceeded"):
        await client.get("http://test.com", max_retries=2)
        
    assert client.client.get.call_count == 2
    await client.close()