import pytest

from inboxgent.cli import main

FAKE_KEY = "sk-ant-FAKEKEY1234567890"


def test_show_config_masks_secret(monkeypatch, capsys) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", FAKE_KEY)
    assert main(["show-config"]) == 0
    out = capsys.readouterr().out
    assert FAKE_KEY not in out
    assert "claude-haiku-5-5" in out


def test_command_required() -> None:
    with pytest.raises(SystemExit):
        main([])
