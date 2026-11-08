"""Data-quality gates G1 (ingest/sample) and G2 (parse). Fail loudly on violation."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime

from inboxgent.parse import ParsedEmail, ParseStats
from inboxgent.sampling import SampledEmail


class GateFailedError(RuntimeError):
    def __init__(self, gate: str, problems: list[str]) -> None:
        super().__init__(f"{gate} failed: " + "; ".join(problems))
        self.gate = gate
        self.problems = problems


@dataclass(frozen=True)
class GateThresholds:
    max_failure_rate: float = 0.05
    date_min: datetime = field(default=datetime(1995, 1, 1, tzinfo=UTC))
    date_max: datetime = field(default=datetime(2003, 1, 1, tzinfo=UTC))


def gate_g1(sample: Sequence[SampledEmail], *, expected_size: int, seed: int | None) -> None:
    problems: list[str] = []
    if seed is None:
        problems.append("seed not recorded")
    if len(sample) != expected_size:
        problems.append(f"sample size {len(sample)} != expected {expected_size}")
    ids = [s.message_id for s in sample]
    if len(set(ids)) != len(ids):
        problems.append("duplicate message ids in sample")
    if any(not 0 < s.inclusion_prob <= 1 for s in sample):
        problems.append("inclusion probability outside (0, 1]")
    if problems:
        raise GateFailedError("G1", problems)


def gate_g2(
    emails: Sequence[ParsedEmail],
    stats: ParseStats,
    thresholds: GateThresholds = GateThresholds(),  # noqa: B008
) -> None:
    problems: list[str] = []
    for name, count in stats.failures.items():
        rate = count / stats.total if stats.total else 0.0
        if rate > thresholds.max_failure_rate:
            problems.append(f"{name} rate {rate:.1%} > {thresholds.max_failure_rate:.1%}")
    dupes = [k for k, v in Counter(e.message_id for e in emails).items() if v > 1]
    if dupes:
        problems.append(f"{len(dupes)} non-unique message ids")
    out_of_range = [
        e.message_id
        for e in emails
        if e.date_utc and not thresholds.date_min <= e.date_utc < thresholds.date_max
    ]
    if out_of_range:
        problems.append(f"{len(out_of_range)} dates outside allowed range")
    if problems:
        raise GateFailedError("G2", problems)
