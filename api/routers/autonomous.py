"""
Autonomous Revenue Operator endpoints — conversations, deals, tasks, dashboard.

Production-safe additive endpoints. Does NOT modify existing /leads or /prospect routes.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import select, func

from db.models import ConversationRecord, DealRecord, LeadRecord, TaskRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1", tags=["autonomous"])
log = logging.getLogger(__name__)


def _new_id(prefix: str = "rec") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ── Conversations ───────────────────────────────────────────────

@router.post("/conversations")
async def create_conversation(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Log an inbound message + outbound auto-response.
    Body: {lead_id?, channel, sender, inbound_message, outbound_response?,
           classification?, next_action?, escalation_required?, auto_sent?}
    """
    channel = str(body.get("channel") or "").strip().lower()
    inbound = str(body.get("inbound_message") or "").strip()
    if not channel or not inbound:
        raise HTTPException(status_code=400, detail="channel_and_inbound_required")

    rec_id = _new_id("conv")
    async with get_session() as session:
        rec = ConversationRecord(
            id=rec_id,
            lead_id=str(body.get("lead_id")) if body.get("lead_id") else None,
            channel=channel,
            sender=str(body.get("sender") or "") or None,
            inbound_message=inbound[:8000],
            outbound_response=str(body.get("outbound_response") or "")[:8000] or None,
            classification=str(body.get("classification") or "") or None,
            sentiment=str(body.get("sentiment") or "") or None,
            next_action=str(body.get("next_action") or "") or None,
            escalation_required=bool(body.get("escalation_required", False)),
            auto_sent=bool(body.get("auto_sent", False)),
        )
        session.add(rec)
        await session.commit()

    return {"id": rec_id, "status": "logged", "created_at": _utcnow().isoformat()}


