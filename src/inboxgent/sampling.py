"""Seeded stratified sampling (custodian x year) with inclusion probabilities."""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass

from inboxgent.parse import ParsedEmail

DEFAULT_SAMPLE_SIZE = 30_000  # gap G-11 default


@dataclass(frozen=True)
class SampledEmail:
    message_id: str
    stratum: str
    inclusion_prob: float


def stratum_of(email: ParsedEmail) -> str:
    year = str(email.date_utc.year) if email.date_utc else "unknown"
    return f"{email.custodian}|{year}"


def _allocate(sizes: dict[str, int], n: int) -> dict[str, int]:
    """Proportional allocation by largest remainder; never exceeds a stratum's size."""
    total = sum(sizes.values())
    if n >= total:
        return dict(sizes)
    exact = {k: n * v / total for k, v in sizes.items()}
    alloc = {k: int(x) for k, x in exact.items()}
    leftover = n - sum(alloc.values())
    order = sorted(sizes, key=lambda k: (-(exact[k] - alloc[k]), k))
    for k in order:
        if leftover == 0:
            break
        if alloc[k] < sizes[k]:
            alloc[k] += 1
            leftover -= 1
    return alloc


def stratified_sample(
    frame: Sequence[ParsedEmail], n: int = DEFAULT_SAMPLE_SIZE, *, seed: int
) -> list[SampledEmail]:
    """Draw ``n`` emails from the sampling frame, stratified and reproducible for a seed.

    The frame should contain canonical (deduplicated) messages only.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    strata: dict[str, list[str]] = defaultdict(list)
    for e in frame:
        strata[stratum_of(e)].append(e.message_id)
    sizes = {k: len(v) for k, v in strata.items()}
    alloc = _allocate(sizes, n)
    out: list[SampledEmail] = []
    for key in sorted(strata):
        ids = sorted(strata[key])
        take = alloc[key]
        if take == 0:
            continue
        rng = random.Random(f"{seed}:{key}")  # noqa: S311  # nosec B311
        chosen = sorted(rng.sample(ids, take))
        prob = take / len(ids)
        out.extend(SampledEmail(mid, key, prob) for mid in chosen)
    return out
