import pytest

from reddit_mcp.infrastructure import settings as settings_module
from reddit_mcp.infrastructure.settings import AppConfig


@pytest.fixture
def isolated_env(monkeypatch, tmp_path):
    """Isolate external configuration so the default UA factory is exercised."""
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    _clear_install_id_caches()
    yield
    _clear_install_id_caches()


def _clear_install_id_caches():
    settings_module._install_id.cache_clear()
    settings_module._process_install_id.cache_clear()


def test_default_user_agent_is_stable_across_instances(isolated_env):
    config_a = AppConfig(_env_file=None)
    config_b = AppConfig(_env_file=None)

    assert config_a.reddit_user_agent == config_b.reddit_user_agent
    assert config_a.reddit_user_agent.startswith("reddit-mcp-server/0.2.0")


def test_default_user_agent_persists_across_restart(isolated_env):
    first_run = AppConfig(_env_file=None).reddit_user_agent

    # Simulate a fresh process (new process ID) reading the persisted install ID.
    settings_module._process_install_id.cache_clear()
    settings_module._install_id.cache_clear()

    assert AppConfig(_env_file=None).reddit_user_agent == first_run


def test_default_user_agent_is_unique_per_install(isolated_env, monkeypatch, tmp_path):
    install_a = AppConfig(_env_file=None).reddit_user_agent

    # Fresh process with a separate state directory = a different install.
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state-2"))
    _clear_install_id_caches()

    install_b = AppConfig(_env_file=None).reddit_user_agent

    assert install_a != install_b


def test_default_user_agent_tolerates_unwritable_state_dir(
    isolated_env, monkeypatch, tmp_path
):
    # A file occupying the state path makes both read and mkdir fail; the
    # factory must fall back to the process-stable ID instead of crashing.
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory")
    monkeypatch.setattr(
        settings_module, "_install_id_path", lambda: blocker / "install-id"
    )

    config_a = AppConfig(_env_file=None)
    config_b = AppConfig(_env_file=None)

    assert config_a.reddit_user_agent == config_b.reddit_user_agent
    assert config_a.reddit_user_agent.startswith("reddit-mcp-server/0.2.0")


def test_explicit_user_agent_wins():
    config = AppConfig(reddit_user_agent="custom-agent", _env_file=None)

    assert config.reddit_user_agent == "custom-agent"