@router.get("/conversations")
async def list_conversations(
    lead_id: str | None = None,
    channel: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    limit = max(1, min(100, limit))
    async with get_session() as session:
        stmt = select(ConversationRecord).order_by(ConversationRecord.created_at.desc()).limit(limit)
        if lead_id:
            stmt = stmt.where(ConversationRecord.lead_id == lead_id)
        if channel:
            stmt = stmt.where(ConversationRecord.channel == channel.lower())
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return {
            "count": len(rows),
            "items": [
                {
                    "id": r.id,
                    "lead_id": r.lead_id,
                    "channel": r.channel,
                    "sender": r.sender,
                    "inbound_message": r.inbound_message[:300],
                    "outbound_response": (r.outbound_response or "")[:300],
                    "classification": r.classification,
                    "next_action": r.next_action,
                    "escalation_required": r.escalation_required,
                    "auto_sent": r.auto_sent,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ],
        }


# ── Deals (POST + PATCH) ────────────────────────────────────────

@router.post("/deals")
async def create_deal(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Create a deal record (e.g., when prospect verbally agrees + invoice issued).
    Body: {lead_id, stage?, amount?, currency?, hubspot_deal_id?}
    """
    lead_id = str(body.get("lead_id") or "").strip()
    if not lead_id:
        raise HTTPException(status_code=400, detail="lead_id_required")

    deal_id = _new_id("deal")
    async with get_session() as session:
        deal = DealRecord(
            id=deal_id,
            lead_id=lead_id,
            hubspot_deal_id=body.get("hubspot_deal_id") or None,
            hubspot_contact_id=body.get("hubspot_contact_id") or None,
            amount=float(body.get("amount") or 0.0),
            currency=str(body.get("currency") or "SAR"),
            stage=str(body.get("stage") or "new"),
        )
        session.add(deal)
        await session.commit()
    return {"id": deal_id, "stage": "new", "created_at": _utcnow().isoformat()}


@router.patch("/deals/{deal_id}")
async def update_deal(deal_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Update deal stage/amount/payment_status. Common path: payment_requested → paid.
    Body: any subset of {stage, amount, currency}
    """
    async with get_session() as session:
        result = await session.execute(select(DealRecord).where(DealRecord.id == deal_id))
        deal = result.scalar_one_or_none()
        if not deal:
            raise HTTPException(status_code=404, detail="deal_not_found")
        if "stage" in body:
            deal.stage = str(body["stage"])
        if "amount" in body:
            deal.amount = float(body["amount"])
        if "currency" in body:
            deal.currency = str(body["currency"])
        if "hubspot_deal_id" in body:
            deal.hubspot_deal_id = str(body["hubspot_deal_id"]) or None
        await session.commit()
    return {"id": deal_id, "stage": deal.stage, "updated_at": _utcnow().isoformat()}


@router.get("/deals")
async def list_deals(stage: str | None = None, limit: int = 20) -> dict[str, Any]:
    limit = max(1, min(100, limit))
    async with get_session() as session:
        stmt = select(DealRecord).order_by(DealRecord.created_at.desc()).limit(limit)
        if stage:
            stmt = stmt.where(DealRecord.stage == stage)
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return {
            "count": len(rows),
            "items": [
                {
                    "id": r.id,
                    "lead_id": r.lead_id,
                    "stage": r.stage,
                    "amount": r.amount,
                    "currency": r.currency,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ],
        }


# ── Tasks ───────────────────────────────────────────────────────

@router.post("/tasks")
async def create_task(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Schedule a follow-up task.
    Body: {lead_id?, deal_id?, task_type, due_at?(iso), notes?, owner?}
    """
    task_type = str(body.get("task_type") or "follow_up").strip()
    if not task_type:
        raise HTTPException(status_code=400, detail="task_type_required")

    due_at = _utcnow() + timedelta(days=2)  # default +2d
    if body.get("due_at"):
        try:
            due_at = datetime.fromisoformat(str(body["due_at"]).replace("Z", "+00:00"))
        except Exception:
            pass

    task_id = _new_id("task")
    async with get_session() as session:
        task = TaskRecord(
            id=task_id,
            lead_id=body.get("lead_id") or None,
            deal_id=body.get("deal_id") or None,
            task_type=task_type,
            due_at=due_at,
            status="pending",
            owner=str(body.get("owner") or "auto"),
            notes=str(body.get("notes") or "") or None,
        )
        session.add(task)
        await session.commit()
    return {"id": task_id, "status": "pending", "due_at": due_at.isoformat()}


@router.patch("/tasks/{task_id}")
async def update_task(task_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    async with get_session() as session:
        result = await session.execute(select(TaskRecord).where(TaskRecord.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="task_not_found")
        if "status" in body:
            task.status = str(body["status"])
            if task.status == "done":
                task.completed_at = _utcnow()
        if "notes" in body:
            task.notes = str(body["notes"])[:2000]
        if "due_at" in body:
            try:
                task.due_at = datetime.fromisoformat(str(body["due_at"]).replace("Z", "+00:00"))
            except Exception:
                pass
        await session.commit()
    return {"id": task_id, "status": task.status}


@router.get("/tasks")
async def list_tasks(status: str = "pending", limit: int = 20) -> dict[str, Any]:
    limit = max(1, min(100, limit))
    async with get_session() as session:
        result = await session.execute(
            select(TaskRecord)
            .where(TaskRecord.status == status)
            .order_by(TaskRecord.due_at.asc())
            .limit(limit)
        )
        rows = result.scalars().all()
        return {
            "count": len(rows),
            "items": [
                {
                    "id": r.id,
                    "lead_id": r.lead_id,
                    "deal_id": r.deal_id,
                    "task_type": r.task_type,
                    "due_at": r.due_at.isoformat() if r.due_at else None,
                    "status": r.status,
                    "owner": r.owner,
                    "notes": r.notes,
                }
                for r in rows
            ],
        }


# ── Dashboard metrics ───────────────────────────────────────────

@router.get("/dashboard/metrics")
async def dashboard_metrics() -> dict[str, Any]:
    """
    Public/internal dashboard summary — counts + top of pipeline.
    """
    async with get_session() as session:
        leads_total = (await session.execute(select(func.count()).select_from(LeadRecord))).scalar() or 0
        leads_new = (await session.execute(select(func.count()).select_from(LeadRecord).where(LeadRecord.status == "new"))).scalar() or 0
        leads_qualified = (await session.execute(select(func.count()).select_from(LeadRecord).where(LeadRecord.status == "qualified"))).scalar() or 0
        leads_won = (await session.execute(select(func.count()).select_from(LeadRecord).where(LeadRecord.status == "won"))).scalar() or 0

        deals_total = (await session.execute(select(func.count()).select_from(DealRecord))).scalar() or 0
        deals_paid_count = (await session.execute(select(func.count()).select_from(DealRecord).where(DealRecord.stage == "paid"))).scalar() or 0
        revenue_paid = (await session.execute(
            select(func.coalesce(func.sum(DealRecord.amount), 0.0)).where(DealRecord.stage == "paid")
        )).scalar() or 0.0

        conversations_total = (await session.execute(select(func.count()).select_from(ConversationRecord))).scalar() or 0
        conversations_today = (await session.execute(
            select(func.count()).select_from(ConversationRecord).where(
                ConversationRecord.created_at >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            )
        )).scalar() or 0

        tasks_pending = (await session.execute(
            select(func.count()).select_from(TaskRecord).where(TaskRecord.status == "pending")
        )).scalar() or 0
        tasks_overdue = (await session.execute(
            select(func.count()).select_from(TaskRecord).where(
                TaskRecord.status == "pending", TaskRecord.due_at < _utcnow()
            )
        )).scalar() or 0

    return {
        "as_of": _utcnow().isoformat(),
        "leads": {
            "total": int(leads_total),
            "new": int(leads_new),
            "qualified": int(leads_qualified),
            "won": int(leads_won),
        },
        "deals": {
            "total": int(deals_total),
            "paid": int(deals_paid_count),
            "revenue_sar_paid": float(revenue_paid),
        },
        "conversations": {
            "total": int(conversations_total),
            "today": int(conversations_today),
        },
        "tasks": {
            "pending": int(tasks_pending),
            "overdue": int(tasks_overdue),
        },
    }
