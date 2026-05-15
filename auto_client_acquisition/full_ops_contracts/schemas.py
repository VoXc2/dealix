"""Canonical Full-Ops 10-Layer contracts (Pydantic v2, extra='forbid').

Each schema is the cross-layer envelope; the layer-specific records
(ApprovalRequest, ProofEvent, Ticket, etc.) are referenced by id —
they live in their original modules and continue to work as-is.

Hard rules baked into every external-facing schema:
  customer_handle  — required
  action_mode      — draft_only | approval_required | approved_execute | blocked
  safety_summary   — short statement of which gates were checked
"""
from __future__ import annotations

import re
from datetime import UTC, datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ── Action mode (used everywhere external) ────────────────────
ActionMode = Literal[
    "draft_only",
    "approval_required",
    "approved_execute",
    "blocked",
]


# ── 1. CustomerHandle ─────────────────────────────────────────
_HANDLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class CustomerHandle(BaseModel):
    """Anonymized customer identifier — never a real name/email/phone."""

    model_config = ConfigDict(extra="forbid")

    handle: str = Field(min_length=1, max_length=64)

    @field_validator("handle")
    @classmethod
    def _shape(cls, v: str) -> str:
        if not _HANDLE_RE.match(v):
            raise ValueError(
                "handle must be alphanumeric + hyphen/underscore, ≤64 chars"
            )
        return v


def _now_utc() -> datetime:
    return datetime.now(UTC)


# ── 2. LeadOpsRecord ──────────────────────────────────────────
class LeadOpsRecord(BaseModel):
    """Envelope for one lead's full pipeline state.

    The detailed normalize/dedupe/enrich/score outputs live in
    `auto_client_acquisition.pipelines.*` modules — this record
    just stitches their ids together for the spine.
    """

    model_config = ConfigDict(extra="forbid")

    leadops_id: str
    customer_handle: str | None = None  # null until a customer is created
    source: Literal[
        "whatsapp", "form", "csv", "warm_intro",
        "google_places", "referral", "api", "manual",
    ]
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    normalized: dict[str, Any] = Field(default_factory=dict)
    dedup_key: str | None = None
    compliance_status: Literal["allowed", "blocked", "needs_review"] = "needs_review"
    enrichment: dict[str, Any] = Field(default_factory=dict)
    score: dict[str, Any] = Field(default_factory=dict)  # fit/urgency/risk
    brief: dict[str, Any] | None = None
    offer_route: dict[str, Any] | None = None  # channel + medium
    next_action: dict[str, Any] | None = None
    draft_id: str | None = None  # ApprovalRequest.approval_id
    approval_id: str | None = None
    safety_summary: str = "approval_required_for_external_actions"
    created_at: datetime = Field(default_factory=_now_utc)


# ── 3. CustomerBrainSnapshot ──────────────────────────────────
class CustomerBrainSnapshot(BaseModel):
    """Per-customer operational memory — composed from existing
    crm_v10, customer_loop, proof_ledger, support_os, market_intelligence.
    """

    model_config = ConfigDict(extra="forbid")

    customer_handle: str
    profile: dict[str, Any] = Field(default_factory=dict)  # name, sector, region, tier
    icp: dict[str, Any] = Field(default_factory=dict)
    offers: list[dict[str, Any]] = Field(default_factory=list)
    channels: list[str] = Field(default_factory=list)  # whatsapp, email, dashboard
    tone_of_voice: dict[str, Any] = Field(default_factory=dict)
    compliance_constraints: list[str] = Field(default_factory=list)
    service_history: list[dict[str, Any]] = Field(default_factory=list)
    proof_history: list[dict[str, Any]] = Field(default_factory=list)
    open_decisions: list[dict[str, Any]] = Field(default_factory=list)
    support_context: dict[str, Any] = Field(default_factory=dict)
    growth_opportunities: list[dict[str, Any]] = Field(default_factory=list)
    source_modules: list[str] = Field(default_factory=list)  # which modules sourced this
    safety_summary: str = "no_pii_in_snapshot"
    built_at: datetime = Field(default_factory=_now_utc)


# ── 4. ServiceSessionRecord ───────────────────────────────────
ServiceType = Literal[
    "diagnostic",
    "leadops_sprint",
    "growth_proof_sprint",
    "support_ops_setup",
    "customer_portal_setup",
    "executive_pack",
    "proof_pack",
    "agency_partner_pack",
    # Commercial engagement sprints (catalog-linked delivery)
    "lead_intelligence_sprint",
    "support_desk_sprint",
    "quick_win_ops",
]
SessionStatus = Literal[
    "draft",
    "waiting_for_approval",
    "active",
    "delivered",
    "proof_pending",
    "complete",
    "blocked",
]


