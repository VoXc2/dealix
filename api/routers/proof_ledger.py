"""
Proof Ledger router — append events + read aggregated Proof Pack.

Endpoints:
    POST /api/v1/proof-ledger/events
        body: {customer_id?, partner_id?, service_id?, session_id?,
               unit_type, label_ar?, revenue_impact_sar?, actor?,
               approval_required?, approved?, risk_level?, meta?}
        Records one Revenue Work Unit (or 4xx if unit_type unknown).

    POST /api/v1/proof-ledger/events/batch
        body: {items: [...]}
        Multi-event insert in one transaction.

    GET  /api/v1/proof-ledger/customer/{customer_id}/pack
        Returns the aggregated Proof Pack for a customer (last 30 days
        unless ?since=ISO is passed).

    GET  /api/v1/proof-ledger/partner/{partner_id}/pack
        Same but partner-scoped.

    GET  /api/v1/proof-ledger/units
        Catalog of supported Revenue Work Unit types (read-only).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import HTMLResponse, Response

from auto_client_acquisition.revenue_company_os.proof_ledger import (
    fetch_for_customer, fetch_for_partner, fetch_for_session, record, record_batch,
)
from auto_client_acquisition.revenue_company_os.proof_pack_builder import build_pack
from auto_client_acquisition.revenue_company_os.proof_pack_pdf import render_html, render_pdf
from auto_client_acquisition.revenue_company_os.revenue_work_units import RWU_CATALOG, known_unit_types
from db.session import get_session

router = APIRouter(prefix="/api/v1/proof-ledger", tags=["proof-ledger"])


def _parse_since(since: str | None, default_days: int = 30) -> datetime:
    if since:
        try:
            v = datetime.fromisoformat(since)
            # Normalize to naive UTC (matches DB TIMESTAMP columns)
            return v.astimezone(timezone.utc).replace(tzinfo=None) if v.tzinfo else v
        except ValueError:
            pass
    return datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=default_days)


@router.get("/units")
async def list_units() -> dict[str, Any]:
    return {
        "count": len(RWU_CATALOG),
        "units": [
            {
                "unit_type": r.unit_type,
                "label_ar": r.label_ar,
                "weight": r.weight,
                "base_revenue_impact_sar": r.base_revenue_impact_sar,
            }
            for r in RWU_CATALOG
        ],
    }


@router.post("/events")
async def add_event(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    unit_type = str(body.get("unit_type") or "")
    if unit_type not in known_unit_types():
        raise HTTPException(status_code=400, detail="unknown_unit_type")
    async with get_session() as session:
        try:
            row = await record(session, **{k: v for k, v in body.items() if k != "session_token"})
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": row.id,
        "unit_type": row.unit_type,
        "occurred_at": row.occurred_at.isoformat() if row.occurred_at else None,
    }


@router.post("/events/batch")
async def add_events(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    items = body.get("items") or []
    if not isinstance(items, list) or not items:
        raise HTTPException(status_code=400, detail="items_required")
    async with get_session() as session:
        try:
            rows = await record_batch(session, items)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"count": len(rows), "ids": [r.id for r in rows]}


@router.get("/customer/{customer_id}/pack")
async def customer_pack(
    customer_id: str,
    since: str | None = Query(default=None),
) -> dict[str, Any]:
    since_dt = _parse_since(since, default_days=30)
    async with get_session() as session:
        events = await fetch_for_customer(session, customer_id, since=since_dt, limit=2000)
    return {
        "customer_id": customer_id,
        "since": since_dt.isoformat(),
        "event_count": len(events),
        "pack": build_pack(events, customer_label=customer_id),
    }


@router.get("/partner/{partner_id}/pack")
async def partner_pack(
    partner_id: str,
    since: str | None = Query(default=None),
) -> dict[str, Any]:
    since_dt = _parse_since(since, default_days=30)
    async with get_session() as session:
        events = await fetch_for_partner(session, partner_id, since=since_dt, limit=5000)
    return {
        "partner_id": partner_id,
        "since": since_dt.isoformat(),
        "event_count": len(events),
        "pack": build_pack(events, customer_label=f"agency:{partner_id}"),
    }


@router.get("/session/{session_id}/pack")
async def session_pack(session_id: str) -> dict[str, Any]:
    async with get_session() as session:
        events = await fetch_for_session(session, session_id)
    return {
        "session_id": session_id,
        "event_count": len(events),
        "pack": build_pack(events, customer_label=f"session:{session_id}"),
    }


@router.get("/customer/{customer_id}/pack.html", response_class=HTMLResponse)
async def customer_pack_html(
    customer_id: str,
    since: str | None = Query(default=None),
) -> HTMLResponse:
    """Printable HTML version of the Proof Pack — browser saves as PDF.

    This is the primary deliverable customers can share. The browser's
    print-to-PDF produces a perfect Arabic-RTL document on any platform.
    """
    since_dt = _parse_since(since, default_days=30)
    async with get_session() as session:
        events = await fetch_for_customer(session, customer_id, since=since_dt, limit=2000)
    pack = build_pack(events, customer_label=customer_id)
    html = render_html(
        pack,
        customer_label=customer_id,
        event_count=len(events),
        since=since_dt,
    )
    return HTMLResponse(content=html, status_code=200)


@router.get("/customer/{customer_id}/pack.pdf")
async def customer_pack_pdf(
    customer_id: str,
    since: str | None = Query(default=None),
):
    """Real PDF if weasyprint is installed; otherwise serves the printable HTML
    with Content-Disposition: inline so the browser opens it for save-as-PDF.
    Either way, the customer gets a verifiable Proof Pack they can forward."""
    since_dt = _parse_since(since, default_days=30)
    async with get_session() as session:
        events = await fetch_for_customer(session, customer_id, since=since_dt, limit=2000)
    pack = build_pack(events, customer_label=customer_id)
    pdf_bytes = render_pdf(
        pack,
        customer_label=customer_id,
        event_count=len(events),
        since=since_dt,
    )
    if pdf_bytes is not None:
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="proof_pack_{customer_id}.pdf"'},
        )
    html = render_html(
        pack,
        customer_label=customer_id,
        event_count=len(events),
        since=since_dt,
    )
    return HTMLResponse(content=html, status_code=200)


@router.get("/partner/{partner_id}/pack.html", response_class=HTMLResponse)
async def partner_pack_html(
    partner_id: str,
    since: str | None = Query(default=None),
) -> HTMLResponse:
    since_dt = _parse_since(since, default_days=30)
    async with get_session() as session:
        events = await fetch_for_partner(session, partner_id, since=since_dt, limit=5000)
    pack = build_pack(events, customer_label=f"agency:{partner_id}")
    html = render_html(
        pack,
        customer_label=f"agency:{partner_id}",
        event_count=len(events),
        since=since_dt,
    )
    return HTMLResponse(content=html, status_code=200)
