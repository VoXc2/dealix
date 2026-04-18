"""
IntelligenceOrchestrator — Main Public API
==========================================
The top-level entry point for the Lead Intelligence Engine.

Ties together:
  Discovery → Enrichment → Scoring → Lead

Public API::

    orchestrator = IntelligenceOrchestrator()

    # Discover companies matching criteria
    companies = await orchestrator.discover(criteria)

    # Enrich + score a single company
    lead = await orchestrator.enrich(company)

    # Full pipeline: discover + enrich + score all
    leads = await orchestrator.run_pipeline(criteria)
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from .enrichment import EnrichmentPipeline, EnrichmentResult
from .models import (
    Company,
    Contact,
    DiscoveryCriteria,
    Lead,
    LeadStatus,
    Region,
    Sector,
)
from .scoring import LeadScorer
from .sources.etimad import EtimadSource
from .sources.hiring import HiringIntentSource
from .sources.linkedin import LinkedInSource
from .sources.news import NewsSource
from .sources.saudi_registry import SaudiBusinessRegistrySource
from .sources.tech_stack import TechStackSource

logger = logging.getLogger(__name__)


class IntelligenceOrchestrator:
    """
    المنسّق الرئيسي لمحرك الاستخبارات — Lead Intelligence Orchestrator.

    يتيح واجهة برمجية بسيطة لاكتشاف وإثراء وتسجيل الـ leads.

    Example::

        from app.intelligence import IntelligenceOrchestrator, DiscoveryCriteria, Sector

        orchestrator = IntelligenceOrchestrator()

        criteria = DiscoveryCriteria(
            sectors=[Sector.ECOMMERCE, Sector.B2B_SAAS],
            regions=[Region.RIYADH],
            min_employees=50,
            limit=20,
        )

        leads = await orchestrator.run_pipeline(criteria)
        for lead in leads:
            print(f"{lead.company.name}: {lead.dealix_score:.0f}/100 ({lead.priority_tier})")
    """

    def __init__(
        self,
        # Source credentials (all optional — fall back to seed/stubs)
        sbc_api_key: str | None = None,
        etimad_api_key: str | None = None,
        unipile_api_key: str | None = None,
        unipile_account_id: str | None = None,
        perplexity_api_key: str | None = None,
        bing_news_api_key: str | None = None,
        builtwith_api_key: str | None = None,
        # Scoring configuration
        score_weights: dict[str, float] | None = None,
        # Pipeline configuration
        enrichment_timeout: float = 30.0,
        max_concurrent_enrichments: int = 5,
    ) -> None:
        """
        تهيئة الـ Orchestrator مع بيانات الاعتماد الاختيارية.

        بدون بيانات اعتماد: يعمل على بيانات الـ seed ويُنتج نتائج تجريبية.
        مع بيانات اعتماد: يستدعي APIs حقيقية.

        Args:
            sbc_api_key: مفتاح API المركز السعودي للأعمال (SBC_API_KEY)
            etimad_api_key: مفتاح Etimad (ETIMAD_API_KEY)
            unipile_api_key: مفتاح Unipile (UNIPILE_API_KEY)
            unipile_account_id: معرّف حساب LinkedIn في Unipile
            perplexity_api_key: مفتاح Perplexity (PERPLEXITY_API_KEY)
            bing_news_api_key: مفتاح Bing News (BING_NEWS_API_KEY)
            builtwith_api_key: مفتاح BuiltWith (BUILTWITH_API_KEY)
            score_weights: أوزان مخصّصة لصيغة التسجيل
            enrichment_timeout: مهلة كل مصدر بالثواني
            max_concurrent_enrichments: الحد الأقصى للشركات المعالَجة في وقت واحد
        """
        # Initialize sources
        self._registry = SaudiBusinessRegistrySource(api_key=sbc_api_key)
        self._etimad = EtimadSource(api_key=etimad_api_key)
        self._linkedin = LinkedInSource(
            api_key=unipile_api_key,
            account_id=unipile_account_id,
        )
        self._news = NewsSource(
            perplexity_api_key=perplexity_api_key,
            bing_api_key=bing_news_api_key,
        )
        self._hiring = HiringIntentSource(linkedin_api_key=unipile_api_key)
        self._tech = TechStackSource(builtwith_api_key=builtwith_api_key)

        # Initialize pipeline components
        self._pipeline = EnrichmentPipeline(
            registry_source=self._registry,
            etimad_source=self._etimad,
            linkedin_source=self._linkedin,
            news_source=self._news,
            hiring_source=self._hiring,
            tech_source=self._tech,
            timeout_seconds=enrichment_timeout,
        )
        self._scorer = LeadScorer(weights=score_weights)
        self._max_concurrent = max_concurrent_enrichments

        # Stats tracking
        self._stats: dict[str, Any] = {
            "total_discovered": 0,
            "total_enriched": 0,
            "total_scored": 0,
            "pipeline_runs": 0,
            "started_at": datetime.utcnow().isoformat(),
        }

    # ─────────────────────────── Main Public API ─────────────────────────────

    async def discover(self, criteria: DiscoveryCriteria) -> list[Company]:
        """
        اكتشف شركات تطابق المعايير المحددة.

        يستعلم:
        1. السجل التجاري (seed أو API)
        2. يُطبّق المرشّحات: قطاع، منطقة، حجم، نشاط ISIC

        Args:
            criteria: معايير الاكتشاف (قطاع، منطقة، حجم...)

        Returns:
            قائمة بالشركات المكتشفة (قبل الإثراء).
        """
        logger.info(
            "Discovery started: sectors=%s regions=%s limit=%d",
            [s.value for s in criteria.sectors],
            [r.value for r in criteria.regions],
            criteria.limit,
        )

        companies = await self._registry.discover(criteria)
        self._stats["total_discovered"] += len(companies)

        logger.info("Discovered %d companies", len(companies))
        return companies

    async def enrich(self, company: Company) -> Lead:
        """
        أثري شركة واحدة وأنشئ Lead مُسجَّل.

        Runs all data sources in parallel, merges results,
        scores the lead, and returns a fully formed Lead object.

        Args:
            company: الشركة المراد إثراؤها

        Returns:
            Lead مُثرَّى ومُسجَّل جاهز للتواصل.
        """
        logger.info("Enriching: %s", company.name)

        # Run enrichment pipeline
        enrichment_result = await self._pipeline.enrich(company)

        # Score the enriched company
        score = self._scorer.score(company, enrichment_result)

        # Build Lead
        lead = Lead(
            company=company,
            score=score,
            status=LeadStatus.QUALIFIED if score.total_score >= 40 else LeadStatus.NEW,
        )
        lead.set_priority_tier()

        self._stats["total_enriched"] += 1
        self._stats["total_scored"] += 1

        logger.info(
            "Enriched %s: score=%.1f tier=%s signals=%d",
            company.name,
            score.total_score,
            lead.priority_tier,
            len(enrichment_result.signals),
        )

        return lead

    async def run_pipeline(
        self,
        criteria: DiscoveryCriteria,
        min_score: float | None = None,
        sort_by_score: bool = True,
    ) -> list[Lead]:
        """
        تشغيل الـ pipeline الكامل: اكتشاف + إثراء + تسجيل.

        Args:
            criteria: معايير الاكتشاف
            min_score: استبعاد الـ leads ذات النتيجة أقل من هذا الحد
            sort_by_score: ترتيب النتائج تنازلياً حسب النتيجة

        Returns:
            قائمة بالـ leads المُثرَّاة والمُسجَّلة.
        """
        self._stats["pipeline_runs"] += 1

        # Step 1: Discovery
        companies = await self.discover(criteria)
        if not companies:
            logger.warning("No companies discovered")
            return []

        # Step 2: Parallel enrichment
        logger.info("Starting batch enrichment for %d companies", len(companies))
        enrichment_results = await self._pipeline.enrich_batch(
            companies, max_concurrent=self._max_concurrent
        )

        # Step 3: Score + build leads
        leads: list[Lead] = []
        for company, enrichment_result in zip(companies, enrichment_results):
            score = self._scorer.score(company, enrichment_result)
            lead = Lead(
                company=company,
                score=score,
                status=LeadStatus.QUALIFIED if score.total_score >= 40 else LeadStatus.NEW,
            )
            lead.set_priority_tier()
            leads.append(lead)

        # Step 4: Filter by min_score
        effective_min = min_score if min_score is not None else criteria.min_score
        if effective_min > 0:
            before = len(leads)
            leads = [l for l in leads if l.dealix_score >= effective_min]
            logger.info("Score filter ≥%.0f: %d → %d leads", effective_min, before, len(leads))

        # Step 5: Sort
        if sort_by_score:
            leads.sort(key=lambda l: l.dealix_score, reverse=True)

        logger.info(
            "Pipeline complete: %d leads (hot=%d warm=%d cool=%d cold=%d)",
            len(leads),
            sum(1 for l in leads if l.priority_tier == "hot"),
            sum(1 for l in leads if l.priority_tier == "warm"),
            sum(1 for l in leads if l.priority_tier == "cool"),
            sum(1 for l in leads if l.priority_tier == "cold"),
        )

        return leads

    async def enrich_companies(self, companies: list[Company]) -> list[Lead]:
        """
        إثراء وتسجيل قائمة من الشركات مباشرة (بدون Discovery).

        Useful when you already have a list of target companies.
        """
        enrichment_results = await self._pipeline.enrich_batch(
            companies, max_concurrent=self._max_concurrent
        )

        leads: list[Lead] = []
        for company, enrichment_result in zip(companies, enrichment_results):
            score = self._scorer.score(company, enrichment_result)
            lead = Lead(
                company=company,
                score=score,
                status=LeadStatus.QUALIFIED if score.total_score >= 40 else LeadStatus.NEW,
            )
            lead.set_priority_tier()
            leads.append(lead)

        leads.sort(key=lambda l: l.dealix_score, reverse=True)
        return leads

    # ─────────────────────────── Utility Methods ─────────────────────────────

    def get_stats(self) -> dict[str, Any]:
        """إحصائيات الـ orchestrator منذ بدء التشغيل."""
        return dict(self._stats)

    @property
    def seed_company_count(self) -> int:
        """عدد الشركات في بيانات الـ seed."""
        return self._registry.seed_count

    def get_all_seed_companies(self) -> list[Company]:
        """جلب كل الشركات من بيانات الـ seed."""
        return self._registry.all_seed_companies

    def explain_lead(self, lead: Lead) -> str:
        """
        شرح نتيجة lead بتنسيق قابل للقراءة.

        Args:
            lead: كائن Lead المراد شرحه

        Returns:
            نص شرح منسّق.
        """
        return self._scorer.explain(lead.score)

    @classmethod
    def from_env(cls) -> "IntelligenceOrchestrator":
        """
        إنشاء orchestrator بقراءة بيانات الاعتماد من متغيرات البيئة.

        Environment variables:
            SBC_API_KEY          — Saudi Business Center API key
            ETIMAD_API_KEY       — Etimad API key
            UNIPILE_API_KEY      — Unipile API key
            UNIPILE_LINKEDIN_ID  — Unipile LinkedIn account ID
            PERPLEXITY_API_KEY   — Perplexity API key
            BING_NEWS_API_KEY    — Bing News API key
            BUILTWITH_API_KEY    — BuiltWith API key
        """
        import os

        return cls(
            sbc_api_key=os.getenv("SBC_API_KEY"),
            etimad_api_key=os.getenv("ETIMAD_API_KEY"),
            unipile_api_key=os.getenv("UNIPILE_API_KEY"),
            unipile_account_id=os.getenv("UNIPILE_LINKEDIN_ID"),
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
            bing_news_api_key=os.getenv("BING_NEWS_API_KEY"),
            builtwith_api_key=os.getenv("BUILTWITH_API_KEY"),
        )
