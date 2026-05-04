"""Typed records for the customer-journey state machine."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class JourneyState(StrEnum):
    LEAD_INTAKE = "lead_intake"
    DIAGNOSTIC_REQUESTED = "diagnostic_requested"
    DIAGNOSTIC_SENT = "diagnostic_sent"
    PILOT_OFFERED = "pilot_offered"
    PAYMENT_PENDING = "payment_pending"
    PAID_OR_COMMITTED = "paid_or_committed"
    IN_DELIVERY = "in_delivery"
    PROOF_PACK_READY = "proof_pack_ready"
    PROOF_PACK_SENT = "proof_pack_sent"
    UPSELL_RECOMMENDED = "upsell_recommended"
    NURTURE = "nurture"
    BLOCKED = "blocked"


# Allowed transitions. Source-of-truth for the state machine —
# anything missing here is rejected as an invalid advance.
ALLOWED_TRANSITIONS: dict[JourneyState, set[JourneyState]] = {
    JourneyState.LEAD_INTAKE: {
        JourneyState.DIAGNOSTIC_REQUESTED,
        JourneyState.NURTURE,
        JourneyState.BLOCKED,
    },
    JourneyState.DIAGNOSTIC_REQUESTED: {
        JourneyState.DIAGNOSTIC_SENT,
        JourneyState.NURTURE,
        JourneyState.BLOCKED,
    },
    JourneyState.DIAGNOSTIC_SENT: {
        JourneyState.PILOT_OFFERED,
        JourneyState.NURTURE,
        JourneyState.BLOCKED,
    },
    JourneyState.PILOT_OFFERED: {
        JourneyState.PAYMENT_PENDING,
        JourneyState.NURTURE,
        JourneyState.BLOCKED,
    },
    JourneyState.PAYMENT_PENDING: {
        JourneyState.PAID_OR_COMMITTED,
        JourneyState.NURTURE,
        JourneyState.BLOCKED,
    },
    JourneyState.PAID_OR_COMMITTED: {
        JourneyState.IN_DELIVERY,
        JourneyState.BLOCKED,
    },
    JourneyState.IN_DELIVERY: {
        JourneyState.PROOF_PACK_READY,
        JourneyState.BLOCKED,
    },
    JourneyState.PROOF_PACK_READY: {
        JourneyState.PROOF_PACK_SENT,
        JourneyState.BLOCKED,
    },
    JourneyState.PROOF_PACK_SENT: {
        JourneyState.UPSELL_RECOMMENDED,
        JourneyState.NURTURE,
    },
    JourneyState.UPSELL_RECOMMENDED: {
        JourneyState.PAID_OR_COMMITTED,
        JourneyState.NURTURE,
    },
    JourneyState.NURTURE: {
        JourneyState.DIAGNOSTIC_REQUESTED,
        JourneyState.PILOT_OFFERED,
        JourneyState.BLOCKED,
    },
    JourneyState.BLOCKED: set(),  # terminal until founder unblocks manually
}


class JourneyTransition(BaseModel):
    """One available transition from current_state."""

    model_config = ConfigDict(use_enum_values=True)

    target: JourneyState
    label_ar: str
    label_en: str
    requires_approval: bool = True
    blocked_reason: str | None = None


class JourneyAdvanceRequest(BaseModel):
    """Body of POST /api/v1/customer-loop/journey/advance."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    current_state: JourneyState
    target_state: JourneyState
    customer_handle: str = "Saudi B2B customer"
    service_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class JourneyAdvanceResult(BaseModel):
    """Result of advancing the journey one step."""

    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(default_factory=lambda: f"jrn_{uuid4().hex[:12]}")
    accepted: bool
    from_state: JourneyState
    to_state: JourneyState | None = None
    rejection_reason: str | None = None
    next_actions_ar: list[str] = Field(default_factory=list)
    next_actions_en: list[str] = Field(default_factory=list)
    approval_required: bool = True
    proof_event_recommended: bool = False
    safety_notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
