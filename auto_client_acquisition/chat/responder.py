"""Chat responder — answer from the KB or escalate to a ticket.

Deterministic: a question is matched against approved KB articles via
``suggest_answer``. A confident approved match is returned with its
citations; anything else creates a support ticket and returns an
escalation message. No approved-KB match means no answer — ever.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from auto_client_acquisition.evidence_control_plane_os.event_store import (
    record_evidence_event,
)
from auto_client_acquisition.knowledge.suggest import suggest_answer
from auto_client_acquisition.support.lifecycle import create_ticket


def respond(
    message: str,
    *,
    channel: str = "chat_widget",
    customer_id: str | None = None,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """Answer a chat message from the KB, or escalate it to a ticket."""
    turn_id = f"chat_{uuid4().hex[:10]}"
    suggestion = suggest_answer(message or "")

    if suggestion.get("found"):
        record_evidence_event(
            event_type="chat_answered",
            entity_type="chat",
            entity_id=turn_id,
            actor="chat_responder",
            action="answer_from_kb",
            summary_en="Chat answered from an approved KB article",
            payload={"confidence": suggestion.get("confidence")},
            tenant_id=tenant_id,
        )
        return {
            "answered": True,
            "escalated": False,
            "turn_id": turn_id,
            "answer_ar": suggestion.get("answer_ar", ""),
            "answer_en": suggestion.get("answer_en", ""),
            "confidence": suggestion.get("confidence", 0.0),
            "citations": suggestion.get("citations", []),
        }

    # No grounded answer — escalate into the support pipeline.
    ticket = create_ticket(
        subject="Chat question",
        message=message or "",
        channel=channel,
        customer_id=customer_id,
        tenant_id=tenant_id,
    )
    record_evidence_event(
        event_type="chat_escalated",
        entity_type="chat",
        entity_id=turn_id,
        actor="chat_responder",
        action="escalate_to_ticket",
        summary_en=f"Chat question escalated to ticket {ticket.ticket_id}",
        tenant_id=tenant_id,
    )
    return {
        "answered": False,
        "escalated": True,
        "turn_id": turn_id,
        "ticket_id": ticket.ticket_id,
        "message_ar": "أحتاج أصعّد سؤالك للفريق — سنرجع لك قريباً.",
        "message_en": "I've escalated your question to the team — we'll get back to you soon.",
    }
