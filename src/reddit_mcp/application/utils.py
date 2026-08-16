import asyncio
import functools
import logging
from datetime import datetime, timezone
from typing import Callable, Any

logger = logging.getLogger(__name__)

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

def calculate_age_in_days(created_utc: float | None) -> int:
    """Calculates the integer age of a post in days relative to now."""
    if not created_utc:
        return 0
    now = datetime.now(timezone.utc)
    created_dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
    delta = now - created_dt
    return max(0, delta.days)

def format_timestamp(created_utc: float | None) -> str:
    """Converts Reddit's Unix timestamp to a human-readable string."""
    if not created_utc:
        return "Unknown date"
    dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
    return dt.strftime("%B %d, %Y")

def build_meta_context() -> dict:
    """Builds a rich temporal and operational context for the AI."""
    now = datetime.now(timezone.utc)
    return {
        "current_server_date": now.strftime("%A, %B %d, %Y"),
        "instruction_note": (
            "1. Use age_in_days for freshness analysis. 2. Use comment_url for citations. "
            "3. If next_page_token is present, you can request the next page. "
            "4. Only high-quality data is returned."
        )
    }

def build_comment_url(subreddit: str, post_id: str, comment_id: str) -> str:
    """Fabricates an absolute deep-link to a specific comment."""
    clean_sub = subreddit.replace('r/', '').replace('/r/', '')
    return f"https://www.reddit.com/r/{clean_sub}/comments/{post_id}/_/{comment_id}/"

def is_high_quality_comment(author: str, body: str, score: int, min_score: int = 2, min_length: int = 40) -> bool:
    """Smart heuristics to filter out bots, low-effort replies, and heavily downvoted opinions."""
    if not body or not author:
        return False
        
    author_lower = author.lower()
    if "bot" in author_lower or author_lower == "automoderator":
        return False
        
    if "i am a bot" in body.lower() or "action was performed automatically" in body.lower():
        return False
        
    if len(body.strip()) < min_length:
        return False
        
    if score < min_score:
        return False
        
    return True

def llm_timeout(timeout_seconds: int = 15):
    """
    Decorator that enforces a strict timeout on tool execution to prevent LLM client disconnects.
    Returns a graceful JSON fallback message for the LLM instead of throwing an unhandled exception.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> dict:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_seconds)
            except asyncio.TimeoutError:
                logger.warning(f"Tool {func.__name__} timed out after {timeout_seconds}s.")
                return {
                    "meta_context": build_meta_context(),
                    "data": [],
                    "next_page_token": None,
                    "status": "partial_timeout",
                    "message": "Request paused to prevent timeout. Use available data or retry."
                }
        return wrapper
    return decorator
