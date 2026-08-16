from unittest.mock import AsyncMock, MagicMock

import pytest

from reddit_mcp.domain.models import RedditThread
from reddit_mcp.infrastructure.arctic_shift_client import (
    ArcticShiftClient,
    ArcticShiftError,
)


@pytest.fixture
def mock_http_client():
    client = MagicMock()
    client.get = AsyncMock()
    return client


@pytest.fixture
def arctic_client(mock_http_client):
    return ArcticShiftClient(http_client=mock_http_client)


@pytest.mark.asyncio
async def test_get_posts_by_ids_success(arctic_client, mock_http_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "abc",
                "title": "Arctic Post",
                "subreddit": "test",
                "score": 50,
                "upvote_ratio": 0.9,
                "num_comments": 5,
                "permalink": "/r/test/comments/abc/",
                "created_utc": 1700000000.0,
                "selftext": "Archive body",
            }
        ]
    }
    mock_http_client.get.return_value = mock_response

    posts = await arctic_client.get_posts_by_ids(["t3_abc"])

    assert len(posts) == 1
    assert posts[0].id == "abc"
    assert posts[0].title == "Arctic Post"


@pytest.mark.asyncio
async def test_get_post_thread_success(arctic_client, mock_http_client):
    # Mocking two HTTP calls: first for post, second for comments
    post_response = MagicMock()
    post_response.json.return_value = {
        "data": [
            {
                "id": "abc",
                "title": "Post",
                "subreddit": "test",
                "created_utc": 1700000000.0,
            }
        ]
    }

    comment_response = MagicMock()
    comment_response.json.return_value = {
        "data": [
            {
                "id": "c1",
                "author": "user",
                "score": 10,
                "body": "Comment body",
                "created_utc": 1700000050.0,
            }
        ]
    }

    mock_http_client.get.side_effect = [post_response, comment_response]

    thread = await arctic_client.get_post_thread("abc")

    assert isinstance(thread, RedditThread)
    assert thread.post.id == "abc"
    assert len(thread.comments) == 1
    assert thread.comments[0].id == "c1"


@pytest.mark.asyncio
async def test_get_subreddit_trends_raises_error(arctic_client):
    # Ensure it refuses to fetch trending data
    with pytest.raises(ArcticShiftError, match="unavailable without OAuth"):
        await arctic_client.get_subreddit_trends("python")
