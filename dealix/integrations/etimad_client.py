"""
Etimad — Saudi government procurement portal.

Etimad publishes every public-sector tender (RFP/RFQ) issued by Saudi
ministries and government agencies. The platform exposes an authenticated
JSON API to licensed partners; we use it to:

1. Subscribe a tenant to tender alerts filtered by sector + region.
2. Pull tender detail (scope, value, deadlines, attachments).
3. Surface tender → bid workflow in the agent-builder marketplace
   (see `dealix/workflows/marketplace/etimad_tender_to_bid.yaml`).

Production access requires a `monafasat`-issued client credential per
service account. Until issued, the client returns 503-shaped
`etimad_not_configured`; surrounding code degrades.

Reference: https://tenders.etimad.sa/Tender/AllTendersForVisitor
            (developer onboarding: monafasat@etimad.sa)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _base() -> str:
    return os.getenv("ETIMAD_API_BASE", "https://tenders.etimad.sa/api/v1").rstrip("/")


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {os.getenv('ETIMAD_API_KEY', '').strip()}",
        "Accept": "application/json",
    }


def is_configured() -> bool:
    return bool(os.getenv("ETIMAD_API_KEY", "").strip())


@dataclass(frozen=True)
class Tender:
    id: str
    title_ar: str
    agency: str
    sector: str
    region: str
    published_at: str
    submission_deadline: str
    estimated_value_sar: float | None
    url: str


async def search_tenders(
    *,
    sector: str | None = None,
    region: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> list[Tender]:
    """List active tenders matching the filters."""
    if not is_configured():
        return []
    params: dict[str, Any] = {"page": page, "pageSize": page_size}
    if sector:
        params["sector"] = sector
    if region:
        params["region"] = region
    if keyword:
        params["q"] = keyword
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{_base()}/tenders", headers=_headers(), params=params)
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("etimad_search_failed", sector=sector, region=region)
        return []
    out: list[Tender] = []
    for item in data.get("items", []) or []:
        out.append(
            Tender(
                id=str(item.get("id", "")),
                title_ar=str(item.get("title", "")),
                agency=str(item.get("agencyName", "")),
                sector=str(item.get("sector", "")),
                region=str(item.get("region", "")),
                published_at=str(item.get("publishedAt", "")),
                submission_deadline=str(item.get("submissionDeadline", "")),
                estimated_value_sar=item.get("estimatedValueSar"),
                url=f"https://tenders.etimad.sa/Tender/Details/{item.get('id')}",
            )
        )
    return out


async def get_tender(tender_id: str) -> dict[str, Any] | None:
    if not is_configured():
        return None
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{_base()}/tenders/{tender_id}", headers=_headers())
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()
    except Exception:
        log.exception("etimad_detail_failed", tender_id=tender_id)
        return None
