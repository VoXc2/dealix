"""Evidence-first contracts for the internal Dealix Revenue Lab.

The Revenue Lab is an internal decision-support layer.  It never scrapes,
sends, changes production, approves a commercial commitment, or treats a
hypothesis as a verified customer fact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class EvidenceReference:
    """A traceable source used to support a company signal."""

    source_ref: str
    source_type: str
    observed_at: str
    title: str = ""
    excerpt: str = ""
    quality: str = "public"  # primary | official | public | internal | demo

    def __post_init__(self) -> None:
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")
        if not self.source_type.strip():
            raise ValueError("source_type is required")
        if not self.observed_at.strip():
            raise ValueError("observed_at is required")
        if self.quality not in {"primary", "official", "public", "internal", "demo"}:
            raise ValueError("unsupported evidence quality")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> EvidenceReference:
        return cls(
            source_ref=str(payload.get("source_ref") or ""),
            source_type=str(payload.get("source_type") or ""),
            observed_at=str(payload.get("observed_at") or ""),
            title=str(payload.get("title") or ""),
            excerpt=str(payload.get("excerpt") or ""),
            quality=str(payload.get("quality") or "public"),
        )


@dataclass(frozen=True)
class CompanySignal:
    """One tenant-scoped account hypothesis and the evidence behind it."""

    tenant_id: str
    account_id: str
    company_name: str
    sector: str
    company_size: str
    department: str
    relationship: str
    permission: str
    decision_maker_role: str
    offer_match: str
    why_now: str
    value_exchange: str
    pain_hypotheses: tuple[str, ...]
    unknowns: tuple[str, ...]
    evidence: tuple[EvidenceReference, ...]
    strategic_fit: int
    urgency: int
    known_metrics: dict[str, float] = field(default_factory=dict)
    demo: bool = False

    def __post_init__(self) -> None:
        required = (
            "tenant_id",
            "account_id",
            "company_name",
            "sector",
            "company_size",
            "department",
            "relationship",
            "permission",
            "decision_maker_role",
            "offer_match",
            "why_now",
            "value_exchange",
        )
        for name in required:
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} is required")
        for name in ("strategic_fit", "urgency"):
            if not 0 <= int(getattr(self, name)) <= 100:
                raise ValueError(f"{name} must be between 0 and 100")
        if not self.pain_hypotheses:
            raise ValueError("at least one pain hypothesis is required")
        if any(value < 0 for value in self.known_metrics.values()):
            raise ValueError("known_metrics values must be non-negative")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> CompanySignal:
        metrics = payload.get("known_metrics") or {}
        if not isinstance(metrics, dict):
            raise ValueError("known_metrics must be an object")
        return cls(
            tenant_id=str(payload.get("tenant_id") or ""),
            account_id=str(payload.get("account_id") or ""),
            company_name=str(payload.get("company_name") or ""),
            sector=str(payload.get("sector") or ""),
            company_size=str(payload.get("company_size") or ""),
            department=str(payload.get("department") or ""),
            relationship=str(payload.get("relationship") or ""),
            permission=str(payload.get("permission") or ""),
            decision_maker_role=str(payload.get("decision_maker_role") or ""),
            offer_match=str(payload.get("offer_match") or ""),
            why_now=str(payload.get("why_now") or ""),
            value_exchange=str(payload.get("value_exchange") or ""),
            pain_hypotheses=tuple(str(item) for item in payload.get("pain_hypotheses") or ()),
            unknowns=tuple(str(item) for item in payload.get("unknowns") or ()),
            evidence=tuple(
                EvidenceReference.from_dict(item) for item in payload.get("evidence") or ()
            ),
            strategic_fit=int(payload.get("strategic_fit") or 0),
            urgency=int(payload.get("urgency") or 0),
            known_metrics={str(key): float(value) for key, value in metrics.items()},
            demo=bool(payload.get("demo", False)),
        )


@dataclass(frozen=True)
class OutcomeEvent:
    """A real or explicitly demo commercial outcome used for learning.

    A source-linked outcome is not customer proof by itself. Customer proof
    requires explicit customer validation and a delivery-proof reference.
    """

    account_id: str
    outcome: str
    source_ref: str
    observed_at: str
    notes: str = ""
    demo: bool = False
    customer_validated: bool = False
    customer_validation_ref: str = ""
    delivery_proof_ref: str = ""
    payment_proof_ref: str = ""

    def __post_init__(self) -> None:
        if not self.account_id.strip() or not self.outcome.strip():
            raise ValueError("account_id and outcome are required")
        if not self.observed_at.strip():
            raise ValueError("observed_at is required")
        if not self.source_ref.strip() and not self.demo:
            raise ValueError("real outcomes require source_ref")
        if self.customer_validated and not self.customer_validation_ref.strip():
            raise ValueError("customer validation requires customer_validation_ref")
        if any(
            ref.strip()
            for ref in (self.delivery_proof_ref, self.payment_proof_ref)
        ) and not self.source_ref.strip():
            raise ValueError("proof references require source_ref")

    def is_customer_proof(self) -> bool:
        return (
            not self.demo
            and bool(self.source_ref.strip())
            and self.customer_validated
            and bool(self.customer_validation_ref.strip())
            and bool(self.delivery_proof_ref.strip())
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> OutcomeEvent:
        return cls(
            account_id=str(payload.get("account_id") or ""),
            outcome=str(payload.get("outcome") or ""),
            source_ref=str(payload.get("source_ref") or ""),
            observed_at=str(payload.get("observed_at") or ""),
            notes=str(payload.get("notes") or ""),
            demo=bool(payload.get("demo", False)),
            customer_validated=bool(payload.get("customer_validated", False)),
            customer_validation_ref=str(payload.get("customer_validation_ref") or ""),
            delivery_proof_ref=str(payload.get("delivery_proof_ref") or ""),
            payment_proof_ref=str(payload.get("payment_proof_ref") or ""),
        )


@dataclass(frozen=True)
class OpportunityNode:
    account_id: str
    company_name: str
    sector: str
    company_size: str
    decision_maker_role: str
    pain_hypotheses: tuple[str, ...]
    unknowns: tuple[str, ...]
    offer_match: str
    why_now: str
    priority_score: int
    evidence_status: str
    evidence_refs: tuple[str, ...]
    prediction_status: str = "not_calibrated"
    conversion_probability: float | None = None
    stage: str = "research"
    next_action: str = "validate_hypotheses"


@dataclass(frozen=True)
class SalesStrategy:
    account_id: str
    objective: str
    positioning: str
    expected_objections: tuple[str, ...]
    response_principles: tuple[str, ...]
    negotiation_give_get: tuple[str, ...]
    negotiation_missing_inputs: tuple[str, ...]
    forbidden_commitments: tuple[str, ...]
    approval_required: bool = True


@dataclass(frozen=True)
class ProposalDraft:
    account_id: str
    offer: str
    problem_statement: str
    scope: tuple[str, ...]
    timeline_days: int
    success_metrics: tuple[str, ...]
    roi: dict[str, Any]
    assumptions: tuple[str, ...]
    approval_status: str = "approval_required"
    external_action_allowed: bool = False


@dataclass(frozen=True)
class DeliveryPlan:
    account_id: str
    timeline_days: int
    phases: tuple[dict[str, Any], ...]
    proof_requirements: tuple[str, ...]
    upsell_gate: str
    approval_status: str = "approval_required"


@dataclass(frozen=True)
class LearningRecommendation:
    account_id: str
    outcome: str
    recommendation: str
    evidence_ref: str
    experiment_required: bool = True
    weight_change_applied: bool = False
    approval_status: str = "approval_required"


@dataclass(frozen=True)
class RevenueLabBundle:
    run_id: str
    generated_at: str
    mode: str
    opportunities: tuple[OpportunityNode, ...]
    strategies: tuple[SalesStrategy, ...]
    proposals: tuple[ProposalDraft, ...]
    delivery_plans: tuple[DeliveryPlan, ...]
    approval_requests: tuple[dict[str, Any], ...]
    proof_events: tuple[dict[str, Any], ...]
    learning_recommendations: tuple[LearningRecommendation, ...]
    blockers: tuple[str, ...]
    summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


__all__ = [
    "CompanySignal",
    "DeliveryPlan",
    "EvidenceReference",
    "LearningRecommendation",
    "OpportunityNode",
    "OutcomeEvent",
    "ProposalDraft",
    "RevenueLabBundle",
    "SalesStrategy",
]
