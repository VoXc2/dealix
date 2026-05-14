"""Proof strength, retainer eligibility, productization gate."""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import StrEnum


class PostProofDecision(StrEnum):
    CONTINUE = "continue"
    EXPAND = "expand"
    PAUSE = "pause"


_PROOF_STRENGTH_WEIGHTS: dict[str, int] = {
    "metric_clarity": 20,
    "evidence_quality": 20,
    "before_after": 15,
    "client_relevance": 15,
    "governance_confidence": 15,
    "retainer_linkage": 15,
}


@dataclass(frozen=True, slots=True)
class ProofStrengthInputs:
    metric_clarity: float = 0.0
    evidence_quality: float = 0.0
    before_after: float = 0.0
    client_relevance: float = 0.0
    governance_confidence: float = 0.0
    retainer_linkage: float = 0.0


def compute_proof_strength_score(inp: ProofStrengthInputs) -> float:
    """Weighted average 0-100 from six sub-scores 0-100."""
    names = {f.name for f in fields(ProofStrengthInputs)}
    if names != set(_PROOF_STRENGTH_WEIGHTS):
        raise RuntimeError("ProofStrengthInputs out of sync with weights")
    if sum(_PROOF_STRENGTH_WEIGHTS.values()) != 100:
        raise RuntimeError("proof strength weights must sum to 100")
    for n in names:
        v = getattr(inp, n)
        if not 0 <= v <= 100:
            raise ValueError(f"{n} must be 0..100, got {v}")
    return round(sum(getattr(inp, k) * w for k, w in _PROOF_STRENGTH_WEIGHTS.items()) / 100.0, 2)


def proof_usable_for_sales(proof_strength_score: float, minimum: float = 70.0) -> bool:
    return proof_strength_score >= minimum


@dataclass(frozen=True, slots=True)
class RetainerEligibilityInputs:
    proof_strength_score: float
    client_health: float
    workflow_recurring: bool = False
    monthly_value_clear: bool = False
    stakeholder_engaged: bool = False


def is_retainer_eligible(inp: RetainerEligibilityInputs) -> bool:
    return (
        inp.workflow_recurring
        and inp.monthly_value_clear
        and inp.stakeholder_engaged
        and inp.proof_strength_score >= 80
        and inp.client_health >= 70
    )


@dataclass(frozen=True, slots=True)
class ProductizationGateInputs:
    manual_step_repeated: int = 0
    time_cost_hours_per_project: float = 0.0
    linked_to_paid_offer: bool = False
    reduces_risk_or_improves_margin: bool = False
    testable: bool = False


def passes_productization_gate(inp: ProductizationGateInputs) -> bool:
    return (
        inp.manual_step_repeated >= 3
        and inp.time_cost_hours_per_project >= 2.0
        and inp.linked_to_paid_offer
        and inp.reduces_risk_or_improves_margin
        and inp.testable
    )


def recommend_post_proof_decision(
    *,
    wants_continue_same_capability: bool,
    wants_adjacent_expansion: bool,
    value_proven: bool,
) -> PostProofDecision:
    """Lightweight triage — real engagements need human judgment."""
    if not value_proven:
        return PostProofDecision.PAUSE
    if wants_adjacent_expansion:
        return PostProofDecision.EXPAND
    if wants_continue_same_capability:
        return PostProofDecision.CONTINUE
    return PostProofDecision.PAUSE
