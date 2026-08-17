import pytest

from reddit_mcp.infrastructure.search.base import SearchProviderError
from reddit_mcp.infrastructure.search.providers.duckduckgo import (
    DuckDuckGoSearchProvider,
    RedditSearchResult,
)


class FakeDDGS:
    def __init__(self, results=None, error=None):
        self._results = results or []
        self._error = error

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def text(self, *args, **kwargs):
        if self._error:
            raise self._error
        return self._results


def make_result(href, title="Title", body="Snippet"):
    return {"href": href, "title": title, "body": body}


@pytest.mark.asyncio
async def test_search_maps_reddit_urls(monkeypatch):
    fake = FakeDDGS(
        results=[
            make_result(
                "https://www.reddit.com/r/python/comments/abc123/post-title/",
                title="A post",
                body="A snippet",
            ),
            make_result("https://example.com/not-reddit", title="Nope", body="Nope"),
        ]
    )
    monkeypatch.setattr(
        "reddit_mcp.infrastructure.search.providers.duckduckgo.DDGS",
        lambda: fake,
    )

    provider = DuckDuckGoSearchProvider()
    results = await provider.search("python tips")

    assert len(results) == 1
    assert isinstance(results[0], RedditSearchResult)
    assert (
        results[0].url == "https://www.reddit.com/r/python/comments/abc123/post-title/"
    )
    assert results[0].title == "A post"
    assert results[0].snippet == "A snippet"


@pytest.mark.asyncio
async def test_search_no_results_returns_empty(monkeypatch):
    monkeypatch.setattr(
        "reddit_mcp.infrastructure.search.providers.duckduckgo.DDGS",
        lambda: FakeDDGS(results=[]),
    )

    provider = DuckDuckGoSearchProvider()
    results = await provider.search("obscure query with no hits")

    assert results == []


@pytest.mark.asyncio
async def test_search_all_non_reddit_results_returns_empty(monkeypatch):
    monkeypatch.setattr(
        "reddit_mcp.infrastructure.search.providers.duckduckgo.DDGS",
        lambda: FakeDDGS(results=[make_result("https://example.com/a")]),
    )

    provider = DuckDuckGoSearchProvider()
    results = await provider.search("anything")

    assert results == []


@pytest.mark.asyncio
async def test_search_error_raises_search_provider_error(monkeypatch):
    monkeypatch.setattr(
        "reddit_mcp.infrastructure.search.providers.duckduckgo.DDGS",
        lambda: FakeDDGS(error=RuntimeError("rate limited")),
    )

    provider = DuckDuckGoSearchProvider()

    with pytest.raises(SearchProviderError, match="DuckDuckGo search failed"):
        await provider.search("python tips")


def test_post_id_extracted_from_comments_url():
    result = RedditSearchResult(
        url="https://www.reddit.com/r/python/comments/abc123/post-title/",
        title="t",
        snippet="s",
    )
    assert result.post_id == "abc123"


def test_post_id_empty_for_non_comment_url():
    result = RedditSearchResult(
        url="https://www.reddit.com/r/python/", title="t", snippet="s"
    )
    assert result.post_id == ""


def test_subreddit_extracted_from_url():
    result = RedditSearchResult(
        url="https://www.reddit.com/r/python/comments/abc123/post-title/",
        title="t",
        snippet="s",
    )
    assert result.subreddit == "python"
