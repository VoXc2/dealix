"""Client Quality Score — 7 dimensions weighted to 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


CLIENT_QUALITY_WEIGHTS: dict[str, int] = {
    "clear_pain": 15,
    "data_readiness": 15,
    "decision_owner": 15,
    "willingness_to_pay": 15,
    "governance_alignment": 15,
    "retainer_potential": 15,
    "strategic_logo_value": 10,
}


class ClientTier(str, Enum):
    IDEAL = "ideal"
    GOOD = "good"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    AVOID = "avoid"


@dataclass(frozen=True)
class ClientQualityComponents:
    clear_pain: int
    data_readiness: int
    decision_owner: int
    willingness_to_pay: int
    governance_alignment: int
    retainer_potential: int
    strategic_logo_value: int

    def __post_init__(self) -> None:
        for name in CLIENT_QUALITY_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_client_quality_score(c: ClientQualityComponents) -> int:
    weighted = 0.0
    for name, w in CLIENT_QUALITY_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_client_tier(score: int) -> ClientTier:
    if score >= 85:
        return ClientTier.IDEAL
    if score >= 70:
        return ClientTier.GOOD
    if score >= 55:
        return ClientTier.DIAGNOSTIC_ONLY
    return ClientTier.AVOID
