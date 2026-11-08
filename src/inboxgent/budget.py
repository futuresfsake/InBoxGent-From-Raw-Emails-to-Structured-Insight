"""In-code spend cap for paid LLM calls (defense in depth beside the provider-side limit)."""

from __future__ import annotations

from dataclasses import dataclass


class BudgetExceededError(RuntimeError):
    """Raised before a call whose projected cost would exceed the cap."""


@dataclass
class BudgetGuard:
    cap_usd: float
    spent_usd: float = 0.0

    def check(self, projected_usd: float) -> None:
        if projected_usd < 0:
            raise ValueError("projected cost must be non-negative")
        if self.spent_usd + projected_usd > self.cap_usd:
            raise BudgetExceededError(
                f"projected spend {self.spent_usd + projected_usd:.4f} USD exceeds cap "
                f"{self.cap_usd:.4f} USD"
            )

    def record(self, actual_usd: float) -> None:
        self.spent_usd += actual_usd

    @property
    def remaining_usd(self) -> float:
        return max(self.cap_usd - self.spent_usd, 0.0)


def estimate_cost_usd(
    input_tokens: int, output_tokens: int, *, usd_per_mtok_in: float, usd_per_mtok_out: float
) -> float:
    return (input_tokens * usd_per_mtok_in + output_tokens * usd_per_mtok_out) / 1_000_000
