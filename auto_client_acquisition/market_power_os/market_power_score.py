"""Composite market power score across eight power sources."""

from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class MarketPowerDimensions:
    category_power: int = 0
    trust_power: int = 0
    proof_power: int = 0
    data_benchmark_power: int = 0
    distribution_power: int = 0
    product_power: int = 0
    standards_power: int = 0
    venture_power: int = 0


_MARKET_POWER_WEIGHTS: dict[str, int] = {
    "category_power": 15,
    "trust_power": 12,
    "proof_power": 14,
    "data_benchmark_power": 11,
    "distribution_power": 11,
    "product_power": 14,
    "standards_power": 11,
    "venture_power": 12,
}


def compute_market_power_score(dimensions: MarketPowerDimensions) -> float:
    """Weighted average 0-100; each dimension is scored 0-100 externally."""
    names = {f.name for f in fields(MarketPowerDimensions)}
    if names != set(_MARKET_POWER_WEIGHTS):
        raise RuntimeError("MarketPowerDimensions out of sync with weights")
    total_w = sum(_MARKET_POWER_WEIGHTS.values())
    if total_w != 100:
        raise RuntimeError(f"market power weights must sum to 100, got {total_w}")
    for name in names:
        v = getattr(dimensions, name)
        if not 0 <= v <= 100:
            raise ValueError(f"{name} must be 0..100, got {v}")
    return round(
        sum(getattr(dimensions, k) * w for k, w in _MARKET_POWER_WEIGHTS.items()) / 100.0,
        2,
    )
