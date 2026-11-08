from pathlib import Path

from inboxgent.ingest import ManifestEntry, iter_manifest
from inboxgent.parse import ParsedEmail, ParseStats, normalize_subject, parse_message

ROOT = Path(__file__).parents[1] / "fixtures" / "maildir"


def _parse_all() -> tuple[list[ParsedEmail], ParseStats]:
    stats = ParseStats()
    out = [parse_message((ROOT / e.rel_path).read_bytes(), e, stats) for e in iter_manifest(ROOT)]
    return out, stats


def test_parses_fixture_with_failure_counts() -> None:
    emails, stats = _parse_all()
    assert len(emails) == stats.total == 6
    assert stats.failures["missing_message_id"] == 1
    assert stats.failures["bad_date"] == 1
    assert stats.failures["missing_recipients"] == 1


def test_headers_are_typed_and_normalized() -> None:
    emails, _ = _parse_all()
    first = next(e for e in emails if e.message_id == "m1@example.test")
    assert first.sender == "alice.a@example.test"
    assert first.recipients_to == ("bob.b@example.test", "carol.c@example.test")
    assert first.recipients_cc == ("dave.d@example.test",)
    assert first.n_recipients == 3
    assert first.date_utc is not None and first.date_utc.utcoffset().total_seconds() == 0
    assert first.date_utc.hour == 15  # 08:30 -0700


def test_synthesized_id_is_stable() -> None:
    e1, _ = _parse_all()
    e2, _ = _parse_all()
    assert sorted(x.message_id for x in e1) == sorted(x.message_id for x in e2)
    assert any(x.message_id.startswith("synth-") for x in e1)


def test_garbage_input_does_not_raise() -> None:
    stats = ParseStats()
    entry = ManifestEntry("c/f/x", "c", "f", 4, "0")
    parsed = parse_message(b"\x00\xff garbage", entry, stats)
    assert parsed.sender == ""
    assert stats.failures["bad_date"] == 1


def test_normalize_subject() -> None:
    assert normalize_subject("RE: FW: Re: Hello World") == "hello world"
