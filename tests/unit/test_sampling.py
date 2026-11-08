from datetime import UTC, datetime

import pytest

from inboxgent.parse import ParsedEmail
from inboxgent.sampling import stratified_sample, stratum_of


def _email(i: int, custodian: str, year: int | None) -> ParsedEmail:
    return ParsedEmail(
        message_id=f"m{i}",
        custodian=custodian,
        folder="inbox",
        date_utc=datetime(year, 6, 1, tzinfo=UTC) if year else None,
        sender="a@x.test",
        recipients_to=(),
        recipients_cc=(),
        recipients_bcc=(),
        subject="s",
        subject_norm="s",
        body_raw="b",
    )


FRAME = (
    [_email(i, "a", 2000) for i in range(60)]
    + [_email(100 + i, "a", 2001) for i in range(30)]
    + [_email(200 + i, "b", 2001) for i in range(10)]
    + [_email(300, "b", None)]
)


def test_exact_size_and_reproducible() -> None:
    s1 = stratified_sample(FRAME, 20, seed=7)
    s2 = stratified_sample(FRAME, 20, seed=7)
    assert len(s1) == 20
    assert s1 == s2


def test_different_seed_changes_sample() -> None:
    assert stratified_sample(FRAME, 20, seed=7) != stratified_sample(FRAME, 20, seed=8)


def test_inclusion_probabilities_reflect_stratum() -> None:
    sample = stratified_sample(FRAME, 20, seed=1)
    by_stratum: dict[str, list[float]] = {}
    for s in sample:
        by_stratum.setdefault(s.stratum, []).append(s.inclusion_prob)
    for probs in by_stratum.values():
        assert len(set(probs)) == 1
        assert 0 < probs[0] <= 1


def test_oversized_request_takes_everything_with_prob_one() -> None:
    sample = stratified_sample(FRAME, 10_000, seed=1)
    assert len(sample) == len(FRAME)
    assert {s.inclusion_prob for s in sample} == {1.0}


def test_unknown_year_stratum() -> None:
    assert stratum_of(FRAME[-1]) == "b|unknown"


def test_negative_n_rejected() -> None:
    with pytest.raises(ValueError):
        stratified_sample(FRAME, -1, seed=1)
