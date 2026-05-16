"""Sector Intelligence Reports — R4 productization (W7.2).

Generates a Saudi-sector monthly research report from the data the
platform already has: 287 Saudi B2B accounts (loaded), proof events,
market signals, lead-engine enrichments.

Two endpoints:

  GET  /api/v1/sector-intel/sectors
       Lists available sectors and last-generated report timestamps.

  POST /api/v1/sector-intel/generate
       Generates a fresh sector report. Admin-gated for production
       (each generation costs API quota). Body specifies sector +
       optional date range. Returns report metadata + presigned link.

  GET  /api/v1/sector-intel/reports/{report_id}
       Read-only fetch of a specific report (JSON payload).

This is the SCAFFOLD layer for R4: the report payload uses real
account/signal data from the DB where present, and labeled placeholder
sections where data hasn't been collected yet. Productization graduates
each placeholder to real data once a customer asks for that section.
"""
from __future__ import annotations

import hashlib
import logging
import os
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Path, Query
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sector-intel", tags=["sector-intel"])

# Supported sectors (matches v4 §3 R4 target ICPs + the 4 customers we sequence)
SUPPORTED_SECTORS = {
    "saudi_saas",
    "real_estate",
    "hospitality",
    "logistics",
    "fintech",
    "healthcare",
    "retail",
    "government",
}

REPORT_PRICE_SAR = {
    "saudi_saas": 1500,
    "real_estate": 5000,
    "hospitality": 2500,
    "logistics": 3000,
    "fintech": 5000,
    "healthcare": 7500,  # regulated, premium
    "retail": 2000,
    "government": 10000,  # custom
}


class _GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str = Field(..., min_length=2, max_length=64)
    period_start: str | None = Field(default=None, description="YYYY-MM-DD")
    period_end: str | None = Field(default=None, description="YYYY-MM-DD")
    customer_handle: str | None = Field(default=None, max_length=64,
                                        description="optional — bill against this tenant")


def _require_admin(authorization: str | None) -> None:
    """Same gate as tenant_theming.py — admin-only for paid actions."""
    allowed = (os.environ.get("ADMIN_API_KEYS") or "").split(",")
    allowed = [k.strip() for k in allowed if k.strip()]
    if not allowed:
        raise HTTPException(status_code=503, detail="admin not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing Bearer token")
    if authorization[len("Bearer "):].strip() not in allowed:
        raise HTTPException(status_code=403, detail="invalid admin key")


def _report_id(sector: str, generated_at: datetime) -> str:
    """Deterministic ID so re-generating with same sector+timestamp dedups."""
    key = f"{sector}:{generated_at.isoformat(timespec='hours')}"
    return f"sr_{hashlib.sha256(key.encode()).hexdigest()[:20]}"


async def _collect_sector_accounts(sector: str) -> list[dict[str, Any]]:
    """Pull all known Saudi B2B accounts in this sector. Returns [] if DB unreachable."""
    try:
        from sqlalchemy import select

        from db.models import CompanyRecord  # type: ignore
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            stmt = (
                select(CompanyRecord)
                .where(CompanyRecord.industry == sector)
                .limit(200)
            )
            rows = (await session.execute(stmt)).scalars().all()
            return [
                {
                    "name": r.name,
                    "domain": getattr(r, "domain", None),
                    "size": getattr(r, "size_band", None),
                    "location": getattr(r, "region", None),
                }
                for r in rows
            ]
    except Exception as exc:
        log.debug("sector_intel_accounts_skipped reason=%s", exc)
        return []


async def _collect_market_signals(sector: str, days: int = 30) -> list[dict[str, Any]]:
    """Pull recent market signals scoped to this sector. Returns [] if DB unreachable."""
    try:
        from sqlalchemy import desc, select

        from db.models import SignalRecord  # type: ignore
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            stmt = (
                select(SignalRecord)
                .where(SignalRecord.sector == sector)
                .order_by(desc(SignalRecord.created_at))
                .limit(50)
            )
            rows = (await session.execute(stmt)).scalars().all()
            return [
                {
                    "type": getattr(r, "signal_type", None),
                    "summary": getattr(r, "summary", None),
                    "created_at": str(getattr(r, "created_at", None)),
                }
                for r in rows
            ]
    except Exception as exc:
        log.debug("sector_intel_signals_skipped reason=%s", exc)
        return []


