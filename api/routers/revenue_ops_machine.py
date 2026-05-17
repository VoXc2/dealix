"""Revenue Ops Machine API — the governed online sales funnel.

Exposes the 16-state funnel: capture a lead, qualify it by A/B/C/D grade, move
it through booking, scope/invoice and delivery/proof. Every draft the machine
produces is gated and queued for founder approval — no endpoint here sends
anything externally.

All routes are admin-key gated (``X-Admin-API-Key``).
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.api_key import require_admin_key
from auto_client_acquisition.proof_ledger.factory import get_default_ledger
from auto_client_acquisition.revenue_ops_machine import (
    FunnelContext,
    FunnelState,
    HandlerResult,
    IllegalTransition,
    RevenueOpsMachineError,
    blocked_proof_events,
    booking_ops,
    delivery_proof_ops,
    gate_specs,
    lead_capture_ops,
    load_context,
    new_context,
    qualification_ops,
    sales_call_ops,
    save_context,
    scope_invoice_ops,
    to_outreach_records,
)
from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    HARD_RULES,
    MILESTONE_GUARDS,
    TRANSITIONS,
)
from db.models import LeadRecord
from db.session import get_db

router = APIRouter(
    prefix="/api/v1/revenue-ops",
    tags=["revenue-ops-machine"],
    dependencies=[Depends(require_admin_key)],
)
log = logging.getLogger(__name__)


# ── helpers ──────────────────────────────────────────────────────────────────
def _parse_budget(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return float(digits) if digits else None


async def _load_lead(session: AsyncSession, lead_id: str) -> LeadRecord:
    result = await session.execute(
        select(LeadRecord).where(LeadRecord.id == lead_id, LeadRecord.deleted_at.is_(None))
    )
    lead = result.scalar_one_or_none()
    if lead is None:
        raise HTTPException(status_code=404, detail=f"lead not found: {lead_id}")
    return lead


def _apply_result(
    session: AsyncSession,
    lead: LeadRecord,
    ctx: FunnelContext,
    result: HandlerResult,
) -> list[dict[str, Any]]:
    """Gate + queue the handler's drafts, record proof events, persist context.

    Returns a JSON-friendly summary of every draft (queued or blocked). Never
    sends; queued rows are always ``status="queued"``, ``approval_required``.
    """
    gated = gate_specs(result.drafts)
    records = to_outreach_records(gated, lead.id)
    for rec in records:
        session.add(rec)
        ctx.queued_draft_ids.append(rec.id)

    ledger = get_default_ledger()
    for event in [*result.proof_events, *blocked_proof_events(gated)]:
        try:
            ledger.record(event)
        except Exception as exc:  # noqa: BLE001 - ledger hiccup must not 500 the funnel
            log.warning("revenue_ops_proof_record_failed:%s", type(exc).__name__)

    lead.meta_json = save_context(lead.meta_json, ctx)
    lead.status = str(ctx.funnel_state)[:32]
    if result.notes:
        log.info("revenue_ops_handler lead=%s notes=%s", lead.id, result.notes)

    rec_by_kind = iter(records)
    summary: list[dict[str, Any]] = []
    for g in gated:
        entry: dict[str, Any] = {
            "kind": g.spec.kind,
            "channel": g.spec.channel,
            "decision": str(g.decision),
            "blocked": g.blocked,
        }
        if g.blocked:
            entry["issues"] = list(g.issues)
        else:
            entry["queue_id"] = next(rec_by_kind).id
            entry["status"] = "queued"
            entry["approval_required"] = True
        summary.append(entry)
    return summary


def _lead_payload(
    lead: LeadRecord, ctx: FunnelContext, drafts: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "lead_id": lead.id,
        "funnel_state": str(ctx.funnel_state),
        "legacy_stage": ctx.legacy_stage,
        "abcd_grade": ctx.abcd_grade,
        "abcd_score": ctx.abcd_score,
        "recommended_offer_id": ctx.recommended_offer_id,
        "version": ctx.version,
        "queued_draft_count": len(ctx.queued_draft_ids),
    }
    if drafts is not None:
        payload["drafts"] = drafts
    return payload


# ── read-only ────────────────────────────────────────────────────────────────
@router.get("/states")
async def list_states() -> dict[str, Any]:
    """The 16 funnel states, the transition graph, and the hard ordering rules."""
    return {
        "states": [str(s) for s in FunnelState],
        "transitions": {
            str(src): sorted(str(t) for t in targets) for src, targets in TRANSITIONS.items()
        },
        "milestone_guards": {
            str(target): str(required) for target, required in MILESTONE_GUARDS.items()
        },
        "hard_rules": list(HARD_RULES),
        "terminal_success": "retainer_candidate",
        "recoverable_terminal": "closed_lost",
    }


@router.get("/lead/{lead_id}")
async def get_lead(lead_id: str, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """Current funnel state + A/B/C/D grade for one lead."""
    lead = await _load_lead(session, lead_id)
    ctx = load_context(lead.id, lead.meta_json)
    return _lead_payload(lead, ctx)


# ── 1. Lead Capture ──────────────────────────────────────────────────────────
@router.post("/capture")
async def capture(
    body: dict[str, Any] = Body(...),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Lead-capture form -> scored lead, recommended offer, queued drafts."""
    lead_id = f"lead_{uuid.uuid4().hex[:24]}"
    lead = LeadRecord(
        id=lead_id,
        source=str(body.get("source") or "website")[:32],
        company_name=str(body.get("company") or body.get("company_name") or "")[:255],
        contact_name=str(body.get("contact_name") or body.get("name") or "")[:255],
        contact_email=(str(body["contact_email"])[:255] if body.get("contact_email") else None),
        contact_phone=(str(body["contact_phone"])[:32] if body.get("contact_phone") else None),
        sector=(str(body["sector"])[:64] if body.get("sector") else None),
        region=(str(body["region"])[:128] if body.get("region") else None),
        company_size=(str(body["company_size"])[:32] if body.get("company_size") else None),
        budget=_parse_budget(body.get("budget")),
        message=(str(body["message"]) if body.get("message") else None),
        pain_points=body.get("pain_points") if isinstance(body.get("pain_points"), list) else [],
    )
    ctx = new_context(lead_id)
    result = lead_capture_ops(ctx, body)
    session.add(lead)
    drafts = _apply_result(session, lead, ctx, result)
    await session.flush()
    return _lead_payload(lead, ctx, drafts)


