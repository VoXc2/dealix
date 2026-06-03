"""Customer Inbox v10 — Chatwoot-inspired typed schemas.

Pure data — no I/O, no LLM. All outbound action surfaces are
``draft_only``, ``approval_required``, or ``blocked``. Cold-WhatsApp
outbound is platform-blocked unless explicit consent is registered.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Channel(StrEnum):
    WEBSITE_CHAT = "website_chat"
    INBOUND_WHATSAPP = "inbound_whatsapp"
    EMAIL = "email"
    MANUAL_LINKEDIN_NOTE = "manual_linkedin_note"
    SUPPORT_FORM = "support_form"
    OUTBOUND_BLOCKED = "outbound_blocked"


class ConsentStatus(StrEnum):
    UNKNOWN = "unknown"
    GRANTED = "granted"
    WITHDRAWN = "withdrawn"
    BLOCKED = "blocked"


class MessageDirection(StrEnum):
    INBOUND = "inbound"
    DRAFT_OUTBOUND = "draft_outbound"
    BLOCKED_OUTBOUND = "blocked_outbound"


class Message(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"msg_{uuid4().hex[:12]}")
    conversation_id: str
    channel: Channel
    direction: MessageDirection
    body_redacted: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Conversation(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"conv_{uuid4().hex[:12]}")
    customer_handle: str  # anonymized handle, e.g. "lead_abc123"
    channel: Channel
    consent_status: ConsentStatus = ConsentStatus.UNKNOWN
    sla_target_hours: int = 24
    customer_stage: str = "lead_intake"
    assigned_owner: str = "founder"
    priority: Literal["low", "medium", "high", "blocked"] = "medium"
    messages: list[Message] = Field(default_factory=list)


class ReplySuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conversation_id: str
    suggested_text_ar: str
    suggested_text_en: str
    action_mode: Literal["draft_only", "approval_required", "blocked"] = "draft_only"
    blocked_reason: str = ""


class SLAStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conversation_id: str
    target_hours: int
    elapsed_hours: float
    breached: bool
    action: Literal["proceed", "escalate", "alert_founder"]