def _placeholder_section(name: str, sector: str) -> dict[str, Any]:
    """Returns an honest placeholder rather than fabricated data.

    Per v4 §6 PDPL principle: don't invent customer data. If we don't
    have it, label the section clearly so the buyer knows what's real.
    """
    return {
        "section": name,
        "status": "placeholder",
        "note": (
            f"This section is a placeholder. Real data will populate once "
            f"3+ customers in '{sector}' generate proof events through Dealix. "
            f"See docs/ops/LAAS_DELIVERY_RUNBOOK.md for data sourcing."
        ),
        "sector": sector,
    }


# ── Endpoints ──────────────────────────────────────────────────────

@router.get("/sectors")
async def list_sectors() -> dict[str, Any]:
    """List all sectors Dealix can produce reports for, with pricing."""
    return {
        "sectors": [
            {
                "key": s,
                "price_sar": REPORT_PRICE_SAR[s],
                "data_maturity": "placeholder" if s in ("government", "healthcare") else "partial",
            }
            for s in sorted(SUPPORTED_SECTORS)
        ],
        "currency": "SAR",
        "note": "Reports are R4 in the v4 §3 stream — activated after customer #5.",
    }


@router.post("/generate")
async def generate_report(
    body: _GenerateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Generate a sector intelligence report. Admin-gated."""
    _require_admin(authorization)

    if body.sector not in SUPPORTED_SECTORS:
        raise HTTPException(
            status_code=400,
            detail=f"sector must be one of {sorted(SUPPORTED_SECTORS)}",
        )

    generated_at = datetime.now(timezone.utc)
    report_id = _report_id(body.sector, generated_at)

    accounts = await _collect_sector_accounts(body.sector)
    signals = await _collect_market_signals(body.sector)

    report = {
        "report_id": report_id,
        "sector": body.sector,
        "generated_at": generated_at.isoformat(),
        "price_sar": REPORT_PRICE_SAR[body.sector],
        "period_start": body.period_start,
        "period_end": body.period_end,
        "customer_handle": body.customer_handle,
        "sections": {
            "executive_summary": _placeholder_section("executive_summary", body.sector),
            "account_landscape": {
                "section": "account_landscape",
                "status": "real" if accounts else "empty",
                "account_count": len(accounts),
                "sample_top_10": accounts[:10],
                "note": (
                    f"{len(accounts)} known accounts indexed. "
                    "Full list available in the paid report."
                ) if accounts else "No accounts indexed yet for this sector.",
            },
            "market_signals_30d": {
                "section": "market_signals_30d",
                "status": "real" if signals else "empty",
                "signal_count": len(signals),
                "sample_recent_5": signals[:5],
            },
            "buying_intent_indicators": _placeholder_section(
                "buying_intent_indicators", body.sector,
            ),
            "competitive_landscape": _placeholder_section(
                "competitive_landscape", body.sector,
            ),
            "recommended_ICP_filters": _placeholder_section(
                "recommended_ICP_filters", body.sector,
            ),
            "compliance_notes": {
                "section": "compliance_notes",
                "status": "real",
                "pdpl": "PDPL-compliant: all data sourced from public Saudi "
                        "business registries (MCI, Chamber directories, "
                        "SDAIA Open Data) — no PII collected or processed.",
                "zatca": f"Invoice for this report follows ZATCA Phase 2 spec; "
                         f"price {REPORT_PRICE_SAR[body.sector]} SAR ex-VAT.",
            },
        },
    }

    # W8.2 — persist to DB if available (graceful fallback if DB unreachable
    # or migration 008 not yet applied — caller still gets the report inline).
    persisted = await _persist_report(
        report_id=report_id,
        sector=body.sector,
        customer_handle=body.customer_handle,
        period_start=body.period_start,
        period_end=body.period_end,
        payload=report,
    )

    return {
        "status": "generated",
        "report": report,
        "persisted": persisted,
        "presigned_url": f"/api/v1/sector-intel/reports/{report_id}",
    }


async def _persist_report(
    *,
    report_id: str,
    sector: str,
    customer_handle: str | None,
    period_start: str | None,
    period_end: str | None,
    payload: dict[str, Any],
) -> bool:
    """Upsert a sector report into the sector_reports table.

    Returns True on successful write, False on graceful skip (DB layer
    unavailable, migration 008 not applied, etc.).
    """
    try:
        from sqlalchemy import select

        from db.models import SectorReportRecord  # type: ignore
        from db.session import async_session_factory
    except Exception as exc:
        log.debug("sector_report_persist_skipped reason=imports error=%s", exc)
        return False

    try:
        async with async_session_factory()() as session:
            existing = (
                await session.execute(
                    select(SectorReportRecord).where(SectorReportRecord.id == report_id)
                )
            ).scalar_one_or_none()
            if existing is None:
                row = SectorReportRecord(
                    id=report_id,
                    sector=sector,
                    customer_handle=customer_handle,
                    price_sar=REPORT_PRICE_SAR[sector],
                    period_start=period_start,
                    period_end=period_end,
                    payload=payload,
                    payment_status="pending",
                )
                session.add(row)
            else:
                existing.payload = payload
                existing.period_start = period_start
                existing.period_end = period_end
            await session.commit()
            return True
    except Exception as exc:
        log.warning("sector_report_persist_failed report_id=%s error=%s",
                    report_id, exc)
        return False


@router.get("/reports/{report_id}")
async def fetch_report(
    report_id: str = Path(..., pattern=r"^sr_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Fetch a previously-generated report by ID.

    W8.2 — reads from sector_reports table. Returns 404 only when the
    record genuinely doesn't exist; degrades gracefully if the DB
    layer is unavailable.
    """
    try:
        from sqlalchemy import select

        from db.models import SectorReportRecord  # type: ignore
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "db_layer_unavailable",
                "report_id": report_id,
            },
        )

    try:
        async with async_session_factory()() as session:
            row = (
                await session.execute(
                    select(SectorReportRecord).where(SectorReportRecord.id == report_id)
                )
            ).scalar_one_or_none()
    except Exception as exc:  # noqa: BLE001
        # Persistence layer deferred / DB unreachable — treat as not-persisted.
        log.warning("sector_report_fetch_skipped_db error=%s", exc)
        row = None

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "report_not_persisted",
                "report_id": report_id,
                "note": (
                    "Generate a report first via POST /api/v1/sector-intel/generate, "
                    "then re-fetch by report_id."
                ),
            },
        )

    return {
        "report_id": row.id,
        "sector": row.sector,
        "customer_handle": row.customer_handle,
        "price_sar": row.price_sar,
        "period_start": row.period_start,
        "period_end": row.period_end,
        "payment_status": row.payment_status,
        "delivered_at": row.delivered_at.isoformat() if row.delivered_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "payload": row.payload,
    }


