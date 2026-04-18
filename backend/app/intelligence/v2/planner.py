"""
LLM Query Planner — Dealix Lead Intelligence Engine V2
======================================================
Uses Groq (llama-3.3-70b) to plan search queries given an ICP.
Output: List[SearchPlan] = [(source_name, query_string, filters)]
"""

from __future__ import annotations

import json
import logging
import os
from typing import List, Optional

import httpx

from app.intelligence.v2.gulf_geo import SAUDI_CITIES
from app.intelligence.v2.i18n import get_arabic_term, AR_BUSINESS_TERMS
from app.intelligence.v2.models import DiscoveryQuery, ICP, SearchPlan

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Available source names (for planner to choose from)
ALL_SOURCES = [
    "google_custom_search",
    "duckduckgo",
    "brave_search",
    "google_places",
    "osm_nominatim",
    "linkedin_public",
    "sa_mc_gov",
    "bayt_jobs",
]

# Quick mode: fewer sources
QUICK_SOURCES = ["duckduckgo", "google_places", "osm_nominatim", "bayt_jobs"]

PLANNER_SYSTEM_PROMPT = """أنت محرك تخطيط البحث عن العملاء المحتملين لـ Dealix في السوق الخليجي.

مهمتك: بناءً على وصف العميل المثالي (ICP)، حدد أفضل مصادر البحث وأفضل استعلامات للبحث.

المصادر المتاحة:
- google_custom_search: بحث Google CSE (انجليزي وعربي)
- duckduckgo: بحث DuckDuckGo HTML (مجاني)
- brave_search: Brave Search API (خصوصية عالية)
- google_places: Google Places API (أفضل للمحلات والمطاعم والخدمات)
- osm_nominatim: OpenStreetMap (مجاني، للعناوين)
- linkedin_public: LinkedIn عبر Google (للشركات والمهنيين)
- sa_mc_gov: سجل وزارة التجارة السعودية (للشركات الرسمية)
- bayt_jobs: وظائف Bayt.com (إشارة التوظيف = نمو)

قواعد:
1. كل ICP يستحق 3-8 استعلامات من مصادر مختلفة
2. اكتب استعلامات بالعربي والإنجليزي
3. كن محدداً: أضف اسم المدينة + القطاع في كل استعلام
4. للمطاعم والمحلات → google_places أولاً
5. للشركات الكبيرة → linkedin_public + sa_mc_gov
6. لإشارات التوظيف → bayt_jobs دائماً

أعد JSON فقط بهذا الشكل:
{
  "plans": [
    {
      "source_name": "google_places",
      "query_string": "مطاعم فاخرة الرياض",
      "filters": {"language": "ar"},
      "language": "ar",
      "priority": 1,
      "rationale": "أفضل مصدر للمطاعم المحلية"
    }
  ]
}"""


def _build_icp_description(icp: ICP) -> str:
    """Build a human-readable ICP description for the LLM."""
    parts = []
    if icp.industries:
        industries_ar = [get_arabic_term(i) or i for i in icp.industries]
        parts.append(f"القطاع: {', '.join(icp.industries)} ({', '.join(str(a) for a in industries_ar if a)})")

    cities = icp.geo.cities or []
    countries = icp.geo.countries or ["SA"]
    parts.append(f"الجغرافيا: {', '.join(countries)} — مدن: {', '.join(cities) or 'كل المدن'}")

    if icp.company_size:
        parts.append(f"حجم الشركة: {icp.company_size}")

    if icp.min_employees or icp.max_employees:
        parts.append(f"الموظفين: {icp.min_employees or '0'}-{icp.max_employees or '∞'}")

    if icp.signals:
        parts.append(f"الإشارات المطلوبة: {', '.join(icp.signals)}")

    if icp.keywords:
        parts.append(f"كلمات مفتاحية: {', '.join(icp.keywords)}")

    if icp.keywords_ar:
        parts.append(f"كلمات بالعربي: {', '.join(icp.keywords_ar)}")

    return "\n".join(parts)


