from reddit_mcp.application.utils import is_high_quality_comment

LONG_BODY = "This is a sufficiently long comment body that adds real substance."
BOT_PHRASE_BODY = "I am a bot, and this action was performed automatically. " * 2
AUTO_PHRASE_BODY = "This action was performed automatically by a moderator. " * 2


def test_high_quality_comment_passes():
    assert is_high_quality_comment(author="human_user", body=LONG_BODY, score=10)


def test_short_body_filtered():
    assert not is_high_quality_comment(author="human_user", body="too short", score=10)


def test_automoderator_author_filtered():
    assert not is_high_quality_comment(author="AutoModerator", body=LONG_BODY, score=10)


def test_bot_suffix_author_filtered():
    assert not is_high_quality_comment(author="user_bot", body=LONG_BODY, score=10)


def test_bot_hyphen_suffix_author_filtered():
    assert not is_high_quality_comment(author="user-bot", body=LONG_BODY, score=10)


def test_bot_substring_in_legitimate_username_passes():
    assert is_high_quality_comment(author="robotics_fan", body=LONG_BODY, score=10)


def test_bottlerocket_username_passes():
    assert is_high_quality_comment(author="BottleRocket", body=LONG_BODY, score=10)


def test_abbotsford_resident_username_passes():
    assert is_high_quality_comment(
        author="abbotsford_resident", body=LONG_BODY, score=10
    )


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
