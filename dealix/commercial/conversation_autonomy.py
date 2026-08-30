"""Route real commercial replies into existing Dealix sales/negotiation workloads.

No send happens here.  The module turns deterministic response classification
into a bounded internal work packet and optionally asks the existing negotiation
engine for an objection plan.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ConversationPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str
    route: str
    proposed_action: str
    stage: str
    suppress: bool
    external_effect_allowed: bool = False
    evidence_refs: list[str] = Field(default_factory=list)
    negotiation_support: dict[str, Any] = Field(default_factory=dict)
    next_evidence: list[str] = Field(default_factory=list)
    next_action: str
    approval_class: str


def _default_route_response(text: str) -> dict[str, Any]:
    from auto_client_acquisition.revenue_os.response_router import route_response

    return route_response(text)


def _default_negotiation_engine() -> Any:
    from intelligence.negotiation_engine import NegotiationEngine

    return NegotiationEngine()


def plan_conversation_turn(
    text: str,
    *,
    evidence_refs: list[str],
    route_result: dict[str, Any] | None = None,
    objection_category: str | None = None,
    negotiation_engine: Any | None = None,
) -> ConversationPlan:
    refs = [ref.strip() for ref in evidence_refs if ref.strip()]
    if not refs:
        raise ValueError("conversation planning requires evidence_refs")
    routed = dict(route_result or _default_route_response(text))
    category = str(routed.get("category", "UNKNOWN"))
    route = str(routed.get("route", "human_review"))
    suppress = bool(routed.get("suppress", False))

    mapping = {
        "POSITIVE": ("prepare_diagnostic", "INTERACTION", "Prepare diagnostic/discovery brief from evidenced reply."),
        "QUESTION": ("draft", "INTERACTION", "Prepare an evidence-backed answer draft and exact next evidence."),
        "OBJECTION": ("prepare_negotiation", "NEGOTIATION_PREP", "Prepare objection and negotiation plan; no commitment."),
        "REFERRAL": ("research", "INTERACTION", "Verify referral provenance and relationship evidence before promotion."),
        "WRONG_PERSON": ("research", "INTERACTION", "Research correct role; do not transfer consent or relationship."),
        "NOT_NOW": ("update_internal_queue", "INTERACTION", "Record agreed timing evidence and bounded future action."),
        "NO": ("internal_review", "SUPPRESSED", "Close respectfully and suppress further marketing candidates."),
        "UNSUBSCRIBE": ("internal_review", "SUPPRESSED", "Suppress immediately; only mandatory acknowledgement may be considered by channel policy."),
        "BOUNCE": ("internal_review", "ENDPOINT_INVALID", "Invalidate endpoint and stop retries."),
        "AUTO_REPLY": ("update_internal_queue", "INTERACTION", "Do not count as engagement; retain thread state."),
        "UNKNOWN": ("internal_review", "INTERACTION", "Human/governance review of ambiguous reply."),
    }
    action, stage, next_action = mapping.get(category, mapping["UNKNOWN"])

    negotiation: dict[str, Any] = {}
    if category == "OBJECTION" and objection_category:
        engine = negotiation_engine or _default_negotiation_engine()
        negotiation = engine.handle_objection(objection_category, context={"source_refs": refs}, lang="both")

    if suppress:
        approval_class = "SUPPRESSION_ENFORCEMENT"
    elif category in {"QUESTION", "OBJECTION", "POSITIVE"}:
        approval_class = "EXACT_EXTERNAL_ACTION_PACKET_BEFORE_ANY_SEND"
    else:
        approval_class = "INTERNAL_ONLY_UNTIL_ELIGIBLE"

    return ConversationPlan(
        category=category,
        route=route,
        proposed_action=action,
        stage=stage,
        suppress=suppress,
        evidence_refs=refs,
        negotiation_support=negotiation,
        next_evidence=["SOURCE_BOUND_NEXT_CUSTOMER_OR_CHANNEL_EVIDENCE"],
        next_action=next_action,
        approval_class=approval_class,
    )


__all__ = ["ConversationPlan", "plan_conversation_turn"]
