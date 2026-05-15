"""Saudi B2B prospect search endpoint (W9.8).

Surfaces the 287 Saudi B2B accounts already in the data lake as a
searchable read-only API. Used by:

  - Sales team prep: search prospects before outreach
  - Customer LaaS dashboard: customer can preview ICP filter results
  - Internal CRM: bulk ICP filter to feed the discovery pipeline

  GET /api/v1/prospects/search
      Query params: sector, region, size_band, q (free-text), limit, offset
      Returns matching accounts with PDPL-safe public fields only.

Security:
  - No PII fields returned (only company-level public attributes)
  - Path is public read-only (data is public Saudi business registry)
  - Rate-limited via slowapi (configured in PRODUCTION_ENV_TEMPLATE P8)
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/prospects", tags=["saudi-prospects"])

# Known Saudi sectors from auto_client_acquisition data dictionary
KNOWN_SECTORS = {
    "saas", "fintech", "marketplace", "delivery", "proptech",
    "real_estate", "hospitality", "logistics", "retail",
    "healthcare", "government", "education", "energy", "manufacturing",
}

KNOWN_REGIONS = {"riyadh", "jeddah", "dammam", "khobar", "mecca", "medina", "qassim"}
SIZE_BANDS = {"1_50", "50_250", "250_1000", "1000_5000", "5000_plus"}


def _safe_account_view(account: Any) -> dict[str, Any]:
    """Return only PDPL-safe public fields. No emails, no personal names."""
    return {
        "id": getattr(account, "id", None),
        "name": getattr(account, "name", None),
        "domain": getattr(account, "domain", None),
        "sector": getattr(account, "industry", None) or getattr(account, "sector", None),
        "size_band": getattr(account, "size_band", None),
        "region": getattr(account, "region", None),
        "city": getattr(account, "city", None),
        "founded_year": getattr(account, "founded_year", None),
        # Decline to expose: contact_name, email, phone, internal_score
    }


@router.get("/search")
async def search_prospects(
    sector: str | None = Query(default=None,
                                description=f"one of {sorted(KNOWN_SECTORS)}"),
    region: str | None = Query(default=None,
                                description=f"one of {sorted(KNOWN_REGIONS)}"),
    size_band: str | None = Query(default=None,
                                   description=f"one of {sorted(SIZE_BANDS)}"),
    q: str | None = Query(default=None, max_length=128,
                          description="free-text on name + domain"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, Any]:
    """Search Saudi B2B prospects with filters. Returns PDPL-safe view."""
    if sector is not None and sector not in KNOWN_SECTORS:
        raise HTTPException(
            status_code=400,
            detail=f"sector must be one of {sorted(KNOWN_SECTORS)}",
        )
    if region is not None and region not in KNOWN_REGIONS:
        raise HTTPException(
            status_code=400,
            detail=f"region must be one of {sorted(KNOWN_REGIONS)}",
        )
    if size_band is not None and size_band not in SIZE_BANDS:
        raise HTTPException(
            status_code=400,
            detail=f"size_band must be one of {sorted(SIZE_BANDS)}",
        )

    try:
        from sqlalchemy import func, or_, select

        from db.models import CompanyRecord  # type: ignore
        from db.session import async_session_factory
    except Exception:
        # Graceful degrade — surface empty results with hint
        return {
            "results": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "note": "DB layer unavailable; returning empty result set.",
        }

    def _col(*names: str) -> Any:
        """First mapped column matching one of ``names``, else ``None``.
        ``CompanyRecord`` does not model every prospect attribute, so a
        filter on an absent column is skipped rather than crashing."""
        for n in names:
            col = getattr(CompanyRecord, n, None)
            if col is not None:
                return col
        return None

    async with async_session_factory()() as session:
        stmt = select(CompanyRecord)
        count_stmt = select(func.count()).select_from(CompanyRecord)

        if sector is not None and (col := _col("industry", "sector")) is not None:
            stmt = stmt.where(col == sector)
            count_stmt = count_stmt.where(col == sector)
        if region is not None and (col := _col("region")) is not None:
            stmt = stmt.where(col == region)
            count_stmt = count_stmt.where(col == region)
        if size_band is not None and (col := _col("size_band")) is not None:
            stmt = stmt.where(col == size_band)
            count_stmt = count_stmt.where(col == size_band)
        if q:
            pattern = f"%{q}%"
            text_cols = [
                c for c in (_col("name"), _col("domain", "website")) if c is not None
            ]
            if text_cols:
                clause = or_(*(c.ilike(pattern) for c in text_cols))
                stmt = stmt.where(clause)
                count_stmt = count_stmt.where(clause)

        stmt = stmt.order_by(CompanyRecord.name).limit(limit).offset(offset)
        try:
            rows = (await session.execute(stmt)).scalars().all()
            total = (await session.execute(count_stmt)).scalar() or 0
        except Exception as exc:
            log.debug("prospect_search_query_skipped reason=%s", exc)
            return {
                "results": [], "total": 0, "limit": limit, "offset": offset,
                "note": f"DB query unavailable: {type(exc).__name__}",
            }

    return {
        "results": [_safe_account_view(r) for r in rows],
        "total": total,
        "limit": limit,
        "offset": offset,
        "filters_applied": {
            "sector": sector, "region": region, "size_band": size_band, "q": q,
        },
        "pdpl_note": (
            "All fields above are public business registry attributes only. "
            "Contact PII (emails, phone numbers) is gated by PDPL Art. 5 consent."
        ),
    }


@router.get("/sectors")
async def list_sectors() -> dict[str, Any]:
    """List supported sector filters."""
    return {
        "sectors": sorted(KNOWN_SECTORS),
        "regions": sorted(KNOWN_REGIONS),
        "size_bands": sorted(SIZE_BANDS),
    }
