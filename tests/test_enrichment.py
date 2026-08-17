from datetime import UTC, datetime, timedelta

from reddit_mcp.domain.enrichment import (
    build_comment_url,
    calculate_age_in_days,
    truncate_text,
)


def test_truncate_text_under_limit():
    assert truncate_text("hello", max_length=10) == "hello"


def test_truncate_text_over_limit():
    result = truncate_text("a" * 25, max_length=10)
    assert result == "a" * 10 + "... (truncated)"


def test_truncate_text_none():
    assert truncate_text(None) == ""


def test_calculate_age_in_days():
    three_days_ago = (datetime.now(UTC) - timedelta(days=3)).timestamp()
    age = calculate_age_in_days(three_days_ago)
    assert isinstance(age, int)
    assert age >= 0
    assert age == 3


def test_calculate_age_in_days_none():
    assert calculate_age_in_days(None) is None


def test_calculate_age_in_days_zero():
    assert calculate_age_in_days(0) is None


def test_build_comment_url_prefix_forms():
    expected = "https://www.reddit.com/r/python/comments/abc123/_/c1d2e3/"
    for sub in ("python", "r/python", "/r/python"):
        assert build_comment_url(sub, "abc123", "c1d2e3") == expected


def test_build_comment_url_strips_whitespace():
    url = build_comment_url("  python  ", "abc123", "c1d2e3")
    assert url == "https://www.reddit.com/r/python/comments/abc123/_/c1d2e3/"
