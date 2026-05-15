"""CRM v10 Pydantic schemas (Twenty CRM-inspired) — typed object model.

Pure schemas + DTOs. No DB, no LLM, no external HTTP. Foundation for a
future Twenty CRM real adapter; today they describe Dealix's CRM
state in-memory only.

Hard rules:
  - Pydantic v2 with ``extra="forbid"`` on every model.
  - No PII fields: contact identity uses ``full_name_redacted_handle``.
  - Bilingual (ar/en) fields where the artifact is customer-facing.
"""
from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def _now() -> datetime:
    return datetime.now(UTC)


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Account(_Strict):
    id: str
    name: str
    sector: str
    region: str
    tier: str
    customer_health_score: float = 0.0
    created_at: datetime = Field(default_factory=_now)
    notes: str = ""


class Contact(_Strict):
    id: str
    account_id: str
    full_name_redacted_handle: str
    role: str
    language_preference: str = "ar"
    consent_status: Literal["unknown", "granted", "withdrawn", "blocked"] = "unknown"
    created_at: datetime = Field(default_factory=_now)


class Lead(_Strict):
    id: str
    account_id: str
    source: Literal["warm_intro", "inbound", "founder_network", "manual", "other"]
    stage: Literal["new", "qualifying", "qualified", "disqualified", "converted"] = "new"
    fit_score: float = 0.0
    urgency_score: float = 0.0
    created_at: datetime = Field(default_factory=_now)
    notes: str = ""


class Deal(_Strict):
    id: str
    account_id: str
    lead_id: str
    stage: Literal[
        "pilot_offered", "payment_pending", "paid_or_committed",
        "in_delivery", "won", "lost",
    ] = "pilot_offered"
    amount_sar: float = 0.0
    currency: Literal["SAR", "USD"] = "SAR"
    expected_close_date: date | None = None
    owner: str = "founder"


class Opportunity(_Strict):
    id: str
    account_id: str
    recommended_service: str
    why_recommended_ar: str
    why_recommended_en: str
    status: Literal["open", "converted_to_deal", "abandoned"] = "open"


class ServiceSession(_Strict):
    id: str
    account_id: str
    service_id: str
    status: Literal["scheduled", "in_progress", "completed", "blocked"] = "scheduled"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    deliverables_count: int = 0


class ProofEventRef(_Strict):
    id: str
    account_id: str
    event_type: str
    redacted_summary: str
    created_at: datetime = Field(default_factory=_now)


class CustomerHealth(_Strict):
    account_id: str
    score: float = 0.0
    factors: dict[str, float] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=_now)


class Partner(_Strict):
    id: str
    name: str
    fit_score: float = 0.0
    allowed_channels: list[str] = Field(default_factory=list)
    blocked_channels: list[str] = Field(default_factory=list)


class SupportTicket(_Strict):
    id: str
    account_id: str
    subject: str
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    priority: Literal["low", "medium", "high", "blocked"] = "medium"
    sla_response_hours: int = 24


class Campaign(_Strict):
    id: str
    name: str
    segment_query: dict
    status: Literal["draft", "approved", "running", "paused", "done"] = "draft"
    consent_required: bool = True


class Proposal(_Strict):
    id: str
    account_id: str
    recommended_service: str
    scope_ar: str
    scope_en: str
    price_sar: float
    status: Literal["draft", "sent", "accepted", "rejected", "expired"] = "draft"


class InvoiceIntent(_Strict):
    id: str
    account_id: str
    amount_sar: float
    description: str
    payment_url: str = ""
    status: Literal["draft", "sent", "paid", "manually_committed", "expired"] = "draft"


class ManualPaymentRecord(_Strict):
    id: str
    account_id: str
    amount_sar: float
    recorded_at: datetime = Field(default_factory=_now)
    evidence_source: str
    notes: str = ""


class ApprovalRequestRef(_Strict):
    id: str
    account_id: str
    action_type: str
    status: Literal["pending", "approved", "rejected", "blocked"] = "pending"


# Registry — first-class CRM object types in deterministic order.
# CustomerHealth is a derived type from compute_health(), not registered.
OBJECT_TYPES: tuple[type[BaseModel], ...] = (
    Account, Contact, Lead, Deal, Opportunity, ServiceSession,
    ProofEventRef, Partner, SupportTicket, Campaign, Proposal,
    InvoiceIntent, ManualPaymentRecord, ApprovalRequestRef,
)

__all__ = [
    "OBJECT_TYPES",
    "Account",
    "ApprovalRequestRef",
    "Campaign",
    "Contact",
    "CustomerHealth",
    "Deal",
    "InvoiceIntent",
    "Lead",
    "ManualPaymentRecord",
    "Opportunity",
    "Partner",
    "ProofEventRef",
    "Proposal",
    "ServiceSession",
    "SupportTicket",
]
