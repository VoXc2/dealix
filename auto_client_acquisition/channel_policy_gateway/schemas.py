"""Schemas for the channel policy gateway (Phase 8)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Channel = Literal["whatsapp", "email", "linkedin", "calls"]
ActionKind = Literal[
    "draft", "send_live", "automate", "scrape",
    "internal_brief", "manual_outreach",
]
PolicyMode = Literal[
    "draft_only",
    "approval_required",
    "approved_manual",
    "internal_only",
    "blocked",
]


class PolicyDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: Channel
    action_kind: ActionKind
    allowed: bool
    action_mode: PolicyMode
    reason_ar: str
    reason_en: str
    safe_alternative_ar: str = ""
    safe_alternative_en: str = ""
    required_conditions: list[str] = Field(default_factory=list)
    missing_conditions: list[str] = Field(default_factory=list)
    safety_summary: str = "no_live_send_no_cold_outreach_no_scraping"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
