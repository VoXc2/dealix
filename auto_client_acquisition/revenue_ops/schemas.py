"""Governed Revenue Ops schemas.

Deterministic, import-safe models used by the Revenue Ops API layer.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class RevenueOpsState(StrEnum):
    """State machine for governed revenue decisions."""

    DRAFT = "draft"
    APPROVED = "approved"
    SENT = "sent"
    USED_IN_MEETING = "used_in_meeting"
    SCOPE_REQUESTED = "scope_requested"
    INVOICE_SENT = "invoice_sent"
    INVOICE_PAID = "invoice_paid"


class OpportunityInput(BaseModel):
    """One opportunity candidate from CRM/pipeline inputs."""

    model_config = ConfigDict(extra="forbid")

    account_name: str = Field(..., min_length=1, max_length=120)
    pipeline_stage: str = Field(..., min_length=1, max_length=80)
    estimated_value_sar: float = Field(..., ge=0)
    risk_signals: tuple[str, ...] = Field(default_factory=tuple)
    source_ref: str = Field(..., min_length=3, max_length=200)


class DiagnosticRequest(BaseModel):
    """Create a governed revenue diagnostic."""

    model_config = ConfigDict(extra="forbid")

    client_name: str = Field(..., min_length=1, max_length=120)
    sector: str = Field(default="b2b", min_length=1, max_length=80)
    crm_source_ref: str = Field(..., min_length=3, max_length=200)
    requested_by: str = Field(default="founder", min_length=1, max_length=80)
    ai_usage_notes: str = ""
    pain_points: tuple[str, ...] = Field(default_factory=tuple)


class UploadRequest(BaseModel):
    """Attach CRM export metadata to an existing diagnostic."""

    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str = Field(..., min_length=3, max_length=120)
    source_ref: str = Field(..., min_length=3, max_length=200)
    filename: str = Field(..., min_length=1, max_length=160)
    row_count: int = Field(..., ge=1, le=2_000_000)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    uploaded_by: str = Field(default="founder", min_length=1, max_length=80)


class ScoreRequest(BaseModel):
    """Score opportunities for next-best-action prioritization."""

    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str = Field(..., min_length=3, max_length=120)
    opportunities: tuple[OpportunityInput, ...] = Field(..., min_length=1)


class FollowUpDraftRequest(BaseModel):
    """Generate approval-first follow-up drafts."""

    model_config = ConfigDict(extra="forbid")

    owner: str = Field(default="founder", min_length=1, max_length=80)
    tone: str = Field(default="professional", min_length=1, max_length=40)
    channels: tuple[str, ...] = Field(default=("email_manual",))
    max_drafts: int = Field(default=3, ge=1, le=20)


class EvidenceEventRequest(BaseModel):
    """Record an evidence event with optional state transition."""

    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str = Field(..., min_length=3, max_length=120)
    event_type: str = Field(..., min_length=1, max_length=80)
    summary_ar: str = Field(..., min_length=1, max_length=500)
    summary_en: str = Field(..., min_length=1, max_length=500)
    source_ref: str = Field(..., min_length=3, max_length=200)
    evidence_ref: str = Field(..., min_length=3, max_length=200)
    recorded_by: str = Field(default="founder", min_length=1, max_length=80)
    target_state: RevenueOpsState | None = None


class InvoiceDraftRequest(BaseModel):
    """Create invoice draft for a governed revenue engagement."""

    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str = Field(..., min_length=3, max_length=120)
    customer_handle: str = Field(..., min_length=1, max_length=80)
    amount_sar: int = Field(..., gt=0, le=250_000)
    description: str = ""
    mode: str = Field(default="test", pattern="^(test|manual_only)$")
    mark_as_sent: bool = False


class ScoredOpportunity(BaseModel):
    """Scored opportunity response item."""

    model_config = ConfigDict(extra="forbid")

    account_name: str
    pipeline_stage: str
    estimated_value_sar: float
    priority_score: float
    risk_count: int
    source_ref: str
    next_action_en: str
    next_action_ar: str


class RevenueDiagnosticRecord(BaseModel):
    """Stored diagnostic record."""

    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str
    client_name: str
    sector: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    requested_by: str
    crm_source_ref: str
    state: RevenueOpsState = RevenueOpsState.DRAFT
    approval_id: str | None = None
    decision_passport: dict[str, Any] = Field(default_factory=dict)
    scores: list[ScoredOpportunity] = Field(default_factory=list)
    uploads: list[dict[str, Any]] = Field(default_factory=list)
    evidence_events: list[dict[str, Any]] = Field(default_factory=list)

    @staticmethod
    def next_id() -> str:
        return f"rops_{uuid4().hex[:12]}"
