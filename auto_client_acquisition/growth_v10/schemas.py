"""Growth v10 — PostHog-inspired event taxonomy + funnel + experiments.

Pure typed schemas. NO LLM. NO PII. Events are auto-redacted on insert.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class EventName(StrEnum):
    LEAD_CREATED = "lead_created"
    COMPANY_BRAIN_BUILT = "company_brain_built"
    DIAGNOSTIC_REQUESTED = "diagnostic_requested"
    DIAGNOSTIC_DELIVERED = "diagnostic_delivered"
    SERVICE_RECOMMENDED = "service_recommended"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_ACCEPTED = "approval_accepted"
    UNSAFE_ACTION_BLOCKED = "unsafe_action_blocked"
    DRAFT_CREATED = "draft_created"
    PROPOSAL_CREATED = "proposal_created"
    PAYMENT_REQUESTED_MANUAL = "payment_requested_manual"
    PILOT_STARTED = "pilot_started"
    PROOF_EVENT_CREATED = "proof_event_created"
    PROOF_PACK_GENERATED = "proof_pack_generated"
    WEEKLY_REPORT_GENERATED = "weekly_report_generated"
    CUSTOMER_HEALTH_CHANGED = "customer_health_changed"
    RENEWAL_RISK_DETECTED = "renewal_risk_detected"


class EventRecord(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    name: EventName
    customer_handle: str  # anonymized
    payload: dict[str, Any] = Field(default_factory=dict)
    redacted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class FunnelStage(StrEnum):
    VISITOR = "visitor"
    LEAD = "lead"
    QUALIFIED = "qualified"
    DIAGNOSTIC_DELIVERED = "diagnostic_delivered"
    PILOT_OFFERED = "pilot_offered"
    PAID_OR_COMMITTED = "paid_or_committed"
    PROOF_DELIVERED = "proof_delivered"


class FunnelStep(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    from_stage: FunnelStage
    to_stage: FunnelStage
    count: int
    conversion_rate: float


class FunnelReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stages: list[FunnelStep]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    total_visitors: int
    total_paid: int


class Experiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: f"exp_{uuid4().hex[:10]}")
    name: str
    hypothesis_ar: str
    hypothesis_en: str
    variants: list[str]
    status: Literal["draft", "running", "paused", "done", "blocked"] = "draft"
    primary_metric: str
    success_threshold: float


class Campaign(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: f"camp_{uuid4().hex[:10]}")
    name: str
    segment_query: dict[str, Any] = Field(default_factory=dict)
    channel: str
    status: Literal["draft", "approved", "running", "paused", "done", "blocked"] = "draft"
    consent_required: bool = True


class FeedbackRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_handle: str
    score: int = Field(ge=0, le=10)
    comment_redacted: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class WeeklyContentCalendar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    week_label: str
    planned_posts: list[dict[str, Any]] = Field(default_factory=list)
    approval_required: bool = True
