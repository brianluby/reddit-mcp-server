from reddit_mcp.infrastructure.settings import AppConfig


def test_default_user_agent_is_per_instance_unique():
    config_a = AppConfig()
    config_b = AppConfig()

    assert config_a.reddit_user_agent != config_b.reddit_user_agent
    assert config_a.reddit_user_agent.startswith("reddit-mcp-server/0.2.0")
    assert config_b.reddit_user_agent.startswith("reddit-mcp-server/0.2.0")


def test_explicit_user_agent_wins():
    config = AppConfig(reddit_user_agent="custom-agent")

    assert config.reddit_user_agent == "custom-agent"
