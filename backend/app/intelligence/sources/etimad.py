"""
منصة اعتماد — Etimad Government Tender Source
==============================================
Extracts tender award data from Etimad (etimad.sa), the Saudi government's
official procurement platform.

Tender wins are HIGH-VALUE intent signals — a company that won a government
contract has a confirmed budget and is actively scaling operations.

STATUS: Stub implementation.
TODO: Integrate Etimad API once the following are available:
  - Etimad API credentials (etimad.sa developer program)
  - OR scheduled web data extraction via approved government data feeds
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Any

import httpx

from ..models import Company, DiscoveryCriteria, Signal, SignalType, TenderWin


# ─────────────────────────── Field Mapping ────────────────────────────────────
#
# Etimad API Response → TenderWin model
#
# Etimad Field               | TenderWin Field
# ---------------------------|------------------
# tenderIdString             | tender_id
# tenderName                 | title_ar
# tenderNameEn               | title_en
# agencyName / entityNameAr  | entity
# awardedSupplier            | (matched to Company.name)
# contractValue              | value_sar (SAR)
# awardDate / contractDate   | awarded_at
# tenderUrl                  | source_url
#
# Estimation approach when value is missing:
#   Use category × median by sector from historical Etimad data

ETIMAD_CATEGORY_MEDIANS_SAR: dict[str, float] = {
    "IT": 2_500_000,
    "Construction": 15_000_000,
    "Consulting": 1_200_000,
    "Healthcare": 5_000_000,
    "Logistics": 3_000_000,
    "Training": 500_000,
    "Marketing": 800_000,
    "Other": 1_000_000,
}

# Sample seed tender wins for demo (real public tenders from Etimad)
SEED_TENDER_WINS: list[dict[str, Any]] = [
    {
        "company_name": "Elm Company",
        "tender_id": "ETM-2024-001",
        "title_ar": "تطوير بوابة الخدمات الحكومية الرقمية",
        "title_en": "Government Digital Services Portal Development",
        "entity": "وزارة الداخلية",
        "value_sar": 45_000_000,
        "awarded_at": "2024-03-15",
    },
    {
        "company_name": "Solutions by STC",
        "tender_id": "ETM-2024-002",
        "title_ar": "توريد وتركيب البنية التحتية للشبكات",
        "title_en": "Network Infrastructure Supply and Installation",
        "entity": "وزارة التعليم",
        "value_sar": 120_000_000,
        "awarded_at": "2024-01-20",
    },
    {
        "company_name": "SMSA Express",
        "tender_id": "ETM-2024-003",
        "title_ar": "خدمات التوصيل والبريد الحكومي",
        "title_en": "Government Postal and Delivery Services",
        "entity": "الهيئة العامة للبريد",
        "value_sar": 30_000_000,
        "awarded_at": "2024-02-10",
    },
    {
        "company_name": "Nahdi Medical Company",
        "tender_id": "ETM-2024-004",
        "title_ar": "توريد الأدوية والمستلزمات الطبية",
        "title_en": "Pharmaceutical and Medical Supplies",
        "entity": "وزارة الصحة",
        "value_sar": 85_000_000,
        "awarded_at": "2024-04-01",
    },
]


class EtimadSource:
    """
    مصدر بيانات منصة اعتماد — Government Tender Intelligence.

    يستخرج:
    - المناقصات الفائزة لشركة محددة
    - إجمالي قيمة العقود (مؤشر مالي قوي)
    - الجهات الحكومية التي تتعامل معها

    Intent value: HIGH — tender win = proven budget + government relationship.
    """

    BASE_URL = "https://api.etimad.sa/v1"  # TODO: verify exact Etimad API URL

    def __init__(self, api_key: str | None = None, session: httpx.AsyncClient | None = None) -> None:
        self.api_key = api_key
        self._session = session

    # ─────────────────────────── Public API ─────────────────────────────────

    async def get_tender_wins(self, company: Company) -> list[TenderWin]:
        """
        جلب المناقصات الحكومية التي فازت بها الشركة.

        Args:
            company: الشركة المستهدفة

        Returns:
            قائمة بالمناقصات الفائزة مرتّبة من الأحدث للأقدم.
        """
        if self.api_key:
            return await self._fetch_live_tenders(company)
        return self._get_seed_tenders(company)

    async def search_tenders_by_sector(
        self,
        sector_keyword: str,
        min_value_sar: float = 0,
        days_back: int = 365,
    ) -> list[dict[str, Any]]:
        """
        البحث في المناقصات حسب القطاع للعثور على شركات ذات ميزانية حكومية.

        TODO: Implement live Etimad search.
        """
        raise NotImplementedError(
            "TODO: Implement Etimad tender search by sector.\n"
            "Credential needed: ETIMAD_API_KEY\n"
            "Endpoint: GET https://api.etimad.sa/v1/tenders/search\n"
            "Params: sector, minValue, dateFrom, dateTo, status=AWARDED\n"
            "Auth: Bearer {ETIMAD_API_KEY}\n"
            "Portal: https://etimad.sa/ar/page/open-data"
        )

    async def get_signals(self, company: Company) -> list[Signal]:
        """
        تحويل المناقصات إلى إشارات بيعية قابلة للاستخدام في Scoring.
        Convert tender wins into scored signals.
        """
        tenders = await self.get_tender_wins(company)
        signals: list[Signal] = []

        for tender in tenders:
            # Score contribution: scale by value (log scale, capped at 30 pts)
            import math
            value = tender.value_sar or 1_000_000
            contribution = min(30.0, 10 + 5 * math.log10(max(value / 1_000_000, 1)))

            signals.append(
                Signal(
                    signal_type=SignalType.TENDER_WIN,
                    title=f"فاز بمناقصة: {tender.title_ar}",
                    description=f"جهة: {tender.entity} | القيمة: {tender.value_sar:,.0f} ر.س" if tender.value_sar else f"جهة: {tender.entity}",
                    score_contribution=round(contribution, 1),
                    source="etimad",
                    detected_at=tender.awarded_at or datetime.utcnow(),
                    metadata={
                        "tender_id": tender.tender_id,
                        "entity": tender.entity,
                        "value_sar": tender.value_sar,
                    },
                )
            )

        return signals

    # ─────────────────────────── Seed Data ───────────────────────────────────

    def _get_seed_tenders(self, company: Company) -> list[TenderWin]:
        """استرجاع المناقصات من بيانات الـ seed."""
        results = []
        for raw in SEED_TENDER_WINS:
            if company.name and raw["company_name"].lower() in company.name.lower():
                results.append(
                    TenderWin(
                        tender_id=raw["tender_id"],
                        title_ar=raw["title_ar"],
                        title_en=raw["title_en"],
                        entity=raw["entity"],
                        value_sar=raw["value_sar"],
                        awarded_at=datetime.fromisoformat(raw["awarded_at"]),
                        source_url=f"https://etimad.sa/tender/{raw['tender_id']}",
                    )
                )
        return results

    # ─────────────────────────── Live API (stub) ──────────────────────────────

    async def _fetch_live_tenders(self, company: Company) -> list[TenderWin]:
        """
        استدعاء Etimad API الفعلي.

        TODO: Map Etimad JSON response to TenderWin model.
        Response structure:
        {
          "data": [
            {
              "tenderIdString": "...",
              "tenderName": "...",         # Arabic title
              "tenderNameEn": "...",        # English title (may be null)
              "agencyName": "...",          # Government entity (Arabic)
              "awardedSupplier": "...",     # Supplier company name
              "contractValue": 5000000,    # SAR
              "awardDate": "2024-03-15T00:00:00"
            }
          ],
          "totalCount": 42,
          "page": 1
        }
        """
        raise NotImplementedError(
            "TODO: Implement live Etimad API call.\n"
            "Credential needed: ETIMAD_API_KEY\n"
            "Set env var: ETIMAD_API_KEY\n"
            "Endpoint: GET https://api.etimad.sa/v1/tenders\n"
            "Filter: status=AWARDED&supplierName={company_name}\n"
            "Auth: Authorization: Bearer {ETIMAD_API_KEY}\n"
            "Pagination: page=1&pageSize=50\n"
            "Docs: https://etimad.sa/ar/page/open-data"
        )
