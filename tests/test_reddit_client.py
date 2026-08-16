import pytest
from unittest.mock import AsyncMock, MagicMock
from reddit_mcp.infrastructure.reddit_client import RedditClient, RedditClientError
from reddit_mcp.domain.models import RedditPost, RedditThread, RedditComment

@pytest.fixture
def mock_http_client():
    client = MagicMock()
    client.get = AsyncMock()
    return client

@pytest.fixture
def mock_search_provider():
    provider = MagicMock()
    provider.search = AsyncMock()
    return provider

@pytest.fixture
def reddit_client(mock_http_client, mock_search_provider):
    return RedditClient(http_client=mock_http_client, search_provider=mock_search_provider)

@pytest.mark.asyncio
async def test_get_subreddit_trends_success(reddit_client, mock_http_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "after": "t3_abc",
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "123",
                        "title": "Test Post",
                        "subreddit": "test",
                        "score": 100,
                        "upvote_ratio": 0.95,
                        "num_comments": 10,
                        "permalink": "/r/test/comments/123/",
                        "created_utc": 1700000000.0,
                        "selftext": "Hello world text"
                    }
                }
            ]
        }
    }
    mock_http_client.get.return_value = mock_response

    posts, next_token = await reddit_client.get_subreddit_trends("test", "hot")
    
    assert len(posts) == 1
    post = posts[0]
    assert post.age_in_days >= 0
    assert "created_at_human" in post.model_dump()
    assert post.text_preview == "Hello world text"

@pytest.mark.asyncio
async def test_get_post_thread_success(reddit_client, mock_http_client):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"data": {"children": [{"kind": "t3", "data": {
            "id": "123", "title": "Post", "subreddit": "test", "score": 10, 
            "upvote_ratio": 1.0, "num_comments": 1, "permalink": "/r/test/comments/123/", 
            "created_utc": 1700000000.0, "selftext": "..."
        }}]}},
        {"data": {"children": [{"kind": "t1", "data": {
            "id": "c1", "author": "user1", "score": 5, "body": "Comment body", "created_utc": 1700000050.0
        }}]}}
    ]
    mock_http_client.get.return_value = mock_response
    
    thread = await reddit_client.get_post_thread("http://reddit.com/r/test/comments/123")
    
    assert isinstance(thread, RedditThread)
    assert thread.comments[0].created_at_human is not None

@pytest.mark.asyncio
async def test_get_post_thread_malformed_json(reddit_client, mock_http_client):
    # Simulate reddit returning an unexpected structure (e.g., dict instead of list)
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": 404}
    mock_http_client.get.return_value = mock_response
    
    with pytest.raises(RedditClientError, match="Unexpected response format"):
        await reddit_client.get_post_thread("http://reddit.com/r/test/comments/123")