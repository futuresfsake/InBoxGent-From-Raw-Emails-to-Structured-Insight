from pathlib import Path

from inboxgent.cleaning import clean, normalize, strip_forwarded, strip_quoted, strip_signature
from inboxgent.ingest import iter_manifest
from inboxgent.parse import ParseStats, parse_message

ROOT = Path(__file__).parents[1] / "fixtures" / "maildir"


def _body(mid: str) -> str:
    stats = ParseStats()
    for e in iter_manifest(ROOT):
        p = parse_message((ROOT / e.rel_path).read_bytes(), e, stats)
        if p.message_id == mid:
            return p.body_raw
    raise AssertionError(mid)


def test_normalize_collapses_whitespace_and_controls() -> None:
    assert normalize("a \t b\x00\r\n\n\n\n c  ") == "a b\n\nc"


def test_forward_block_removed() -> None:
    out = clean(_body("m4@example.test")).text
    assert out == "FYI, see below."


def test_quoted_reply_and_original_message_removed() -> None:
    out = clean(_body("m3@example.test")).text
    assert out == "Will do. Draft attached tomorrow."


def test_signature_removed() -> None:
    out = clean(_body("m1@example.test")).text
    assert "Example Corp" not in out
    assert out.startswith("Hi Bob,")


def test_on_wrote_header_removed() -> None:
    text = "Sounds good.\n\nOn Mon, May 14, 2001 at 8:30 AM, Alice wrote:\n> hello"
    assert strip_quoted(text).strip() == "Sounds good."


def test_disclaimer_removed() -> None:
    out = clean(_body("m6@example.test")).text
    assert out == "Body only."


def test_lineage_records_per_step_removal() -> None:
    r = clean(_body("m3@example.test"))
    assert r.chars_removed_by_step["strip_forwarded"] > 0
    assert set(r.chars_removed_by_step) == {
        "normalize",
        "strip_forwarded",
        "strip_quoted",
        "strip_signature",
        "final_normalize",
    }


def test_individual_steps_are_noops_on_clean_text() -> None:
    t = "Plain message."
    assert strip_forwarded(t) == strip_quoted(t) == strip_signature(t) == t
