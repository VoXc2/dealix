"""Resilience Score — 8 dimensions, total 100, with scaling tier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


RESILIENCE_WEIGHTS: dict[str, int] = {
    "governance_coverage": 20,
    "source_passport_coverage": 15,
    "ai_run_logging": 15,
    "proof_pack_completion": 15,
    "incident_response_quality": 10,
    "bad_revenue_rejected": 10,
    "delivery_repeatability": 10,
    "partner_compliance": 5,
}


class ResilienceTier(str, Enum):
    RESILIENT = "resilient"        # 85+
    IMPROVING = "improving"        # 70..84
    FRAGILE = "fragile"            # 55..69
    DO_NOT_SCALE = "do_not_scale"  # <55


@dataclass(frozen=True)
class ResilienceComponents:
    governance_coverage: int
    source_passport_coverage: int
    ai_run_logging: int
    proof_pack_completion: int
    incident_response_quality: int
    bad_revenue_rejected: int
    delivery_repeatability: int
    partner_compliance: int

    def __post_init__(self) -> None:
        for name in RESILIENCE_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_resilience_score(c: ResilienceComponents) -> int:
    weighted = 0.0
    for name, w in RESILIENCE_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_resilience(score: int) -> ResilienceTier:
    if score >= 85:
        return ResilienceTier.RESILIENT
    if score >= 70:
        return ResilienceTier.IMPROVING
    if score >= 55:
        return ResilienceTier.FRAGILE
    return ResilienceTier.DO_NOT_SCALE
