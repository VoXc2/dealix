"""
Actions router — unified Approval Queue across all customers.

The queue is the single human bottleneck per the Doctrine. Every
ProofEventRecord with `approval_required=True AND approved=False` is a
pending decision waiting on the founder/operator. This router exposes:

    GET   /api/v1/actions/pending
        Optional filters: ?customer_id=cus_xxx, ?max_age_hours=24
        Returns {count, items:[{...with age_hours}]}

    POST  /api/v1/actions/{event_id}/approve
        body: {note?: "...", actor?: "founder"}
        Sets approved=True, audit-logs the decision.

    POST  /api/v1/actions/{event_id}/reject
        body: {reason?: "...", actor?: "founder"}
        Keeps approved=False, stamps meta.rejected_at + reason.

Defensive: per-query session, _errors map on failure.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import desc, select

from db.models import ProofEventRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/actions", tags=["actions"])

log = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _serialize_event(e: ProofEventRecord, now: datetime) -> dict[str, Any]:
    occurred = e.occurred_at
    age_hours = 0.0
    if occurred:
        age_hours = round((now - occurred).total_seconds() / 3600.0, 1)
    return {
        "event_id": e.id,
        "unit_type": e.unit_type,
        "label_ar": e.label_ar,
        "customer_id": e.customer_id,
        "partner_id": e.partner_id,
        "service_id": e.service_id,
        "session_id": e.session_id,
        "actor": e.actor,
        "risk_level": e.risk_level,
        "revenue_impact_sar": float(e.revenue_impact_sar or 0.0),
        "occurred_at": occurred.isoformat() if occurred else None,
        "age_hours": age_hours,
        "approval_required": bool(e.approval_required),
        "approved": bool(e.approved),
        "meta": dict(e.meta_json or {}),
    }


@router.get("/pending")
async def list_pending(
    customer_id: str | None = Query(default=None),
    max_age_hours: int | None = Query(default=None, ge=1, le=720),
    limit: int = Query(default=50, ge=1, le=500),
) -> dict[str, Any]:
    """List all proof events that need human approval. Defensive."""
    errors: dict[str, str] = {}
    items: list[dict[str, Any]] = []
    now = _now()

    try:
        async with get_session() as s:
            stmt = (
                select(ProofEventRecord)
                .where(
                    ProofEventRecord.approval_required == True,  # noqa: E712
                    ProofEventRecord.approved == False,  # noqa: E712
                )
                .order_by(desc(ProofEventRecord.occurred_at))
            )
            if customer_id:
                stmt = stmt.where(ProofEventRecord.customer_id == customer_id)
            if max_age_hours is not None:
                cutoff = now - timedelta(hours=max_age_hours)
                stmt = stmt.where(ProofEventRecord.occurred_at >= cutoff)
            rows = list((await s.execute(stmt.limit(limit))).scalars().all())
        items = [_serialize_event(r, now) for r in rows]
    except Exception as exc:  # noqa: BLE001
        errors["fetch"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    response: dict[str, Any] = {
        "count": len(items),
        "as_of": now.isoformat(),
        "items": items,
    }
    if errors:
        response["_errors"] = errors
    return response


@router.post("/{event_id}/approve")
async def approve(event_id: str, body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Approve a pending action + (if gates allow) auto-execute it.

    Rules:
      1. Mark event approved=True, audit-log who approved + when.
      2. Call auto_executor.auto_execute_approved(event):
         - If channel allowed AND gate open → actually send (Resend, WA, etc.)
         - If gate closed → kept as approved-but-not-sent (founder sends manually)
         - If hard refusal channel (cold WA / linkedin auto-DM) → never executed
      3. Append execution result to meta_json (audit trail).
    """
    actor = str((body or {}).get("actor") or "founder")
    note = (body or {}).get("note") or None
    skip_auto_execute = bool((body or {}).get("skip_auto_execute", False))

    async with get_session() as session:
        row = (await session.execute(
            select(ProofEventRecord).where(ProofEventRecord.id == event_id)
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="event_not_found")
        if row.approved:
            return {"status": "already_approved", "event_id": event_id}
        row.approved = True
        meta = dict(row.meta_json or {})
        meta["approved_at"] = _now().isoformat()
        meta["approved_by"] = actor
        if note:
            meta["approval_note"] = str(note)[:500]
        row.meta_json = meta
        await session.commit()
        log.info(
            "action_approved event_id=%s actor=%s unit_type=%s customer_id=%s",
            event_id, actor, row.unit_type, row.customer_id,
        )

        # Attempt auto-execution unless caller opts out
        execution: dict[str, Any] = {"executed": False, "skipped": True, "reason": "skip_auto_execute=true"}
        if not skip_auto_execute:
            try:
                from auto_client_acquisition.execution.auto_executor import (
                    auto_execute_approved,
                )
                result = await auto_execute_approved(row)
                execution = {
                    "executed": result.executed,
                    "channel": result.channel,
                    "transport": result.transport,
                    "provider_id": result.provider_id,
                    "reason": result.reason,
                    "safe_to_retry": result.safe_to_retry,
                }
                # Persist execution result back into meta
                meta["auto_execution"] = execution
                row.meta_json = meta
                await session.commit()
                log.info(
                    "auto_execute event_id=%s executed=%s channel=%s reason=%s",
                    event_id, result.executed, result.channel, result.reason,
                )
            except Exception as exc:  # noqa: BLE001
                log.warning("auto_execute_failed event_id=%s err=%s", event_id, exc)
                execution = {"executed": False, "error": str(exc)[:200]}

        return {
            "status": "approved",
            "event_id": event_id,
            "unit_type": row.unit_type,
            "customer_id": row.customer_id,
            "approved_at": meta["approved_at"],
            "auto_execution": execution,
        }


@router.post("/{event_id}/reject")
async def reject(event_id: str, body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Reject a pending action. Keeps approved=False, stamps reason."""
    actor = str((body or {}).get("actor") or "founder")
    reason = (body or {}).get("reason") or "no_reason_given"

    async with get_session() as session:
        row = (await session.execute(
            select(ProofEventRecord).where(ProofEventRecord.id == event_id)
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="event_not_found")
        meta = dict(row.meta_json or {})
        meta["rejected_at"] = _now().isoformat()
        meta["rejected_by"] = actor
        meta["rejection_reason"] = str(reason)[:500]
        row.meta_json = meta
        # approval_required stays True so it disappears from the queue but
        # remains auditable. We toggle approval_required=False to remove it
        # from /pending.
        row.approval_required = False
        await session.commit()
        log.info(
            "action_rejected event_id=%s actor=%s reason=%s",
            event_id, actor, str(reason)[:80],
        )
        return {
            "status": "rejected",
            "event_id": event_id,
            "reason": str(reason)[:500],
            "rejected_at": meta["rejected_at"],
        }


@router.get("/funnel")
async def actions_funnel() -> dict[str, Any]:
    """Approval-queue health snapshot — count + revenue-at-stake per status."""
    now = _now()
    async with get_session() as s:
        pending = list((await s.execute(
            select(ProofEventRecord).where(
                ProofEventRecord.approval_required == True,  # noqa: E712
                ProofEventRecord.approved == False,  # noqa: E712
            )
        )).scalars().all())
        approved_recent = list((await s.execute(
            select(ProofEventRecord).where(
                ProofEventRecord.approved == True,  # noqa: E712
                ProofEventRecord.occurred_at >= now - timedelta(days=7),
            )
        )).scalars().all())
    return {
        "as_of": now.isoformat(),
        "pending": {
            "count": len(pending),
            "revenue_at_stake_sar": round(sum(float(e.revenue_impact_sar or 0) for e in pending), 2),
            "by_unit": _group_count(pending),
        },
        "approved_last_7d": {
            "count": len(approved_recent),
            "revenue_realized_sar": round(sum(float(e.revenue_impact_sar or 0) for e in approved_recent), 2),
            "by_unit": _group_count(approved_recent),
        },
    }


def _group_count(events) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in events:
        out[e.unit_type] = out.get(e.unit_type, 0) + 1
    return out
