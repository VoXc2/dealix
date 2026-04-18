"""
Arabic News Intelligence Source — via Perplexity API
=====================================================
Fetches recent Arabic and English news about a target company using
the Perplexity Sonar API, which provides real-time web-grounded answers.

Also supports Bing News API as a fallback for structured news results.

Sources tapped by Perplexity:
  - Argaam (أرقام)         - Arabic financial news
  - Al-Eqtisadiah (الاقتصادية)
  - Saudi Gazette
  - Arab News
  - Bloomberg / Reuters (for publicly listed companies)
  - GDELT (global event database)

STATUS: Stub implementation.
TODO: Obtain Perplexity API key and/or Bing News API key.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import httpx

from ..models import Company, NewsEvent, Signal, SignalType


# ─────────────────────────── Seed News (Demo) ────────────────────────────────
# Static news events for demo purposes — enables the CLI to run without API keys.

SEED_NEWS: list[dict[str, Any]] = [
    {
        "company_name": "Tabby",
        "headline": "Tabby raises $200M in Series D funding, reaches $1.5B valuation",
        "headline_ar": "تابي تجمع 200 مليون دولار في جولة Series D وتصل إلى تقييم 1.5 مليار دولار",
        "summary": "Saudi BNPL fintech Tabby has raised $200M led by Hassana Investment Company",
        "source_name": "Magnitt",
        "url": "https://magnitt.com/news/tabby-series-d",
        "published_at": "2024-02-20",
        "sentiment": "positive",
        "signal_type": SignalType.FUNDING,
    },
    {
        "company_name": "Foodics",
        "headline": "Foodics secures $170M Series C to expand across MENA",
        "headline_ar": "فودكس تحصل على 170 مليون دولار في جولة Series C للتوسع في منطقة الشرق الأوسط وأفريقيا",
        "summary": "Restaurant management SaaS Foodics plans regional expansion with new funding",
        "source_name": "Wamda",
        "url": "https://wamda.com/foodics-series-c",
        "published_at": "2024-01-10",
        "sentiment": "positive",
        "signal_type": SignalType.FUNDING,
    },
    {
        "company_name": "ROSHN",
        "headline": "ROSHN launches Sedra mega-development in Riyadh with 30,000 units",
        "headline_ar": "روشن تطلق مشروع سدرة في الرياض بـ 30,000 وحدة سكنية",
        "summary": "ROSHN Group announces massive residential development Sedra north of Riyadh",
        "source_name": "Arab News",
        "url": "https://arabnews.com/roshn-sedra",
        "published_at": "2024-03-01",
        "sentiment": "positive",
        "signal_type": SignalType.EXPANSION,
    },
    {
        "company_name": "Salla",
        "headline": "Salla crosses 50,000 merchant milestone on its e-commerce platform",
        "headline_ar": "سلة تتجاوز 50,000 تاجر على منصتها للتجارة الإلكترونية",
        "summary": "Salla e-commerce platform announces major merchant growth milestone",
        "source_name": "Argaam",
        "url": "https://argaam.com/salla-merchants",
        "published_at": "2024-04-05",
        "sentiment": "positive",
        "signal_type": SignalType.EXPANSION,
    },
    {
        "company_name": "Nahdi Medical Company",
        "headline": "Nahdi Medical launches new digital health platform for customers",
        "headline_ar": "نهضة تطلق منصة صحة رقمية جديدة لعملائها",
        "summary": "Nahdi Medical Company expands digital services with new health app",
        "source_name": "Saudi Gazette",
        "url": "https://saudigazette.com.sa/nahdi-digital",
        "published_at": "2024-03-20",
        "sentiment": "positive",
        "signal_type": SignalType.PRODUCT_LAUNCH,
    },
]


class NewsSource:
    """
    مصدر الأخبار العربية والإنجليزية عبر Perplexity API.

    يُنتج:
    - آخر الأخبار عن الشركة (آخر 90 يوم)
    - تحليل المشاعر (إيجابي / محايد / سلبي)
    - إشارات ذكية: تمويل، توسع، شراكات، تغيير قيادي
    """

    PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
    BING_NEWS_BASE_URL = "https://api.bing.microsoft.com/v7.0/news/search"

    PERPLEXITY_MODEL = "sonar-pro"  # Best for real-time grounded search

    def __init__(
        self,
        perplexity_api_key: str | None = None,
        bing_api_key: str | None = None,
        session: httpx.AsyncClient | None = None,
    ) -> None:
        """
        Args:
            perplexity_api_key: مفتاح Perplexity API — متغير البيئة: PERPLEXITY_API_KEY
            bing_api_key: مفتاح Bing News API — متغير البيئة: BING_NEWS_API_KEY (اختياري)
            session: httpx.AsyncClient اختياري للمشاركة
        """
        self.perplexity_api_key = perplexity_api_key
        self.bing_api_key = bing_api_key
        self._session = session

    # ─────────────────────────── Public API ─────────────────────────────────

    async def get_news(
        self,
        company: Company,
        days_back: int = 90,
        language: str = "ar",
        max_results: int = 10,
    ) -> list[NewsEvent]:
        """
        جلب آخر الأخبار عن شركة محددة.

        Args:
            company: الشركة المستهدفة
            days_back: عدد الأيام للبحث فيها (الافتراضي 90 يوم)
            language: لغة الأخبار — 'ar' أو 'en' أو 'both'
            max_results: الحد الأقصى للنتائج

        Returns:
            قائمة بالأخبار مرتّبة من الأحدث للأقدم.
        """
        # Use seed if no API keys configured
        if not self.perplexity_api_key:
            return self._get_seed_news(company, max_results)

        return await self._fetch_via_perplexity(company, days_back, language, max_results)

    async def get_signals(self, company: Company) -> list[Signal]:
        """
        تحويل الأخبار إلى إشارات بيعية.
        Convert news events into scored intent signals.
        """
        news_events = await self.get_news(company, days_back=90)
        signals: list[Signal] = []

        for event in news_events:
            if event.signal_type is None:
                continue

            # Score based on signal type + sentiment
            base_score = {
                SignalType.FUNDING: 25.0,
                SignalType.EXPANSION: 20.0,
                SignalType.PARTNERSHIP: 15.0,
                SignalType.PRODUCT_LAUNCH: 15.0,
                SignalType.LEADERSHIP_CHANGE: 10.0,
                SignalType.NEWS_MENTION: 5.0,
            }.get(event.signal_type, 5.0)

            # Sentiment multiplier
            sentiment_mult = {"positive": 1.0, "neutral": 0.7, "negative": 0.3}.get(
                event.sentiment or "neutral", 0.7
            )

            # Recency decay: older news scores less
            if event.published_at:
                days_old = (datetime.utcnow() - event.published_at).days
                recency_mult = max(0.2, 1.0 - (days_old / 90) * 0.8)
            else:
                recency_mult = 0.5

            contribution = round(base_score * sentiment_mult * recency_mult, 1)

            signals.append(
                Signal(
                    signal_type=event.signal_type,
                    title=event.headline_ar or event.headline,
                    description=event.summary,
                    score_contribution=contribution,
                    source=event.source_name or "news",
                    detected_at=event.published_at or datetime.utcnow(),
                    metadata={
                        "url": event.url,
                        "sentiment": event.sentiment,
                        "headline_en": event.headline,
                    },
                )
            )

        return signals

    # ─────────────────────────── Seed Data ───────────────────────────────────

    def _get_seed_news(self, company: Company, max_results: int) -> list[NewsEvent]:
        """استرجاع الأخبار من بيانات الـ seed."""
        results = []
        for raw in SEED_NEWS:
            if company.name and raw["company_name"].lower() in company.name.lower():
                results.append(
                    NewsEvent(
                        headline=raw["headline"],
                        headline_ar=raw.get("headline_ar"),
                        summary=raw.get("summary"),
                        source_name=raw.get("source_name"),
                        url=raw.get("url"),
                        published_at=datetime.fromisoformat(raw["published_at"])
                        if raw.get("published_at")
                        else None,
                        sentiment=raw.get("sentiment"),
                        signal_type=raw.get("signal_type"),
                    )
                )
        return results[:max_results]

    # ─────────────────────────── Perplexity (stub) ───────────────────────────

    async def _fetch_via_perplexity(
        self,
        company: Company,
        days_back: int,
        language: str,
        max_results: int,
    ) -> list[NewsEvent]:
        """
        استدعاء Perplexity Sonar API للحصول على أخبار حديثة.

        TODO: Parse structured response into NewsEvent objects.
        The Perplexity response is conversational — use LLM extraction
        to pull structured fields (headline, date, sentiment, signal_type).

        Request format:
        POST https://api.perplexity.ai/chat/completions
        {
          "model": "sonar-pro",
          "messages": [
            {
              "role": "system",
              "content": "Extract news events as JSON..."
            },
            {
              "role": "user",
              "content": "أعطني آخر الأخبار عن شركة {company.name} خلال آخر {days_back} يوم..."
            }
          ],
          "search_recency_filter": "month",
          "return_citations": true
        }
        """
        raise NotImplementedError(
            "TODO: Implement Perplexity news fetch.\n"
            "Credential needed: PERPLEXITY_API_KEY\n"
            "Set env var: PERPLEXITY_API_KEY\n"
            "Get key: https://www.perplexity.ai/settings/api\n"
            "Endpoint: POST https://api.perplexity.ai/chat/completions\n"
            "Model: sonar-pro (best for real-time grounded search)\n"
            "Pricing: ~$5 per 1,000 requests (Sonar Pro)\n"
            "\n"
            "Suggested system prompt:\n"
            "'You are a business intelligence analyst. Extract structured news events\n"
            " about the given company as a JSON array with fields:\n"
            " headline, headline_ar, summary, source_name, url, published_at,\n"
            " sentiment (positive/neutral/negative), signal_type (funding/expansion/...)\n"
            " Respond ONLY with valid JSON.'"
        )

    async def _fetch_via_bing(
        self,
        company: Company,
        days_back: int,
        max_results: int,
    ) -> list[NewsEvent]:
        """
        استدعاء Bing News Search API كبديل للحصول على أخبار منظّمة.

        TODO: Implement Bing News API call.
        Endpoint: GET https://api.bing.microsoft.com/v7.0/news/search
        Headers: Ocp-Apim-Subscription-Key: {BING_NEWS_API_KEY}
        Params: q={company_name}, mkt=ar-SA, freshness=Month, count={max_results}
        """
        raise NotImplementedError(
            "TODO: Implement Bing News API fetch.\n"
            "Credential needed: BING_NEWS_API_KEY\n"
            "Set env var: BING_NEWS_API_KEY\n"
            "Portal: https://www.microsoft.com/en-us/bing/apis/bing-news-search-api\n"
            "Endpoint: GET https://api.bing.microsoft.com/v7.0/news/search\n"
            "Params: q={company_name}&mkt=ar-SA&freshness=Month&count={max_results}\n"
            "Headers: Ocp-Apim-Subscription-Key: {BING_NEWS_API_KEY}"
        )
