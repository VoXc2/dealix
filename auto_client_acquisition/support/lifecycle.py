"""Support ticket lifecycle orchestration.

create → classify → draft-reply (from KB) → escalate / resolve. Each
transition writes an evidence event. Sending a drafted reply is routed
through the approval center — this layer never sends.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from auto_client_acquisition.approval_center import ApprovalRequest, create_approval
from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    record_evidence_event,
)
from auto_client_acquisition.knowledge.suggest import suggest_answer
from auto_client_acquisition.support.risk import (
    is_auto_answerable,
    risk_level_for_category,
)
from auto_client_acquisition.support.ticket_store import (
    SupportTicket,
    TicketStore,
    get_default_ticket_store,
)
from auto_client_acquisition.support_os.classifier import classify_message
from auto_client_acquisition.support_os.escalation import should_escalate
from auto_client_acquisition.support_os.sla import category_to_priority, compute_sla
from auto_client_acquisition.support_os.ticket import classify_sentiment_bilingual


def _store(store: TicketStore | None) -> TicketStore:
    return store or get_default_ticket_store()


def _evidence(tkt: SupportTicket, event_type: str, action: str, summary: str,
              approval_id: str | None = None) -> None:
    record_evidence_event(
        event_type=event_type,
        entity_type="support_ticket",
        entity_id=tkt.ticket_id,
        action=action,
        summary_en=summary,
        approval_id=approval_id,
        tenant_id=tkt.tenant_id,
    )


def _classify(subject: str, message: str) -> dict[str, Any]:
    text = f"{subject}\n{message}".strip()
    classification = classify_message(text)
    escalation = should_escalate(classification=classification, message=text)
    priority = category_to_priority(classification.category)
    return {
        "category": classification.category,
        "intent": classification.category,
        "priority": priority,
        "sentiment": classify_sentiment_bilingual(text),
        "risk_level": risk_level_for_category(classification.category),
        "escalation_needed": escalation.should_escalate,
        "escalation_reason": escalation.reason_en if escalation.should_escalate else "",
    }


def create_ticket(
    *,
    subject: str,
    message: str,
    channel: str = "unknown",
    customer_id: str | None = None,
    tenant_id: str | None = None,
    store: TicketStore | None = None,
) -> SupportTicket:
    """Create, classify and persist a support ticket in one step."""
    store = _store(store)
    fields = _classify(subject, message)
    tkt = SupportTicket(
        tenant_id=tenant_id,
        customer_id=customer_id,
        channel=channel,
        subject=subject,
        message_redacted=redact_text(message) if message else "",
        status="escalated" if fields["escalation_needed"] else "open",
        **fields,
    )
    sla = compute_sla(tkt.priority)  # type: ignore[arg-type]
    tkt = store.create(tkt)
    tkt = store.update(
        tkt.ticket_id,
        {"sla_due_at": tkt.created_at + timedelta(minutes=sla.minutes)},
    )
    _evidence(
        tkt, "support_ticket_created", "create",
        f"Support ticket created ({tkt.category}, risk={tkt.risk_level})",
    )
    return tkt


def classify_ticket(ticket_id: str, *, store: TicketStore | None = None) -> SupportTicket:
    """Re-run classification on an existing ticket."""
    store = _store(store)
    tkt = store.get(ticket_id)
    if tkt is None:
        raise ValueError(f"support ticket {ticket_id} not found")
    fields = _classify(tkt.subject, tkt.message_redacted)
    tkt = store.update(ticket_id, fields)
    _evidence(tkt, "support_ticket_classified", "classify",
              f"Ticket re-classified as {tkt.category}")
    return tkt


def draft_reply(ticket_id: str, *, store: TicketStore | None = None) -> dict[str, Any]:
    """Draft a KB-grounded reply, or escalate if the ticket is high-risk
    or the KB has no confident answer. Never sends."""
    store = _store(store)
    tkt = store.get(ticket_id)
    if tkt is None:
        raise ValueError(f"support ticket {ticket_id} not found")

    suggestion = suggest_answer(f"{tkt.subject}\n{tkt.message_redacted}")
    confidence = float(suggestion.get("confidence", 0.0))
    answerable = is_auto_answerable(
        category=tkt.category,
        escalation_needed=tkt.escalation_needed,
        kb_confidence=confidence,
    )

    if suggestion.get("found") and answerable:
        citations = [c["article_id"] for c in suggestion.get("citations", [])]
        tkt = store.update(
            ticket_id,
            {
                "suggested_reply": suggestion.get("answer_en", ""),
                "kb_article_ids": citations,
                "status": "in_progress",
            },
        )
        _evidence(tkt, "support_reply_drafted", "draft_reply",
                  f"KB-grounded reply drafted (confidence={confidence})")
        return {
            "ticket_id": ticket_id,
            "drafted": True,
            "escalated": False,
            "kb_article_ids": citations,
            "confidence": confidence,
        }

    # No confident KB answer or the ticket is high-risk → escalate.
    reason = (
        tkt.escalation_reason
        or "no confident knowledge-base answer — needs human review"
    )
    tkt = store.update(
        ticket_id,
        {"status": "escalated", "escalation_needed": True, "escalation_reason": reason},
    )
    _evidence(tkt, "support_ticket_escalated", "escalate",
              f"Ticket escalated on draft: {reason}")
    return {
        "ticket_id": ticket_id,
        "drafted": False,
        "escalated": True,
        "reason": reason,
    }


def escalate_ticket(
    ticket_id: str, *, reason: str = "", store: TicketStore | None = None
) -> SupportTicket:
    store = _store(store)
    tkt = store.get(ticket_id)
    if tkt is None:
        raise ValueError(f"support ticket {ticket_id} not found")
    tkt = store.update(
        ticket_id,
        {"status": "escalated", "escalation_needed": True,
         "escalation_reason": reason or "manual escalation"},
    )
    _evidence(tkt, "support_ticket_escalated", "escalate",
              f"Ticket escalated: {reason or 'manual'}")
    return tkt


def resolve_ticket(ticket_id: str, *, store: TicketStore | None = None) -> SupportTicket:
    store = _store(store)
    tkt = store.get(ticket_id)
    if tkt is None:
        raise ValueError(f"support ticket {ticket_id} not found")
    from auto_client_acquisition.support.ticket_store import _now

    tkt = store.update(ticket_id, {"status": "resolved", "resolved_at": _now()})
    _evidence(tkt, "support_ticket_resolved", "resolve", "Ticket resolved")
    return tkt


def request_send_reply(
    ticket_id: str, *, store: TicketStore | None = None
) -> dict[str, Any]:
    """Queue an approval to send the drafted reply. Support NEVER sends
    directly — this always returns ``approval_required``."""
    store = _store(store)
    tkt = store.get(ticket_id)
    if tkt is None:
        raise ValueError(f"support ticket {ticket_id} not found")

    approval = create_approval(
        ApprovalRequest(
            object_type="support_ticket",
            object_id=ticket_id,
            action_type="support_reply_draft",
            action_mode="approval_required",
            risk_level=tkt.risk_level,
            channel=tkt.channel if tkt.channel != "unknown" else None,
            summary_en=f"Send support reply for ticket {ticket_id}",
            summary_ar="إرسال ردّ دعم على التذكرة",
            customer_id=tkt.customer_id,
            proof_impact=f"support:{ticket_id}",
        )
    )
    _evidence(tkt, "support_reply_send_requested", "request_send",
              f"Approval requested to send reply for ticket {ticket_id}",
              approval_id=approval.approval_id)
    return {
        "ticket_id": ticket_id,
        "sent": False,
        "approval_status": "approval_required",
        "approval_id": approval.approval_id,
    }
