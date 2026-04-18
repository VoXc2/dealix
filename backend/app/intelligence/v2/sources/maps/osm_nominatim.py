"""
OpenStreetMap Nominatim Source — Dealix Lead Intelligence Engine V2
===================================================================
Free geocoder + business finder using OSM Nominatim.
No API key required. Respects OSM's usage policy (1 req/sec max).
Docs: https://nominatim.org/release-docs/develop/api/Search/
"""

from __future__ import annotations

import logging
from typing import List
from urllib.parse import urljoin

from app.intelligence.v2.gulf_geo import GULF_COUNTRIES, NOMINATIM_COUNTRY_CODES
from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry

logger = logging.getLogger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_DETAILS_URL = "https://nominatim.openstreetmap.org/details"


class OSMNominatimSource(BaseSource):
    """
    OpenStreetMap Nominatim geocoder adapter.
    Good for finding business addresses and geo-validation.
    Strictly rate-limited: 1 req/sec per OSM policy.
    """

    SOURCE_NAME = "osm_nominatim"
    REQUIRES_KEY = False
    RATE_LIMIT_CPS = 0.8   # Slightly under 1 to be safe

    @with_retry(max_attempts=2, base_delay=2.0)
    @rate_limited(calls_per_second=0.8)
    async def _search(self, query: str, country_codes: List[str]) -> List[dict]:
        client = await self.get_client()
        # Convert country codes to Nominatim format
        country_codes_osm = [
            NOMINATIM_COUNTRY_CODES.get(c, c.lower()) for c in country_codes
        ]
        params = {
            "q": query,
            "format": "jsonv2",
            "addressdetails": 1,
            "extratags": 1,
            "namedetails": 1,
            "limit": 20,
            "countrycodes": ",".join(country_codes_osm),
            "accept-language": "ar,en",
        }
        headers = {
            "User-Agent": "Dealix-LeadEngine/2.0 (https://dealix.sa; ops@dealix.sa)",
        }
        resp = await client.get(NOMINATIM_URL, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def _parse_result(self, result: dict, plan: SearchPlan) -> RawLead:
        extra_tags = result.get("extratags", {}) or {}
        name_details = result.get("namedetails", {}) or {}
        address = result.get("address", {}) or {}

        # Extract names
        name_en = name_details.get("name:en") or result.get("name") or result.get("display_name", "")
        name_ar = name_details.get("name:ar") or name_details.get("name:ara")

        # Extract contact info from extra tags
        phone = extra_tags.get("phone") or extra_tags.get("contact:phone")
        email = extra_tags.get("email") or extra_tags.get("contact:email")
        website = extra_tags.get("website") or extra_tags.get("contact:website")

        domain = None
        if website:
            from urllib.parse import urlparse
            domain = urlparse(website).netloc.lstrip("www.")

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("county")
        )
        country = address.get("country_code", "sa").upper()
        if country == "AE":
            country = "UAE"

        industry = result.get("type") or result.get("category")
        osm_id = result.get("osm_id")
        osm_url = f"https://www.openstreetmap.org/{result.get('osm_type', 'node')}/{osm_id}" if osm_id else None

        provenance = self._make_provenance(plan, url=osm_url, is_mock=False)

        return RawLead(
            provenance=provenance,
            company_name=name_en.split(",")[0].strip(),
            company_name_ar=name_ar,
            domain=domain,
            website=website,
            phone=phone,
            email=email,
            address=result.get("display_name"),
            city=city,
            country=country,
            industry=industry,
            raw_data={
                "osm_id": osm_id,
                "lat": result.get("lat"),
                "lon": result.get("lon"),
                "type": result.get("type"),
                "extra_tags": extra_tags,
            },
        )

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        country_codes = query.icp.geo.countries or ["SA"]

        try:
            results = await self._search(plan.query_string, country_codes)

            # Filter: only return amenities/shops/offices (business nodes)
            business_types = {
                "amenity", "shop", "office", "company", "building",
                "clinic", "hospital", "restaurant", "hotel", "school",
                "bank", "pharmacy", "supermarket",
            }
            filtered = [
                r for r in results
                if r.get("type") in business_types or r.get("category") in {"amenity", "shop", "office"}
            ]

            if not filtered:
                filtered = results  # Don't filter too aggressively

            leads = [self._parse_result(r, plan) for r in filtered[:15]]
            logger.info(f"[osm_nominatim] Found {len(leads)} results for: {plan.query_string[:60]}")
            return leads
        except Exception as e:
            logger.error(f"[osm_nominatim] Error: {e}")
            return self._mock_leads(query, plan, count=2)
