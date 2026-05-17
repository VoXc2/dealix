"""
Outreach preparation router.

POST /api/v1/outreach/prepare-from-data
    Take enriched accounts + apply suppression + per-channel policy →
    produce ready/needs_review/blocked counts. Optionally persist to
    outreach_queue with approval_required=True.

GET  /api/v1/outreach/queue
    List queue rows.

POST /api/v1/outreach/queue/{id}/approve
    Mark a queued message as approved (does NOT auto-send).

POST /api/v1/outreach/queue/{id}/skip
    Mark as skipped with reason.

PDPL & policy guards:
    - Suppression hit → blocked
    - opt_out=true on contact → blocked
    - high risk → needs_review
    - missing source → needs_review
    - approval_required=True for cold outbound regardless
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import select

from auto_client_acquisition.outreach_sequence import (
    compute_next_step,
    list_sequences,
)

from db.models import (
    AccountRecord,
    ContactRecord,
    LeadScoreRecord,
    OutreachQueueRecord,
    SuppressionRecord,
)
from db.session import async_session_factory

router = APIRouter(prefix="/api/v1/outreach", tags=["outreach"])
log = logging.getLogger(__name__)


def _new_id(prefix: str = "") -> str:
    suffix = uuid.uuid4().hex[:24]
    return f"{prefix}{suffix}" if prefix else suffix


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# Channel policy
CHANNEL_DEFAULT_APPROVAL = {
    "email_warm": True,            # always require approval first 30 days
    "phone_task": True,            # human dials anyway
    "website_form_or_phone_task": True,
    "in_person_or_phone": True,
    "linkedin_manual": True,       # never auto, always human
    "whatsapp_inbound_only": True, # never cold WhatsApp
    "needs_enrichment": True,
}


def _build_message_template(account: dict[str, Any], score: dict[str, Any]) -> str:
    """
    Generate a Khaliji opening message based on account + score.
    Deterministic — no LLM. Replace later with LLM-generated personalization.
    """
    name = account.get("company_name") or "فريقكم"
    sector = account.get("sector") or "نشاطكم"
    city = account.get("city") or "السعودية"
    priority = score.get("priority") or "P2"
    channel = score.get("recommended_channel") or "email"

    if priority == "P0":
        opening = (
            f"السلام عليكم، نتابع نشاط {name} في {city} ولاحظنا عدة مؤشرات تخص "
            f"تسريع التعامل مع leads العربية في {sector}. "
            "Dealix يخدم نفس القطاع ويرد خلال 45 ثانية بالعربي الخليجي مع التزام PDPL. "
            "تناسبكم 20 دقيقة هذا الأسبوع نوضح كيف يطبق على وضعكم؟"
        )
    elif priority == "P1":
        opening = (
            f"مرحباً، Dealix منصة AI sales rep بالعربي الخليجي تخدم شركات {sector} في {city}. "
            "نرد على leads خلال 45 ثانية ونحجز demos تلقائياً. "
            "هل عندكم تحدي حالي مع وقت الرد على leads؟"
        )
    else:
        opening = (
            f"السلام عليكم {name}، نقدم AI sales rep بالعربي للسوق السعودي. "
            "رغبت أعرف هل تواجهون تحدي مع وقت الرد على العملاء الجدد بعد التواصل الأولي؟"
        )

    opening += f"\n\n— Sami | Dealix\nhttps://dealix.me\nالقناة المقترحة: {channel} | الأولوية: {priority}"
    return opening


@router.post("/prepare-from-data")
async def prepare_from_data(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """
    Walk enriched accounts and produce an outreach plan.

    Body:
        priority: filter by P0/P1/P2/P3 (default: all P0+P1)
        max_accounts: int (default 50)
        persist: bool (default False) — actually create OutreachQueueRecord rows
        channels: list[str] (default: all)
    """
    priorities = body.get("priority") or ["P0", "P1"]
    if isinstance(priorities, str):
        priorities = [priorities]
    max_accounts = int(body.get("max_accounts") or 50)
    persist = bool(body.get("persist", False))
    allowed_channels = body.get("channels")

    if max_accounts < 1 or max_accounts > 500:
        raise HTTPException(400, "max_accounts_out_of_range")

    async with async_session_factory() as session:
        try:
            # Get enriched accounts with their latest scores
            accounts = (await session.execute(
                select(AccountRecord).where(AccountRecord.status == "enriched")
                .limit(max_accounts * 3)  # over-fetch then filter
            )).scalars().all()

            scores = (await session.execute(
                select(LeadScoreRecord)
                .where(LeadScoreRecord.account_id.in_([a.id for a in accounts]))
            )).scalars().all()
            score_map: dict[str, LeadScoreRecord] = {}
            for s in scores:
                if s.account_id not in score_map or s.created_at > score_map[s.account_id].created_at:
                    score_map[s.account_id] = s

            contacts = (await session.execute(
                select(ContactRecord).where(
                    ContactRecord.account_id.in_([a.id for a in accounts])
                )
            )).scalars().all()
            contacts_by_acc: dict[str, list[ContactRecord]] = {}
            for c in contacts:
                contacts_by_acc.setdefault(c.account_id, []).append(c)

            suppressed = (await session.execute(select(SuppressionRecord))).scalars().all()
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}

        sup_emails = {s.email for s in suppressed if s.email}
        sup_phones = {s.phone for s in suppressed if s.phone}
        sup_domains = {s.domain for s in suppressed if s.domain}

        ready: list[dict[str, Any]] = []
        needs_review: list[dict[str, Any]] = []
        blocked: list[dict[str, Any]] = []
        queue_rows: list[OutreachQueueRecord] = []

        for acc in accounts:
            score = score_map.get(acc.id)
            if not score:
                continue
            if score.priority not in priorities:
                continue

            channel = score.recommended_channel
            if allowed_channels and channel not in allowed_channels:
                continue

            account_payload = {
                "id": acc.id, "company_name": acc.company_name,
                "domain": acc.domain, "website": acc.website,
                "city": acc.city, "sector": acc.sector,
            }
            score_payload = {
                "fit": score.fit_score, "intent": score.intent_score,
                "total": score.total_score, "priority": score.priority,
                "recommended_channel": channel, "reason": score.reason,
            }

            ac_contacts = contacts_by_acc.get(acc.id, [])
            block_reasons: list[str] = []
            review_reasons: list[str] = []

            # Suppression check
            if acc.domain and acc.domain in sup_domains:
                block_reasons.append("domain_suppressed")
            for c in ac_contacts:
                if c.opt_out:
                    block_reasons.append("contact_opted_out")
                if c.email and c.email in sup_emails:
                    block_reasons.append("email_suppressed")
                if c.phone and c.phone in sup_phones:
                    block_reasons.append("phone_suppressed")

            # Risk gates
            if (acc.risk_level or "").lower() == "high":
                review_reasons.append("high_risk_level")
            if not (acc.extra or {}).get("allowed_use"):
                review_reasons.append("missing_allowed_use")
            if not channel or channel == "needs_enrichment":
                review_reasons.append("needs_enrichment")

            if block_reasons:
                blocked.append({
                    "account_id": acc.id, "company": acc.company_name,
                    "priority": score.priority, "reasons": block_reasons,
                })
                continue

            # Build the message
            message = _build_message_template(account_payload, score_payload)

            entry = {
                "account_id": acc.id, "company": acc.company_name,
                "channel": channel, "priority": score.priority,
                "score": score.total_score, "message": message,
                "approval_required": CHANNEL_DEFAULT_APPROVAL.get(channel or "", True),
                "due_at": (_utcnow() + timedelta(hours=2)).isoformat(),
            }

            if review_reasons:
                entry["review_reasons"] = review_reasons
                needs_review.append(entry)
            else:
                ready.append(entry)
                if persist:
                    queue_rows.append(OutreachQueueRecord(
                        id=_new_id("oq_"),
                        lead_id=acc.id,
                        channel=channel or "manual",
                        message=message,
                        approval_required=True,  # always require for first 30 days
                        status="queued",
                        due_at=_utcnow() + timedelta(hours=2),
                        risk_reason=None,
                    ))

            if len(ready) + len(needs_review) >= max_accounts:
                break

        if persist and queue_rows:
            for q in queue_rows:
                session.add(q)
            try:
                await session.commit()
            except Exception as exc:  # noqa: BLE001
                await session.rollback()
                return {"status": "commit_failed", "error": str(exc)}

    return {
        "status": "ok",
        "filters": {"priorities": priorities, "channels": allowed_channels},
        "ready_count": len(ready),
        "needs_review_count": len(needs_review),
        "blocked_count": len(blocked),
        "persisted": persist and bool(queue_rows),
        "ready": ready,
        "needs_review": needs_review,
        "blocked": blocked,
    }


@router.get("/queue")
async def list_queue(status: str | None = None, limit: int = 100) -> dict[str, Any]:
    async with async_session_factory() as session:
        try:
            q = select(OutreachQueueRecord).order_by(OutreachQueueRecord.due_at).limit(min(500, limit))
            if status:
                q = q.where(OutreachQueueRecord.status == status)
            rows = (await session.execute(q)).scalars().all()
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc), "items": []}
        return {
            "count": len(rows),
            "items": [
                {
                    "id": r.id, "lead_id": r.lead_id, "channel": r.channel,
                    "message": r.message, "approval_required": r.approval_required,
                    "status": r.status, "due_at": r.due_at.isoformat(),
                    "sent_at": r.sent_at.isoformat() if r.sent_at else None,
                    "risk_reason": r.risk_reason,
                }
                for r in rows
            ],
        }


@router.post("/queue/{queue_id}/approve")
async def approve_queue(queue_id: str) -> dict[str, Any]:
    async with async_session_factory() as session:
        try:
            q = (await session.execute(
                select(OutreachQueueRecord).where(OutreachQueueRecord.id == queue_id)
            )).scalar_one_or_none()
            if not q:
                raise HTTPException(404, "queue_not_found")
            q.status = "approved"
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}
        try:
            await session.commit()
        except Exception as exc:  # noqa: BLE001
            await session.rollback()
            return {"status": "commit_failed", "error": str(exc)}
    return {"id": queue_id, "status": "approved"}


@router.get("/sequences")
async def get_sequences() -> dict[str, Any]:
    """List the named multi-step outreach sequences.

    DOCTRINE — sequences only PREPARE drafts. Every step that sends
    externally carries `requires_approval=True`; nothing auto-sends.
    """
    return {
        "status": "ok",
        "sequences": list_sequences(),
        "doctrine": "sequences_prepare_drafts_only_no_auto_send",
    }


@router.post("/sequences/next-step")
async def sequence_next_step(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Compute the next pending step for a lead enrolled in a sequence.

    Body:
        sequence: sequence name (e.g. "warm_linkedin")
        lead_id: the lead identifier
        enrolled_on: ISO date the lead was enrolled
        completed_steps: int — steps already prepared (default 0)
        as_of: optional ISO date to evaluate against (default today)

    Returns the next due step as a DRAFT instruction. The step always
    carries `requires_approval` — the founder must approve before any
    external message is sent.
    """
    sequence = str(body.get("sequence") or "").strip()
    lead_id = str(body.get("lead_id") or "").strip()
    enrolled_on = str(body.get("enrolled_on") or "").strip()
    if not sequence or not lead_id or not enrolled_on:
        raise HTTPException(400, "sequence, lead_id and enrolled_on are required")
    try:
        completed = int(body.get("completed_steps") or 0)
    except (TypeError, ValueError):
        raise HTTPException(400, "completed_steps must be an integer")

    result = compute_next_step(
        sequence_name=sequence,
        lead_id=lead_id,
        enrolled_on=enrolled_on,
        completed_steps=completed,
        as_of=body.get("as_of"),
    )
    return {
        "status": "ok",
        "sequence": result.sequence,
        "lead_id": result.lead_id,
        "has_pending_step": result.has_pending_step,
        "next_step": result.next_step,
        "completed_steps": result.completed_steps,
        "total_steps": result.total_steps,
        "reason_en": result.reason_en,
        "reason_ar": result.reason_ar,
        "doctrine": "prepare_draft_only_requires_founder_approval",
    }


@router.post("/queue/{queue_id}/skip")
async def skip_queue(queue_id: str, body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    reason = str(body.get("reason") or "manual_skip")[:255]
    async with async_session_factory() as session:
        try:
            q = (await session.execute(
                select(OutreachQueueRecord).where(OutreachQueueRecord.id == queue_id)
            )).scalar_one_or_none()
            if not q:
                raise HTTPException(404, "queue_not_found")
            q.status = "skipped"
            q.risk_reason = reason
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}
        try:
            await session.commit()
        except Exception as exc:  # noqa: BLE001
            await session.rollback()
            return {"status": "commit_failed", "error": str(exc)}
    return {"id": queue_id, "status": "skipped", "reason": reason}
