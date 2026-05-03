"""
Prospects router — founder-managed CRM-lite for warm-intro outreach.

The `dealix standup` CLI reads from these endpoints. Status ladder:
    identified  → messaged  → replied  → meeting  → pilot  → closed_won
                                                            ↘  closed_lost

Endpoints:
    POST   /api/v1/prospects                       Create
    GET    /api/v1/prospects                       List (filter by status, due)
    GET    /api/v1/prospects/{id}                  Read
    PATCH  /api/v1/prospects/{id}                  Update (any field)
    POST   /api/v1/prospects/{id}/advance          Move status forward + log RWU
    POST   /api/v1/prospects/{id}/note             Append a timestamped note
    GET    /api/v1/prospects/standup               Today's queue for the founder
    GET    /api/v1/prospects/funnel                Counts per status
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import func, select

from auto_client_acquisition.revenue_company_os.proof_ledger import record as record_proof
from db.models import ProspectRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/prospects", tags=["prospects"])


_STATUS_LADDER = (
    "identified", "messaged", "replied", "meeting",
    "pilot", "closed_won", "closed_lost",
)
_TERMINAL = {"closed_won", "closed_lost"}

_STATUS_TO_RWU = {
    "messaged":  "draft_created",        # outbound message went out
    "replied":   "opportunity_created",  # they engaged → real opportunity
    "meeting":   "meeting_drafted",      # call booked
    "pilot":     "approval_collected",   # they said yes to Pilot
    "closed_won": "meeting_closed",      # paid → emit closed RWU
}


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_id() -> str:
    return f"prs_{uuid.uuid4().hex[:14]}"


def _parse_dt(v) -> datetime | None:
    if not v:
        return None
    if isinstance(v, datetime):
        return v.astimezone(timezone.utc).replace(tzinfo=None) if v.tzinfo else v
    try:
        d = datetime.fromisoformat(str(v))
        return d.astimezone(timezone.utc).replace(tzinfo=None) if d.tzinfo else d
    except (ValueError, TypeError):
        return None


def _serialize(p: ProspectRecord) -> dict[str, Any]:
    return {
        "id": p.id,
        "name": p.name,
        "company": p.company,
        "role_title": p.role_title,
        "linkedin_url": p.linkedin_url,
        "contact_email": p.contact_email,
        "contact_phone": p.contact_phone,
        "sector": p.sector,
        "city": p.city,
        "relationship_type": p.relationship_type,
        "status": p.status,
        "next_step_ar": p.next_step_ar,
        "next_step_due_at": p.next_step_due_at.isoformat() if p.next_step_due_at else None,
        "last_message_at": p.last_message_at.isoformat() if p.last_message_at else None,
        "last_reply_at": p.last_reply_at.isoformat() if p.last_reply_at else None,
        "notes_ar": p.notes_ar,
        "expected_value_sar": p.expected_value_sar,
        "deal_id": p.deal_id,
        "customer_id": p.customer_id,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }


@router.post("")
async def create(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    name = str(body.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="name_required")
    rel = str(body.get("relationship_type") or "cold").lower()
    if rel not in {"cold", "warm_1st_degree", "warm_2nd_degree", "referral",
                   "ex_colleague", "inbound"}:
        rel = "cold"

    row = ProspectRecord(
        id=_new_id(),
        name=name,
        company=body.get("company") or None,
        role_title=body.get("role_title") or None,
        linkedin_url=body.get("linkedin_url") or None,
        contact_email=(body.get("contact_email") or "").lower() or None,
        contact_phone=body.get("contact_phone") or None,
        sector=body.get("sector") or None,
        city=body.get("city") or None,
        relationship_type=rel,
        status="identified",
        next_step_ar=body.get("next_step_ar") or "أرسل warm-intro DM",
        next_step_due_at=_parse_dt(body.get("next_step_due_at")) or _now(),
        notes_ar=body.get("notes_ar") or None,
        expected_value_sar=float(body.get("expected_value_sar") or 499.0),
        actor=str(body.get("actor") or "founder"),
        meta_json=dict(body.get("meta") or {}),
    )
    async with get_session() as session:
        session.add(row)
        await session.commit()
    return _serialize(row)


@router.get("")
async def list_prospects(
    status: str | None = Query(default=None),
    due_by_hours: int | None = Query(default=None, description="Show prospects with next_step_due_at within N hours"),
    limit: int = Query(default=50, ge=1, le=500),
) -> dict[str, Any]:
    async with get_session() as session:
        stmt = select(ProspectRecord).order_by(ProspectRecord.next_step_due_at.asc())
        if status:
            stmt = stmt.where(ProspectRecord.status == status)
        if due_by_hours is not None:
            cutoff = _now() + timedelta(hours=due_by_hours)
            stmt = stmt.where(ProspectRecord.next_step_due_at <= cutoff)
        rows = list((await session.execute(stmt.limit(limit))).scalars().all())
    return {"count": len(rows), "prospects": [_serialize(r) for r in rows]}


@router.get("/standup")
async def standup() -> dict[str, Any]:
    """Today's founder queue. The single endpoint `dealix standup` reads."""
    now = _now()
    async with get_session() as session:
        # 1. Due today (next_step_due_at <= end of today)
        eod = now.replace(hour=23, minute=59, second=59)
        due_today = list((await session.execute(
            select(ProspectRecord)
            .where(
                ProspectRecord.next_step_due_at <= eod,
                ProspectRecord.status.notin_(("closed_won", "closed_lost")),
            )
            .order_by(ProspectRecord.next_step_due_at.asc())
            .limit(20)
        )).scalars().all())

        # 2. Stale "messaged" — no reply >3 days, suggest follow-up
        cutoff_3d = now - timedelta(days=3)
        stale_messaged = list((await session.execute(
            select(ProspectRecord)
            .where(
                ProspectRecord.status == "messaged",
                ProspectRecord.last_message_at <= cutoff_3d,
            )
            .order_by(ProspectRecord.last_message_at.asc())
            .limit(10)
        )).scalars().all())

        # 3. Wins yesterday (status changed to closed_won in last 24h)
        cutoff_1d = now - timedelta(days=1)
        wins_yesterday = list((await session.execute(
            select(ProspectRecord)
            .where(
                ProspectRecord.status == "closed_won",
                ProspectRecord.updated_at >= cutoff_1d,
            )
            .order_by(ProspectRecord.updated_at.desc())
            .limit(5)
        )).scalars().all())

        # 4. Funnel snapshot
        funnel_q = await session.execute(
            select(ProspectRecord.status, func.count(ProspectRecord.id))
            .group_by(ProspectRecord.status)
        )
        funnel = {status: int(count) for status, count in funnel_q.all()}

    return {
        "as_of": now.isoformat(),
        "due_today": [_serialize(r) for r in due_today],
        "stale_messaged": [_serialize(r) for r in stale_messaged],
        "wins_yesterday": [_serialize(r) for r in wins_yesterday],
        "funnel": funnel,
        "advice_ar": (
            "إذا 0 ردود رغم 30 رسالة → بدّل القناة (WhatsApp 1st-degree)."
            if (funnel.get("messaged", 0) >= 30 and funnel.get("replied", 0) == 0)
            else "ابدأ بالأهم: ابعث رسائل due_today أولاً، ثم تابع stale_messaged."
        ),
    }


