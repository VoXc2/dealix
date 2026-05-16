"""Governed Revenue & AI Ops core contracts.

This module codifies the operating posture requested for Dealix:
- Positioning: Governed Revenue & AI Operations
- North star: Governed Value Decisions Created
- Chain: Signal -> Source -> Approval -> Action -> Evidence -> Decision -> Value -> Asset
- Strict state machine for commercial proof levels (L2 -> L7)
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


POSITIONING_EN = "Dealix — Governed Revenue & AI Operations"
POSITIONING_AR = "Dealix — تشغيل الإيراد والذكاء الاصطناعي بحوكمة وأدلة وقياس قيمة"

NORTH_STAR = {
    "metric_id": "governed_value_decisions_created",
    "name_en": "Governed Value Decisions Created",
    "name_ar": "القرارات القيمية المحكومة المُنشأة",
    "definition_en": (
        "Count of operational or revenue decisions that include clear source, "
        "explicit approval, documented evidence, and measurable value."
    ),
    "definition_ar": (
        "عدد القرارات التشغيلية أو الإيرادية التي تمت بمصدر واضح، "
        "وموافقة واضحة، ودليل موثق، وأثر قابل للقياس."
    ),
}


class OperatingChainStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step: str
    question_ar: str
    question_en: str


OPERATING_CHAIN: tuple[OperatingChainStep, ...] = (
    OperatingChainStep(
        step="signal",
        question_ar="ما الإشارة الحقيقية؟",
        question_en="What is the real signal?",
    ),
    OperatingChainStep(
        step="source",
        question_ar="ما مصدرها؟",
        question_en="What is the source?",
    ),
    OperatingChainStep(
        step="approval",
        question_ar="من وافق؟",
        question_en="Who approved?",
    ),
    OperatingChainStep(
        step="action",
        question_ar="ما الفعل؟",
        question_en="What action was taken?",
    ),
    OperatingChainStep(
        step="evidence",
        question_ar="ما الدليل؟",
        question_en="What is the evidence?",
    ),
    OperatingChainStep(
        step="decision",
        question_ar="ما القرار؟",
        question_en="What decision was made?",
    ),
    OperatingChainStep(
        step="value",
        question_ar="ما القيمة؟",
        question_en="What value was created?",
    ),
    OperatingChainStep(
        step="asset",
        question_ar="كيف يصبح أصلًا قابلًا لإعادة الاستخدام؟",
        question_en="How does it become a reusable asset?",
    ),
)


class ServiceOffer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_id: str
    name_ar: str
    name_en: str
    price_range_sar: str
    stage: Literal["diagnostic", "sprint", "retainer", "specialized", "executive"]
    featured_in_first_meeting: bool = False


SERVICE_LADDER: tuple[ServiceOffer, ...] = (
    ServiceOffer(
        service_id="governed_revenue_ops_diagnostic",
        name_ar="تشخيص تشغيل الإيراد والذكاء الاصطناعي المحكوم",
        name_en="Governed Revenue Ops Diagnostic",
        price_range_sar="4,999 - 25,000",
        stage="diagnostic",
        featured_in_first_meeting=True,
    ),
    ServiceOffer(
        service_id="revenue_intelligence_sprint",
        name_ar="سبرينت ذكاء الإيراد",
        name_en="Revenue Intelligence Sprint",
        price_range_sar="25,000+",
        stage="sprint",
        featured_in_first_meeting=True,
    ),
    ServiceOffer(
        service_id="governed_ops_retainer",
        name_ar="ريتينر تشغيل محكوم",
        name_en="Governed Ops Retainer",
        price_range_sar="4,999 - 35,000 / month",
        stage="retainer",
        featured_in_first_meeting=True,
    ),
    ServiceOffer(
        service_id="ai_governance_for_revenue_teams",
        name_ar="حوكمة الذكاء الاصطناعي لفرق الإيراد",
        name_en="AI Governance for Revenue Teams",
        price_range_sar="custom",
        stage="specialized",
    ),
    ServiceOffer(
        service_id="crm_data_readiness_for_ai",
        name_ar="جاهزية CRM والبيانات للذكاء الاصطناعي",
        name_en="CRM / Data Readiness for AI",
        price_range_sar="custom",
        stage="specialized",
    ),
    ServiceOffer(
        service_id="board_decision_memo",
        name_ar="مذكرة القرار لمجلس الإدارة",
        name_en="Board Decision Memo",
        price_range_sar="custom",
        stage="executive",
    ),
    ServiceOffer(
        service_id="trust_pack_lite",
        name_ar="حزمة الثقة المصغّرة",
        name_en="Trust Pack Lite",
        price_range_sar="on-demand",
        stage="specialized",
    ),
)


class ValueState(StrEnum):
    PREPARED_NOT_SENT = "prepared_not_sent"
    SENT = "sent"
    REPLIED_INTERESTED = "replied_interested"
    MEETING_BOOKED = "meeting_booked"
    USED_IN_MEETING = "used_in_meeting"
    SCOPE_REQUESTED = "scope_requested"
    PILOT_INTRO_REQUESTED = "pilot_intro_requested"
    INVOICE_SENT = "invoice_sent"
    INVOICE_PAID = "invoice_paid"


ValueLevel = Literal["L2", "L4", "L5", "L6", "L7_candidate", "L7_confirmed"]

LEVEL_BY_STATE: dict[ValueState, ValueLevel] = {
    ValueState.PREPARED_NOT_SENT: "L2",
    ValueState.SENT: "L4",
    ValueState.REPLIED_INTERESTED: "L4",
    ValueState.MEETING_BOOKED: "L4",
    ValueState.USED_IN_MEETING: "L5",
    ValueState.SCOPE_REQUESTED: "L6",
    ValueState.PILOT_INTRO_REQUESTED: "L6",
    ValueState.INVOICE_SENT: "L7_candidate",
    ValueState.INVOICE_PAID: "L7_confirmed",
}

ALLOWED_TRANSITIONS: dict[ValueState, set[ValueState]] = {
    ValueState.PREPARED_NOT_SENT: {ValueState.SENT},
    ValueState.SENT: {ValueState.REPLIED_INTERESTED, ValueState.MEETING_BOOKED},
    ValueState.REPLIED_INTERESTED: {ValueState.MEETING_BOOKED},
    ValueState.MEETING_BOOKED: {ValueState.USED_IN_MEETING},
    ValueState.USED_IN_MEETING: {
        ValueState.SCOPE_REQUESTED,
        ValueState.PILOT_INTRO_REQUESTED,
    },
    ValueState.SCOPE_REQUESTED: {ValueState.INVOICE_SENT},
    ValueState.PILOT_INTRO_REQUESTED: {ValueState.INVOICE_SENT},
    ValueState.INVOICE_SENT: {ValueState.INVOICE_PAID},
    ValueState.INVOICE_PAID: set(),
}

_FOUNDER_APPROVAL_REQUIRED_TO_ENTER: set[ValueState] = {
    ValueState.SENT,
    ValueState.INVOICE_SENT,
}


class GovernedValueAdvanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    current_state: ValueState
    target_state: ValueState
    founder_confirmed: bool = False
    payment_received: bool = False
    source_reference: str = Field(default="", max_length=200)
    approval_reference: str = Field(default="", max_length=200)
    evidence_reference: str = Field(default="", max_length=200)


class GovernedValueAdvanceResult(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    accepted: bool
    from_state: ValueState
    to_state: ValueState | None = None
    level: ValueLevel | None = None
    rejection_reason: str | None = None
    revenue_eligible: bool = False
    founder_approval_required: bool = False
    governed_value_decision_created: bool = False
    missing_chain_links: list[str] = Field(default_factory=list)


def list_state_machine() -> dict[str, object]:
    """Expose state machine as JSON-ready structure for API/UI use."""
    states = []
    for state in ValueState:
        states.append(
            {
                "state": state.value,
                "level": LEVEL_BY_STATE[state],
                "allowed_transitions": sorted(
                    target.value for target in ALLOWED_TRANSITIONS[state]
                ),
                "founder_approval_required_to_enter": (
                    state in _FOUNDER_APPROVAL_REQUIRED_TO_ENTER
                ),
                "revenue_eligible": state == ValueState.INVOICE_PAID,
            }
        )
    return {"states": states, "states_total": len(states)}


def _missing_chain_links(req: GovernedValueAdvanceRequest) -> list[str]:
    missing: list[str] = []
    if not req.source_reference.strip():
        missing.append("source")
    if not req.approval_reference.strip():
        missing.append("approval")
    if not req.evidence_reference.strip():
        missing.append("evidence")
    return missing


def advance_state(req: GovernedValueAdvanceRequest) -> GovernedValueAdvanceResult:
    source = ValueState(req.current_state)
    target = ValueState(req.target_state)
    allowed = ALLOWED_TRANSITIONS.get(source, set())

    if target not in allowed:
        return GovernedValueAdvanceResult(
            accepted=False,
            from_state=source,
            rejection_reason=(
                f"transition {source.value} -> {target.value} not allowed; "
                f"valid targets: {sorted(t.value for t in allowed) or '[terminal]'}"
            ),
            founder_approval_required=target in _FOUNDER_APPROVAL_REQUIRED_TO_ENTER,
        )

    if target in _FOUNDER_APPROVAL_REQUIRED_TO_ENTER and not req.founder_confirmed:
        return GovernedValueAdvanceResult(
            accepted=False,
            from_state=source,
            rejection_reason="founder_confirmed=true required before external action",
            founder_approval_required=True,
        )

    if target == ValueState.INVOICE_PAID and not req.payment_received:
        return GovernedValueAdvanceResult(
            accepted=False,
            from_state=source,
            rejection_reason="payment_received=true required for L7_confirmed",
            founder_approval_required=False,
        )

    missing_links = _missing_chain_links(req)
    return GovernedValueAdvanceResult(
        accepted=True,
        from_state=source,
        to_state=target,
        level=LEVEL_BY_STATE[target],
        revenue_eligible=target == ValueState.INVOICE_PAID,
        founder_approval_required=target in _FOUNDER_APPROVAL_REQUIRED_TO_ENTER,
        governed_value_decision_created=len(missing_links) == 0,
        missing_chain_links=missing_links,
    )
