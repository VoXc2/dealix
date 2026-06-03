"""Portfolio priority score for business units under the holding model."""

from __future__ import annotations

from dataclasses import dataclass

_PORTFOLIO_WEIGHTS: dict[str, int] = {
    "revenue_signal": 25,
    "repeatability": 20,
    "proof_signal": 20,
    "retainer_signal": 20,
    "product_signal": 15,
}


@dataclass(frozen=True, slots=True)
class PortfolioUnitInputs:
    revenue_signal: int = 0
    repeatability: int = 0
    proof_signal: int = 0
    retainer_signal: int = 0
    product_signal: int = 0


def _validate_dim(name: str, v: int) -> None:
    if not 0 <= v <= 100:
        raise ValueError(f"{name} must be 0..100, got {v}")


def compute_portfolio_priority_score(inputs: PortfolioUnitInputs) -> float:
    """Weighted average 0-100 across five portfolio dimensions."""
    d = {
        "revenue_signal": inputs.revenue_signal,
        "repeatability": inputs.repeatability,
        "proof_signal": inputs.proof_signal,
        "retainer_signal": inputs.retainer_signal,
        "product_signal": inputs.product_signal,
    }
    if set(d) != set(_PORTFOLIO_WEIGHTS):
        raise RuntimeError("Portfolio inputs out of sync with weights")
    for name, v in d.items():
        _validate_dim(name, v)
    total_w = sum(_PORTFOLIO_WEIGHTS.values())
    if total_w != 100:
        raise RuntimeError(f"portfolio weights must sum to 100, got {total_w}")
    return round(sum(d[k] * _PORTFOLIO_WEIGHTS[k] for k in d) / 100.0, 2)
