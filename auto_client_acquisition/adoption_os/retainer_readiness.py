"""Retainer Readiness gate.

eligible iff:
- adoption_score >= 70
- proof_score >= 80
- workflow_owner_present
- governance_risk_controlled
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RetainerReadiness:
    eligible: bool
    gaps: list[str] = field(default_factory=list)
    recommended_offer: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate(
    *,
    customer_id: str = "",
    adoption_score: float,
    proof_score: float,
    workflow_owner_present: bool,
    governance_risk_controlled: bool,
) -> RetainerReadiness:
    gaps: list[str] = []
    if adoption_score < 70:
        gaps.append(f"adoption_below_70:{adoption_score}")
    if proof_score < 80:
        gaps.append(f"proof_score_below_80:{proof_score}")
    if not workflow_owner_present:
        gaps.append("workflow_owner_missing")
    if not governance_risk_controlled:
        gaps.append("governance_risk_open")

    eligible = not gaps
    if eligible:
        if proof_score >= 90 and adoption_score >= 85:
            offer = "monthly_revops_os_premium"
        else:
            offer = "monthly_revops_os_standard"
    elif "workflow_owner_missing" in gaps:
        offer = "owner_assignment_workshop"
    elif any(g.startswith("proof_score_below_80") for g in gaps):
        offer = "second_revenue_intelligence_sprint"
    else:
        offer = "adoption_acceleration_sprint"

    return RetainerReadiness(eligible=eligible, gaps=gaps, recommended_offer=offer)


__all__ = ["RetainerReadiness", "evaluate"]
