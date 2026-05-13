"""Enterprise rollout adoption gates — 7 ordered gates."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AdoptionGate(str, Enum):
    SPONSOR = "sponsor"
    DATA = "data"
    WORKFLOW = "workflow"
    GOVERNANCE = "governance"
    PROOF = "proof"
    ADOPTION = "adoption"
    RETAINER = "retainer"


ADOPTION_GATES: tuple[AdoptionGate, ...] = tuple(AdoptionGate)


@dataclass(frozen=True)
class AdoptionGateChecks:
    sponsor_present: bool
    source_passport_complete: bool
    workflow_owner_named: bool
    governance_boundaries_agreed: bool
    proof_pack_score: float
    outputs_reviewed_twice: bool
    adoption_score: float
    monthly_value_clear: bool


@dataclass(frozen=True)
class AdoptionGateResult:
    highest_passed: AdoptionGate | None
    next_gate: AdoptionGate | None
    failed_gate: AdoptionGate | None
    failure_reason: str | None


def evaluate_adoption_gates(c: AdoptionGateChecks) -> AdoptionGateResult:
    """Return the highest gate passed and the next one to attack."""

    if not c.sponsor_present:
        return AdoptionGateResult(None, AdoptionGate.SPONSOR, AdoptionGate.SPONSOR, "missing_sponsor")
    if not c.source_passport_complete:
        return AdoptionGateResult(AdoptionGate.SPONSOR, AdoptionGate.DATA, AdoptionGate.DATA, "source_passport_incomplete")
    if not c.workflow_owner_named:
        return AdoptionGateResult(AdoptionGate.DATA, AdoptionGate.WORKFLOW, AdoptionGate.WORKFLOW, "no_workflow_owner")
    if not c.governance_boundaries_agreed:
        return AdoptionGateResult(AdoptionGate.WORKFLOW, AdoptionGate.GOVERNANCE, AdoptionGate.GOVERNANCE, "governance_not_agreed")
    if c.proof_pack_score < 70:
        return AdoptionGateResult(AdoptionGate.GOVERNANCE, AdoptionGate.PROOF, AdoptionGate.PROOF, "proof_score_below_70")
    if not c.outputs_reviewed_twice:
        return AdoptionGateResult(AdoptionGate.PROOF, AdoptionGate.ADOPTION, AdoptionGate.ADOPTION, "outputs_not_reused")
    if c.proof_pack_score < 80 or c.adoption_score < 70 or not c.monthly_value_clear:
        return AdoptionGateResult(AdoptionGate.ADOPTION, AdoptionGate.RETAINER, AdoptionGate.RETAINER, "retainer_gate_not_met")
    return AdoptionGateResult(AdoptionGate.RETAINER, None, None, None)
