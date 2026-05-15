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


@dataclass(frozen=True, slots=True)
class RetainerReadinessResult:
    """Retainer eligibility decision with gaps and a recommended next offer."""

    customer_id: str
    eligible: bool
    recommended_offer: str
    gaps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate(
    *,
    customer_id: str,
    adoption_score: float,
    proof_score: float,
    workflow_owner_present: bool,
    governance_risk_controlled: bool,
) -> RetainerReadinessResult:
    """Decide retainer eligibility from adoption + proof signals.

    Eligibility requires adoption >= 70, proof >= 80, a named workflow owner,
    and controlled governance risk. Always returns a non-empty recommended
    offer so the customer is guided even when eligibility fails.
    """
    gaps: list[str] = []
    if adoption_score < 70:
        gaps.append("adoption_score_below_70")
    if proof_score < 80:
        gaps.append("proof_score_below_80")
    if not workflow_owner_present:
        gaps.append("workflow_owner_missing")
    if not governance_risk_controlled:
        gaps.append("governance_risk_not_controlled")

    eligible = not gaps
    if eligible:
        recommended_offer = "monthly_governed_ai_operations_retainer"
    elif adoption_score >= 40 and proof_score >= 50:
        recommended_offer = "proof_consolidation_sprint"
    else:
        recommended_offer = "capability_diagnostic"

    return RetainerReadinessResult(
        customer_id=customer_id,
        eligible=eligible,
        recommended_offer=recommended_offer,
        gaps=gaps,
    )


__all__ = [
    "AdoptionRetainerReadiness",
    "RetainerReadinessResult",
    "adoption_retainer_readiness_passes",
    "evaluate",
    "wave2_retainer_eligibility",
]
