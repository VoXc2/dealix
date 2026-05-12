"""
Apollo.io enrichment — best MENA B2B coverage at the price point.

Apollo has no official Python SDK; we hit the REST API directly via httpx.
Inert unless APOLLO_API_KEY is set; the orchestrator branches to the next
provider on miss.

Reference: https://docs.apollo.io/reference/people-enrichment
            https://docs.apollo.io/reference/organization-enrichment
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_BASE = "https://api.apollo.io/v1"


def is_configured() -> bool:
    return bool(os.getenv("APOLLO_API_KEY", "").strip())


async def lookup_apollo(
    *,
    company_name: str | None = None,
    domain: str | None = None,
    email: str | None = None,
) -> "EnrichmentResult":
    """Return an EnrichmentResult; matched=False when Apollo is off or misses."""
    from dealix.enrichment import EnrichmentResult

    api_key = os.getenv("APOLLO_API_KEY", "").strip()
    if not api_key:
        return EnrichmentResult(matched=False, source="apollo")

    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }

    # People-enrich is preferred when we have an email; org-enrich for domain.
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            if email:
                r = await c.post(
                    f"{_BASE}/people/match",
                    headers=headers,
                    json={"email": email, "reveal_personal_emails": False},
                )
            elif domain:
                r = await c.post(
                    f"{_BASE}/organizations/enrich",
                    headers=headers,
                    json={"domain": domain},
                )
            elif company_name:
                r = await c.post(
                    f"{_BASE}/organizations/search",
                    headers=headers,
                    json={"q_organization_name": company_name, "page": 1},
                )
            else:
                return EnrichmentResult(matched=False, source="apollo")
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception(
            "apollo_lookup_failed", company=company_name, domain=domain, has_email=bool(email)
        )
        return EnrichmentResult(matched=False, source="apollo")

    org = data.get("organization") or (data.get("organizations") or [{}])[0]
    person = data.get("person") or {}
    if not (org or person):
        return EnrichmentResult(matched=False, source="apollo")

    return EnrichmentResult(
        matched=True,
        source="apollo",
        confidence=0.85,
        data={
            "company_name": org.get("name") or company_name,
            "domain": org.get("primary_domain") or domain,
            "industry": org.get("industry"),
            "employee_count": org.get("estimated_num_employees"),
            "founded_year": org.get("founded_year"),
            "city": org.get("city"),
            "country": org.get("country"),
            "linkedin_url": org.get("linkedin_url"),
            "person": {
                "full_name": person.get("name"),
                "title": person.get("title"),
                "linkedin_url": person.get("linkedin_url"),
            }
            if person
            else None,
        },
    )
