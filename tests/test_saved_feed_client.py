from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from xml.sax.saxutils import escape

import httpx
import pytest

from reddit_mcp.infrastructure.saved_feed_client import (
    SavedFeedClient,
    SavedFeedError,
    SavedFeedNotConfiguredError,
)

FEED_URL = (
    "https://old.reddit.com/saved.rss"
    "?feed=cafebabedeadbeef&user=testuser"
)


def _feed_response(entries_xml: str) -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.text = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<feed xmlns="http://www.w3.org/2005/Atom">{entries_xml}</feed>'
    )
    return response


def _entry_xml(
    entry_id: str,
    title: str,
    link: str,
    category: str,
    updated: datetime,
    escaped_content: str,
) -> str:
    return f"""
        <entry>
            <id>{entry_id}</id>
            <title>{title}</title>
            <link href="{link}"/>
            <updated>{updated.isoformat()}</updated>
            <category term="{category}"/>
            <content type="html">{escaped_content}</content>
        </entry>"""


def _entry(
    entry_id: str,
    title: str,
    link: str,
    category: str,
    updated: datetime,
    content: str,
) -> str:
    # Real feeds XML-escape the HTML payload inside <content>.
    return _entry_xml(entry_id, title, link, category, updated, escape(content))


@pytest.fixture
def recent() -> datetime:
    return datetime.now(UTC) - timedelta(days=1)


@pytest.fixture
def client():
    feed_client = SavedFeedClient(feed_url=FEED_URL, user_agent="test-agent")
    feed_client._client = MagicMock()
    feed_client._client.get = AsyncMock()
    return feed_client


@pytest.mark.asyncio
async def test_get_saved_posts_parses_posts_and_skips_comments(client, recent):
    entries = _entry(
        "e1",
        "Async Python patterns worth knowing",
        "https://www.reddit.com/r/python/comments/abc123/async_patterns/",
        "python",
        recent,
        '<!-- SC_OFF --><div class="md"><p>Great <b>writeup</b> on asyncio.</p></div><!-- SC_ON -->',
    ) + _entry(
        "e2",
        "comment by someone",
        "https://www.reddit.com/r/rust/comments/def456/some_post/some_comment/",
        "rust",
        recent,
        "<p>A saved comment body.</p>",
    )
    client._client.get.return_value = _feed_response(entries)

    posts, skipped_comments = await client.get_saved_posts(time_filter="month")

    assert skipped_comments == 1
    assert len(posts) == 1
    post = posts[0]
    assert post.id == "abc123"
    assert post.title == "Async Python patterns worth knowing"
    assert post.subreddit == "python"
    assert post.url.endswith("/comments/abc123/async_patterns/")
    assert post.age_in_days == 1  # saved one day ago
    assert post.created_at_human
    assert "writeup" in post.text_preview
    assert "<b>" not in post.text_preview  # HTML stripped
    assert post.score == 0 and post.num_comments == 0 and post.upvote_ratio == 0.0


@pytest.mark.asyncio
async def test_get_saved_posts_time_filter_excludes_old_entries(client, recent):
    old = datetime.now(UTC) - timedelta(days=40)
    entries = _entry(
        "e1",
        "Recent post title",
        "/r/python/comments/aaa/recent/",
        "python",
        recent,
        "<p>x</p>",
    ) + _entry(
        "e2",
        "Ancient post title",
        "/r/python/comments/bbb/old/",
        "python",
        old,
        "<p>x</p>",
    )
    client._client.get.return_value = _feed_response(
        entries.replace("/r/python/", "https://www.reddit.com/r/python/")
    )

    posts, _ = await client.get_saved_posts(time_filter="month")

    assert [p.id for p in posts] == ["aaa"]

    posts, _ = await client.get_saved_posts(time_filter="all")
    assert [p.id for p in posts] == ["aaa", "bbb"]


@pytest.mark.asyncio
async def test_get_saved_posts_applies_limit(client, recent):
    entries = "".join(
        _entry(
            f"e{i}",
            f"Saved post title number {i}",
            f"https://www.reddit.com/r/x/comments/i{i}/slug/",
            "x",
            recent,
            "<p>x</p>",
        )
        for i in range(5)
    )
    client._client.get.return_value = _feed_response(entries)

    posts, _ = await client.get_saved_posts(time_filter="all", limit=3)

    assert len(posts) == 3


@pytest.mark.asyncio
async def test_get_saved_posts_not_configured_raises():
    client = SavedFeedClient(feed_url=None, user_agent="test-agent")

    with pytest.raises(SavedFeedNotConfiguredError):
        await client.get_saved_posts()


@pytest.mark.asyncio
async def test_get_saved_posts_rejects_non_reddit_feed_url():
    client = SavedFeedClient(
        feed_url="https://evil.example.com/saved.rss?feed=deadbeef", user_agent="t"
    )

    with pytest.raises(SavedFeedError, match="https link on reddit.com"):
        await client.get_saved_posts()


@pytest.mark.asyncio
async def test_get_saved_posts_http_error_never_leaks_feed_token(client):
    request = httpx.Request("GET", FEED_URL)
    client._client.get = AsyncMock(
        side_effect=httpx.ConnectError("refused", request=request)
    )

    with pytest.raises(SavedFeedError) as exc_info:
        await client.get_saved_posts()

    assert "cafebabedeadbeef" not in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_saved_posts_malformed_xml_raises(client):
    response = MagicMock()
    response.status_code = 200
    response.url = httpx.URL("https://old.reddit.com/saved.rss")
    response.text = "<not-atom"
    client._client.get.return_value = response

    with pytest.raises(SavedFeedError, match="could not be read"):
        await client.get_saved_posts()


@pytest.mark.asyncio
async def test_get_saved_posts_login_redirect_reports_token_rejection(client):
    # Reddit 302s to /login when the feed token is rejected; the final 200
    # login page must surface as an actionable error, not an XML parse failure.
    response = MagicMock()
    response.status_code = 200
    response.url = httpx.URL("https://old.reddit.com/login/?reason=lor2&dest=saved.rss")
    response.text = "<!DOCTYPE html><html><title>Welcome to Reddit</title></html>"
    client._client.get.return_value = response

    with pytest.raises(SavedFeedError, match="token was rejected"):
        await client.get_saved_posts()


@pytest.mark.asyncio
async def test_get_saved_posts_requests_full_window(client, recent):
    client._client.get.return_value = _feed_response(
        _entry(
            "e1",
            "Some saved post title",
            "https://www.reddit.com/r/x/comments/zzz/slug/",
            "x",
            recent,
            "<p>x</p>",
        )
    )

    await client.get_saved_posts(time_filter="week")

    call = client._client.get.await_args
    requested = str(call.args[0])
    # limit is merged into the URL without clobbering the secret query params
    assert "limit=100" in requested
    assert "feed=cafebabedeadbeef" in requested
    assert "user=testuser" in requested
