"""
Clearbit (now Breeze Intelligence) — depth on tech stack and employee bands.

Reference: https://dashboard.clearbit.com/docs#enrichment-api
"""

from __future__ import annotations

import os

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_PERSON_URL = "https://person.clearbit.com/v2/combined/find"
_COMPANY_URL = "https://company.clearbit.com/v2/companies/find"


def is_configured() -> bool:
    return bool(os.getenv("CLEARBIT_API_KEY", "").strip())


async def lookup_clearbit(
    *,
    domain: str | None = None,
    email: str | None = None,
) -> "EnrichmentResult":
    from dealix.enrichment import EnrichmentResult

    api_key = os.getenv("CLEARBIT_API_KEY", "").strip()
    if not api_key:
        return EnrichmentResult(matched=False, source="clearbit")

    auth = (api_key, "")
    try:
        async with httpx.AsyncClient(timeout=15, auth=auth) as c:
            if email:
                r = await c.get(_PERSON_URL, params={"email": email})
            elif domain:
                r = await c.get(_COMPANY_URL, params={"domain": domain})
            else:
                return EnrichmentResult(matched=False, source="clearbit")
            if r.status_code == 404:
                return EnrichmentResult(matched=False, source="clearbit")
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("clearbit_lookup_failed", domain=domain, has_email=bool(email))
        return EnrichmentResult(matched=False, source="clearbit")

    company = data.get("company") or data
    if not company:
        return EnrichmentResult(matched=False, source="clearbit")

    return EnrichmentResult(
        matched=True,
        source="clearbit",
        confidence=0.78,
        data={
            "company_name": company.get("name"),
            "domain": company.get("domain") or domain,
            "industry": (company.get("category") or {}).get("industry"),
            "employee_count": company.get("metrics", {}).get("employees"),
            "founded_year": company.get("foundedYear"),
            "city": (company.get("geo") or {}).get("city"),
            "country": (company.get("geo") or {}).get("country"),
            "tech_stack": company.get("tech", []),
            "linkedin_url": (company.get("linkedin") or {}).get("handle"),
        },
    )
