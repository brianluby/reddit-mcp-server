"""Pure enrichment helpers for mapping raw Reddit data to domain representations."""

from datetime import UTC, datetime


def truncate_text(text: str | None, max_length: int = 2000) -> str:
    """
    Truncates text to a maximum length to prevent context window overflow.
    Intelligently cuts off text and appends '... (truncated)'.
    """
    if not text:
        return ""
    if len(text) > max_length:
        return text[:max_length] + "... (truncated)"
    return text


def calculate_age_in_days(created_utc: float | None) -> int | None:
    """Calculates the integer age of a post in days relative to now."""
    if not created_utc:
        return None
    now = datetime.now(UTC)
    created_dt = datetime.fromtimestamp(created_utc, tz=UTC)
    delta = now - created_dt
    return max(0, delta.days)


def format_timestamp(created_utc: float | None) -> str:
    """Converts Reddit's Unix timestamp to a human-readable string."""
    if not created_utc:
        return "Unknown date"
    dt = datetime.fromtimestamp(created_utc, tz=UTC)
    return dt.strftime("%B %d, %Y")


def build_comment_url(subreddit: str, post_id: str, comment_id: str) -> str:
    """Fabricates an absolute deep-link to a specific comment."""
    clean_sub = subreddit.strip()
    if clean_sub.startswith("/r/"):
        clean_sub = clean_sub[3:]
    elif clean_sub.startswith("r/"):
        clean_sub = clean_sub[2:]
    return f"https://www.reddit.com/r/{clean_sub}/comments/{post_id}/_/{comment_id}/"
