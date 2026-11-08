from pathlib import Path

from inboxgent.config import API_KEY_ENV, Settings, load_settings

FAKE_KEY = "sk-ant-FAKEKEY1234567890"


def test_defaults_load(tmp_path: Path) -> None:
    settings = load_settings(tmp_path / "missing.yaml")
    assert settings.llm.budget_usd == 0.0
    assert settings.llm.api_key is None


def test_api_key_from_env_is_masked(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv(API_KEY_ENV, FAKE_KEY)
    settings = load_settings(tmp_path / "missing.yaml")
    assert settings.llm.api_key is not None
    assert settings.llm.api_key.get_secret_value() == FAKE_KEY
    assert FAKE_KEY not in repr(settings)
    assert FAKE_KEY not in settings.model_dump_json()


def test_api_key_in_yaml_is_ignored(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv(API_KEY_ENV, raising=False)
    cfg = tmp_path / "c.yaml"
    cfg.write_text(f"llm:\n  api_key: {FAKE_KEY}\n", encoding="utf-8")
    settings = load_settings(cfg, env_file=tmp_path / "none.env")
    assert settings.llm.api_key is None


def test_component_seed_is_stable_and_distinct() -> None:
    s = Settings(seed=1)
    assert s.component_seed("split") == s.component_seed("split")
    assert s.component_seed("split") != s.component_seed("bootstrap")
