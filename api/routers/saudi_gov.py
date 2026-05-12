"""
Saudi-government data exposure (T6f):

    GET  /api/v1/saudi-gov/tenders               — Etimad tender alerts.
    GET  /api/v1/saudi-gov/tenders/{id}          — single tender detail.
    GET  /api/v1/saudi-gov/maroof/{cr_number}    — Maroof merchant profile.
    GET  /api/v1/saudi-gov/judicial/{cr_number}  — Najiz commercial-risk snapshot.
    GET  /api/v1/saudi-gov/tadawul/{symbol}      — listed-company snapshot.
    GET  /api/v1/saudi-gov/misa/{licence}        — MISA foreign-investment licence.

All endpoints degrade to 503 `service_not_configured` when the relevant
credential is unset — no surprise outages, no silent 200s with empty
data.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from core.logging import get_logger
from dealix.integrations import etimad_client, maroof_client, misa_client
from dealix.integrations import najiz_client, najm_client, tadawul_client

router = APIRouter(prefix="/api/v1/saudi-gov", tags=["saudi-gov"])
log = get_logger(__name__)


def _require(configured: bool, service: str) -> None:
    if not configured:
        raise HTTPException(503, f"{service}_not_configured")


@router.get("/tenders")
async def list_tenders(
    sector: str | None = Query(default=None),
    region: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    page: int = Query(default=1, ge=1, le=1000),
    page_size: int = Query(default=25, ge=1, le=100),
) -> dict[str, object]:
    _require(etimad_client.is_configured(), "etimad")
    rows = await etimad_client.search_tenders(
        sector=sector, region=region, keyword=keyword, page=page, page_size=page_size
    )
    return {
        "count": len(rows),
        "tenders": [
            {
                "id": t.id,
                "title_ar": t.title_ar,
                "agency": t.agency,
                "sector": t.sector,
                "region": t.region,
                "published_at": t.published_at,
                "submission_deadline": t.submission_deadline,
                "estimated_value_sar": t.estimated_value_sar,
                "url": t.url,
            }
            for t in rows
        ],
    }


@router.get("/tenders/{tender_id}")
async def get_tender(tender_id: str) -> dict[str, object]:
    _require(etimad_client.is_configured(), "etimad")
    data = await etimad_client.get_tender(tender_id)
    if data is None:
        raise HTTPException(404, "tender_not_found")
    return data


@router.get("/maroof/{cr_number}")
async def maroof_lookup(cr_number: str) -> dict[str, object]:
    _require(maroof_client.is_configured(), "maroof")
    profile = await maroof_client.lookup(cr_number)
    if profile is None:
        raise HTTPException(404, "merchant_not_found")
    return {
        "cr_number": profile.cr_number,
        "verified": profile.verified,
        "rating": profile.rating,
        "review_count": profile.review_count,
        "badge_color": profile.badge_color,
    }


@router.get("/judicial/{cr_number}")
async def judicial_snapshot(cr_number: str) -> dict[str, object]:
    _require(najiz_client.is_configured(), "najiz")
    snap = await najiz_client.snapshot(cr_number)
    if snap is None:
        raise HTTPException(404, "snapshot_unavailable")
    return {
        "cr_number": snap.cr_number,
        "open_disputes": snap.open_disputes,
        "bankruptcy_filings": snap.bankruptcy_filings,
        "execution_orders": snap.execution_orders,
        "risk_score": snap.risk_score,
    }


@router.get("/najm/{vin}")
async def najm_history(vin: str) -> dict[str, object]:
    _require(najm_client.is_configured(), "najm")
    h = await najm_client.vehicle_history(vin)
    if h is None:
        raise HTTPException(404, "vehicle_not_found")
    return {
        "vin": h.vin,
        "claim_count": h.claim_count,
        "at_fault_count": h.at_fault_count,
        "risk_class": h.risk_class,
    }


@router.get("/tadawul/{symbol}")
async def tadawul_lookup(symbol: str) -> dict[str, object]:
    _require(tadawul_client.is_configured(), "tadawul")
    c = await tadawul_client.lookup_symbol(symbol)
    if c is None:
        raise HTTPException(404, "symbol_not_found")
    return {
        "symbol": c.symbol,
        "name_ar": c.name_ar,
        "name_en": c.name_en,
        "sector": c.sector,
        "market_cap_sar": c.market_cap_sar,
        "last_close": c.last_close,
        "pe_ratio": c.pe_ratio,
    }


@router.get("/misa/{licence_number}")
async def misa_lookup(licence_number: str) -> dict[str, object]:
    _require(misa_client.is_configured(), "misa")
    licence = await misa_client.licence_status(licence_number)
    if licence is None:
        raise HTTPException(404, "licence_not_found")
    return {
        "licence_number": licence.licence_number,
        "active": licence.active,
        "issued_at": licence.issued_at,
        "expires_at": licence.expires_at,
        "country_of_origin": licence.country_of_origin,
        "activity": licence.activity,
    }
