"""Pydantic models for Revenue Ops Autopilot (local JSON persistence)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

WarRoomOutreachStatus = Literal[
    "not_contacted",
    "message_drafted",
    "approved_to_send",
    "sent_manual",
    "replied",
    "proof_pack_sent",
    "meeting_booked",
    "scope_requested",
    "invoice_sent",
    "paid",
    "delivery_started",
    "proof_pack_delivered",
    "upsell_candidate",
    "referral_requested",
    "closed_lost",
]

LeadStage = Literal[
    "new_lead",
    "qualified_A",
    "qualified_B",
    "nurture",
    "partner_candidate",
    "meeting_booked",
    "meeting_done",
    "scope_requested",
    "scope_sent",
    "invoice_sent",
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "sprint_candidate",
    "retainer_candidate",
    "closed_lost",
]

TicketStatus = Literal["new", "open", "waiting_founder", "resolved", "escalated"]

ApprovalNeed = Literal["none", "founder_review", "blocked_escalation"]


class FunnelLeadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    role: str = ""
    industry: str = ""
    country: str = ""
    source: str = "dealix_diagnostic"
    pain: str = ""
    crm_status: str = ""
    hubspot_contact_id: str = ""
    hubspot_deal_id: str = ""
    ai_usage: str = ""
    budget_range: str = ""
    urgency: str = ""
    consent_marketing: bool = False
    consent_proof_pack: bool = False
    lead_score: int = 0
    score_breakdown: dict[str, int] = Field(default_factory=dict)
    stage: LeadStage = "new_lead"
    war_room_status: WarRoomOutreachStatus = "not_contacted"
    segment: str = ""
    pain_hypothesis: str = ""
    offer_id: str = ""
    proof_asset: str = ""
    next_action: str = ""
    next_action_due: str | None = None
    next_action_hint_ar: str = ""
    outreach_draft_snippet_ar: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class OpportunityRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    lead_id: str | None = None
    account_id: str | None = None
    offer_id: str = "seven_day_diagnostic"
    stage: LeadStage = "qualified_B"
    amount_sar: float | None = None
    probability: float | None = None
    expected_close_date: str | None = None
    next_action: str | None = None
    evidence_level: str = "L1"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SupportTicketRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    account_id: str | None = None
    contact_id: str | None = None
    email: str | None = None
    channel: str = "web_form"
    subject: str | None = None
    message: str
    intent: str = "unknown"
    priority: str = "p3"
    risk_level: str = "low"
    status: TicketStatus = "new"
    assigned_to: str = "founder"
    ai_summary_ar: str = ""
    suggested_response_ar: str = ""
    kb_source_ids: list[str] = Field(default_factory=list)
    approval_need: ApprovalNeed = "founder_review"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EvidenceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    event_type: str
    entity_type: str = ""
    entity_id: str = ""
    account_id: str | None = None
    contact_id: str | None = None
    source: str = "revenue_autopilot"
    summary: str = ""
    linked_asset: str | None = None
    confidence: str = "high"
    approval_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DiagnosticDeliveryRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    lead_id: str | None = None
    stage: Literal[
        "intake",
        "onboarding",
        "delivery",
        "proof_pack_draft",
        "complete",
    ] = "intake"
    onboarding_checklist: list[str] = Field(default_factory=list)
    proof_pack_outline_ar: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class InvoiceDraftRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    lead_id: str | None = None
    opportunity_id: str | None = None
    tier: Literal["starter", "standard", "executive"] = "starter"
    amount_sar: float
    line_items_ar: list[str] = Field(default_factory=list)
    status: Literal["draft", "approval_required", "sent", "paid"] = "approval_required"
    governance_note_ar: str = (
        "لا يتم إرسال الفاتورة تلقائياً؛ يحتاج موافقة المؤسس وفق سياسة Dealix."
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