@router.get("/funnel")
async def funnel() -> dict[str, Any]:
    async with get_session() as session:
        rows = (await session.execute(
            select(ProspectRecord.status, func.count(ProspectRecord.id),
                   func.coalesce(func.sum(ProspectRecord.expected_value_sar), 0.0))
            .group_by(ProspectRecord.status)
        )).all()
    out = {s: {"count": int(c), "expected_value_sar": float(v)} for s, c, v in rows}
    # Always include all stages so dashboards don't have holes
    for s in _STATUS_LADDER:
        out.setdefault(s, {"count": 0, "expected_value_sar": 0.0})
    return {"funnel": out}


@router.get("/{prospect_id}")
async def read(prospect_id: str) -> dict[str, Any]:
    async with get_session() as session:
        row = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.id == prospect_id)
        )).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="prospect_not_found")
    return _serialize(row)


@router.patch("/{prospect_id}")
async def update(prospect_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    fields_mut = {
        "name", "company", "role_title", "linkedin_url", "contact_email",
        "contact_phone", "sector", "city", "relationship_type",
        "next_step_ar", "notes_ar", "expected_value_sar", "deal_id",
    }
    async with get_session() as session:
        row = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.id == prospect_id)
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="prospect_not_found")
        for k, v in body.items():
            if k in fields_mut:
                setattr(row, k, v)
        if "next_step_due_at" in body:
            row.next_step_due_at = _parse_dt(body["next_step_due_at"])
        await session.commit()
        return _serialize(row)


