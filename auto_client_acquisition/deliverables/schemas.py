"""Deliverable schemas — Pydantic v2 with extra='forbid'."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DeliverableType = Literal[
    "company_brain_report",
    "market_lead_audit",
    "opportunity_ranking",
    "draft_pack",
    "objection_support_map",
    "executive_pack",
    "proof_pack",
    "diagnostic_report",
    "follow_up_plan",
    "risk_map",
    "case_study",
    "monthly_exec_brief",
    "weekly_pipeline_audit",
    "support_classification_report",
    "other",
]

DeliverableStatus = Literal[
    "draft",
    "internal_review",
    "customer_review_required",
    "approved",
    "revision_requested",
    "delivered",
    "archived",
]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Deliverable(BaseModel):
    """One customer-visible service output. Decoupled from ServiceSessionRecord.

    Hard rules:
      - customer_visible=False blocks portal display (Article 4).
      - proof_related=True only when paired with a proof_event_id
        (Article 8 — no fake proof).
      - approval_required=True forces transitions through
        customer_review_required → approved before delivered.
    """

    model_config = ConfigDict(extra="forbid")

    deliverable_id: str = Field(..., min_length=1, max_length=64)
    session_id: str = Field(..., min_length=1, max_length=64)
    customer_handle: str = Field(..., min_length=1, max_length=64)
    type: DeliverableType
    title_ar: str = Field(..., min_length=1, max_length=200)
    title_en: str = Field(..., min_length=1, max_length=200)
    status: DeliverableStatus = "draft"
    version: int = Field(default=1, ge=1)
    customer_visible: bool = True
    approval_required: bool = True
    proof_related: bool = False
    proof_event_id: str | None = None  # required when proof_related=True
    artifact_uri: str | None = None  # path/URL to the actual file
    quality_gate_status: Literal["pending", "passed", "failed", "not_applicable"] = "pending"
    created_at: datetime = Field(default_factory=_now_utc)
    updated_at: datetime = Field(default_factory=_now_utc)
