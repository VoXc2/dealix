"""V12 Support OS — Ticket schema.

Wave 12 §32.3.8 (Engine 8 hardening) extends Ticket with 7 fields that
make support a growth signal, not just an inbox:

- ``sentiment``                — bilingual regex-classified
- ``root_cause``               — short string
- ``suggested_reply``          — pre-drafted bilingual reply (draft_only)
- ``proof_opportunity``        — bool: does this ticket point to an upsell?
- ``customer_health_impact``   — float in [-1.0, 1.0] (negative = drops health)
- ``escalation_needed``        — bool
- ``next_action``              — short structured string
"""
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

# Wave 12 §32.3.8 — bilingual sentiment classification (regex-based, no LLM).
Sentiment = Literal["positive", "neutral", "frustrated", "angry"]


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

    # ─── Wave 12 §32.3.8 hardening fields (all optional for back-compat) ───
    sentiment: Sentiment | None = None
    """Bilingual regex-classified sentiment (positive/neutral/frustrated/angry)."""

    root_cause: str = ""
    """Short root-cause string (e.g. "follow_up_gap", "billing_confusion")."""

    suggested_reply: str = ""
    """Pre-drafted bilingual reply (draft_only — never auto-sent)."""

    proof_opportunity: bool = False
    """True when ticket resolution points to a proof event / upsell."""

    customer_health_impact: float = 0.0
    """Health-score delta in [-1.0, 1.0] (negative = drops health)."""

    escalation_needed: bool = False
    """True when ticket category triggers founder escalation."""

    next_action: str = ""
    """Short structured next action (e.g. "draft_reply", "escalate_to_founder")."""


def classify_sentiment_bilingual(text: str) -> Sentiment:
    """Wave 12 §32.3.8 — bilingual regex sentiment classifier.

    Saudi-dialect markers + English markers. NO LLM in v1 (deterministic).
    Returns one of the 4 canonical Sentiment values.
    """
    text_lower = text.lower().strip()
    if not text_lower:
        return "neutral"

    # Angry markers (highest priority — pre-empts other classifications)
    angry_markers = (
        # Arabic
        "غاضب", "زعلان", "خربان", "ما عاد", "كذب", "نصب",
        "احتيال", "احتجاج", "أرفع شكوى", "سأشتكي", "محامي",
        # English
        "outraged", "lawsuit", "fraud", "scam", "lying", "absolutely unacceptable",
    )
    for marker in angry_markers:
        if marker in text_lower:
            return "angry"

    # Frustrated markers
    frustrated_markers = (
        # Arabic
        "محبط", "تعبت", "زهقت", "ما اشتغل", "مشكلة", "للمرة",
        "ما يشتغل", "مالها داعي", "ما رد", "تأخير", "متى راح",
        # English
        "frustrated", "again", "still not", "this is the third",
        "doesn't work", "broken", "annoying", "wasting",
    )
    for marker in frustrated_markers:
        if marker in text_lower:
            return "frustrated"

    # Positive markers
    positive_markers = (
        # Arabic
        "ممتاز", "رائع", "جيد", "شكرا", "شكراً", "أحسنتم", "بارك الله",
        # English
        "great", "thank you", "thanks", "excellent", "love it", "appreciate",
    )
    for marker in positive_markers:
        if marker in text_lower:
            return "positive"

    return "neutral"


def is_proof_opportunity_category(category: str) -> bool:
    """Wave 12 §32.3.8 — auto-tag categories where ticket resolution
    typically points to a proof event or upsell opportunity."""
    return category in {
        "technical_issue",     # resolved → "we fixed your X" proof
        "billing_question",    # resolved → "we clarified billing" proof
        "upgrade_question",    # active → upsell signal
        "connector_setup",     # resolved → integration proof
    }


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