@router.post("/{prospect_id}/advance")
async def advance(prospect_id: str, body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Move status forward by ONE step (or jump to a target status).

    Body (optional):
        target_status: "messaged"|"replied"|"meeting"|"pilot"|"closed_won"|"closed_lost"
        next_step_ar: human note for the next step
        next_step_due_at: ISO datetime
    Emits a Proof Event when status implies one (see _STATUS_TO_RWU).
    """
    target = (body or {}).get("target_status")
    async with get_session() as session:
        row = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.id == prospect_id)
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="prospect_not_found")
        if row.status in _TERMINAL:
            raise HTTPException(status_code=400, detail=f"prospect_already_terminal:{row.status}")

        if target:
            if target not in _STATUS_LADDER:
                raise HTTPException(status_code=400, detail=f"unknown_target_status:{target}")
            new_status = target
        else:
            idx = _STATUS_LADDER.index(row.status)
            if idx + 1 >= len(_STATUS_LADDER):
                raise HTTPException(status_code=400, detail="already_at_end")
            new_status = _STATUS_LADDER[idx + 1]

        old_status = row.status
        row.status = new_status

        # Side-effect timestamps
        if new_status == "messaged":
            row.last_message_at = _now()
        if new_status == "replied":
            row.last_reply_at = _now()

        if (body or {}).get("next_step_ar"):
            row.next_step_ar = body["next_step_ar"]
        if (body or {}).get("next_step_due_at"):
            row.next_step_due_at = _parse_dt(body["next_step_due_at"])

        unit = _STATUS_TO_RWU.get(new_status)
        proof_id: str | None = None
        if unit:
            try:
                proof = await record_proof(
                    session,
                    unit_type=unit,
                    customer_id=row.customer_id,
                    revenue_impact_sar=(
                        float(row.expected_value_sar) if new_status == "closed_won"
                        else None
                    ),
                    actor="prospects_router",
                    risk_level="low",
                    meta={
                        "prospect_id": row.id,
                        "from": old_status,
                        "to": new_status,
                        "company": row.company,
                    },
                )
                proof_id = proof.id
            except ValueError:
                pass
        await session.commit()
    return {
        "prospect_id": prospect_id,
        "from": old_status,
        "to": new_status,
        "rwu_emitted": unit,
        "proof_event_id": proof_id,
    }


@router.post("/{prospect_id}/note")
async def add_note(prospect_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    note = str(body.get("note_ar") or "").strip()
    if not note:
        raise HTTPException(status_code=400, detail="note_ar_required")
    async with get_session() as session:
        row = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.id == prospect_id)
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="prospect_not_found")
        ts = _now().isoformat()
        prev = row.notes_ar or ""
        row.notes_ar = (f"{prev}\n[{ts}] {note}" if prev else f"[{ts}] {note}")[:8000]
        await session.commit()
        return _serialize(row)
