"""Retainer readiness from adoption signals — complements proof_architecture retainer gate."""

from __future__ import annotations

from dataclasses import dataclass


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


__all__ = ["AdoptionRetainerReadiness", "adoption_retainer_readiness_passes", "wave2_retainer_eligibility"]
