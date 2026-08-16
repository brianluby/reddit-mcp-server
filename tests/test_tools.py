import pytest
from unittest.mock import AsyncMock, MagicMock
from reddit_mcp.application import tools
from reddit_mcp.application.tools import DependencyContainer
import asyncio
from reddit_mcp.domain.models import (
    PaginatedPostResponse, 
    PaginatedCommentResponse, 
    RedditPost, 
    RedditComment, 
    RedditThread
)
from reddit_mcp.application.utils import truncate_text

@pytest.fixture
def sample_post():
    return RedditPost(
        id="123",
        title="Valid Test Post Title",
        subreddit="test",
        score=100,
        upvote_ratio=0.95,
        num_comments=10,
        url="https://reddit.com/r/test/comments/123",
        age_in_days=5,
        created_at_human="October 15, 2023",
        text_preview="Hello preview"
    )

@pytest.fixture(autouse=True)
def mock_reddit_client():
    mock_client = MagicMock()
    mock_client.search = AsyncMock()
    mock_client.native_reddit_search = AsyncMock()
    mock_client.get_subreddit_trends = AsyncMock()
    mock_client.get_post_thread = AsyncMock()
    DependencyContainer.override_reddit_client(mock_client)
    yield mock_client
    DependencyContainer._reddit_client = None

@pytest.mark.asyncio
async def test_search_knowledge_filters_short_titles(mock_reddit_client, sample_post):
    # Create a post with a very short title
    bad_post = sample_post.model_copy()
    bad_post.title = "Hi"
    
    mock_reddit_client.search.return_value = ([sample_post, bad_post], None)
    
    result = await tools.search_knowledge("query")
    
    # Should only return the valid_post
    assert len(result.data) == 1
    assert result.data[0].title == "Valid Test Post Title"

@pytest.mark.asyncio
async def test_extract_public_opinion_logic(mock_reddit_client, sample_post):
    # One high quality, one low quality (short)
    good_comment = RedditComment(
        id="c1", author="user1", score=10, body="This is a long enough and high quality comment for testing.",
        comment_url="url1", created_at_human="date"
    )
    bad_comment = RedditComment(
        id="c2", author="bot", score=-5, body="short",
        comment_url="url2", created_at_human="date"
    )
    
    mock_thread = RedditThread(post=sample_post, comments=[good_comment, bad_comment])
    mock_reddit_client.get_post_thread.return_value = mock_thread
    
    result = await tools.extract_public_opinion("http://url")
    
    # Should filter out the bad comment at application layer
    assert len(result.data) == 1
    assert result.data[0].id == "c1"
    assert "instruction_note" in result.meta_context.model_dump()

@pytest.mark.asyncio
async def test_explore_reddit_discussions_pagination(mock_reddit_client, sample_post):
    # Simulate reddit client returning a next_page_token
    mock_reddit_client.native_reddit_search.return_value = ([sample_post], "after_token_123")
    
    result = await tools.explore_reddit_discussions("keyword")
    
    assert len(result.data) == 1
    assert result.next_page_token == "after_token_123"

@pytest.mark.asyncio
async def test_search_knowledge_empty_results(mock_reddit_client):
    # Simulate an empty search result
    mock_reddit_client.search.return_value = ([], None)
    
    result = await tools.search_knowledge("nonexistent_query")
    
    assert len(result.data) == 0
    assert result.next_page_token is None

@pytest.mark.asyncio
async def test_tool_llm_timeout(monkeypatch):
    # We test the timeout by mocking asyncio.wait_for to raise a TimeoutError
    async def mock_wait_for(aw, timeout=None, **kwargs):
        aw.close()  # Close the unawaited coroutine to prevent RuntimeWarning
        raise asyncio.TimeoutError()
        
    monkeypatch.setattr(asyncio, "wait_for", mock_wait_for)
    
    result = await tools.search_knowledge("query")
    
    # It should not crash, but return a fallback dict
    assert isinstance(result, dict)
    assert result["status"] == "partial_timeout"
    assert "Request paused" in result["message"]
    assert len(result["data"]) == 0

def test_truncate_text_util():
    # Phase 4 Utils test
    long_text = "A" * 3000
    truncated = truncate_text(long_text, 2000)
    
    assert len(truncated) == 2000 + len("... (truncated)")
    assert truncated.endswith("... (truncated)")
    
    # Test empty
    assert truncate_text(None) == ""
    assert truncate_text("") == ""