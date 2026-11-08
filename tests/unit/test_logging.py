import logging

from inboxgent.logging import REDACTED, redact, setup_logging

FAKE_KEY = "sk-ant-FAKEKEY1234567890"


def test_redact_api_key() -> None:
    assert FAKE_KEY not in redact(f"calling with {FAKE_KEY}")


def test_redact_key_value_pair() -> None:
    assert "hunter2" not in redact("password=hunter2")
    assert REDACTED in redact("password=hunter2")


def test_logger_redacts(caplog) -> None:
    logger = setup_logging("INFO")
    logger.propagate = True
    with caplog.at_level(logging.INFO, logger="inboxgent"):
        logger.info("key is %s", FAKE_KEY)
    assert FAKE_KEY not in caplog.text
