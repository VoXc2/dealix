"""
Support router — Tier-1 SLA + tickets + bot classifier.

Endpoints:
    GET  /api/v1/support/sla
        Static SLA matrix used by the support page + bot.

    POST /api/v1/support/classify
        body: {"text": "وصف المشكلة"}
        Pure classifier (keyword-based) → priority + category + escalation.
        No LLM call — deterministic + fast + offline-safe.

    POST /api/v1/support/tickets
        body: {name?, email, subject, message, priority?, category?, partner_id?}
        Creates a SupportTicketRecord. Auto-classifies if priority not given.

    GET  /api/v1/support/tickets/{ticket_id}
        Returns the ticket if email matches OR caller is the partner.

    GET  /api/v1/support/tickets?email=...
        Lists open tickets for an email (rate-limited; partial info only).
"""

from __future__ import annotations

import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import select

from api.dependencies import get_optional_partner
from db.models import SupportTicketRecord
from db.session import get_session
from dealix.auth.magic_link import MagicLinkPayload

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/support", tags=["support"])


# ── SLA matrix ────────────────────────────────────────────────────


SLA_MATRIX = {
    "P0": {"hours": 1,  "label_ar": "خلال ساعة",  "desc_ar": "أمان / إرسال خاطئ / تعطل كامل"},
    "P1": {"hours": 8,  "label_ar": "نفس اليوم",   "desc_ar": "خدمة مهمة لا تعمل"},
    "P2": {"hours": 24, "label_ar": "24 ساعة",     "desc_ar": "connector / Proof Pack متأخر"},
    "P3": {"hours": 48, "label_ar": "48 ساعة",     "desc_ar": "سؤال أو طلب تحسين"},
}


# ── Classifier ────────────────────────────────────────────────────


# Keywords are matched in lowercased Arabic + Latin text. Order matters:
# the FIRST match wins (P0 before P1 before P2 before P3).
_KEYWORDS: list[tuple[str, str, list[str]]] = [
    # P0 — security / wrong send / outage
    ("P0", "security",     ["أمان", "اختراق", "تسريب", "خطأ في الإرسال", "إرسال خاطئ", "wrong send", "leaked", "leak", "breach"]),
    ("P0", "outage",       ["تعطل كامل", "down", "outage", "كل شيء توقف", "everything broken"]),
    ("P0", "billing_dispute", ["خصم خاطئ", "نزاع دفع", "chargeback", "fraud", "احتيال"]),
    # P1 — critical service broken
    ("P1", "service_down", ["proof pack لا يعمل", "command center لا يعمل", "service down", "خدمة لا تعمل", "broken"]),
    ("P1", "angry",        ["غاضب", "غاضبة", "زعلان", "زعلانة", "angry", "furious"]),
    # P2 — connector / proof delay / billing question
    ("P2", "connector",    ["connector", "hubspot", "salesforce", "gmail", "متصل", "تكامل"]),
    ("P2", "proof_delay",  ["proof pack متأخر", "تقرير متأخر", "delay", "متأخر", "تأخّر"]),
    ("P2", "billing",      ["billing", "moyasar", "فاتورة", "دفع", "اشتراك"]),
    ("P2", "privacy",      ["pdpl", "خصوصية", "بياناتي", "privacy", "gdpr"]),
    # P3 — general question / improvement
    ("P3", "pilot_question", ["pilot", "diagnostic", "تجربة", "كيف ابدأ", "ابدأ"]),
    ("P3", "upgrade",        ["upgrade", "ترقية", "خطة", "growth os"]),
    ("P3", "question",       ["سؤال", "question", "كيف", "how"]),
]


def classify_text(text: str) -> dict[str, Any]:
    """Deterministic keyword classifier. Returns priority + category + escalation flag."""
    if not text:
        return {"priority": "P3", "category": "question", "escalate_human": False, "matched": []}
    haystack = text.lower()
    for priority, category, words in _KEYWORDS:
        for w in words:
            # Match whole-word for English, substring for Arabic (no stemming).
            pattern = r"\b" + re.escape(w.lower()) + r"\b" if all(c.isascii() for c in w) else re.escape(w.lower())
            if re.search(pattern, haystack):
                return {
                    "priority": priority,
                    "category": category,
                    # Escalate to human for P0 + payment_dispute + privacy + angry
                    "escalate_human": priority == "P0" or category in ("billing_dispute", "privacy", "angry"),
                    "matched": [w],
                }
    return {"priority": "P3", "category": "question", "escalate_human": False, "matched": []}