def _fallback_plans(query: DiscoveryQuery) -> List[SearchPlan]:
    """Generate basic search plans without LLM (fallback)."""
    icp = query.icp
    industries = icp.industries or ["business"]
    cities = icp.geo.cities or ["Riyadh", "الرياض"]
    city_en = cities[0] if cities else "Riyadh"
    city_ar_candidates = [c for c in cities if any("\u0600" <= ch <= "\u06FF" for ch in c)]
    city_ar = city_ar_candidates[0] if city_ar_candidates else "الرياض"

    industry_en = industries[0] if industries else "business"
    industry_ar = get_arabic_term(industry_en) or industry_en

    sources = QUICK_SOURCES if query.depth.value == "quick" else ALL_SOURCES

    plans = []
    for source_name in sources:
        if source_name == "google_places":
            plans.append(SearchPlan(
                source_name="google_places",
                query_string=f"{industry_ar} {city_ar}",
                filters={"language": "ar"},
                language="ar",
                priority=1,
                rationale="Google Places for local business discovery",
            ))
        elif source_name == "duckduckgo":
            plans.append(SearchPlan(
                source_name="duckduckgo",
                query_string=f"{industry_en} companies {city_en} Saudi Arabia",
                filters={},
                language="en",
                priority=2,
                rationale="General web search for businesses",
            ))
            plans.append(SearchPlan(
                source_name="duckduckgo",
                query_string=f"شركات {industry_ar} {city_ar} +966",
                filters={},
                language="ar",
                priority=2,
                rationale="Arabic web search for businesses",
            ))
        elif source_name == "bayt_jobs":
            plans.append(SearchPlan(
                source_name="bayt_jobs",
                query_string=industry_en,
                filters={},
                language="en",
                priority=3,
                rationale="Hiring signal discovery",
            ))
        elif source_name == "osm_nominatim":
            plans.append(SearchPlan(
                source_name="osm_nominatim",
                query_string=f"{industry_en} {city_en}",
                filters={},
                language="en",
                priority=3,
                rationale="OSM geocoder for business locations",
            ))
        elif source_name == "linkedin_public":
            plans.append(SearchPlan(
                source_name="linkedin_public",
                query_string=f"{industry_en} {city_en} Saudi Arabia",
                filters={},
                language="en",
                priority=2,
                rationale="LinkedIn company discovery",
            ))
        elif source_name == "sa_mc_gov":
            plans.append(SearchPlan(
                source_name="sa_mc_gov",
                query_string=industry_ar or industry_en,
                filters={},
                language="ar",
                priority=2,
                rationale="Saudi commercial registry",
            ))
        elif source_name in ("google_custom_search", "brave_search"):
            plans.append(SearchPlan(
                source_name=source_name,
                query_string=f"{industry_en} {city_en} Saudi Arabia contact email phone",
                filters={},
                language="en",
                priority=2,
                rationale=f"{source_name} search for contact info",
            ))

    return plans[:10]  # Cap to avoid explosion


async def plan_queries(query: DiscoveryQuery) -> List[SearchPlan]:
    """
    Use Groq LLM to generate smart search plans for the ICP.
    Falls back to rule-based plans if LLM is unavailable.
    """
    if not GROQ_API_KEY:
        logger.info("[planner] No GROQ_API_KEY — using fallback rule-based plans")
        return _fallback_plans(query)

    icp_description = _build_icp_description(query.icp)
    available_sources = QUICK_SOURCES if query.depth.value == "quick" else ALL_SOURCES

    user_message = f"""ICP للبحث:
{icp_description}

المصادر المتاحة: {', '.join(available_sources)}
الحد الأقصى للنتائج: {query.limit}
عمق البحث: {query.depth.value}

أنشئ خطة بحث مثلى."""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "response_format": {"type": "json_object"},
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            plans_raw = parsed.get("plans", [])

            plans = []
            for p in plans_raw:
                # Validate source_name is one we support
                source = p.get("source_name", "")
                if source not in ALL_SOURCES:
                    continue
                plans.append(SearchPlan(
                    source_name=source,
                    query_string=p.get("query_string", ""),
                    filters=p.get("filters", {}),
                    language=p.get("language", "en"),
                    priority=p.get("priority", 5),
                    rationale=p.get("rationale"),
                ))

            if not plans:
                logger.warning("[planner] LLM returned no valid plans, using fallback")
                return _fallback_plans(query)

            logger.info(f"[planner] LLM generated {len(plans)} search plans")
            return sorted(plans, key=lambda x: x.priority)

    except Exception as e:
        logger.error(f"[planner] LLM planning failed: {e}. Using fallback.")
        return _fallback_plans(query)
