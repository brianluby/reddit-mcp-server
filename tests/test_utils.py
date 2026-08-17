from datetime import UTC, datetime, timedelta

from reddit_mcp.application.utils import (
    calculate_age_in_days,
    is_high_quality_comment,
    truncate_text,
)

LONG_BODY = "This is a sufficiently long comment body that adds real substance."
BOT_PHRASE_BODY = "I am a bot, and this action was performed automatically. " * 2
AUTO_PHRASE_BODY = "This action was performed automatically by a moderator. " * 2


def test_high_quality_comment_passes():
    assert is_high_quality_comment(author="human_user", body=LONG_BODY, score=10)


def test_short_body_filtered():
    assert not is_high_quality_comment(author="human_user", body="too short", score=10)


def test_automoderator_author_filtered():
    assert not is_high_quality_comment(author="AutoModerator", body=LONG_BODY, score=10)


def test_bot_author_filtered():
    assert not is_high_quality_comment(author="helpful_bot", body=LONG_BODY, score=10)


def test_bot_phrase_body_filtered():
    assert not is_high_quality_comment(
        author="human_user", body=BOT_PHRASE_BODY, score=10
    )


def test_automated_action_phrase_body_filtered():
    assert not is_high_quality_comment(
        author="human_user", body=AUTO_PHRASE_BODY, score=10
    )


def test_young_thread_score_one_passes_age_zero():
    assert is_high_quality_comment(
        author="human_user", body=LONG_BODY, score=1, thread_age_in_days=0
    )


def test_young_thread_score_one_passes_age_one():
    assert is_high_quality_comment(
        author="human_user", body=LONG_BODY, score=1, thread_age_in_days=1
    )


def test_young_thread_score_one_passes_age_two():
    assert is_high_quality_comment(
        author="human_user", body=LONG_BODY, score=1, thread_age_in_days=2
    )


def test_old_thread_score_one_filtered():
    assert not is_high_quality_comment(
        author="human_user", body=LONG_BODY, score=1, thread_age_in_days=3
    )


def test_no_thread_age_score_one_filtered():
    assert not is_high_quality_comment(author="human_user", body=LONG_BODY, score=1)


def test_no_thread_age_score_two_passes():
    assert is_high_quality_comment(author="human_user", body=LONG_BODY, score=2)


def test_young_thread_min_score_below_one_wins():
    assert is_high_quality_comment(
        author="human_user",
        body=LONG_BODY,
        score=0,
        min_score=0,
        thread_age_in_days=1,
    )


def test_young_thread_explicit_min_score_floored_at_one():
    assert not is_high_quality_comment(
        author="human_user",
        body=LONG_BODY,
        score=0,
        min_score=5,
        thread_age_in_days=1,
    )
    assert is_high_quality_comment(
        author="human_user",
        body=LONG_BODY,
        score=1,
        min_score=5,
        thread_age_in_days=1,
    )


def test_empty_body_filtered():
    assert not is_high_quality_comment(author="human_user", body="", score=10)


def test_empty_author_filtered():
    assert not is_high_quality_comment(author="", body=LONG_BODY, score=10)


def test_truncate_text_under_limit():
    assert truncate_text("hello", max_length=10) == "hello"


def test_truncate_text_over_limit():
    result = truncate_text("a" * 25, max_length=10)
    assert result == "a" * 10 + "... (truncated)"


def test_truncate_text_none():
    assert truncate_text(None) == ""


def test_calculate_age_in_days():
    three_days_ago = (datetime.now(UTC) - timedelta(days=3)).timestamp()
    assert calculate_age_in_days(three_days_ago) == 3


def test_calculate_age_in_days_none():
    assert calculate_age_in_days(None) == 0
