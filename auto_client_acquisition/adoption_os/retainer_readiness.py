"""Retainer readiness from adoption signals — complements proof_architecture retainer gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class AdoptionRetainerReadiness:
    workflow_owner_exists: bool
    outputs_used: bool
    approval_path_works: bool
    proof_score: int
    client_asks_continuation: bool
    monthly_value_exists: bool
    governance_risk_controlled: bool


def adoption_retainer_readiness_passes(
    r: AdoptionRetainerReadiness,
) -> tuple[bool, tuple[str, ...]]:
    errs: list[str] = []
    if not r.workflow_owner_exists:
        errs.append("workflow_owner_missing")
    if not r.outputs_used:
        errs.append("outputs_not_used")
    if not r.approval_path_works:
        errs.append("approval_path_broken")
    if r.proof_score < 80:
        errs.append("proof_score_below_80")
    if not r.client_asks_continuation:
        errs.append("no_continuation_pull")
    if not r.monthly_value_exists:
        errs.append("monthly_value_unclear")
    if not r.governance_risk_controlled:
        errs.append("governance_risk_not_controlled")
    return not errs, tuple(errs)


def wave2_retainer_eligibility(
    *,
    proof_score: int,
    adoption_score: int,
    workflow_owner_exists: bool,
    monthly_workflow_exists: bool,
    governance_risk_controlled: bool,
) -> tuple[bool, tuple[str, ...]]:
    """
    Milestone 2 gate — numeric proof + adoption plus operating structure.

    Aligns with Commercial Trust → Retainer Engine handoff (no auto-sell).
    """
    errs: list[str] = []
    if proof_score < 80:
        errs.append("proof_score_below_80")
    if adoption_score < 70:
        errs.append("adoption_score_below_70")
    if not workflow_owner_exists:
        errs.append("workflow_owner_missing")
    if not monthly_workflow_exists:
        errs.append("monthly_workflow_missing")
    if not governance_risk_controlled:
        errs.append("governance_risk_not_controlled")
    return not errs, tuple(errs)


# ── Retainer readiness gate with recommended-offer routing ───────────────


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


__all__ = [
    "AdoptionRetainerReadiness",
    "RetainerReadiness",
    "adoption_retainer_readiness_passes",
    "evaluate",
    "wave2_retainer_eligibility",
]
