"""Support Inbox state store.

Wraps support_os.{classifier, ticket, escalation, responder} into one
classify-store-draft-escalate flow. The HTTP webhook in
api/routers/support_webhook.py calls into this.

In-memory + JSONL persistence (Article 11).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.support_os.classifier import classify_message
from auto_client_acquisition.support_os.escalation import should_escalate
from auto_client_acquisition.support_os.responder import draft_response
from auto_client_acquisition.support_os.sla import compute_sla
from auto_client_acquisition.support_os.ticket import (
    Ticket,
    TicketStatus,
    create_ticket,
)

_JSONL_PATH = os.path.join("data", "support_tickets.jsonl")
_INDEX: dict[str, Ticket] = {}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(ticket: Ticket) -> None:
    _ensure_dir()
    _INDEX[ticket.id] = ticket
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(ticket.model_dump_json() + "\n")


_CATEGORY_TO_PRIORITY = {
    "refund": "p0",
    "payment": "p0",
    "privacy_pdpl": "p0",
    "angry_customer": "p0",
    "technical_issue": "p1",
    "connector_setup": "p2",
    "onboarding": "p2",
    "diagnostic_question": "p2",
    "proof_pack_question": "p2",
    "upgrade_question": "p3",
    "billing": "p1",
    "unknown": "p3",
}


def classify_and_store(
    *,
    message_text: str,
    customer_id: str | None = None,
    channel: str = "unknown",
) -> dict[str, Any]:
    """Run classify → ticket → escalation → draft → persist.

    Returns {
      'ticket': ...,
      'classification': ...,
      'escalation': ...,
      'draft': ...,
    }
    """
    classification = classify_message(message_text)
    category = classification.category
    priority = _CATEGORY_TO_PRIORITY.get(category, "p2")

    # Trust the caller for redaction (matches support_os contract);
    # also strip obvious PII patterns just in case
    redacted = _redact_pii(message_text)

    ticket = create_ticket(
        message_text_redacted=redacted,
        customer_id=customer_id,
        channel=channel,
        category=category,
        priority=priority,  # type: ignore[arg-type]
    )

    escalation = should_escalate(classification=classification, message=message_text)
    draft = draft_response(message=message_text, classification=classification)

    if escalation.should_escalate:
        ticket.status = "escalated"
        ticket.notes_en = f"escalated: {escalation.reason_en}"
        ticket.notes_ar = f"تصعيد: {escalation.reason_ar}"

    _persist(ticket)

    return {
        "ticket": ticket.model_dump(mode="json"),
        "classification": {
            "category": classification.category,
            "confidence": classification.confidence,
            "is_arabic": classification.is_arabic,
            "needs_human_immediately": classification.needs_human_immediately,
        },
        "escalation": {
            "should_escalate": escalation.should_escalate,
            "reason_ar": escalation.reason_ar,
            "reason_en": escalation.reason_en,
        },
        "draft": {
            "action_mode": draft.action_mode,
            "text_ar": draft.text_ar,
            "text_en": draft.text_en,
            "insufficient_evidence": draft.insufficient_evidence,
        },
        "sla": _safe_dict(compute_sla(priority)),  # type: ignore[arg-type]
    }


def _safe_dict(obj: Any) -> dict[str, Any]:
    """Convert dataclass / Pydantic / dict-like to a plain dict."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    try:
        from dataclasses import asdict, is_dataclass
        if is_dataclass(obj):
            return asdict(obj)
    except Exception:
        pass
    if isinstance(obj, dict):
        return obj
    return {"value": str(obj)}


def _redact_pii(text: str) -> str:
    """Lightweight regex redaction — not a substitute for the full
    redactor in proof_ledger.evidence_export, just a safety net."""
    import re
    # email
    text = re.sub(r"[\w.+-]+@[\w.-]+\.\w+", "[EMAIL]", text)
    # phone (Saudi format roughly)
    text = re.sub(r"\+?9665\d{8}", "[PHONE]", text)
    text = re.sub(r"\b05\d{8}\b", "[PHONE]", text)
    return text


def get_ticket(ticket_id: str) -> Ticket | None:
    return _INDEX.get(ticket_id)


def list_tickets(
    *,
    customer_id: str | None = None,
    status: TicketStatus | None = None,
    limit: int = 50,
) -> list[Ticket]:
    tickets = list(_INDEX.values())
    if customer_id:
        tickets = [t for t in tickets if t.customer_id == customer_id]
    if status:
        tickets = [t for t in tickets if t.status == status]
    return sorted(tickets, key=lambda t: t.created_at, reverse=True)[:limit]


def set_status(*, ticket_id: str, status: TicketStatus) -> Ticket | None:
    t = _INDEX.get(ticket_id)
    if t is None:
        return None
    t.status = status
    _persist(t)
    return t
