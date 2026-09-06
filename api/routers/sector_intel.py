"""Sector Intelligence Reports — research/delivery capability, not price authority.

Generates Saudi-sector research from source-bound platform data. The capability
is useful for diagnostics, discovery, delivery and proof preparation, but it is
not a standalone public fixed-price product. Any customer commercial scope must
flow through the canonical customer-specific quote path.
"""
from __future__ import annotations

import hashlib
import logging
import os
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Path
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sector-intel", tags=["sector-intel"])

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

_COMMERCIAL_AUTHORITY = {
    "mode": "internal_research_delivery_capability",
    "price_authority": "customer_specific_quote_after_qualified_discovery",
    "public_fixed_price": False,
    "live_charge_allowed": False,
}


class _GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str = Field(..., min_length=2, max_length=64)
    period_start: str | None = Field(default=None, description="YYYY-MM-DD")
    period_end: str | None = Field(default=None, description="YYYY-MM-DD")
    customer_handle: str | None = Field(default=None, max_length=64,
                                        description="optional delivery context; not billing authority")


def _require_admin(authorization: str | None) -> None:
    """Admin-only because generation can consume research/API resources."""
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
    """Pull known Saudi B2B accounts in this sector. Returns [] if DB unreachable."""
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
    del days
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
    """Return an honest placeholder rather than fabricated data."""
    return {
        "section": name,
        "status": "placeholder",
        "note": (
            f"This section is a placeholder. Real data will populate once "
            f"evidence-backed customer/market observations exist for '{sector}'."
        ),
        "sector": sector,
    }


@router.get("/sectors")
async def list_sectors() -> dict[str, Any]:
    """List research sectors without publishing prices or sales authority."""
    return {
        "sectors": [
            {
                "key": s,
                "data_maturity": "placeholder" if s in ("government", "healthcare") else "partial",
            }
            for s in sorted(SUPPORTED_SECTORS)
        ],
        "commercial_authority": dict(_COMMERCIAL_AUTHORITY),
        "note": "Sector intelligence supports diagnostics/discovery/delivery; it is not a public fixed-price offer.",
    }


@router.post("/generate")
async def generate_report(
    body: _GenerateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Generate a source-bound sector report. Admin-gated; no billing side effect."""
    _require_admin(authorization)

    if body.sector not in SUPPORTED_SECTORS:
        raise HTTPException(
            status_code=400,
            detail=f"sector must be one of {sorted(SUPPORTED_SECTORS)}",
        )

    generated_at = datetime.now(UTC)
    report_id = _report_id(body.sector, generated_at)

    accounts = await _collect_sector_accounts(body.sector)
    signals = await _collect_market_signals(body.sector)

    report = {
        "report_id": report_id,
        "sector": body.sector,
        "generated_at": generated_at.isoformat(),
        "commercial_authority": dict(_COMMERCIAL_AUTHORITY),
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
                    f"{len(accounts)} known accounts indexed. Full account data remains evidence-bound."
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
                "pdpl": (
                    "Use lawful/public/first-party sources only; public business data does not imply consent or relationship."
                ),
                "commercial": (
                    "No standalone report price or payment authority. Any customer scope follows qualified discovery and a customer-specific quote."
                ),
            },
        },
    }

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
        "commercial_authority": dict(_COMMERCIAL_AUTHORITY),
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
    """Persist research output using legacy table fields without creating billing truth."""
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
                    price_sar=0,
                    period_start=period_start,
                    period_end=period_end,
                    payload=payload,
                    payment_status="not_applicable",
                )
                session.add(row)
            else:
                existing.payload = payload
                existing.period_start = period_start
                existing.period_end = period_end
                existing.price_sar = 0
                existing.payment_status = "not_applicable"
            await session.commit()
            return True
    except Exception as exc:
        log.warning("sector_report_persist_failed report_id=%s error=%s", report_id, exc)
        return False


@router.get("/reports/{report_id}")
async def fetch_report(
    report_id: str = Path(..., pattern=r"^sr_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Fetch a previously-generated research report by ID."""
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
    except (ConnectionError, OSError) as exc:
        log.warning("sector_report_fetch_db_unavailable error=%s", exc)
        row = None
    except Exception as exc:
        if "connect" in str(exc).lower() or exc.__class__.__name__ in (
            "OperationalError",
            "InterfaceError",
            "DBAPIError",
        ):
            log.warning("sector_report_fetch_db_error error=%s", exc)
            row = None
        else:
            raise

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "report_not_persisted",
                "report_id": report_id,
                "note": (
                    "Persistence is deferred — generate a report via POST "
                    "/api/v1/sector-intel/generate, then re-fetch by report_id."
                ),
            },
        )

    return {
        "report_id": row.id,
        "sector": row.sector,
        "customer_handle": row.customer_handle,
        "period_start": row.period_start,
        "period_end": row.period_end,
        "delivered_at": row.delivered_at.isoformat() if row.delivered_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "payload": row.payload,
        "commercial_authority": dict(_COMMERCIAL_AUTHORITY),
        "legacy_storage_fields_are_not_commercial_authority": True,
    }


@router.get("/sample/{sector}")
async def sample_report(sector: str) -> dict[str, Any]:
    """Return a case-safe Saudi sector sample; sample is not customer proof."""
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
            "commercial_authority": dict(_COMMERCIAL_AUTHORITY),
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
        "commercial_authority": dict(_COMMERCIAL_AUTHORITY),
    }
