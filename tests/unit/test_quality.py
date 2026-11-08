from pathlib import Path

import pytest

from inboxgent.ingest import iter_manifest
from inboxgent.parse import ParseStats, parse_message
from inboxgent.quality import GateFailedError, GateThresholds, gate_g1, gate_g2
from inboxgent.sampling import SampledEmail, stratified_sample

ROOT = Path(__file__).parents[1] / "fixtures" / "maildir"


def _parsed():
    stats = ParseStats()
    emails = [
        parse_message((ROOT / e.rel_path).read_bytes(), e, stats) for e in iter_manifest(ROOT)
    ]
    return emails, stats


def test_g2_fails_on_fixture_with_default_threshold() -> None:
    emails, stats = _parsed()
    with pytest.raises(GateFailedError) as err:
        gate_g2(emails, stats)
    assert err.value.gate == "G2"


def test_g2_passes_with_lenient_threshold() -> None:
    emails, stats = _parsed()
    gate_g2(emails, stats, GateThresholds(max_failure_rate=0.5))


def test_g2_flags_out_of_range_dates() -> None:
    emails, stats = _parsed()
    from datetime import UTC, datetime

    with pytest.raises(GateFailedError):
        gate_g2(
            emails,
            stats,
            GateThresholds(max_failure_rate=1.0, date_max=datetime(2000, 1, 1, tzinfo=UTC)),
        )


def test_g1_passes_and_fails() -> None:
    emails, _ = _parsed()
    sample = stratified_sample(emails, 3, seed=1)
    gate_g1(sample, expected_size=3, seed=1)
    with pytest.raises(GateFailedError):
        gate_g1(sample, expected_size=4, seed=None)
    with pytest.raises(GateFailedError):
        gate_g1([SampledEmail("a", "s", 0.5), SampledEmail("a", "s", 0.5)], expected_size=2, seed=1)