class ServiceSessionRecord(BaseModel):
    """Envelope for one delivered service to one customer.

    Wave 13 Phase 3 additions (all optional, backward-compatible):
      - service_offering_id  → links to service_catalog.registry
      - daily_artifacts       → {day_number, artifact_id, status,
                                  created_at, customer_visible}
      - next_customer_action  → bilingual single-sentence next step (customer-facing)
      - next_founder_action   → bilingual single-sentence next step (founder-facing)
      - day_number            → current day in service (1-indexed)
    """

    model_config = ConfigDict(extra="forbid")

    session_id: str
    customer_handle: str
    service_type: ServiceType
    status: SessionStatus = "draft"
    inputs: dict[str, Any] = Field(default_factory=dict)
    deliverables: list[dict[str, Any]] = Field(default_factory=list)
    approval_ids: list[str] = Field(default_factory=list)
    proof_event_ids: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    invoice_intent_id: str | None = None
    next_step: dict[str, Any] | None = None
    started_at: datetime = Field(default_factory=_now_utc)
    completed_at: datetime | None = None
    safety_summary: str = "no_live_send_no_live_charge"
    # Wave 13 Phase 3 — Service Session Runtime
    service_offering_id: str | None = None
    daily_artifacts: list[dict[str, Any]] = Field(default_factory=list)
    next_customer_action: dict[str, Any] | None = None  # {ar, en}
    next_founder_action: dict[str, Any] | None = None   # {ar, en}
    day_number: int = 0  # 0=not started, 1+=running


# Allowed transitions for ServiceSessionRecord.status
SESSION_TRANSITIONS: dict[SessionStatus, set[SessionStatus]] = {
    "draft": {"waiting_for_approval", "blocked"},
    "waiting_for_approval": {"active", "blocked"},
    "active": {"delivered", "blocked"},
    "delivered": {"proof_pending", "blocked"},
    "proof_pending": {"complete", "blocked"},
    "complete": set(),
    "blocked": set(),
}


# ── 5. ApprovalRequestEnriched ────────────────────────────────
class ApprovalRequestEnriched(BaseModel):
    """Wraps the existing approval_center.ApprovalRequest with cross-layer
    fields (policy_findings + bulk_group_id + customer_handle).

    The actual ApprovalRequest still lives in
    `auto_client_acquisition.approval_center.schemas.ApprovalRequest`.
    """

    model_config = ConfigDict(extra="forbid")

    approval_id: str
    customer_handle: str | None = None
    policy_findings: list[str] = Field(default_factory=list)
    expires_at: datetime | None = None
    bulk_group_id: str | None = None
    safety_summary: str = "approval_required"


# ── 6. PaymentStateRecord ─────────────────────────────────────
PaymentMethod = Literal[
    "moyasar_test",
    "moyasar_live",
    "bank_transfer",
    "cash_in_person",
    "manual_other",
]
PaymentStatus = Literal[
    "invoice_intent",
    "invoice_sent_manual",
    "payment_pending",
    "payment_evidence_uploaded",
    "payment_confirmed",
    "delivery_kickoff",
    "refunded",
    "voided",
]


class PaymentStateRecord(BaseModel):
    """Payment state for one customer × one service session.

    Hard rule (Article 8 / NO_FAKE_REVENUE):
      invoice_intent          ≠ revenue
      invoice_sent_manual     ≠ revenue
      payment_evidence_uploaded → possible revenue
      payment_confirmed       = revenue
    """

    model_config = ConfigDict(extra="forbid")

    payment_id: str
    customer_handle: str
    service_session_id: str | None = None
    invoice_intent_id: str | None = None
    amount_sar: float = Field(ge=0, le=1_000_000)
    method: PaymentMethod
    status: PaymentStatus = "invoice_intent"
    evidence_reference: str | None = None  # required when status >= payment_evidence_uploaded
    confirmed_by: str | None = None
    confirmed_at: datetime | None = None
    delivery_kickoff_id: str | None = None
    safety_summary: str = "no_live_charge_no_fake_revenue"
    created_at: datetime = Field(default_factory=_now_utc)


# ── 7. SupportTicketEnriched ──────────────────────────────────
SupportPriority = Literal["p0", "p1", "p2", "p3"]
SupportStatus = Literal["open", "in_progress", "waiting_customer", "resolved", "closed"]


class SupportTicketEnriched(BaseModel):
    """Cross-layer envelope around support_os.Ticket."""

    model_config = ConfigDict(extra="forbid")

    ticket_id: str
    customer_handle: str
    conversation_id: str | None = None
    category: str  # one of 12 from support_os.classifier
    priority: SupportPriority
    status: SupportStatus = "open"
    sla_due_at: datetime | None = None
    sla_breached: bool = False
    escalation_chain: list[str] = Field(default_factory=list)
    draft_reply_id: str | None = None  # ApprovalRequest awaiting approval
    proof_event_ids: list[str] = Field(default_factory=list)
    safety_summary: str = "no_live_send_redacted"
    created_at: datetime = Field(default_factory=_now_utc)


