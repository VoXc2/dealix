"""
Brave Search API Source — Dealix Lead Intelligence Engine V2
============================================================
Official Brave Search API — privacy-focused, good Gulf coverage.
Env var: BRAVE_SEARCH_KEY
Docs: https://api.search.brave.com/
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

BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"


class BraveSearchSource(BaseSource):
    """
    Brave Search API adapter.
    Falls back to mock data when BRAVE_SEARCH_KEY is missing.
    Free plan: 2000 queries/month.
    """

    SOURCE_NAME = "brave_search"
    REQUIRES_KEY = True
    RATE_LIMIT_CPS = 1.0   # Brave allows up to 1 QPS on free tier

    @property
    def api_key(self) -> str | None:
        return os.getenv("BRAVE_SEARCH_KEY")

    @with_retry(max_attempts=3, base_delay=1.0)
    @rate_limited(calls_per_second=1.0)
    async def _search(self, query: str) -> dict:
        client = await self.get_client()
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }
        params = {
            "q": query,
            "count": 10,
            "country": "sa",
            "search_lang": "ar",
            "ui_lang": "ar-SA",
            "safesearch": "moderate",
            "freshness": None,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        resp = await client.get(BRAVE_API_URL, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def _parse_result(self, result: dict, plan: SearchPlan) -> RawLead:
        url = result.get("url", "")
        domain = urlparse(url).netloc.lstrip("www.") if url else None

        description = result.get("description", "") or ""
        title = result.get("title", "") or ""
        combined = f"{title} {description}"

        phone_match = re.search(r"(\+?966\s?\d[\d\s\-]{7,12}|\b05\d{8}\b)", combined)
        phone = phone_match.group(0).replace(" ", "") if phone_match else None

        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", combined)
        email = email_match.group(0) if email_match else None

        provenance = self._make_provenance(plan, url=url, is_mock=False)
        return RawLead(
            provenance=provenance,
            company_name=title.split(" - ")[0].strip() if title else domain,
            domain=domain,
            website=url,
            phone=phone,
            email=email,
            description=description,
            raw_data=result,
        )

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        if not self.api_key:
            logger.info("[brave_search] No API key — returning mock data")
            return self._mock_leads(query, plan, count=3)

        try:
            data = await self._search(plan.query_string)
            results = data.get("web", {}).get("results", [])
            leads = [self._parse_result(r, plan) for r in results]
            logger.info(f"[brave_search] Found {len(leads)} results for: {plan.query_string[:60]}")
            return leads
        except Exception as e:
            logger.error(f"[brave_search] Error: {e}")
            return self._mock_leads(query, plan, count=2)
