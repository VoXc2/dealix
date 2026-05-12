"""
Wathq — Saudi commercial registry API (authoritative for VAT, CR number,
official trade name, registered address).

Wathq is operated by the Saudi Ministry of Commerce; access is via the
Saudi Business Center developer portal. Each API uses an X-APP-KEY header.

Wiring this *before* Apollo/Clearbit on Saudi domains produces an
enrichment signal Apollo and Clearbit cannot match. It is the
Saudi-sovereign moat of the enrichment pipeline.

Reference: https://api.wathq.sa/documentation
"""

from __future__ import annotations

import os

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_BASE = "https://api.wathq.sa/v5"


def is_configured() -> bool:
    return bool(os.getenv("WATHQ_API_KEY", "").strip())


async def lookup_wathq(
    *,
    cr_number: str | None = None,
    vat_number: str | None = None,
) -> "EnrichmentResult":
    from dealix.enrichment import EnrichmentResult

    api_key = os.getenv("WATHQ_API_KEY", "").strip()
    if not api_key:
        return EnrichmentResult(matched=False, source="wathq")
    headers = {"Accept": "application/json", "APP_KEY": api_key}
    path: str | None = None
    if cr_number:
        path = f"/commercialregistration/info/{cr_number}"
    elif vat_number:
        path = f"/tax/info/{vat_number}"
    if not path:
        return EnrichmentResult(matched=False, source="wathq")

    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{_BASE}{path}", headers=headers)
            if r.status_code == 404:
                return EnrichmentResult(matched=False, source="wathq")
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("wathq_lookup_failed", cr=cr_number, vat=vat_number)
        return EnrichmentResult(matched=False, source="wathq")

    # Wathq returns nested objects; flatten the canonical fields we care about.
    crEntity = (data.get("crEntityInfo") or {}) if cr_number else {}
    taxEntity = (data.get("taxpayerInfo") or {}) if vat_number else {}
    payload = {
        "cr_number": crEntity.get("crNumber") or cr_number,
        "vat_number": taxEntity.get("vatNumber") or vat_number,
        "company_name_ar": crEntity.get("name") or taxEntity.get("name"),
        "company_name_en": crEntity.get("nameInEnglish")
        or taxEntity.get("nameInEnglish"),
        "registration_status": crEntity.get("status") or taxEntity.get("status"),
        "issue_date": crEntity.get("issueDate") or taxEntity.get("registrationDate"),
        "city": (crEntity.get("location") or {}).get("city")
        or (taxEntity.get("address") or {}).get("city"),
        "activities": [
            a.get("name") for a in (crEntity.get("activities") or []) if a.get("name")
        ],
        "raw": data,
    }
    return EnrichmentResult(matched=True, source="wathq", confidence=0.95, data=payload)