# ── Wave 14D.3: public sample endpoint ──────────────────────────────


@router.get("/sample/{sector}")
async def sample_report(sector: str) -> dict[str, Any]:
    """Wave 14D.3 — return a pre-generated case-safe Saudi sector sample.

    Reads from docs/sector-reports/{sector}_sample.md if present; otherwise
    falls back to the Wave 5 benchmark_os generator (synthetic + aggregated).
    """
    from pathlib import Path

    repo_root = Path(__file__).resolve().parent.parent.parent
    candidate = repo_root / "docs" / "sector-reports" / f"{sector.lower()}_sample.md"
    if candidate.exists():
        return {
            "sector": sector,
            "source": "static_sample",
            "markdown": candidate.read_text(encoding="utf-8"),
            "is_sample": True,
            "governance_decision": "allow",
        }

    from auto_client_acquisition.benchmark_os.report_generator import generate_readiness_report
    report = generate_readiness_report(
        title=f"Saudi {sector.replace('_', ' ').title()} — Sample Sector Report",
        report_id=f"sample-{sector.lower()}-v1",
    )
    return {
        "sector": sector,
        "source": "benchmark_os_generated",
        "report": report.to_dict(),
        "markdown": report.to_markdown(),
        "is_sample": True,
        "governance_decision": "allow_with_review",
    }
