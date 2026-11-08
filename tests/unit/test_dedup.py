from pathlib import Path

from inboxgent.dedup import canonical_id, exact_clusters
from inboxgent.ingest import iter_manifest
from inboxgent.parse import ParsedEmail, ParseStats, parse_message

ROOT = Path(__file__).parents[1] / "fixtures" / "maildir"


def _emails() -> list[ParsedEmail]:
    stats = ParseStats()
    return [parse_message((ROOT / e.rel_path).read_bytes(), e, stats) for e in iter_manifest(ROOT)]


def test_fixture_has_one_exact_duplicate_pair() -> None:
    sizes = sorted(len(v) for v in exact_clusters(_emails()).values())
    assert sizes == [1, 1, 1, 1, 2]


def test_canonical_prefers_earliest_sent_copy() -> None:
    emails = _emails()
    pair = [
        e for e in emails if e.subject_norm == "q2 budget review" and e.sender.startswith("alice")
    ]
    assert len(pair) == 2
    assert canonical_id(pair) == "m1@example.test"
