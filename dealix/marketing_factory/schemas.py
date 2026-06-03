"""Marketing Factory — content calendar + UTM records (governed, draft-first)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ContentStatus = Literal[
    "draft",
    "approval_pending",
    "approved",
    "published_manual",
]


class CalendarSlotRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    scheduled_date: str
    channel: str
    title_ar: str
    body_draft_ar: str
    cta_label_ar: str = "اطلب Risk Score"
    cta_path: str = "/dealix-diagnostic"
    utm_campaign: str = ""
    utm_medium: str = "social"
    utm_source: str = "dealix"
    status: ContentStatus = "draft"
    evidence_note: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UtmLinkRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    base_url: str
    full_url: str
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_content: str = ""
    calendar_slot_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
