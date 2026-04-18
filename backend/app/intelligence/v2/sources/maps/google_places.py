"""
Google Places (New) API Source — Dealix Lead Intelligence Engine V2
===================================================================
Uses Google Places API v1 Text Search + Place Details.
Env var: GOOGLE_PLACES_KEY
Docs: https://developers.google.com/maps/documentation/places/web-service/text-search
"""

from __future__ import annotations

import logging
import os
import re
from typing import List, Optional

from app.intelligence.v2.gulf_geo import SAUDI_CITIES, get_city_bbox
from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry

logger = logging.getLogger(__name__)

PLACES_TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
PLACES_DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"

# Fields to request from Places API
TEXT_SEARCH_FIELDS = (
    "places.id,places.displayName,places.formattedAddress,"
    "places.nationalPhoneNumber,places.internationalPhoneNumber,"
    "places.websiteUri,places.rating,places.userRatingCount,"
    "places.businessStatus,places.primaryTypeDisplayName,"
    "places.location,places.regularOpeningHours"
)


class GooglePlacesSource(BaseSource):
    """
    Google Places (New) Text Search + Details adapter.
    Best source for local Saudi business discovery (restaurants, clinics, etc.)
    Falls back to mock data when GOOGLE_PLACES_KEY is missing.
    """

    SOURCE_NAME = "google_places"
    REQUIRES_KEY = True
    RATE_LIMIT_CPS = 0.5   # ~100K requests/month free; be conservative

    @property
    def api_key(self) -> str | None:
        return os.getenv("GOOGLE_PLACES_KEY")

    def _get_location_bias(self, query: DiscoveryQuery) -> dict | None:
        """Build a location bias dict for the Places API."""
        cities = query.icp.geo.cities
        if cities:
            bbox = get_city_bbox(cities[0].lower())
            if bbox:
                lat_min, lon_min, lat_max, lon_max = bbox
                center_lat = (lat_min + lat_max) / 2
                center_lon = (lon_min + lon_max) / 2
                radius = max(
                    abs(lat_max - lat_min),
                    abs(lon_max - lon_min)
                ) * 111_000 / 2  # rough meters
                return {
                    "circle": {
                        "center": {"latitude": center_lat, "longitude": center_lon},
                        "radius": min(radius, 50_000),  # cap at 50km
                    }
                }
        # Default: Saudi Arabia center
        return {
            "circle": {
                "center": {"latitude": 24.68, "longitude": 46.72},
                "radius": 500_000,
            }
        }

    @with_retry(max_attempts=3, base_delay=2.0)
    @rate_limited(calls_per_second=0.5)
    async def _text_search(self, query: str, location_bias: dict | None) -> dict:
        client = await self.get_client()
        body = {
            "textQuery": query,
            "languageCode": "ar",
            "maxResultCount": 20,
        }
        if location_bias:
            body["locationBias"] = location_bias

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": TEXT_SEARCH_FIELDS,
        }
        resp = await client.post(PLACES_TEXT_SEARCH_URL, json=body, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def _parse_place(self, place: dict, plan: SearchPlan) -> RawLead:
        place_id = place.get("id", "")
        display_name = place.get("displayName", {})
        name = display_name.get("text", "") if isinstance(display_name, dict) else str(display_name)
        # Try to get Arabic name
        name_ar = None
        if display_name.get("languageCode") == "ar":
            name_ar = name

        phone = place.get("internationalPhoneNumber") or place.get("nationalPhoneNumber")
        website = place.get("websiteUri")
        domain = None
        if website:
            from urllib.parse import urlparse
            domain = urlparse(website).netloc.lstrip("www.")

        address = place.get("formattedAddress", "")
        primary_type = place.get("primaryTypeDisplayName", {})
        industry = primary_type.get("text") if isinstance(primary_type, dict) else str(primary_type)

        rating = place.get("rating")
        review_count = place.get("userRatingCount")

        provenance = self._make_provenance(
            plan,
            url=f"https://maps.google.com/?cid={place_id}",
            is_mock=False,
        )

        return RawLead(
            provenance=provenance,
            company_name=name,
            company_name_ar=name_ar,
            domain=domain,
            website=website,
            phone=phone,
            address=address,
            industry=industry,
            place_id=place_id,
            rating=rating,
            review_count=review_count,
            raw_data=place,
        )

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        if not self.api_key:
            logger.info("[google_places] No API key — returning mock data")
            return self._mock_leads(query, plan, count=5)

        try:
            location_bias = self._get_location_bias(query)
            data = await self._text_search(plan.query_string, location_bias)
            places = data.get("places", [])
            leads = [self._parse_place(p, plan) for p in places]
            logger.info(f"[google_places] Found {len(leads)} places for: {plan.query_string[:60]}")
            return leads
        except Exception as e:
            logger.error(f"[google_places] Error: {e}")
            return self._mock_leads(query, plan, count=3)
