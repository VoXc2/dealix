"""
Google Custom Search API Source — Dealix Lead Intelligence Engine V2
====================================================================
Uses Google Custom Search JSON API with CSE (Programmable Search Engine).
Env vars: GOOGLE_CSE_KEY, GOOGLE_CSE_CX
"""

from __future__ import annotations

import logging
import os
import re
from typing import List
from urllib.parse import urlparse

from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry

logger = logging.getLogger(__name__)

GOOGLE_CSE_API = "https://www.googleapis.com/customsearch/v1"


class GoogleCustomSearchSource(BaseSource):
    """
    Google Custom Search API adapter.
    Returns up to 10 results per query (API limit).
    Falls back to mock data when GOOGLE_CSE_KEY or GOOGLE_CSE_CX are missing.
    """

    SOURCE_NAME = "google_custom_search"
    REQUIRES_KEY = True
    RATE_LIMIT_CPS = 0.5    # Google CSE: 100/day free, don't hammer

    @property
    def api_key(self) -> str | None:
        return os.getenv("GOOGLE_CSE_KEY")

    @property
    def cse_cx(self) -> str | None:
        return os.getenv("GOOGLE_CSE_CX")

    @with_retry(max_attempts=3, base_delay=2.0)
    @rate_limited(calls_per_second=0.5)
    async def _search(self, query: str, start: int = 1) -> dict:
        client = await self.get_client()
        params = {
            "key": self.api_key,
            "cx": self.cse_cx,
            "q": query,
            "start": start,
            "num": 10,
            "gl": "sa",        # Geolocation bias: Saudi Arabia
            "lr": "lang_ar",   # Language: Arabic preferred
        }
        resp = await client.get(GOOGLE_CSE_API, params=params)
        resp.raise_for_status()
        return resp.json()

    def _parse_item(self, item: dict, plan: SearchPlan) -> RawLead:
        """Parse a single CSE result item into a RawLead."""
        provenance = self._make_provenance(plan, url=item.get("link"), is_mock=False)

        link = item.get("link", "")
        domain = urlparse(link).netloc.lstrip("www.") if link else None

        # Extract phone from snippet using regex
        snippet = item.get("snippet", "") + " " + item.get("title", "")
        phone_match = re.search(r"(\+?966\s?\d[\d\s\-]{7,12}|\b05\d{8}\b)", snippet)
        phone = phone_match.group(0).replace(" ", "") if phone_match else None

        # Extract email from snippet
        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", snippet)
        email = email_match.group(0) if email_match else None

        return RawLead(
            provenance=provenance,
            company_name=item.get("title", "").split(" - ")[0].strip(),
            domain=domain,
            website=link,
            phone=phone,
            email=email,
            description=item.get("snippet"),
            raw_data=item,
        )

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        if not self.api_key or not self.cse_cx:
            logger.info("[google_custom_search] No API key/CX — returning mock data")
            return self._mock_leads(query, plan, count=3)

        try:
            data = await self._search(plan.query_string)
            items = data.get("items", [])
            leads = [self._parse_item(item, plan) for item in items]
            logger.info(f"[google_custom_search] Found {len(leads)} results for: {plan.query_string[:60]}")
            return leads
        except Exception as e:
            logger.error(f"[google_custom_search] Error: {e}")
            return self._mock_leads(query, plan, count=2)
