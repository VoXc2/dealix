"""
Hiring Intent Source — LinkedIn Jobs, Bayt, Taqat
==================================================
Detects active hiring signals as a proxy for company growth and budget availability.

INTENT LOGIC:
  ┌──────────────────────────────────────────────────┐
  │ Company hiring → growing → has budget → buy now  │
  └──────────────────────────────────────────────────┘

  High-value hiring patterns:
  - "Sales Director" / "VP Sales" → scaling revenue ops → hot lead
  - "Software Engineer" (5+ positions) → scaling tech → digital budget
  - "Marketing Manager" / "Growth Manager" → investing in acquisition
  - "Finance Manager" → formalising operations → enterprise-ready

STATUS: Stub implementation.
TODO: Integrate live job board APIs.
  - LinkedIn Jobs: via Unipile API (see linkedin.py)
  - Bayt.com: web data extraction (check ToS / API availability)
  - Taqat (HADAF): Saudi national employment platform API
  - Indeed: Indeed Publisher API (requires application)
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import httpx

from ..models import Company, HiringSignal, Signal, SignalType


# ─────────────────────────── Seniority Detection ─────────────────────────────

SENIORITY_KEYWORDS: dict[str, list[str]] = {
    "c_level": ["CEO", "CTO", "CMO", "CFO", "COO", "Chief", "مدير عام", "الرئيس التنفيذي"],
    "vp": ["VP", "Vice President", "نائب الرئيس"],
    "director": ["Director", "مدير", "Head of"],
    "manager": ["Manager", "Lead", "مشرف"],
    "individual_contributor": ["Engineer", "Specialist", "Analyst", "مهندس", "محلل"],
}

# Seed hiring signals for demo
SEED_HIRING: list[dict[str, Any]] = [
    {
        "company_name": "Salla",
        "jobs": [
            {"title": "Senior Backend Engineer", "department": "Engineering", "seniority": "individual_contributor"},
            {"title": "VP of Marketing", "department": "Marketing", "seniority": "vp"},
            {"title": "Head of Sales", "department": "Sales", "seniority": "director"},
        ],
    },
    {
        "company_name": "Foodics",
        "jobs": [
            {"title": "Sales Manager - KSA", "department": "Sales", "seniority": "manager"},
            {"title": "Customer Success Manager", "department": "CS", "seniority": "manager"},
            {"title": "Senior Product Manager", "department": "Product", "seniority": "individual_contributor"},
            {"title": "Data Engineer", "department": "Engineering", "seniority": "individual_contributor"},
        ],
    },
    {
        "company_name": "Tabby",
        "jobs": [
            {"title": "Enterprise Sales Director", "department": "Sales", "seniority": "director"},
            {"title": "CFO", "department": "Finance", "seniority": "c_level"},
            {"title": "Mobile Engineer (iOS/Android)", "department": "Engineering", "seniority": "individual_contributor"},
        ],
    },
    {
        "company_name": "ROSHN",
        "jobs": [
            {"title": "Digital Marketing Manager", "department": "Marketing", "seniority": "manager"},
            {"title": "CRM Manager", "department": "Sales", "seniority": "manager"},
            {"title": "Head of Technology", "department": "IT", "seniority": "director"},
        ],
    },
    {
        "company_name": "Noon Academy",
        "jobs": [
            {"title": "Growth Marketing Lead", "department": "Marketing", "seniority": "manager"},
            {"title": "Android Engineer", "department": "Engineering", "seniority": "individual_contributor"},
        ],
    },
]

# Score weight by seniority of open role
SENIORITY_SCORE_WEIGHT = {
    "c_level": 20.0,
    "vp": 15.0,
    "director": 12.0,
    "manager": 8.0,
    "individual_contributor": 4.0,
}


class HiringIntentSource:
    """
    مصدر إشارات التوظيف — Hiring Intent Intelligence.

    يجمع بيانات التوظيف من:
    1. LinkedIn Jobs (عبر Unipile)
    2. Bayt.com
    3. Taqat (منصة هدف السعودية)
    4. Indeed Saudi Arabia

    يُنتج:
    - HiringSignal objects لكل وظيفة مفتوحة
    - نتيجة intent مجمّعة بناءً على حجم + سنوية التوظيف
    """

    BAYT_BASE_URL = "https://www.bayt.com/api/v1"
    TAQAT_BASE_URL = "https://api.taqat.gov.sa/v1"

    def __init__(
        self,
        linkedin_api_key: str | None = None,
        bayt_api_key: str | None = None,
        session: httpx.AsyncClient | None = None,
    ) -> None:
        self.linkedin_api_key = linkedin_api_key
        self.bayt_api_key = bayt_api_key
        self._session = session

    # ─────────────────────────── Public API ─────────────────────────────────

    async def get_hiring_signals(
        self,
        company: Company,
        days_back: int = 90,
    ) -> list[HiringSignal]:
        """
        جلب إشارات التوظيف النشطة للشركة المستهدفة.

        Args:
            company: الشركة المستهدفة
            days_back: عدد الأيام للبحث فيها

        Returns:
            قائمة بإشارات التوظيف مع تفاصيل الوظيفة والسنوية.
        """
        if not self.linkedin_api_key and not self.bayt_api_key:
            return self._get_seed_signals(company)

        signals_all: list[HiringSignal] = []

        # Gather from all sources in parallel
        import asyncio
        tasks = []
        if self.linkedin_api_key:
            tasks.append(self._fetch_linkedin_jobs(company, days_back))
        if self.bayt_api_key:
            tasks.append(self._fetch_bayt_jobs(company, days_back))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, list):
                signals_all.extend(result)

        return signals_all

    async def get_signals(self, company: Company) -> list[Signal]:
        """
        تحويل إشارات التوظيف إلى نقاط قابلة للتسجيل.
        """
        hiring = await self.get_hiring_signals(company)
        signals: list[Signal] = []

        if not hiring:
            return signals

        total_jobs = len(hiring)
        max_seniority_score = 0.0

        for job in hiring:
            s = SENIORITY_SCORE_WEIGHT.get(job.seniority or "individual_contributor", 4.0)
            max_seniority_score = max(max_seniority_score, s)

            signals.append(
                Signal(
                    signal_type=SignalType.HIRING,
                    title=f"وظيفة مفتوحة: {job.job_title}",
                    description=f"القسم: {job.department or 'غير محدد'} | المصدر: {job.source}",
                    score_contribution=s,
                    source=job.source,
                    detected_at=job.posted_at or datetime.utcnow(),
                )
            )

        # Volume bonus: many open roles = high growth
        if total_jobs >= 5:
            signals.append(
                Signal(
                    signal_type=SignalType.HIRING,
                    title=f"توظيف كثيف: {total_jobs} وظيفة مفتوحة",
                    description="عدد كبير من الوظائف المفتوحة يدل على نمو قوي",
                    score_contribution=min(15.0, total_jobs * 1.5),
                    source="hiring_aggregate",
                )
            )

        return signals

    # ─────────────────────────── Seed Data ───────────────────────────────────

    def _get_seed_signals(self, company: Company) -> list[HiringSignal]:
        """استرجاع إشارات التوظيف من بيانات الـ seed."""
        for entry in SEED_HIRING:
            if company.name and entry["company_name"].lower() in company.name.lower():
                return [
                    HiringSignal(
                        job_title=job["title"],
                        department=job.get("department"),
                        location="Saudi Arabia",
                        posted_at=datetime.utcnow() - timedelta(days=15),
                        source="linkedin_jobs",
                        seniority=job.get("seniority", "individual_contributor"),
                    )
                    for job in entry["jobs"]
                ]
        return []

    # ─────────────────────────── LinkedIn Jobs (stub) ────────────────────────

    async def _fetch_linkedin_jobs(
        self, company: Company, days_back: int
    ) -> list[HiringSignal]:
        """
        جلب وظائف LinkedIn Jobs عبر Unipile.

        TODO: Implement via Unipile LinkedIn Jobs endpoint.
        Endpoint: POST https://api.unipile.com/api/v1/linkedin/job-postings
        Body: { "account_id": "...", "company_id": "...", "location": "Saudi Arabia" }
        """
        raise NotImplementedError(
            "TODO: Implement LinkedIn Jobs fetch via Unipile.\n"
            "Credentials needed: UNIPILE_API_KEY, UNIPILE_LINKEDIN_ACCOUNT_ID\n"
            "Endpoint: POST https://api.unipile.com/api/v1/linkedin/job-postings\n"
            "Body: {\n"
            "  'account_id': '...',\n"
            "  'company_id': '...',  # LinkedIn company numeric ID\n"
            "  'location': 'Saudi Arabia',\n"
            "  'datePosted': 'past-month'\n"
            "}"
        )

    # ─────────────────────────── Bayt.com (stub) ─────────────────────────────

    async def _fetch_bayt_jobs(
        self, company: Company, days_back: int
    ) -> list[HiringSignal]:
        """
        جلب وظائف Bayt.com.

        TODO: Check Bayt API availability (may require partnership).
        Alternative: Use SerpAPI Google Jobs search targeting bayt.com.
        """
        raise NotImplementedError(
            "TODO: Implement Bayt.com job listing fetch.\n"
            "Option 1 — Bayt API (requires partnership):\n"
            "  Contact: api@bayt.com\n"
            "  Base URL: https://www.bayt.com/api/v1/jobs\n"
            "\n"
            "Option 2 — SerpAPI Google Jobs (recommended workaround):\n"
            "  Credential: SERPAPI_KEY\n"
            "  Query: site:bayt.com {company_name} Saudi Arabia jobs\n"
            "  Endpoint: https://serpapi.com/search.json?engine=google_jobs&q=...\n"
        )

    # ─────────────────────────── Taqat (stub) ────────────────────────────────

    async def _fetch_taqat_jobs(self, company: Company) -> list[HiringSignal]:
        """
        جلب وظائف منصة طاقات (هدف) — التوظيف الحكومي السعودي.

        TODO: Implement Taqat/HADAF API integration.
        Endpoint: https://api.taqat.gov.sa/v1/jobs
        Requires: TAQAT_API_KEY (contact: portal@taqat.gov.sa)
        """
        raise NotImplementedError(
            "TODO: Implement Taqat (HADAF) job fetch.\n"
            "Credential needed: TAQAT_API_KEY\n"
            "Set env var: TAQAT_API_KEY\n"
            "Portal: https://www.taqat.gov.sa\n"
            "Contact for API access: portal@taqat.gov.sa\n"
            "Endpoint: GET https://api.taqat.gov.sa/v1/jobs?company={name}&location=SA"
        )

    # ─────────────────────────── Utils ───────────────────────────────────────

    @staticmethod
    def detect_seniority(job_title: str) -> str:
        """تحديد سنوية المنصب من المسمى الوظيفي."""
        title_lower = job_title.lower()
        for seniority, keywords in SENIORITY_KEYWORDS.items():
            if any(kw.lower() in title_lower for kw in keywords):
                return seniority
        return "individual_contributor"
