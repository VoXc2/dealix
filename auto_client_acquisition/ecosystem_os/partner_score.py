"""Partner Score — 6 dimensions, total 100, with ladder classification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


PARTNER_SCORE_WEIGHTS: dict[str, int] = {
    "lead_quality": 20,
    "method_alignment": 20,
    "qa_compliance": 20,
    "governance_compliance": 20,
    "client_feedback": 10,
    "expansion_potential": 10,
}


class PartnerLadder(str, Enum):
    REJECT = "reject_or_pause"             # <55
    REFERRAL_ONLY = "referral_only"        # 55..69
    IMPLEMENTATION = "implementation"      # 70..84
    CERTIFIED_OR_STRATEGIC = "certified_or_strategic"  # 85+


@dataclass(frozen=True)
class PartnerScoreComponents:
    lead_quality: int
    method_alignment: int
    qa_compliance: int
    governance_compliance: int
    client_feedback: int
    expansion_potential: int

    def __post_init__(self) -> None:
        for name in PARTNER_SCORE_WEIGHTS:
            v = getattr(self, name)
            if not 0 <= v <= 100:
                raise ValueError(f"{name}_out_of_range_0_100")


def compute_partner_score(c: PartnerScoreComponents) -> int:
    weighted = 0.0
    for name, w in PARTNER_SCORE_WEIGHTS.items():
        weighted += getattr(c, name) * (w / 100.0)
    return round(weighted)


def classify_partner_ladder(score: int) -> PartnerLadder:
    if score >= 85:
        return PartnerLadder.CERTIFIED_OR_STRATEGIC
    if score >= 70:
        return PartnerLadder.IMPLEMENTATION
    if score >= 55:
        return PartnerLadder.REFERRAL_ONLY
    return PartnerLadder.REJECT