# ── 8. ProofEventEnriched ─────────────────────────────────────
EvidenceLevel = Literal["observed", "customer_confirmed", "payment_confirmed"]


class ProofEventEnriched(BaseModel):
    """Cross-layer envelope around proof_ledger.ProofEvent.

    Adds the file-attachment uri + consent signature pointer + pack id.
    """

    model_config = ConfigDict(extra="forbid")

    proof_event_id: str
    customer_handle: str
    service_session_id: str | None = None
    event_type: str  # one of ProofEventType from proof_ledger
    summary_ar: str = ""
    summary_en: str = ""
    evidence_level: EvidenceLevel = "observed"
    evidence_attachment_uri: str | None = None  # file://data/proof_attachments/...
    metric_snapshot_id: str | None = None
    consent_signature_id: str | None = None
    pack_id: str | None = None  # if assembled into a proof pack
    pii_redacted: bool = True
    consent_for_publication: bool = False
    approval_status: Literal["pending", "approved", "rejected"] = "pending"
    safety_summary: str = "pii_redacted_internal_only_default"
    created_at: datetime = Field(default_factory=_now_utc)


# ── 9. ExecutivePackRecord ────────────────────────────────────
class ExecutivePackRecord(BaseModel):
    """Daily / weekly / monthly executive pack for one customer.

    Composed from layers 1-8 + market_intelligence.
    """

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    customer_handle: str
    cadence: Literal["daily", "weekly", "monthly"]
    week_label: str | None = None
    executive_summary_ar: str = ""
    executive_summary_en: str = ""
    revenue_movement: dict[str, Any] = Field(default_factory=dict)
    leads: dict[str, Any] = Field(default_factory=dict)
    support: dict[str, Any] = Field(default_factory=dict)
    blockers: list[dict[str, Any]] = Field(default_factory=list)
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    proof_events: list[dict[str, Any]] = Field(default_factory=list)
    risks: list[dict[str, Any]] = Field(default_factory=list)
    next_3_actions: list[dict[str, Any]] = Field(default_factory=list)
    sector_context: dict[str, Any] = Field(default_factory=dict)
    appendix: dict[str, Any] = Field(default_factory=dict)
    safety_summary: str = "no_fake_revenue_no_fake_forecast"
    built_at: datetime = Field(default_factory=_now_utc)


# ── 10. CustomerPortalView ────────────────────────────────────
class CustomerPortalView(BaseModel):
    """The customer-facing portal aggregate.

    Mirrors what `api/routers/customer_company_portal.py` returns,
    so consumers (the dashboard JS, founder previews) have a typed
    handle on it.
    """

    model_config = ConfigDict(extra="forbid")

    customer_handle: str
    company_name: str | None = None
    state: Literal["demo", "signed_up", "active"] = "demo"
    plan: dict[str, Any] = Field(default_factory=dict)
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    decisions_pending: list[dict[str, Any]] = Field(default_factory=list)
    drafts_waiting: list[dict[str, Any]] = Field(default_factory=list)
    support_tickets: list[dict[str, Any]] = Field(default_factory=list)
    deliverables: list[dict[str, Any]] = Field(default_factory=list)
    proof_pack: dict[str, Any] = Field(default_factory=dict)
    executive_pack: dict[str, Any] = Field(default_factory=dict)
    billing_state: dict[str, Any] = Field(default_factory=dict)
    next_action: dict[str, Any] | None = None
    safety_summary: str = "no_internal_terms_8_section_invariant"
    rendered_at: datetime = Field(default_factory=_now_utc)


# ── 11. CaseStudyCandidate ────────────────────────────────────
class CaseStudyCandidate(BaseModel):
    """Case-study-in-progress; never publishable until consent +
    redaction + approval are all True.
    """

    model_config = ConfigDict(extra="forbid")

    candidate_id: str
    customer_handle: str
    proof_event_ids: list[str] = Field(min_length=1)
    narrative_draft_ar: str = ""
    narrative_draft_en: str = ""
    consent_status: Literal["not_requested", "requested", "signed", "declined"] = "not_requested"
    consent_signature_id: str | None = None
    redaction_status: Literal["not_run", "complete", "needs_review"] = "not_run"
    approval_status: Literal["pending", "approved", "rejected"] = "pending"
    publish_pack_id: str | None = None
    sector: str | None = None
    objection_addressed: str | None = None
    safety_summary: str = "no_publish_without_consent_and_approval"
    created_at: datetime = Field(default_factory=_now_utc)

    def is_publishable(self) -> bool:
        return (
            self.consent_status == "signed"
            and self.consent_signature_id is not None
            and self.redaction_status == "complete"
            and self.approval_status == "approved"
        )
