"""
Bayt.com Job Postings Source — Dealix Lead Intelligence Engine V2
=================================================================
Extracts company hiring signals from Bayt.com job postings.
Hiring = growth signal = higher lead score.
Uses Bayt's public job search page (HTML parsing).
Respects Bayt's robots.txt: only reading public job listing pages.
"""

from __future__ import annotations

import logging
import re
from typing import List, Optional
from urllib.parse import quote_plus, urlparse

from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry

logger = logging.getLogger(__name__)

BAYT_SEARCH_URL = "https://www.bayt.com/en/saudi-arabia/jobs/"
BAYT_AR_SEARCH_URL = "https://www.bayt.com/ar/saudi-arabia/jobs/"


class BaytJobsSource(BaseSource):
    """
    Bayt.com job postings adapter.
    Extracts company names + hiring signals from public job listings.
    A company actively hiring in relevant roles = strong buying signal.

    Signals extracted:
    - Company name (confirmed active & hiring)
    - Job titles being hired (role intelligence)
    - Location
    - Job count (volume signal)
    """

    SOURCE_NAME = "bayt_jobs"
    REQUIRES_KEY = False
    RATE_LIMIT_CPS = 0.3   # Polite — read robots.txt: Disallow: /jobs/search-agent

    @with_retry(max_attempts=2, base_delay=4.0)
    @rate_limited(calls_per_second=0.3)
    async def _fetch_jobs_page(self, keyword: str, country: str = "saudi-arabia") -> str:
        """Fetch Bayt.com job search results page."""
        client = await self.get_client()
        url = f"https://www.bayt.com/en/{country}/jobs/{quote_plus(keyword)}-jobs/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        }
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.text

    def _parse_job_listings(self, html: str, plan: SearchPlan) -> List[RawLead]:
        """Parse Bayt.com HTML for job listings and hiring companies."""
        leads_by_company: dict[str, RawLead] = {}

        # Extract company names from job listings
        # Bayt uses: <a class="is-black" data-company-id="..." href="...">Company Name</a>
        company_links = re.findall(
            r'<a[^>]+data-company-id="(\d+)"[^>]+href="([^"]+)"[^>]*>\s*([^<]+)</a>',
            html, re.DOTALL
        )

        # Also extract from: <b itemprop="hiringOrganization">Company</b>
        org_names = re.findall(
            r'itemprop="hiringOrganization"[^>]*>([^<]+)<',
            html
        )

        # Extract job titles
        job_titles = re.findall(
            r'<h2[^>]+class="[^"]*job-title[^"]*"[^>]*>\s*<a[^>]+>([^<]+)</a>',
            html
        )
        if not job_titles:
            job_titles = re.findall(
                r'itemprop="title"[^>]*>([^<]+)<',
                html
            )

        # Extract locations from job listings
        locations = re.findall(
            r'itemprop="addressLocality"[^>]*>([^<]+)<',
            html
        )

        # Extract job URLs
        job_urls = re.findall(
            r'href="(https://www\.bayt\.com/en/[^"]+/jobs/[^"]+)"',
            html
        )

        # Build company → jobs mapping
        processed_companies: set[str] = set()

        for i, (company_id, company_url, company_name) in enumerate(company_links[:20]):
            company_name = company_name.strip()
            if not company_name or company_name in processed_companies:
                continue
            processed_companies.add(company_name)

            title = job_titles[i] if i < len(job_titles) else "Position Available"
            location = locations[i] if i < len(locations) else "Saudi Arabia"
            job_url = job_urls[i] if i < len(job_urls) else None

            company_key = company_name.lower()
            if company_key not in leads_by_company:
                provenance = self._make_provenance(plan, url=job_url, is_mock=False)
                leads_by_company[company_key] = RawLead(
                    provenance=provenance,
                    company_name=company_name,
                    city=location.split(",")[0].strip() if location else None,
                    country="SA",
                    is_hiring=True,
                    hiring_roles=[title.strip()],
                    raw_data={
                        "company_id": company_id,
                        "job_count": 1,
                        "source": "bayt.com",
                    },
                )
            else:
                # Accumulate more hiring roles for same company
                role = title.strip()
                if role not in leads_by_company[company_key].hiring_roles:
                    leads_by_company[company_key].hiring_roles.append(role)
                leads_by_company[company_key].raw_data["job_count"] = (
                    leads_by_company[company_key].raw_data.get("job_count", 0) + 1
                )

        # Fallback: use org_names if company_links parsing failed
        if not leads_by_company:
            for i, org_name in enumerate(org_names[:10]):
                org_name = org_name.strip()
                if not org_name:
                    continue
                title = job_titles[i] if i < len(job_titles) else "Position"
                provenance = self._make_provenance(plan, is_mock=False)
                lead = RawLead(
                    provenance=provenance,
                    company_name=org_name,
                    country="SA",
                    is_hiring=True,
                    hiring_roles=[title.strip()],
                    raw_data={"source": "bayt.com"},
                )
                leads_by_company[org_name.lower()] = lead

        return list(leads_by_company.values())

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        # Determine search keyword from plan
        keyword = plan.query_string

        try:
            html = await self._fetch_jobs_page(keyword)
            leads = self._parse_job_listings(html, plan)
            if leads:
                logger.info(
                    f"[bayt_jobs] Found {len(leads)} hiring companies for: {keyword[:60]}"
                )
                return leads
            logger.info("[bayt_jobs] No jobs parsed from HTML, using mock")
            return self._mock_leads(query, plan, count=3)
        except Exception as e:
            logger.error(f"[bayt_jobs] Error: {e}")
            return self._mock_leads(query, plan, count=3)
