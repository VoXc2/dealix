"""
Saudi Ministry of Commerce Registry Source — Dealix Lead Intelligence Engine V2
===============================================================================
Saudi Ministry of Commerce (mc.gov.sa) public business registry search.
This is a stub — the MC site uses dynamic JavaScript so we use their
public search endpoints and fall back gracefully to mock data.
"""

from __future__ import annotations

import logging
import re
from typing import List, Optional

from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry

logger = logging.getLogger(__name__)

# MC.gov.sa public search endpoints (discovered via browser dev tools)
MC_SEARCH_BASE = "https://mc.gov.sa/ar/companies/Pages/default.aspx"
MC_API_SEARCH = "https://cr.mc.gov.sa/api/v1/commercialregistrations/search"


class SaudiMCGovSource(BaseSource):
    """
    Saudi Ministry of Commerce (mc.gov.sa) public registry stub.

    The MC website uses a JavaScript SPA. This adapter:
    1. Tries the discovered API endpoint
    2. Falls back to mock data with is_mock=True

    When fully implemented, this source provides:
    - Commercial registration number (السجل التجاري)
    - Company name (AR + EN)
    - Activity type (ISIC code)
    - Registered city / region
    - Owner info (limited)
    - Capital (SAR)
    """

    SOURCE_NAME = "sa_mc_gov"
    REQUIRES_KEY = False   # Public registry, no key needed (but JS-heavy)
    RATE_LIMIT_CPS = 0.5

    @with_retry(max_attempts=2, base_delay=3.0)
    @rate_limited(calls_per_second=0.5)
    async def _search_api(self, query: str, city: Optional[str] = None) -> dict:
        """
        Attempt to call MC.gov.sa API endpoint.
        This endpoint was discovered via browser dev tools and may change.
        """
        client = await self.get_client()
        params = {
            "searchText": query,
            "pageNumber": 1,
            "pageSize": 20,
        }
        if city:
            params["city"] = city

        headers = {
            "Accept": "application/json",
            "Referer": "https://mc.gov.sa/",
            "Origin": "https://mc.gov.sa",
        }

        resp = await client.get(MC_API_SEARCH, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def _parse_registration(self, reg: dict, plan: SearchPlan) -> RawLead:
        """Parse a MC.gov.sa business registration record."""
        cr_number = reg.get("crNumber") or reg.get("registrationNumber", "")
        name_ar = reg.get("nameAr") or reg.get("arabicName", "")
        name_en = reg.get("nameEn") or reg.get("englishName", "")
        city = reg.get("city") or reg.get("cityName", "")
        activity = reg.get("activityDescription") or reg.get("mainActivity", "")
        capital = reg.get("capital") or reg.get("paidCapital")
        status = reg.get("status") or reg.get("registrationStatus", "")

        # Build a plausible website from name
        domain_guess = None
        if name_en:
            slug = re.sub(r"[^a-z0-9]", "", name_en.lower().replace(" ", ""))[:15]
            domain_guess = f"{slug}.com.sa" if slug else None

        provenance = self._make_provenance(
            plan,
            url=f"https://mc.gov.sa/ar/companies/Pages/CompanyDetails.aspx?crNumber={cr_number}",
            is_mock=False,
        )

        return RawLead(
            provenance=provenance,
            company_name=name_en or name_ar,
            company_name_ar=name_ar,
            domain=domain_guess,
            city=city,
            country="SA",
            industry=activity,
            raw_data={
                "cr_number": cr_number,
                "capital_sar": capital,
                "status": status,
                "activity": activity,
            },
        )

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        city = None
        if query.icp.geo.cities:
            city = query.icp.geo.cities[0]

        try:
            data = await self._search_api(plan.query_string, city)
            registrations = (
                data.get("data", [])
                or data.get("items", [])
                or data.get("results", [])
                or (data if isinstance(data, list) else [])
            )

            if registrations:
                leads = [self._parse_registration(r, plan) for r in registrations[:20]]
                logger.info(
                    f"[sa_mc_gov] Found {len(leads)} registrations for: {plan.query_string[:60]}"
                )
                return leads
            else:
                logger.info("[sa_mc_gov] API returned empty — using mock")
                return self._mock_leads(query, plan, count=3)

        except Exception as e:
            # Expected: MC API is not publicly documented and may block requests
            logger.info(f"[sa_mc_gov] API unavailable ({type(e).__name__}) — using mock")
            return self._mock_leads(query, plan, count=3)
