"""Client maturity engine — ladder level, offers, and guardrails."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.client_maturity_os.maturity_score import (
    MATURITY_LADDER_STATES,
    ClientMaturityDimensions,
    client_maturity_band,
    client_maturity_score,
)
from auto_client_acquisition.client_maturity_os.offer_matrix import (
    blocked_offers_for_level,
    level7_entry_gates_met,
    primary_offer_for_level,
    retainer_eligibility_met,
)


@dataclass(frozen=True, slots=True)
class ClientMaturityInputs:
    dimensions: ClientMaturityDimensions
    proof_score: int
    adoption_score: int
    workflow_count: int
    workflow_owner_exists: bool
    monthly_cadence_active: bool
    governance_risk_controlled: bool
    shadow_ai_uncontrolled: bool
    has_executive_sponsor: bool
    has_governance_owner: bool
    requires_audit: bool
    clear_budget: bool


@dataclass(frozen=True, slots=True)
class MaturityEngineResult:
    client_id: str
    maturity_level: int
    current_state: str
    maturity_score: int
    maturity_band: str
    recommended_next_offer: str
    blocked_offers: tuple[str, ...]
    reason: str


def _infer_maturity_level(score: int, inp: ClientMaturityInputs, d: ClientMaturityDimensions) -> int:
    if inp.shadow_ai_uncontrolled and d.governance_coverage < 50:
        return 0 if score < 50 else 1
    if score < 35:
        return 0
    if score < 48:
        return 1
    if score < 58:
        return 2
    if score < 68:
        return 3
    if score < 78:
        if d.governance_coverage >= 70 and inp.proof_score >= 70:
            return 4
        return 3
    if score < 86:
        if inp.monthly_cadence_active and inp.adoption_score >= 60:
            return 5
        return 4
    if score < 93:
        if inp.workflow_count >= 2:
            return 6
        return 5
    if level7_entry_gates_met(
        workflow_count=inp.workflow_count,
        has_executive_sponsor=inp.has_executive_sponsor,
        has_governance_owner=inp.has_governance_owner,
        requires_audit=inp.requires_audit,
        monthly_cadence_active=inp.monthly_cadence_active,
        clear_budget=inp.clear_budget,
    ):
        return 7
    return 6


def _reason_for_level(level: int, inp: ClientMaturityInputs, d: ClientMaturityDimensions) -> str:
    if inp.shadow_ai_uncontrolled and d.governance_coverage < 50:
        return "Shadow AI signals with incomplete governance coverage; stabilize policy and inventory first."
    if level <= 1:
        return "Early maturity: prioritize diagnostics, use-case clarity, and governance boundaries."
    if level <= 3:
        return "Workflow exists but governance, audit coverage, or proof cadence still incomplete."
    if level == 4:
        return "Governed workflow in place; scale with monthly operating cadence and proof discipline."
    if level == 5:
        return "Operating capability emerging; deepen workspace usage and value reporting."
    if level == 6:
        return "Multi-workflow signals; prepare enterprise operating program and cross-functional proof."
    return "Enterprise control plane only when audit, sponsors, owners, cadence, and budget gates are met."


def maturity_engine_result(client_id: str, inp: ClientMaturityInputs) -> MaturityEngineResult:
    d = inp.dimensions
    score = client_maturity_score(d)
    band = client_maturity_band(score)
    level = _infer_maturity_level(score, inp, d)
    state = MATURITY_LADDER_STATES[level]
    offer = primary_offer_for_level(level)

    blocked = set(blocked_offers_for_level(level))
    if not retainer_eligibility_met(
        proof_score=inp.proof_score,
        adoption_score=inp.adoption_score,
        workflow_owner_exists=inp.workflow_owner_exists,
        monthly_cadence_active=inp.monthly_cadence_active,
        governance_risk_controlled=inp.governance_risk_controlled,
    ):
        blocked.add("Monthly Retainer")
    if not level7_entry_gates_met(
        workflow_count=inp.workflow_count,
        has_executive_sponsor=inp.has_executive_sponsor,
        has_governance_owner=inp.has_governance_owner,
        requires_audit=inp.requires_audit,
        monthly_cadence_active=inp.monthly_cadence_active,
        clear_budget=inp.clear_budget,
    ):
        blocked.add("AI Control Plane")

    return MaturityEngineResult(
        client_id=client_id,
        maturity_level=level,
        current_state=state,
        maturity_score=score,
        maturity_band=band,
        recommended_next_offer=offer,
        blocked_offers=tuple(sorted(blocked)),
        reason=_reason_for_level(level, inp, d),
    )
