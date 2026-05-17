"""Typed records for the proof ledger."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ProofEventType(StrEnum):
    LEAD_INTAKE = "lead_intake"
    MEETING_BOOKED = "meeting_booked"
    MEETING_COMPLETED = "meeting_completed"
    DIAGNOSTIC_DELIVERED = "diagnostic_delivered"
    PILOT_OFFERED = "pilot_offered"
    INVOICE_PREPARED = "invoice_prepared"
    PAYMENT_CONFIRMED = "payment_confirmed"
    DELIVERY_STARTED = "delivery_started"
    DELIVERY_TASK_COMPLETED = "delivery_task_completed"
    PROOF_PACK_ASSEMBLED = "proof_pack_assembled"
    PROOF_PACK_SENT = "proof_pack_sent"
    UPSELL_RECOMMENDED = "upsell_recommended"
    PARTNER_INTRO_SENT = "partner_intro_sent"
    RISK_BLOCKED = "risk_blocked"


class RevenueWorkUnitType(StrEnum):
    OPPORTUNITY_CREATED = "opportunity_created"
    DRAFT_CREATED = "draft_created"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_REJECTED = "approval_rejected"
    DIAGNOSTIC_CREATED = "diagnostic_created"
    PILOT_OFFERED = "pilot_offered"
    INVOICE_PREPARED = "invoice_prepared"
    PAYMENT_CONFIRMED = "payment_confirmed"
    DELIVERY_TASK_COMPLETED = "delivery_task_completed"
    PROOF_PACK_ASSEMBLED = "proof_pack_assembled"
    UPSELL_RECOMMENDED = "upsell_recommended"
    PARTNER_SUGGESTED = "partner_suggested"
    RISK_BLOCKED = "risk_blocked"


class ProofEvent(BaseModel):
    """A single recorded event. May or may not be customer-public."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"evt_{uuid4().hex[:12]}")
    event_type: ProofEventType
    customer_handle: str = "Saudi B2B customer"
    service_id: str | None = None
    summary_ar: str = ""
    summary_en: str = ""
    evidence_source: str = ""
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    consent_for_publication: bool = False
    redacted_summary_ar: str = ""
    redacted_summary_en: str = ""
    approval_status: str = "approval_required"
    risk_level: str = "low"
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def is_publishable(self) -> bool:
        return self.consent_for_publication and self.approval_status == "approved"


class RevenueWorkUnit(BaseModel):
    """One unit of measurable revenue work."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"rwu_{uuid4().hex[:12]}")
    unit_type: RevenueWorkUnitType
    customer_handle: str = "Saudi B2B customer"
    service_id: str | None = None
    quantity: int = 1
    description: str = ""
    proof_event_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
