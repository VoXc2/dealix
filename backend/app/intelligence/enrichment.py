"""
EnrichmentPipeline — Parallel Data Enrichment Engine
=====================================================
Takes a raw Company record and runs all data sources in parallel (asyncio.gather),
then merges results into a fully enriched Company ready for scoring.

Pipeline steps:
  1. Saudi Business Registry → official data (CR, VAT, GOSI)
  2. Etimad → tender wins + government contract value
  3. LinkedIn → decision makers + company updates
  4. News → recent events + sentiment
  5. Hiring Intent → open roles → growth signal
  6. Tech Stack → technologies + digital maturity

All sources run concurrently. Failures in individual sources are logged
but do not block the pipeline — graceful degradation.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from .models import Company, Signal
from .sources.etimad import EtimadSource
from .sources.hiring import HiringIntentSource
from .sources.linkedin import LinkedInSource
from .sources.news import NewsSource
from .sources.saudi_registry import SaudiBusinessRegistrySource
from .sources.tech_stack import TechStackSource

logger = logging.getLogger(__name__)


class EnrichmentResult:
    """نتيجة إثراء شركة واحدة — تتضمن كل البيانات المُجمَّعة والإشارات."""

    def __init__(self, company: Company) -> None:
        self.company = company
        self.signals: list[Signal] = []
        self.enrichment_errors: list[str] = []
        self.sources_succeeded: list[str] = []
        self.sources_failed: list[str] = []
        self.enriched_at: datetime = datetime.utcnow()
        self.digital_maturity_score: float = 0.0

    def add_signals(self, signals: list[Signal], source_name: str) -> None:
        """إضافة إشارات من مصدر معين."""
        self.signals.extend(signals)
        if source_name not in self.sources_succeeded:
            self.sources_succeeded.append(source_name)

    def add_error(self, source_name: str, error: str) -> None:
        """تسجيل خطأ من مصدر معين."""
        self.enrichment_errors.append(f"[{source_name}] {error}")
        self.sources_failed.append(source_name)

    @property
    def total_signal_score(self) -> float:
        """مجموع نقاط جميع الإشارات (مُقيَّد بـ 100)."""
        return min(100.0, sum(s.score_contribution for s in self.signals))


class EnrichmentPipeline:
    """
    خط أنابيب الإثراء المتوازي — Parallel Enrichment Pipeline.

    يُشغّل جميع مصادر البيانات بشكل متوازٍ باستخدام asyncio.gather،
    ويدمج النتائج في سجل Company مُثرّى جاهز للتسجيل.

    Example usage::

        pipeline = EnrichmentPipeline()
        result = await pipeline.enrich(company)
        enriched_company = result.company
        signals = result.signals
    """

    def __init__(
        self,
        registry_source: SaudiBusinessRegistrySource | None = None,
        etimad_source: EtimadSource | None = None,
        linkedin_source: LinkedInSource | None = None,
        news_source: NewsSource | None = None,
        hiring_source: HiringIntentSource | None = None,
        tech_source: TechStackSource | None = None,
        timeout_seconds: float = 30.0,
    ) -> None:
        """
        Args:
            registry_source: مصدر سجل الأعمال السعودي
            etimad_source: مصدر اعتماد للمناقصات
            linkedin_source: مصدر LinkedIn
            news_source: مصدر الأخبار
            hiring_source: مصدر إشارات التوظيف
            tech_source: مصدر كشف التقنيات
            timeout_seconds: مهلة كل مصدر بالثواني
        """
        self.registry = registry_source or SaudiBusinessRegistrySource()
        self.etimad = etimad_source or EtimadSource()
        self.linkedin = linkedin_source or LinkedInSource()
        self.news = news_source or NewsSource()
        self.hiring = hiring_source or HiringIntentSource()
        self.tech = tech_source or TechStackSource()
        self.timeout = timeout_seconds

    async def enrich(self, company: Company) -> EnrichmentResult:
        """
        إثراء شركة واحدة بتشغيل جميع المصادر بشكل متوازٍ.

        Args:
            company: الشركة المراد إثراؤها

        Returns:
            EnrichmentResult يتضمن الشركة المُثرّاة وكل الإشارات.
        """
        result = EnrichmentResult(company)

        # Define tasks with source names for error reporting
        tasks: list[tuple[str, Any]] = [
            ("etimad", self._safe_enrich_etimad(company, result)),
            ("linkedin", self._safe_enrich_linkedin(company, result)),
            ("news", self._safe_enrich_news(company, result)),
            ("hiring", self._safe_enrich_hiring(company, result)),
            ("tech_stack", self._safe_enrich_tech(company, result)),
        ]

        # Run all tasks in parallel
        await asyncio.gather(
            *[task for _, task in tasks],
            return_exceptions=False,
        )

        # Mark company as enriched
        company.enriched = True
        company.updated_at = datetime.utcnow()
        company.signals = result.signals

        # Update data_sources
        company.data_sources = list(set(
            company.data_sources + result.sources_succeeded
        ))

        logger.info(
            "Enrichment complete for %s: %d signals, %d sources OK, %d failed",
            company.name,
            len(result.signals),
            len(result.sources_succeeded),
            len(result.sources_failed),
        )

        return result

    async def enrich_batch(
        self,
        companies: list[Company],
        max_concurrent: int = 5,
    ) -> list[EnrichmentResult]:
        """
        إثراء مجموعة من الشركات بشكل متوازٍ (مع حدّ أقصى للطلبات المتزامنة).

        Args:
            companies: قائمة الشركات المراد إثراؤها
            max_concurrent: الحد الأقصى للشركات المعالَجة في وقت واحد

        Returns:
            قائمة بنتائج الإثراء بنفس ترتيب الإدخال.
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def bounded_enrich(company: Company) -> EnrichmentResult:
            async with semaphore:
                return await self.enrich(company)

        results = await asyncio.gather(
            *[bounded_enrich(c) for c in companies],
            return_exceptions=True,
        )

        # Replace exceptions with empty results
        final: list[EnrichmentResult] = []
        for company, result in zip(companies, results):
            if isinstance(result, Exception):
                logger.error("Enrichment failed for %s: %s", company.name, result)
                empty = EnrichmentResult(company)
                empty.add_error("pipeline", str(result))
                final.append(empty)
            else:
                final.append(result)

        return final

    # ─────────────────────────── Safe Task Wrappers ───────────────────────────

    async def _safe_enrich_etimad(
        self, company: Company, result: EnrichmentResult
    ) -> None:
        """إثراء بيانات اعتماد — آمن من الأخطاء."""
        try:
            async with asyncio.timeout(self.timeout):
                # Get tender wins
                tender_wins = await self.etimad.get_tender_wins(company)
                if tender_wins:
                    company.tender_wins = tender_wins
                    logger.debug("Etimad: %d tenders for %s", len(tender_wins), company.name)

                # Get intent signals
                signals = await self.etimad.get_signals(company)
                result.add_signals(signals, "etimad")

        except NotImplementedError:
            # API not configured — expected in dev
            logger.debug("Etimad: not configured for %s", company.name)
        except TimeoutError:
            result.add_error("etimad", "Timeout")
        except Exception as exc:
            result.add_error("etimad", str(exc))
            logger.warning("Etimad enrichment failed for %s: %s", company.name, exc)

    async def _safe_enrich_linkedin(
        self, company: Company, result: EnrichmentResult
    ) -> None:
        """إثراء LinkedIn — آمن من الأخطاء."""
        try:
            async with asyncio.timeout(self.timeout):
                signals = await self.linkedin.get_signals(company)
                result.add_signals(signals, "linkedin")

        except NotImplementedError:
            logger.debug("LinkedIn: not configured for %s", company.name)
        except TimeoutError:
            result.add_error("linkedin", "Timeout")
        except Exception as exc:
            result.add_error("linkedin", str(exc))
            logger.warning("LinkedIn enrichment failed for %s: %s", company.name, exc)

    async def _safe_enrich_news(
        self, company: Company, result: EnrichmentResult
    ) -> None:
        """إثراء الأخبار — آمن من الأخطاء."""
        try:
            async with asyncio.timeout(self.timeout):
                news_events = await self.news.get_news(company)
                if news_events:
                    company.last_news_events = news_events

                signals = await self.news.get_signals(company)
                result.add_signals(signals, "news")

        except NotImplementedError:
            logger.debug("News: not configured for %s", company.name)
        except TimeoutError:
            result.add_error("news", "Timeout")
        except Exception as exc:
            result.add_error("news", str(exc))
            logger.warning("News enrichment failed for %s: %s", company.name, exc)

    async def _safe_enrich_hiring(
        self, company: Company, result: EnrichmentResult
    ) -> None:
        """إثراء التوظيف — آمن من الأخطاء."""
        try:
            async with asyncio.timeout(self.timeout):
                hiring_signals = await self.hiring.get_hiring_signals(company)
                if hiring_signals:
                    company.hiring_signals = hiring_signals

                signals = await self.hiring.get_signals(company)
                result.add_signals(signals, "hiring")

        except NotImplementedError:
            logger.debug("Hiring: not configured for %s", company.name)
        except TimeoutError:
            result.add_error("hiring", "Timeout")
        except Exception as exc:
            result.add_error("hiring", str(exc))
            logger.warning("Hiring enrichment failed for %s: %s", company.name, exc)

    async def _safe_enrich_tech(
        self, company: Company, result: EnrichmentResult
    ) -> None:
        """إثراء التقنيات — آمن من الأخطاء."""
        try:
            async with asyncio.timeout(self.timeout):
                tech = await self.tech.detect(company)
                if tech:
                    company.tech_stack = list(set(company.tech_stack + tech))

                signals = await self.tech.get_signals(company)
                result.add_signals(signals, "tech_stack")

                maturity = await self.tech.estimate_digital_maturity(company)
                result.digital_maturity_score = maturity

        except NotImplementedError:
            logger.debug("TechStack: not configured for %s", company.name)
        except TimeoutError:
            result.add_error("tech_stack", "Timeout")
        except Exception as exc:
            result.add_error("tech_stack", str(exc))
            logger.warning("TechStack enrichment failed for %s: %s", company.name, exc)
