"""
LinkedIn Intelligence Source — via Unipile API
===============================================
Discovers decision-makers, company updates, and hiring signals from LinkedIn
using the Unipile unified social API (GDPR-compliant, within ToS).

WHY UNIPILE: LinkedIn ToS prohibits direct scraping. Unipile provides an
official API gateway that handles LinkedIn sessions legally via their
managed infrastructure.

STATUS: Stub implementation.
TODO: Connect Unipile API once credentials are available.
  - Unipile API key + Account ID (LinkedIn session via Unipile dashboard)
  - Endpoint docs: https://api.unipile.com/docs

ENDPOINTS NEEDED:
  POST /linkedin/company/employees  → paginated list of employees
  POST /linkedin/company/info       → company details + follower count
  POST /linkedin/search/people      → people search by title + company
  GET  /linkedin/job-postings       → open jobs for a company page
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from ..models import Company, Contact, HiringSignal, Signal, SignalType


class LinkedInSource:
    """
    مصدر بيانات LinkedIn عبر Unipile API.

    يوفر:
    - صانعو القرار (C-level, VP, Director)
    - تحديثات الشركة (توسع، إطلاق منتج، شراكة)
    - الوظائف المفتوحة (إشارات نمو)
    - بيانات الموظفين (تحقق من الحجم)

    Compliance note: يستخدم Unipile فقط — لا web scraping مباشر.
    """

    UNIPILE_BASE_URL = "https://api.unipile.com/api/v1"

    def __init__(
        self,
        api_key: str | None = None,
        account_id: str | None = None,
        session: httpx.AsyncClient | None = None,
    ) -> None:
        """
        Args:
            api_key: مفتاح Unipile API — متغير البيئة: UNIPILE_API_KEY
            account_id: معرّف حساب LinkedIn في Unipile — متغير البيئة: UNIPILE_LINKEDIN_ACCOUNT_ID
            session: httpx.AsyncClient اختياري للمشاركة
        """
        self.api_key = api_key
        self.account_id = account_id
        self._session = session

    # ─────────────────────────── Public API ─────────────────────────────────

    async def get_decision_makers(
        self,
        company: Company,
        titles: list[str] | None = None,
        max_results: int = 10,
    ) -> list[Contact]:
        """
        جلب صانعي القرار من LinkedIn للشركة المستهدفة.

        Args:
            company: الشركة المستهدفة
            titles: قائمة بالمسمّيات الوظيفية للبحث عنها.
                    الافتراضي: CEO, CTO, CMO, VP, Director
            max_results: الحد الأقصى للنتائج

        Returns:
            قائمة بجهات الاتصال مع بيانات LinkedIn.
        """
        if not self.api_key:
            raise NotImplementedError(
                "TODO: Implement LinkedIn decision-maker lookup via Unipile.\n"
                "Credentials needed:\n"
                "  UNIPILE_API_KEY — from https://dashboard.unipile.com\n"
                "  UNIPILE_LINKEDIN_ACCOUNT_ID — LinkedIn session ID in Unipile\n"
                "Endpoint: POST https://api.unipile.com/api/v1/linkedin/search/people\n"
                "Body: {\n"
                "  'account_id': '{UNIPILE_LINKEDIN_ACCOUNT_ID}',\n"
                "  'keywords': '{company_name}',\n"
                "  'title': 'CEO OR CTO OR CMO OR VP OR Director',\n"
                "  'current_company': '{company_linkedin_id}'\n"
                "}\n"
                "Headers: X-API-KEY: {UNIPILE_API_KEY}"
            )

        default_titles = titles or [
            "CEO", "Chief Executive Officer",
            "CTO", "Chief Technology Officer",
            "CMO", "Chief Marketing Officer",
            "VP Marketing", "VP Sales", "VP Growth",
            "Director", "Head of",
            "المدير التنفيذي", "نائب الرئيس",
        ]

        return await self._search_people(company, default_titles, max_results)

    async def get_company_info(self, company: Company) -> dict[str, Any]:
        """
        جلب معلومات الشركة من LinkedIn (متابعون، وصف، تحديثات).

        TODO: Implement Unipile company info endpoint.
        Endpoint: POST https://api.unipile.com/api/v1/linkedin/company/info
        Body: { "account_id": "...", "company_url": "linkedin.com/company/..." }
        """
        if not self.api_key:
            raise NotImplementedError(
                "TODO: Implement LinkedIn company info lookup via Unipile.\n"
                "Credentials needed: UNIPILE_API_KEY, UNIPILE_LINKEDIN_ACCOUNT_ID\n"
                "Endpoint: POST https://api.unipile.com/api/v1/linkedin/company/info\n"
                "Body: { 'account_id': '...', 'company_url': 'linkedin.com/company/{handle}' }"
            )
        raise NotImplementedError("TODO: Wire up live Unipile company info call")

    async def get_hiring_signals(self, company: Company) -> list[HiringSignal]:
        """
        جلب الوظائف المفتوحة من LinkedIn Jobs للشركة.

        TODO: Implement Unipile job postings endpoint.
        Endpoint: POST https://api.unipile.com/api/v1/linkedin/job-postings
        """
        if not self.api_key:
            raise NotImplementedError(
                "TODO: Implement LinkedIn job postings via Unipile.\n"
                "Credentials needed: UNIPILE_API_KEY, UNIPILE_LINKEDIN_ACCOUNT_ID\n"
                "Endpoint: POST https://api.unipile.com/api/v1/linkedin/job-postings\n"
                "Body: { 'account_id': '...', 'company_id': '...', 'location': 'Saudi Arabia' }"
            )
        raise NotImplementedError("TODO: Wire up live Unipile job postings call")

    async def get_signals(self, company: Company) -> list[Signal]:
        """
        استخراج إشارات قابلة للتسجيل من بيانات LinkedIn.

        يستخدم بيانات الـ social_handles الموجودة مع الشركة.
        """
        signals: list[Signal] = []

        # Signal: LinkedIn handle exists
        if company.social_handles.linkedin:
            signals.append(
                Signal(
                    signal_type=SignalType.CONTENT_ENGAGEMENT,
                    title="حضور على LinkedIn",
                    description=f"الشركة لديها صفحة LinkedIn: {company.social_handles.linkedin}",
                    score_contribution=5.0,
                    source="linkedin",
                )
            )

        # Signal: decision makers found
        if company.decision_makers:
            dm_count = len(company.decision_makers)
            signals.append(
                Signal(
                    signal_type=SignalType.CONTENT_ENGAGEMENT,
                    title=f"تم التعرف على {dm_count} صانع قرار",
                    description="وجود صانعي قرار معروفين يرفع نتيجة Authority",
                    score_contribution=min(20.0, dm_count * 5.0),
                    source="linkedin",
                )
            )

        return signals

    async def send_connection_request(
        self,
        contact: Contact,
        message: str,
    ) -> dict[str, Any]:
        """
        إرسال طلب تواصل على LinkedIn عبر Unipile.

        TODO: Implement after Unipile credentials are configured.
        Endpoint: POST https://api.unipile.com/api/v1/linkedin/connection-requests
        Body: { "account_id": "...", "profile_url": "...", "message": "..." }

        Compliance: يلتزم بحدود LinkedIn (max 20 requests/day per account).
        """
        if not self.api_key:
            raise NotImplementedError(
                "TODO: Implement LinkedIn connection request via Unipile.\n"
                "Credentials needed: UNIPILE_API_KEY, UNIPILE_LINKEDIN_ACCOUNT_ID\n"
                "Rate limit: LinkedIn allows max ~20 connection requests/day per account.\n"
                "Endpoint: POST https://api.unipile.com/api/v1/linkedin/connection-requests\n"
                "Body: {\n"
                "  'account_id': '...',\n"
                "  'profile_url': 'https://linkedin.com/in/...',\n"
                "  'message': 'رسالة الطلب (max 300 chars)'\n"
                "}"
            )
        raise NotImplementedError("TODO: Wire up live Unipile connection request")

    async def send_inmail(
        self,
        contact: Contact,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        """
        إرسال InMail عبر Unipile (يحتاج LinkedIn Premium).

        TODO: Implement after Unipile credentials are configured.
        """
        if not self.api_key:
            raise NotImplementedError(
                "TODO: Implement LinkedIn InMail via Unipile.\n"
                "Credentials needed: UNIPILE_API_KEY, UNIPILE_LINKEDIN_ACCOUNT_ID\n"
                "Requires: LinkedIn Premium/Sales Navigator account\n"
                "Endpoint: POST https://api.unipile.com/api/v1/linkedin/inmails"
            )
        raise NotImplementedError("TODO: Wire up live Unipile InMail")

    # ─────────────────────────── Private ─────────────────────────────────────

    async def _search_people(
        self,
        company: Company,
        titles: list[str],
        max_results: int,
    ) -> list[Contact]:
        """Unipile people search — live implementation."""
        # This branch is only reached when api_key is set
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "account_id": self.account_id,
            "keywords": company.name,
            "title": " OR ".join(titles[:5]),  # LinkedIn API limits OR clauses
            "location": "Saudi Arabia",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{self.UNIPILE_BASE_URL}/linkedin/search/people",
                json=payload,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()

        contacts = []
        for person in data.get("results", [])[:max_results]:
            contacts.append(
                Contact(
                    full_name=person.get("fullName", ""),
                    title=person.get("title"),
                    linkedin_url=person.get("profileUrl"),
                    source="linkedin_unipile",
                    enriched_at=datetime.utcnow(),
                    is_decision_maker=any(
                        t.lower() in (person.get("title") or "").lower()
                        for t in ["ceo", "cto", "cmo", "vp", "director", "chief"]
                    ),
                )
            )

        return contacts
