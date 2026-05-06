"""V12 Support OS — Ticket schema."""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Priority = Literal["p0", "p1", "p2", "p3"]

TicketStatus = Literal[
    "open",
    "in_progress",
    "waiting_customer",
    "escalated",
    "resolved",
    "closed",
]


# SLA in minutes by priority (matches V12 plan).
_SLA_MINUTES: dict[Priority, int] = {
    "p0": 60,           # security/payment/privacy/live-action — within 1 hour
    "p1": 60 * 24,      # blocked customer — same day
    "p2": 60 * 24,      # normal — 24 hours
    "p3": 60 * 48,      # questions — 48 hours
}


def _ticket_id(channel: str, customer_id: str, snippet: str) -> str:
    digest = hashlib.sha256(
        f"{channel}|{customer_id}|{snippet[:80]}".encode("utf-8")
    ).hexdigest()
    return f"tkt_{digest[:16]}"


class Ticket(BaseModel):
    """A support ticket. ``message_text_redacted`` MUST be PII-redacted
    by the caller — this layer doesn't re-run the redactor."""

    model_config = ConfigDict(extra="forbid")

    id: str
    customer_id: str | None = None
    channel: str = "unknown"
    message_text_redacted: str
    category: str = "unknown"
    priority: Priority = "p2"
    status: TicketStatus = "open"
    sla_due_at: datetime
    evidence_ids: list[str] = Field(default_factory=list)
    proof_event_ids: list[str] = Field(default_factory=list)
    notes_ar: str = ""
    notes_en: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def create_ticket(
    *,
    message_text_redacted: str,
    customer_id: str | None = None,
    channel: str = "unknown",
    category: str = "unknown",
    priority: Priority = "p2",
) -> Ticket:
    now = datetime.now(UTC)
    sla = now + timedelta(minutes=_SLA_MINUTES.get(priority, 60 * 24))
    return Ticket(
        id=_ticket_id(channel, customer_id or "", message_text_redacted),
        customer_id=customer_id,
        channel=channel,
        message_text_redacted=message_text_redacted,
        category=category,
        priority=priority,
        status="open",
        sla_due_at=sla,
    )