# ── 2-6. Stage handlers ──────────────────────────────────────────────────────
async def _run_handler(session: AsyncSession, lead_id: str, run) -> dict[str, Any]:
    lead = await _load_lead(session, lead_id)
    ctx = load_context(lead.id, lead.meta_json)
    try:
        result = run(ctx)
    except IllegalTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RevenueOpsMachineError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    drafts = _apply_result(session, lead, ctx, result)
    return _lead_payload(lead, ctx, drafts)


@router.post("/qualify")
async def qualify(
    body: dict[str, Any] = Body(default={}),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Route a captured lead to qualified_A / qualified_B / nurture."""
    lead_id = str(body.get("lead_id") or "")
    if not lead_id:
        raise HTTPException(status_code=422, detail="lead_id required")
    return await _run_handler(session, lead_id, qualification_ops)


@router.post("/booking")
async def booking(
    body: dict[str, Any] = Body(...),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """``step`` = ``book`` (-> meeting_booked) or ``done`` (-> meeting_done)."""
    lead_id = str(body.get("lead_id") or "")
    step = str(body.get("step") or "")
    if not lead_id:
        raise HTTPException(status_code=422, detail="lead_id required")
    return await _run_handler(session, lead_id, lambda ctx: booking_ops(ctx, step))


@router.post("/sales-call")
async def sales_call(
    body: dict[str, Any] = Body(default={}),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """After the call: meeting_done -> scope_requested."""
    lead_id = str(body.get("lead_id") or "")
    if not lead_id:
        raise HTTPException(status_code=422, detail="lead_id required")
    return await _run_handler(session, lead_id, sales_call_ops)


@router.post("/scope-invoice")
async def scope_invoice(
    body: dict[str, Any] = Body(...),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """``step`` = ``scope`` -> ``invoice`` -> ``paid``."""
    lead_id = str(body.get("lead_id") or "")
    step = str(body.get("step") or "")
    if not lead_id:
        raise HTTPException(status_code=422, detail="lead_id required")
    return await _run_handler(session, lead_id, lambda ctx: scope_invoice_ops(ctx, step))


@router.post("/delivery-proof")
async def delivery_proof(
    body: dict[str, Any] = Body(...),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """``step`` = ``start`` -> ``proof`` -> ``upsell`` -> ``retainer``."""
    lead_id = str(body.get("lead_id") or "")
    step = str(body.get("step") or "")
    if not lead_id:
        raise HTTPException(status_code=422, detail="lead_id required")
    return await _run_handler(session, lead_id, lambda ctx: delivery_proof_ops(ctx, step))


# ── manual transition ────────────────────────────────────────────────────────
@router.post("/advance")
async def advance_state(
    body: dict[str, Any] = Body(...),
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Manually move a lead to ``target_state``. 409 if the transition is illegal."""
    lead_id = str(body.get("lead_id") or "")
    target_raw = str(body.get("target_state") or "")
    if not lead_id or not target_raw:
        raise HTTPException(status_code=422, detail="lead_id and target_state required")
    try:
        target = FunnelState(target_raw)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"unknown funnel state: {target_raw}") from exc

    lead = await _load_lead(session, lead_id)
    ctx = load_context(lead.id, lead.meta_json)
    try:
        ctx.transition_to(target)
    except IllegalTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    lead.meta_json = save_context(lead.meta_json, ctx)
    lead.status = str(ctx.funnel_state)[:32]
    return _lead_payload(lead, ctx)
