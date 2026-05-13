"""Adoption Score — 8 dimensions, total 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


ADOPTION_WEIGHTS: dict[str, int] = {
    "executive_sponsor": 15,
    "workflow_owner": 15,
    "data_readiness": 10,
    "user_engagement": 15,
    "approval_completion": 10,
    "proof_visibility": 15,
    "monthly_cadence": 10,
    "expansion_pull": 10,
}


class AdoptionTier(str, Enum):
    SCALE = "scale_account"          # 85+
    RETAINER_READY = "retainer_ready"  # 70..84
    NEEDS_ENABLEMENT = "needs_enablement"  # 55..69
    RISKY = "risky_adoption"         # <55


@dataclass(frozen=True)
class AdoptionComponents:
    executive_sponsor: int
    workflow_owner: int
    data_readiness: int
    user_engagement: int
    approval_completion: int
    proof_visibility: int
    monthly_cadence: int
    expansion_pull: int

    def __post_init__(self) -> None:
        for name in ADOPTION_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_adoption_score(c: AdoptionComponents) -> int:
    weighted = 0.0
    for name, w in ADOPTION_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_adoption(score: int) -> AdoptionTier:
    if score >= 85:
        return AdoptionTier.SCALE
    if score >= 70:
        return AdoptionTier.RETAINER_READY
    if score >= 55:
        return AdoptionTier.NEEDS_ENABLEMENT
    return AdoptionTier.RISKY
