from pathlib import Path

from inboxgent.ingest import iter_manifest, manifest_hash

FIXTURE = Path(__file__).parents[1] / "fixtures" / "maildir"


def test_manifest_covers_fixture() -> None:
    entries = list(iter_manifest(FIXTURE))
    assert len(entries) == 6
    assert {e.custodian for e in entries} == {"alice-a", "bob-b"}
    assert {e.folder for e in entries} == {"sent", "inbox"}


def test_manifest_hash_is_deterministic() -> None:
    a = list(iter_manifest(FIXTURE))
    b = list(iter_manifest(FIXTURE))
    assert manifest_hash(a) == manifest_hash(b)


def test_manifest_hash_changes_with_content(tmp_path: Path) -> None:
    (tmp_path / "c" / "f").mkdir(parents=True)
    f = tmp_path / "c" / "f" / "1"
    f.write_bytes(b"one")
    h1 = manifest_hash(list(iter_manifest(tmp_path)))
    f.write_bytes(b"two")
    assert manifest_hash(list(iter_manifest(tmp_path))) != h1
