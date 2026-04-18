"""
Lead Enrichment — Dealix Lead Intelligence Engine V2
====================================================
For each NormalizedLead:
- WHOIS lookup (domain age, registrar, country)
- Website presence check
- Email discovery (info@, contact@, etc.)
- LinkedIn URL discovery via Google
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

import httpx

from app.intelligence.v2.models import EnrichedLead, NormalizedLead

logger = logging.getLogger(__name__)

# Common email prefixes to try for domain-based email discovery
EMAIL_PREFIXES = ["info", "contact", "hello", "sales", "admin", "support", "marketing"]

# Common ecommerce platforms detected from website
ECOMMERCE_SIGNATURES = {
    "salla.sa": "Salla",
    "salla.com": "Salla",
    "zid.sa": "Zid",
    "shopify.com": "Shopify",
    "myshopify.com": "Shopify",
    "woocommerce": "WooCommerce",
    "magento": "Magento",
    "opencart": "OpenCart",
}


async def _whois_lookup(domain: str) -> dict:
    """
    WHOIS lookup for domain age and registrar.
    Uses python-whois in a thread pool to avoid blocking.
    """
    if not domain:
        return {}

    def _do_whois():
        try:
            import whois
            w = whois.whois(domain)
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            registrar = w.registrar
            if isinstance(registrar, list):
                registrar = registrar[0]

            country = w.country
            if isinstance(country, list):
                country = country[0]

            return {
                "registrar": str(registrar) if registrar else None,
                "creation_date": creation_date if isinstance(creation_date, datetime) else None,
                "country": str(country) if country else None,
            }
        except Exception:
            return {}

    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, _do_whois),
            timeout=10.0,
        )
        return result
    except asyncio.TimeoutError:
        return {}
    except Exception:
        return {}


async def _check_website(domain: str) -> dict:
    """Check if a website exists and detect basic tech signals."""
    if not domain:
        return {"has_website": False}

    url = f"https://{domain}"
    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(8.0, connect=4.0),
            follow_redirects=True,
        ) as client:
            resp = await client.get(url, headers={"User-Agent": "Dealix-LeadEngine/2.0"})
            if resp.status_code < 400:
                html = resp.text[:5000]  # Only check first 5KB
                # Detect ecommerce platform
                platform = None
                for sig, name in ECOMMERCE_SIGNATURES.items():
                    if sig in html.lower() or sig in str(resp.url).lower():
                        platform = name
                        break

                return {
                    "has_website": True,
                    "status_code": resp.status_code,
                    "final_url": str(resp.url),
                    "ecommerce_platform": platform,
                    "has_ecommerce": platform is not None,
                }
            return {"has_website": False, "status_code": resp.status_code}
    except Exception:
        return {"has_website": False}


async def _discover_emails(domain: str) -> List[str]:
    """
    Try common email patterns for a domain.
    Checks if the domain has MX records first.
    """
    if not domain:
        return []

    # Check if domain resolves (basic check)
    import socket
    try:
        socket.getaddrinfo(domain, None)
    except (socket.gaierror, OSError):
        return []

    # Return common patterns (not validated against mail server — just patterns)
    discovered = [f"{prefix}@{domain}" for prefix in EMAIL_PREFIXES[:3]]
    return discovered


async def _find_linkedin(company_name: str, domain: Optional[str] = None) -> Optional[str]:
    """
    Try to find a LinkedIn company URL via DuckDuckGo.
    Simple heuristic: site:linkedin.com/company + company name.
    """
    if not company_name:
        return None

    search_query = f"site:linkedin.com/company {company_name}"
    if domain:
        # Try domain slug too
        slug = domain.split(".")[0]
        search_query = f"site:linkedin.com/company {company_name} OR {slug}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            data = {"q": search_query, "kl": "wt-wt"}
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0",
            }
            resp = await client.post(
                "https://html.duckduckgo.com/html/",
                data=data,
                headers=headers,
            )
            html = resp.text
            match = re.search(
                r'href="(https://(?:www\.)?linkedin\.com/company/[^?"&]+)"',
                html
            )
            if match:
                return match.group(1)
    except Exception:
        pass
    return None


async def enrich_lead(normalized: NormalizedLead) -> EnrichedLead:
    """Enrich a single NormalizedLead."""
    enriched = EnrichedLead(
        normalized_lead=normalized,
        enrichment_sources=[],
    )

    domain = normalized.domain

    # Run enrichment tasks concurrently
    tasks = {}
    if domain:
        tasks["whois"] = _whois_lookup(domain)
        tasks["website"] = _check_website(domain)
        tasks["emails"] = _discover_emails(domain)

    if not normalized.linkedin_url:
        tasks["linkedin"] = _find_linkedin(normalized.company_name, domain)

    if tasks:
        task_names = list(tasks.keys())
        task_coros = list(tasks.values())
        results = await asyncio.gather(*task_coros, return_exceptions=True)

        for name, result in zip(task_names, results):
            if isinstance(result, Exception):
                continue

            if name == "whois" and result:
                enriched.whois_registrar = result.get("registrar")
                creation_date = result.get("creation_date")
                if creation_date:
                    enriched.whois_creation_date = creation_date
                    try:
                        # Handle timezone-aware datetimes from python-whois
                        if hasattr(creation_date, 'tzinfo') and creation_date.tzinfo is not None:
                            from datetime import timezone
                            now = datetime.now(timezone.utc)
                        else:
                            now = datetime.utcnow()
                        enriched.domain_age_days = (now - creation_date).days
                    except Exception:
                        enriched.domain_age_days = None
                enriched.whois_country = result.get("country")
                enriched.enrichment_sources.append("whois")

            elif name == "website" and result:
                enriched.has_website = result.get("has_website", False)
                enriched.has_ecommerce = result.get("has_ecommerce", False)
                enriched.ecommerce_platform = result.get("ecommerce_platform")
                enriched.enrichment_sources.append("website_check")

            elif name == "emails" and result:
                enriched.discovered_emails = result
                enriched.enrichment_sources.append("email_patterns")

            elif name == "linkedin" and result:
                enriched.linkedin_url = result
                enriched.linkedin_found = True
                enriched.enrichment_sources.append("linkedin_discovery")

    enriched.enriched_at = datetime.utcnow()
    return enriched


async def enrich_leads(
    normalized_leads: List[NormalizedLead],
    concurrency: int = 5,
) -> List[EnrichedLead]:
    """Enrich all normalized leads with controlled concurrency."""
    semaphore = asyncio.Semaphore(concurrency)

    async def _bounded_enrich(lead: NormalizedLead) -> EnrichedLead:
        async with semaphore:
            return await enrich_lead(lead)

    results = await asyncio.gather(
        *[_bounded_enrich(lead) for lead in normalized_leads],
        return_exceptions=False,
    )
    logger.info(f"[enrichment] Enriched {len(results)} leads")
    return results
