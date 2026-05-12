"""
Lead enrichment chain — Apollo → Clearbit → Wathq → heuristics.

Each client lives in its own module so it can be tested + retried
independently. The orchestrator (`enrich(...)`) calls them in order
and stops at the first response that yields a confident match,
preserving the original payload's existing fields.

Wathq is the Saudi commercial registry — authoritative for VAT,
commercial registration number, official address. Including it before
falling back to heuristics gives Dealix a uniquely Saudi-grade
enrichment signal that Apollo + Clearbit can't replicate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class EnrichmentResult:
    matched: bool
    source: str  # "apollo" | "clearbit" | "wathq" | "heuristic" | "none"
    data: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0  # 0..1


async def enrich(
    *,
    company_name: str,
    domain: str | None = None,
    email: str | None = None,
    vat_number: str | None = None,
    cr_number: str | None = None,
) -> EnrichmentResult:
    """Run the enrichment chain. Returns the first confident match."""
    from dealix.enrichment.apollo_client import lookup_apollo
    from dealix.enrichment.clearbit_client import lookup_clearbit
    from dealix.enrichment.wathq_client import lookup_wathq

    # 1) Wathq — Saudi-first, authoritative for VAT/CR.
    if vat_number or cr_number:
        res = await lookup_wathq(vat_number=vat_number, cr_number=cr_number)
        if res.matched:
            return res

    # 2) Apollo — best B2B coverage (people + firmographics).
    res = await lookup_apollo(company_name=company_name, domain=domain, email=email)
    if res.matched:
        return res

    # 3) Clearbit — depth on tech stack + employee bands.
    if domain or email:
        res = await lookup_clearbit(domain=domain, email=email)
        if res.matched:
            return res

    return EnrichmentResult(matched=False, source="none")
