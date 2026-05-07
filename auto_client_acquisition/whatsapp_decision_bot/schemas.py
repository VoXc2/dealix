"""Schemas for the WhatsApp Decision Layer (Phase 7)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

CommandIntent = Literal[
    "today_status",
    "top_3_decisions",
    "overdue_deals",
    "open_support",
    "weekly_report",
    "draft_reply",
    "approve_reply",
    "escalate_ticket",
    "risks_overview",
    "blocked_unsafe",
    "unknown",
]

ActionMode = Literal[
    "preview_only",
    "draft_only",
    "approval_required",
    "approved_manual",
    "blocked",
]


class CommandResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: CommandIntent
    action_mode: ActionMode
    text_input: str
    output_ar: str = ""
    output_en: str = ""
    requires_approval: bool = True
    payload: dict[str, Any] = Field(default_factory=dict)
    safety_summary: str = "no_live_send_no_customer_outbound"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ApprovalPreview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_kind: str
    target_handle: str | None = None
    text_to_send_ar: str = ""
    text_to_send_en: str = ""
    would_send_live: bool = False  # ALWAYS False
    blocked_reasons: list[str] = Field(default_factory=list)
    requires_human_approval: bool = True
    safety_summary: str = "preview_only_no_live_send"
