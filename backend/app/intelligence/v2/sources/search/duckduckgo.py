"""
DuckDuckGo HTML Search Source — Dealix Lead Intelligence Engine V2
=================================================================
Uses html.duckduckgo.com (no API key needed).
Respects DDG's robots.txt (no deep crawling, just SERP results).
"""

from __future__ import annotations

import logging
import re
from typing import List
from urllib.parse import quote_plus, urlparse

from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry

logger = logging.getLogger(__name__)

DDG_URL = "https://html.duckduckgo.com/html/"


class DuckDuckGoSource(BaseSource):
    """
    DuckDuckGo HTML search adapter.
    No API key required. Parses HTML SERP via regex/simple parsing.
    Rate-limited to avoid being blocked.
    """

    SOURCE_NAME = "duckduckgo"
    REQUIRES_KEY = False
    RATE_LIMIT_CPS = 0.3   # Be gentle — no key means be slow

    @with_retry(max_attempts=2, base_delay=3.0)
    @rate_limited(calls_per_second=0.3)
    async def _search(self, query: str) -> str:
        client = await self.get_client()
        data = {"q": query, "kl": "sa-ar"}  # Saudi Arabia locale
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ar-SA,ar;q=0.9,en;q=0.8",
            "Referer": "https://duckduckgo.com/",
        }
        resp = await client.post(DDG_URL, data=data, headers=headers)
        resp.raise_for_status()
        return resp.text

    def _parse_results(self, html: str, plan: SearchPlan) -> List[RawLead]:
        """Parse DDG HTML SERP. Extracts title, URL, snippet."""
        leads = []

        # Extract result blocks: <a class="result__a" href="...">title</a>
        # and <a class="result__snippet">snippet</a>
        result_links = re.findall(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
        snippets = re.findall(
            r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )

        for i, (url, title) in enumerate(result_links[:10]):
            # Clean HTML tags from title/snippet
            title_clean = re.sub(r"<[^>]+>", "", title).strip()
            snippet_clean = re.sub(r"<[^>]+>", "", snippets[i] if i < len(snippets) else "").strip()

            domain = urlparse(url).netloc.lstrip("www.") if url else None

            # Extract phone
            combined_text = f"{title_clean} {snippet_clean}"
            phone_match = re.search(r"(\+?966\s?\d[\d\s\-]{7,12}|\b05\d{8}\b)", combined_text)
            phone = phone_match.group(0).replace(" ", "") if phone_match else None

            email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", combined_text)
            email = email_match.group(0) if email_match else None

            provenance = self._make_provenance(plan, url=url, is_mock=False)
            lead = RawLead(
                provenance=provenance,
                company_name=title_clean.split(" - ")[0].strip() if title_clean else domain,
                domain=domain,
                website=url,
                phone=phone,
                email=email,
                description=snippet_clean,
                raw_data={"title": title_clean, "snippet": snippet_clean, "url": url},
            )
            leads.append(lead)

        return leads

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        try:
            html = await self._search(plan.query_string)
            leads = self._parse_results(html, plan)
            if leads:
                logger.info(f"[duckduckgo] Found {len(leads)} results for: {plan.query_string[:60]}")
                return leads
            # Fallback to mock if HTML parsing yielded nothing
            logger.warning("[duckduckgo] No results parsed from HTML, using mock")
            return self._mock_leads(query, plan, count=2)
        except Exception as e:
            logger.error(f"[duckduckgo] Error: {e}")
            return self._mock_leads(query, plan, count=2)