# ── Endpoints ─────────────────────────────────────────────────────


@router.get("/sla")
async def get_sla() -> dict[str, Any]:
    return {"sla": SLA_MATRIX}


@router.post("/classify")
async def classify_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = str(body.get("text") or "")
    out = classify_text(text)
    out["sla"] = SLA_MATRIX[out["priority"]]
    return out


@router.post("/tickets")
async def create_ticket(
    body: dict[str, Any] = Body(...),
    partner: MagicLinkPayload | None = Depends(get_optional_partner),
) -> dict[str, Any]:
    email = str(body.get("email") or "").strip().lower()
    subject = str(body.get("subject") or "").strip()
    message = str(body.get("message") or "").strip()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="email_required")
    if not subject or not message:
        raise HTTPException(status_code=400, detail="subject_and_message_required")

    classified = classify_text(subject + "\n" + message)
    priority = str(body.get("priority") or classified["priority"]).upper()
    if priority not in SLA_MATRIX:
        priority = classified["priority"]
    category = str(body.get("category") or classified["category"])

    ticket_id = f"tkt_{uuid.uuid4().hex[:14]}"
    async with get_session() as session:
        session.add(SupportTicketRecord(
            id=ticket_id,
            subject=subject[:500],
            message=message,
            name=str(body.get("name") or "")[:255] or None,
            email=email,
            priority=priority,
            category=category,
            partner_id=(partner.sub if partner else (str(body.get("partner_id") or "") or None)),
            customer_id=str(body.get("customer_id") or "") or None,
            status="open",
            sla_target_hours=SLA_MATRIX[priority]["hours"],
            escalated=bool(classified["escalate_human"]),
            meta_json={"classifier": classified},
        ))

    log.info(
        "support_ticket_created id=%s priority=%s category=%s escalate=%s",
        ticket_id, priority, category, classified["escalate_human"],
    )
    return {
        "ticket_id": ticket_id,
        "priority": priority,
        "category": category,
        "sla": SLA_MATRIX[priority],
        "escalate_human": classified["escalate_human"],
        "status": "open",
    }


@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    email: str = Query(default=""),
    partner: MagicLinkPayload | None = Depends(get_optional_partner),
) -> dict[str, Any]:
    async with get_session() as session:
        row = await session.execute(
            select(SupportTicketRecord).where(SupportTicketRecord.id == ticket_id)
        )
        ticket = row.scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    requester_email = (email or "").strip().lower()
    is_owner = (requester_email == (ticket.email or "").lower())
    is_partner = (partner is not None and ticket.partner_id == partner.sub)
    if not (is_owner or is_partner):
        raise HTTPException(status_code=403, detail="not_authorized")
    return {
        "ticket_id": ticket.id,
        "subject": ticket.subject,
        "priority": ticket.priority,
        "category": ticket.category,
        "status": ticket.status,
        "escalated": ticket.escalated,
        "sla_target_hours": ticket.sla_target_hours,
        "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
    }


@router.get("/tickets")
async def list_tickets(
    email: str = Query(default=""),
    partner: MagicLinkPayload | None = Depends(get_optional_partner),
) -> dict[str, Any]:
    """List tickets for the partner (when authenticated) or by email."""
    if partner is None and not email:
        raise HTTPException(status_code=400, detail="email_or_session_required")
    async with get_session() as session:
        if partner is not None:
            q = select(SupportTicketRecord).where(SupportTicketRecord.partner_id == partner.sub)
        else:
            q = select(SupportTicketRecord).where(SupportTicketRecord.email == email.lower())
        rows = (await session.execute(q)).scalars().all()
    return {
        "count": len(rows),
        "tickets": [
            {
                "ticket_id": t.id,
                "subject": t.subject,
                "priority": t.priority,
                "status": t.status,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in rows
        ],
    }
