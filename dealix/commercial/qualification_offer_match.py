"""Evidence-gated qualification and canonical offer matching.

Persistence-neutral by design: this module does not create another CRM or
Opportunity Graph. Callers persist the returned state in the canonical Company
Machine. No state promotion is allowed by score or model inference alone.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_commercial_factory import SectorCommercialFactory


class QualificationState(StrEnum):
    RESEARCH_ONLY = "RESEARCH_ONLY"
    SIGNAL = "SIGNAL"
    REAL_INTERACTION = "REAL_INTERACTION"
    QUALIFIED_PROBLEM = "QUALIFIED_PROBLEM"
    DISCOVERY_READY = "DISCOVERY_READY"
    PROPOSAL_READY = "PROPOSAL_READY"
    DECISION_PENDING = "DECISION_PENDING"
    WON = "WON"
    LOST = "LOST"
    NURTURE = "NURTURE"


class QualificationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_id: str
    sector: Sector
    buyer_role: str = "UNKNOWN"
    problem: str = "UNKNOWN"
    trigger: str = "UNKNOWN"

    market_signal_refs: list[str] = Field(default_factory=list)
    real_interaction_refs: list[str] = Field(default_factory=list)
    consent_refs: list[str] = Field(default_factory=list)
    problem_evidence_refs: list[str] = Field(default_factory=list)
    impact_evidence_refs: list[str] = Field(default_factory=list)
    urgency_evidence_refs: list[str] = Field(default_factory=list)
    authority_evidence_refs: list[str] = Field(default_factory=list)
    budget_signal_refs: list[str] = Field(default_factory=list)
    delivery_fit_refs: list[str] = Field(default_factory=list)
    timing_refs: list[str] = Field(default_factory=list)
    risk_refs: list[str] = Field(default_factory=list)

    discovery_requested: bool = False
    discovery_completed: bool = False
    explicit_customer_proposal_request: bool = False
    customer_decision_pending: bool = False
    verified_won_refs: list[str] = Field(default_factory=list)
    verified_lost_refs: list[str] = Field(default_factory=list)
    nurture_reason: str = ""


class QualificationDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    entity_id: str
    state: QualificationState
    gate_reasons: list[str]
    evidence_refs: list[str]
    assessed: dict[str, bool]
    proposal_allowed: bool
    proposal_basis: str
    research_counts_as_relationship: bool = False
    public_contact_counts_as_consent: bool = False


class OfferMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    offer: str
    basis: list[str]
    truth_class: str = "RECOMMENDED"
    requires_customer_specific_scope: bool = True


def _present(values: list[str]) -> bool:
    return bool([value for value in values if value.strip()])


def qualify(inp: QualificationInput) -> QualificationDecision:
    assessed = {
        "REAL_INTERACTION": _present(inp.real_interaction_refs),
        "CONSENT": _present(inp.consent_refs),
        "PROBLEM": _present(inp.problem_evidence_refs) and inp.problem != "UNKNOWN",
        "IMPACT": _present(inp.impact_evidence_refs),
        "URGENCY": _present(inp.urgency_evidence_refs),
        "AUTHORITY": _present(inp.authority_evidence_refs),
        "BUDGET_SIGNAL": _present(inp.budget_signal_refs),
        "DELIVERY_FIT": _present(inp.delivery_fit_refs),
        "OFFER_FIT": False,
        "TIMING": _present(inp.timing_refs),
        "RISK": _present(inp.risk_refs),
        "EVIDENCE": any(
            (
                inp.market_signal_refs,
                inp.real_interaction_refs,
                inp.problem_evidence_refs,
                inp.impact_evidence_refs,
            )
        ),
    }

    state = QualificationState.RESEARCH_ONLY
    reasons: list[str] = []
    if _present(inp.market_signal_refs):
        state = QualificationState.SIGNAL
    if assessed["REAL_INTERACTION"]:
        state = QualificationState.REAL_INTERACTION

    qualified_problem = (
        assessed["REAL_INTERACTION"]
        and assessed["PROBLEM"]
        and assessed["IMPACT"]
        and assessed["DELIVERY_FIT"]
    )
    if qualified_problem:
        state = QualificationState.QUALIFIED_PROBLEM
    else:
        for key in ("REAL_INTERACTION", "PROBLEM", "IMPACT", "DELIVERY_FIT"):
            if not assessed[key]:
                reasons.append(f"missing_{key.lower()}_evidence")

    if qualified_problem and inp.discovery_requested:
        state = QualificationState.DISCOVERY_READY
    if qualified_problem and (inp.discovery_completed or inp.explicit_customer_proposal_request):
        state = QualificationState.PROPOSAL_READY
    if state == QualificationState.PROPOSAL_READY and inp.customer_decision_pending:
        state = QualificationState.DECISION_PENDING

    if _present(inp.verified_won_refs):
        if state not in {QualificationState.PROPOSAL_READY, QualificationState.DECISION_PENDING}:
            raise ValueError("WON cannot skip qualification/proposal evidence")
        state = QualificationState.WON
    if _present(inp.verified_lost_refs):
        if not assessed["REAL_INTERACTION"]:
            raise ValueError("LOST requires a real interaction trail")
        state = QualificationState.LOST
    if inp.nurture_reason and state not in {QualificationState.WON, QualificationState.LOST}:
        state = QualificationState.NURTURE

    proposal_allowed = qualified_problem or inp.explicit_customer_proposal_request
    proposal_basis = (
        "QUALIFIED_PROBLEM"
        if qualified_problem
        else "EXPLICIT_CUSTOMER_REQUEST"
        if inp.explicit_customer_proposal_request
        else "BLOCKED"
    )

    refs: list[str] = []
    for values in (
        inp.market_signal_refs,
        inp.real_interaction_refs,
        inp.consent_refs,
        inp.problem_evidence_refs,
        inp.impact_evidence_refs,
        inp.urgency_evidence_refs,
        inp.authority_evidence_refs,
        inp.budget_signal_refs,
        inp.delivery_fit_refs,
        inp.timing_refs,
        inp.risk_refs,
        inp.verified_won_refs,
        inp.verified_lost_refs,
    ):
        refs.extend(values)

    return QualificationDecision(
        entity_id=inp.entity_id,
        state=state,
        gate_reasons=sorted(set(reasons)),
        evidence_refs=list(dict.fromkeys(refs)),
        assessed=assessed,
        proposal_allowed=proposal_allowed,
        proposal_basis=proposal_basis,
    )


def match_offers(inp: QualificationInput, decision: QualificationDecision) -> list[OfferMatch]:
    """Recommend only canonical sector offers; never manufacture qualification."""
    if decision.state in {QualificationState.RESEARCH_ONLY, QualificationState.SIGNAL}:
        return []
    if inp.problem == "UNKNOWN" or not _present(inp.problem_evidence_refs):
        return []

    pack = SectorCommercialFactory().build(inp.sector)
    matches: list[OfferMatch] = []
    for offer in pack.offer_matches:
        basis = [
            f"sector::{inp.sector.value}",
            f"buyer::{inp.buyer_role}",
            f"problem::{inp.problem}",
        ]
        if inp.trigger != "UNKNOWN":
            basis.append(f"trigger::{inp.trigger}")
        basis.extend(f"evidence::{ref}" for ref in inp.problem_evidence_refs[:2])
        matches.append(OfferMatch(offer=offer, basis=basis))
    return matches


def qualification_receipt(inp: QualificationInput) -> dict[str, Any]:
    decision = qualify(inp)
    offers = match_offers(inp, decision)
    assessed = dict(decision.assessed)
    assessed["OFFER_FIT"] = bool(offers)
    return {
        "entity_id": inp.entity_id,
        "state": decision.state.value,
        "assessed": assessed,
        "proposal_allowed": decision.proposal_allowed,
        "proposal_basis": decision.proposal_basis,
        "offer_matches": [offer.model_dump(mode="json") for offer in offers],
        "research_counts_as_relationship": False,
        "public_contact_counts_as_consent": False,
    }


__all__ = [
    "QualificationState",
    "QualificationInput",
    "QualificationDecision",
    "OfferMatch",
    "qualify",
    "match_offers",
    "qualification_receipt",
]
