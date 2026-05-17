"""Revenue Autopilot persistence records — Pydantic schemas.

The orchestrator keeps an in-memory index and appends engagement
snapshots to a JSONL log (same pattern as ``leadops_spine``).
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_autopilot.funnel import FunnelStage
from auto_client_acquisition.revenue_autopilot.lead_scorer import (
    LeadScore,
    LeadSignals,
)


def _now() -> datetime:
    return datetime.now(UTC)


class Contact(BaseModel):
    """Minimal contact captured at lead intake. No raw PII in logs."""

    model_config = ConfigDict(extra="forbid")

    name: str = ""
    company: str = ""
    email: str = ""
    phone: str = ""
    region: str = ""


class StageTransition(BaseModel):
    """One forward move through the funnel."""

    model_config = ConfigDict(extra="forbid")

    from_stage: FunnelStage
    to_stage: FunnelStage
    automation: str
    actor: str = "autopilot"
    occurred_at: datetime = Field(default_factory=_now)


class EvidenceEvent(BaseModel):
    """An append-only evidence event logged by an automation."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=lambda: f"ev_{uuid4().hex[:12]}")
    engagement_id: str
    kind: str
    payload: dict = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=_now)


class DraftRef(BaseModel):
    """A draft produced by an automation — never an executed external action.

    When ``approval_id`` is set, the draft has been queued in the
    Approval Command Center for founder review before any external send.
    """

    model_config = ConfigDict(extra="forbid")

    draft_id: str = Field(default_factory=lambda: f"drf_{uuid4().hex[:12]}")
    action_type: str
    action_mode: str = "draft_only"
    summary_en: str = ""
    summary_ar: str = ""
    approval_id: str | None = None
    created_at: datetime = Field(default_factory=_now)


class AutopilotEngagement(BaseModel):
    """The full state of one lead moving through the Revenue Autopilot."""

    model_config = ConfigDict(extra="forbid")

    engagement_id: str = Field(default_factory=lambda: f"eng_{uuid4().hex[:12]}")
    contact: Contact = Field(default_factory=Contact)
    signals: LeadSignals = Field(default_factory=LeadSignals)
    lead_score: LeadScore | None = None
    current_stage: FunnelStage = "new_lead"
    stage_history: list[StageTransition] = Field(default_factory=list)
    drafts: list[DraftRef] = Field(default_factory=list)
    evidence_events: list[EvidenceEvent] = Field(default_factory=list)
    approval_ids: list[str] = Field(default_factory=list)
    tier_recommendation: str | None = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


class AutomationResult(BaseModel):
    """What one automation run produced — returned by the orchestrator."""

    model_config = ConfigDict(extra="forbid")

    automation: str
    engagement_id: str
    stage_before: FunnelStage
    stage_after: FunnelStage
    draft_ids: list[str] = Field(default_factory=list)
    approval_ids: list[str] = Field(default_factory=list)
    evidence_event_ids: list[str] = Field(default_factory=list)
    notes_en: str = ""
    notes_ar: str = ""


__all__ = [
    "AutomationResult",
    "AutopilotEngagement",
    "Contact",
    "DraftRef",
    "EvidenceEvent",
    "StageTransition",
]
