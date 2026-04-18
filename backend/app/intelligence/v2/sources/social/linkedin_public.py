"""
LinkedIn Public Search Source — Dealix Lead Intelligence Engine V2
=================================================================
LinkedIn company/person discovery via Google site:linkedin.com queries.
Uses Google Custom Search or DuckDuckGo as the actual search backend.
No LinkedIn API key required (uses public indexing).
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

DDG_URL = "https://html.duckduckgo.com/html/"


class LinkedInPublicSource(BaseSource):
    """
    LinkedIn public company search via site:linkedin.com Google/DDG queries.
    Extracts company URLs, names, and descriptions from search results.
    For full profile data, LinkedIn Sales Navigator API would be needed.
    """

    SOURCE_NAME = "linkedin_public"
    REQUIRES_KEY = False
    RATE_LIMIT_CPS = 0.2   # Very slow — mimicking human browsing

    @with_retry(max_attempts=2, base_delay=5.0)
    @rate_limited(calls_per_second=0.2)
    async def _search_ddg(self, query: str) -> str:
        """Use DuckDuckGo to search LinkedIn company pages."""
        client = await self.get_client()
        # Prefix with site:linkedin.com to target LinkedIn
        li_query = f"site:linkedin.com/company {query}"
        data = {"q": li_query, "kl": "sa-ar"}
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }
        resp = await client.post(DDG_URL, data=data, headers=headers)
        resp.raise_for_status()
        return resp.text

    def _parse_linkedin_results(self, html: str, plan: SearchPlan) -> List[RawLead]:
        """Parse DDG SERP for LinkedIn company links."""
        leads = []

        # Find all LinkedIn company URLs and titles
        result_links = re.findall(
            r'<a[^>]+class="result__a"[^>]+href="(https://(?:www\.)?linkedin\.com/company/[^"]+)"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
        snippets = re.findall(
            r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )

        for i, (url, title) in enumerate(result_links[:10]):
            title_clean = re.sub(r"<[^>]+>", "", title).strip()
            snippet_clean = re.sub(r"<[^>]+>", "", snippets[i] if i < len(snippets) else "").strip()

            # Extract company slug from LinkedIn URL
            slug_match = re.search(r"linkedin\.com/company/([^/?&]+)", url)
            company_slug = slug_match.group(1) if slug_match else None

            # Try to extract company name and HQ from snippet
            hq_match = re.search(
                r"(?:Headquarters|Location|HQ|مقر)[:\s]+([^\|\.]+)",
                snippet_clean, re.IGNORECASE
            )
            employees_match = re.search(
                r"([\d,]+)\s*(?:employees|موظف)",
                snippet_clean, re.IGNORECASE
            )

            provenance = self._make_provenance(plan, url=url, is_mock=False)
            lead = RawLead(
                provenance=provenance,
                company_name=title_clean.split(" | ")[0].strip() if title_clean else company_slug,
                linkedin_url=url,
                description=snippet_clean,
                raw_data={
                    "linkedin_url": url,
                    "company_slug": company_slug,
                    "headquarters": hq_match.group(1).strip() if hq_match else None,
                    "employees_text": employees_match.group(0) if employees_match else None,
                    "snippet": snippet_clean,
                },
            )
            leads.append(lead)

        return leads

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        try:
            html = await self._search_ddg(plan.query_string)
            leads = self._parse_linkedin_results(html, plan)
            if leads:
                logger.info(
                    f"[linkedin_public] Found {len(leads)} LinkedIn companies "
                    f"for: {plan.query_string[:60]}"
                )
                return leads
            # No results parsed, use mock
            logger.info("[linkedin_public] No LinkedIn results parsed, using mock")
            return self._mock_leads(query, plan, count=2)
        except Exception as e:
            logger.error(f"[linkedin_public] Error: {e}")
            return self._mock_leads(query, plan, count=2)
