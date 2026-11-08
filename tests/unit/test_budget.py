import pytest

from inboxgent.budget import BudgetExceededError, BudgetGuard, estimate_cost_usd


def test_zero_cap_blocks_everything() -> None:
    with pytest.raises(BudgetExceededError):
        BudgetGuard(cap_usd=0.0).check(0.0001)


def test_stops_at_cap_with_mocked_calls() -> None:
    guard = BudgetGuard(cap_usd=1.0)
    calls = 0
    for _ in range(100):
        try:
            guard.check(0.3)
        except BudgetExceededError:
            break
        guard.record(0.3)
        calls += 1
    assert calls == 3
    assert guard.spent_usd <= 1.0


def test_estimate_cost() -> None:
    cost = estimate_cost_usd(1_000_000, 500_000, usd_per_mtok_in=1.0, usd_per_mtok_out=4.0)
    assert cost == pytest.approx(3.0)
