"""
Meetings router — log meetings + return the daily meeting-intelligence brief.

Endpoints:
    POST /api/v1/meetings/log
        body: {customer_id?, lead_id?, deal_id?, occurred_at?,
               duration_minutes?, channel?, outcome, notes_ar?,
               next_action_ar?, follow_up_due_at?}
        Records one MeetingRecord. Emits meeting_held RWU when
        outcome == "held"|"follow_up_required". Emits meeting_closed
        RWU when outcome == "closed_won".

    POST /api/v1/meetings/closed
        Convenience wrapper that forces outcome=closed_won and emits
        meeting_closed RWU + sets revenue_impact from body.deal_amount_sar.

    GET  /api/v1/meetings/brief?role=meeting_intelligence
        Defensive — returns the daily brief from the
        Call & Meeting Intelligence OS, never 500s.

    GET  /api/v1/meetings/recent?days=7
        Lists last N days of meetings (read-only).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.call_meeting_intelligence_os import (
    build_brief as build_meeting_brief,
)
from auto_client_acquisition.revenue_company_os.proof_ledger import record as record_proof
from db.models import MeetingRecord, ProofEventRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/meetings", tags=["meetings"])


_VALID_OUTCOMES = {
    "held", "closed_won", "closed_lost",
    "follow_up_required", "rescheduled", "no_show",
}
_VALID_CHANNELS = {"meet", "zoom", "phone", "in_person", "whatsapp_call"}


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _parse_dt(v: str | None) -> datetime | None:
    if not v:
        return None
    try:
        d = datetime.fromisoformat(v)
        return d.astimezone(timezone.utc).replace(tzinfo=None) if d.tzinfo else d
    except (ValueError, TypeError):
        return None


def _new_id() -> str:
    return f"mtg_{uuid.uuid4().hex[:14]}"


def _outcome_to_unit(outcome: str) -> str | None:
    if outcome == "closed_won":
        return "meeting_closed"
    if outcome in ("held", "follow_up_required", "closed_lost"):
        return "meeting_held"
    return None  # no_show / rescheduled emit nothing


@router.post("/log")
async def log_meeting(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Record a meeting outcome + emit the matching RWU."""
    outcome = str(body.get("outcome") or "held").lower()
    if outcome not in _VALID_OUTCOMES:
        raise HTTPException(
            status_code=400,
            detail=f"invalid_outcome (must be one of {sorted(_VALID_OUTCOMES)})",
        )

    channel = str(body.get("channel") or "meet").lower()
    if channel not in _VALID_CHANNELS:
        raise HTTPException(
            status_code=400,
            detail=f"invalid_channel (must be one of {sorted(_VALID_CHANNELS)})",
        )

    occurred_at = _parse_dt(body.get("occurred_at")) or _now()
    follow_up_due_at = _parse_dt(body.get("follow_up_due_at"))

    meeting = MeetingRecord(
        id=_new_id(),
        customer_id=body.get("customer_id") or None,
        lead_id=body.get("lead_id") or None,
        deal_id=body.get("deal_id") or None,
        occurred_at=occurred_at,
        duration_minutes=int(body.get("duration_minutes") or 0),
        channel=channel,
        outcome=outcome,
        notes_ar=(body.get("notes_ar") or None),
        next_action_ar=(body.get("next_action_ar") or None),
        follow_up_due_at=follow_up_due_at,
        actor=str(body.get("actor") or "sales"),
        meta_json=dict(body.get("meta") or {}),
    )

    proof_id: str | None = None
    unit_type = _outcome_to_unit(outcome)

    async with get_session() as session:
        session.add(meeting)
        if unit_type is not None:
            try:
                # Closed-won meetings: revenue_impact from body if provided,
                # else default base impact (5000 SAR).
                rev_impact = None
                if outcome == "closed_won":
                    deal_amount = body.get("deal_amount_sar")
                    if deal_amount is not None:
                        rev_impact = float(deal_amount)
                proof = await record_proof(
                    session,
                    unit_type=unit_type,
                    customer_id=meeting.customer_id,
                    revenue_impact_sar=rev_impact,
                    actor=meeting.actor,
                    risk_level="low",
                    meta={"meeting_id": meeting.id, "outcome": outcome, "channel": channel},
                )
                proof_id = proof.id
                meeting.proof_event_id = proof_id
            except ValueError as exc:  # noqa: BLE001
                raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "id": meeting.id,
        "outcome": outcome,
        "occurred_at": meeting.occurred_at.isoformat(),
        "follow_up_due_at": (
            meeting.follow_up_due_at.isoformat() if meeting.follow_up_due_at else None
        ),
        "proof_event_id": proof_id,
        "rwu_emitted": unit_type,
    }


@router.post("/closed")
async def log_closed(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Convenience wrapper — forces outcome=closed_won."""
    body = dict(body or {})
    body["outcome"] = "closed_won"
    return await log_meeting(body)


@router.get("/brief")
async def brief(
    role: str = Query(default="meeting_intelligence"),
    days: int = Query(default=7, ge=1, le=30),
) -> dict[str, Any]:
    """Defensive brief — never 500s; surfaces _errors map instead."""
    role = role.lower()
    if role != "meeting_intelligence":
        raise HTTPException(
            status_code=400,
            detail="this endpoint serves the meeting_intelligence role only",
        )
    since = _now() - timedelta(days=days)
    errors: dict[str, str] = {}
    meetings: list = []
    proof_events: list = []

    try:
        async with get_session() as s:
            meetings = list((await s.execute(
                select(MeetingRecord).where(MeetingRecord.occurred_at >= since).limit(500)
            )).scalars().all())
    except Exception as exc:  # noqa: BLE001
        errors["meetings"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    try:
        async with get_session() as s:
            proof_events = list((await s.execute(
                select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since).limit(500)
            )).scalars().all())
    except Exception as exc:  # noqa: BLE001
        errors["proof_events"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    try:
        out = build_meeting_brief(meetings, proof_events)
    except Exception as exc:  # noqa: BLE001
        errors["build"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        out = {
            "role": "meeting_intelligence",
            "brief_type": "degraded",
            "summary": {},
            "top_decisions": [],
            "blocked_today_ar": [],
        }
    if errors:
        out["_errors"] = errors
    return out


@router.get("/recent")
async def recent(days: int = Query(default=7, ge=1, le=90)) -> dict[str, Any]:
    """Read-only listing of recent meetings."""
    since = _now() - timedelta(days=days)
    async with get_session() as s:
        rows = list((await s.execute(
            select(MeetingRecord)
            .where(MeetingRecord.occurred_at >= since)
            .order_by(MeetingRecord.occurred_at.desc())
            .limit(200)
        )).scalars().all())
    return {
        "count": len(rows),
        "since": since.isoformat(),
        "meetings": [
            {
                "id": r.id,
                "customer_id": r.customer_id,
                "outcome": r.outcome,
                "channel": r.channel,
                "occurred_at": r.occurred_at.isoformat() if r.occurred_at else None,
                "follow_up_due_at": (
                    r.follow_up_due_at.isoformat() if r.follow_up_due_at else None
                ),
                "next_action_ar": r.next_action_ar,
                "duration_minutes": r.duration_minutes,
            }
            for r in rows
        ],
    }
