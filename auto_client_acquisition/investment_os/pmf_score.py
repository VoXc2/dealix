"""PMF scorecard weights and banding for Dealix offer/investment review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PmfBand = Literal["scale", "build", "pilot", "hold_or_kill"]

# Percent weights (must sum to 100). See docs/pmf/PMF_SCORE.md
PMF_WEIGHTS: dict[str, int] = {
    "repeated_pain": 15,
    "clear_buyer": 10,
    "willingness_to_pay": 15,
    "delivery_repeatability": 15,
    "proof_strength": 15,
    "retainer_conversion": 15,
    "productization_signal": 10,
    "governance_safety": 5,
}


def _validate_scores(**kwargs: float) -> None:
    w_keys = set(PMF_WEIGHTS)
    if set(kwargs) != w_keys:
        missing = w_keys - set(kwargs)
        extra = set(kwargs) - w_keys
        raise ValueError(f"Expected keys {sorted(w_keys)}; missing={sorted(missing)} extra={sorted(extra)}")
    for name, v in kwargs.items():
        if not 0 <= v <= 100:
            raise ValueError(f"{name} must be 0..100, got {v}")


@dataclass(frozen=True, slots=True)
class PmfScoreInputs:
    repeated_pain: float
    clear_buyer: float
    willingness_to_pay: float
    delivery_repeatability: float
    proof_strength: float
    retainer_conversion: float
    productization_signal: float
    governance_safety: float

    def as_dict(self) -> dict[str, float]:
        return {
            "repeated_pain": self.repeated_pain,
            "clear_buyer": self.clear_buyer,
            "willingness_to_pay": self.willingness_to_pay,
            "delivery_repeatability": self.delivery_repeatability,
            "proof_strength": self.proof_strength,
            "retainer_conversion": self.retainer_conversion,
            "productization_signal": self.productization_signal,
            "governance_safety": self.governance_safety,
        }


def compute_pmf_score(inputs: PmfScoreInputs) -> float:
    """Weighted average of eight dimensions, each 0–100. Result 0–100."""
    d = inputs.as_dict()
    _validate_scores(**d)
    total_w = sum(PMF_WEIGHTS.values())
    if total_w != 100:
        raise RuntimeError(f"PMF_WEIGHTS must sum to 100, got {total_w}")
    return round(sum(d[k] * PMF_WEIGHTS[k] for k in PMF_WEIGHTS) / 100.0, 2)


def pmf_band(score: float) -> PmfBand:
    if score < 0 or score > 100:
        raise ValueError(f"score must be 0..100, got {score}")
    if score >= 85:
        return "scale"
    if score >= 70:
        return "build"
    if score >= 55:
        return "pilot"
    return "hold_or_kill"
