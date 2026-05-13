"""Client Health Score — 7 dimensions, total 100."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


CLIENT_HEALTH_WEIGHTS: dict[str, int] = {
    "clear_owner": 15,
    "data_readiness": 15,
    "stakeholder_engagement": 15,
    "proof_strength": 20,
    "governance_alignment": 15,
    "monthly_workflow_need": 10,
    "expansion_potential": 10,
}


class ClientHealthTier(str, Enum):
    EXPAND_AGGRESSIVELY = "expand_aggressively"  # 85+
    OFFER_RETAINER = "offer_retainer"            # 70..84
    CONTINUE_CAREFULLY = "continue_carefully"    # 55..69
    PAUSE_OR_DIAGNOSTIC = "pause_or_diagnostic"  # <55


@dataclass(frozen=True)
class ClientHealthComponents:
    clear_owner: int
    data_readiness: int
    stakeholder_engagement: int
    proof_strength: int
    governance_alignment: int
    monthly_workflow_need: int
    expansion_potential: int

    def __post_init__(self) -> None:
        for name in CLIENT_HEALTH_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_client_health_score(c: ClientHealthComponents) -> int:
    weighted = 0.0
    for name, w in CLIENT_HEALTH_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_client_health(score: int) -> ClientHealthTier:
    if score >= 85:
        return ClientHealthTier.EXPAND_AGGRESSIVELY
    if score >= 70:
        return ClientHealthTier.OFFER_RETAINER
    if score >= 55:
        return ClientHealthTier.CONTINUE_CAREFULLY
    return ClientHealthTier.PAUSE_OR_DIAGNOSTIC
