import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from reddit_mcp.application import tools
from reddit_mcp.application.tools import DependencyContainer
from reddit_mcp.application.utils import truncate_text
from reddit_mcp.domain.models import (
    RedditComment,
    RedditPost,
    RedditThread,
)
from reddit_mcp.infrastructure.arctic_shift_client import ArcticShiftError
from reddit_mcp.infrastructure.reddit_client import (
    RedditAuthRequiredError,
    RedditClientError,
)
from reddit_mcp.infrastructure.search.base import SearchProviderError
from reddit_mcp.infrastructure.search.providers.duckduckgo import RedditSearchResult


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
        text_preview="Hello preview",
    )


@pytest.fixture(autouse=True)
def mock_reddit_client():
    mock_client = MagicMock()
    mock_client.search = AsyncMock()
    mock_client.native_reddit_search = AsyncMock()
    mock_client.get_subreddit_trends = AsyncMock()
    mock_client.get_post_thread = AsyncMock()

    mock_arctic = MagicMock()
    mock_arctic.get_posts_by_ids = AsyncMock()
    mock_arctic.get_post_thread = AsyncMock()

    mock_search = MagicMock()
    mock_search.search = AsyncMock()

    DependencyContainer._reddit_client = mock_client
    DependencyContainer._arctic_shift_client = mock_arctic
    DependencyContainer._search_provider = mock_search

    yield mock_client

    DependencyContainer._reddit_client = None
    DependencyContainer._arctic_shift_client = None
    DependencyContainer._search_provider = None


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
        id="c1",
        author="user1",
        score=10,
        body="This is a long enough and high quality comment for testing.",
        comment_url="url1",
        created_at_human="date",
    )
    bad_comment = RedditComment(
        id="c2",
        author="bot",
        score=-5,
        body="short",
        comment_url="url2",
        created_at_human="date",
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
    mock_reddit_client.native_reddit_search.return_value = (
        [sample_post],
        "after_token_123",
    )

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
        raise TimeoutError()

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


@pytest.mark.asyncio
async def test_fallback_search_knowledge(sample_post):
    # Simulate missing OAuth credentials (subclass of RedditClientError)
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.search.side_effect = RedditAuthRequiredError()

    # Mock DuckDuckGo returning a URL
    mock_search = DependencyContainer.get_search_provider()
    mock_search.search.return_value = [
        RedditSearchResult(url="http://reddit.com/comments/123", title="t", snippet="s")
    ]

    # Mock Arctic Shift returning the parsed post
    mock_arctic = DependencyContainer.get_arctic_shift_client()
    mock_arctic.get_posts_by_ids.return_value = [sample_post]

    result = await tools.search_knowledge("query")
    assert len(result.data) == 1
    assert result.data[0].id == "123"
    assert result.status == "success"
    assert result.data_source == "arctic_shift"
    assert "Arctic Shift" in result.message
    assert "lag" in result.message


@pytest.mark.asyncio
async def test_fallback_search_knowledge_on_client_error(sample_post):
    # Simulate failed credentials (generic RedditClientError, e.g. HTTP 401)
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.search.side_effect = RedditClientError("HTTP 401")

    mock_search = DependencyContainer.get_search_provider()
    mock_search.search.return_value = [
        RedditSearchResult(url="http://reddit.com/comments/123", title="t", snippet="s")
    ]

    mock_arctic = DependencyContainer.get_arctic_shift_client()
    mock_arctic.get_posts_by_ids.return_value = [sample_post]

    result = await tools.search_knowledge("query")
    assert len(result.data) == 1
    assert result.data[0].id == "123"
    assert result.status == "success"
    assert result.data_source == "arctic_shift"
    assert "Arctic Shift" in result.message


@pytest.mark.asyncio
async def test_fallback_explore_on_client_error(sample_post):
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.native_reddit_search.side_effect = RedditClientError("HTTP 401")

    mock_search = DependencyContainer.get_search_provider()
    mock_search.search.return_value = [
        RedditSearchResult(url="http://reddit.com/comments/123", title="t", snippet="s")
    ]

    mock_arctic = DependencyContainer.get_arctic_shift_client()
    mock_arctic.get_posts_by_ids.return_value = [sample_post]

    result = await tools.explore_reddit_discussions("keyword")
    assert len(result.data) == 1
    assert result.data[0].id == "123"
    assert result.status == "success"
    assert result.data_source == "arctic_shift"
    assert "Arctic Shift" in result.message
    assert result.next_page_token is None


@pytest.mark.asyncio
async def test_fallback_extract_public_opinion_on_client_error(sample_post):
    good_comment = RedditComment(
        id="c1",
        author="user1",
        score=10,
        body="This is a long enough and high quality comment for testing.",
        comment_url="url1",
        created_at_human="date",
    )

    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.get_post_thread.side_effect = RedditClientError("HTTP 401")

    mock_arctic = DependencyContainer.get_arctic_shift_client()
    mock_arctic.get_post_thread.return_value = RedditThread(
        post=sample_post, comments=[good_comment]
    )

    result = await tools.extract_public_opinion("http://url")
    assert len(result.data) == 1
    assert result.data[0].id == "c1"
    assert result.status == "success"
    assert result.data_source == "arctic_shift"
    assert "Arctic Shift" in result.message


@pytest.mark.asyncio
async def test_degraded_search_knowledge_when_ddg_fails():
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.search.side_effect = RedditClientError("HTTP 401")

    mock_search = DependencyContainer.get_search_provider()
    mock_search.search.side_effect = SearchProviderError("DDG is down")

    result = await tools.search_knowledge("query")
    assert result.status == "degraded"
    assert len(result.data) == 0
    assert result.message
    assert "unavailable" in result.message


@pytest.mark.asyncio
async def test_degraded_search_knowledge_when_arctic_fails():
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.search.side_effect = RedditClientError("rate limited")

    mock_search = DependencyContainer.get_search_provider()
    mock_search.search.return_value = [
        RedditSearchResult(url="http://reddit.com/comments/123", title="t", snippet="s")
    ]

    mock_arctic = DependencyContainer.get_arctic_shift_client()
    mock_arctic.get_posts_by_ids.side_effect = ArcticShiftError("archive down")

    result = await tools.search_knowledge("query")
    assert result.status == "degraded"
    assert len(result.data) == 0
    assert result.message
    assert "unavailable" in result.message


@pytest.mark.asyncio
async def test_degraded_extract_public_opinion_when_arctic_fails():
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.get_post_thread.side_effect = RedditClientError("network error")

    mock_arctic = DependencyContainer.get_arctic_shift_client()
    mock_arctic.get_post_thread.side_effect = ArcticShiftError("archive down")

    result = await tools.extract_public_opinion("http://url")
    assert result.status == "degraded"
    assert len(result.data) == 0
    assert result.message
    assert "unavailable" in result.message


@pytest.mark.asyncio
async def test_extract_public_opinion_young_thread_keeps_low_score_comments(
    mock_reddit_client, sample_post
):
    young_post = sample_post.model_copy(update={"age_in_days": 0})
    fresh_comment = RedditComment(
        id="c1",
        author="user1",
        score=1,
        body="This is a long enough comment that just has not been voted on yet.",
        comment_url="url1",
        created_at_human="date",
    )

    mock_reddit_client.get_post_thread.return_value = RedditThread(
        post=young_post, comments=[fresh_comment]
    )

    result = await tools.extract_public_opinion("http://url")

    assert len(result.data) == 1
    assert result.data[0].id == "c1"


@pytest.mark.asyncio
async def test_extract_public_opinion_old_thread_filters_low_score_comments(
    mock_reddit_client, sample_post
):
    old_post = sample_post.model_copy(update={"age_in_days": 5})
    stale_comment = RedditComment(
        id="c1",
        author="user1",
        score=1,
        body="This is a long enough comment that never earned any upvotes.",
        comment_url="url1",
        created_at_human="date",
    )

    mock_reddit_client.get_post_thread.return_value = RedditThread(
        post=old_post, comments=[stale_comment]
    )

    result = await tools.extract_public_opinion("http://url")

    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_fallback_analyze_niche_trends():
    # Simulate missing OAuth credentials (subclass of RedditClientError)
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.get_subreddit_trends.side_effect = RedditAuthRequiredError()

    result = await tools.analyze_niche_trends("python")

    # Trending tool should fail gracefully with a warning
    assert result.status == "warning"
    assert "Trending data is unavailable" in result.message
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_fallback_analyze_niche_trends_on_client_error():
    mock_reddit = DependencyContainer.get_reddit_client()
    mock_reddit.get_subreddit_trends.side_effect = RedditClientError("HTTP 401")

    result = await tools.analyze_niche_trends("python")

    assert result.status == "warning"
    assert "Trending data is unavailable" in result.message
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_tool_schema_bounds():
    from reddit_mcp.interface.server import create_server

    mcp = create_server()

    search_tool = await mcp.get_tool("search_knowledge")
    limit_schema = search_tool.parameters["properties"]["limit"]
    assert limit_schema["minimum"] == 1
    assert limit_schema["maximum"] == 100

    opinion_tool = await mcp.get_tool("extract_public_opinion")
    max_comments_schema = opinion_tool.parameters["properties"]["max_comments"]
    assert max_comments_schema["minimum"] == 1
    assert max_comments_schema["maximum"] == 100
