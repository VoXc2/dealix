"""
LLM-Based Lead Scoring — Dealix Lead Intelligence Engine V2
===========================================================
Scores each EnrichedLead against the ICP using Groq (llama-3.3-70b).
Generates talking points in Arabic for Arabic-language leads.
Falls back to rule-based scoring when LLM is unavailable.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import List, Optional

import httpx

from app.intelligence.v2.models import (
    DiscoveryQuery,
    EnrichedLead,
    LeadTier,
    ScoredLead,
)

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

SCORING_SYSTEM_PROMPT_AR = """أنت خبير تقييم عملاء B2B لـ Dealix في السوق الخليجي.

مهمتك: قيّم مدى تطابق شركة مستهدفة مع ملف العميل المثالي (ICP) وأعطِ نتيجة من 0 إلى 100.

معايير التقييم:
- القطاع: هل الشركة في القطاع المطلوب؟ (30 نقطة)
- الجغرافيا: هل هي في المنطقة المستهدفة؟ (20 نقطة)
- الإشارات: هل تعلن عن توظيف أو توسع أو تمويل؟ (25 نقطة)
- البيانات: هل لديها موقع ورقم هاتف وإيميل؟ (15 نقطة)
- الحجم: هل حجمها مناسب للـ ICP؟ (10 نقطة)

أعد JSON فقط بهذا الشكل:
{
  "icp_score": 75,
  "intent_score": 60,
  "total_score": 70,
  "score_rationale_ar": "شركة في قطاع المطاعم بالرياض مع إشارة توظيف قوية",
  "talking_points_ar": [
    "تعلنون عن وظائف جديدة — هذا يعني نمو وحاجة لأدوات إدارة أفضل",
    "موقعكم في الرياض يتيح لنا تقديم دعم محلي مباشر",
    "قطاع المطاعم يستفيد كثيراً من حلول CRM المتخصصة"
  ]
}"""

SCORING_SYSTEM_PROMPT_EN = """You are a B2B lead qualification expert for Dealix, focusing on Gulf markets.

Score a target company against the Ideal Customer Profile (ICP) from 0-100.

Scoring criteria:
- Industry fit: Is the company in the target industry? (30 pts)
- Geography: Is it in the target region? (20 pts)
- Buying signals: Is it hiring, expanding, or funded? (25 pts)
- Data quality: Does it have website, phone, email? (15 pts)
- Company size: Does size match ICP? (10 pts)

Return JSON only:
{
  "icp_score": 75,
  "intent_score": 60,
  "total_score": 70,
  "score_rationale": "Restaurant company in Riyadh with strong hiring signal",
  "talking_points": [
    "You're actively hiring — we can help onboard your team faster",
    "Local Riyadh presence means we can meet in person",
    "Restaurant sector benefits greatly from specialized CRM"
  ]
}"""


def _rule_based_score(enriched: EnrichedLead, query: DiscoveryQuery) -> dict:
    """Fallback scoring when LLM is unavailable."""
    lead = enriched.normalized_lead
    score = 0
    rationale_parts = []

    # Industry fit (30 pts)
    if lead.industry and query.icp.industries:
        industry_lower = lead.industry.lower()
        for target_industry in query.icp.industries:
            if target_industry.lower() in industry_lower or industry_lower in target_industry.lower():
                score += 30
                rationale_parts.append(f"Industry match: {lead.industry}")
                break
        else:
            score += 10  # Partial credit

    # Geography (20 pts)
    target_cities = [c.lower() for c in query.icp.geo.cities]
    target_countries = [c.upper() for c in query.icp.geo.countries]

    if lead.country in target_countries:
        score += 10
    if lead.city and any(c in lead.city.lower() for c in target_cities):
        score += 10
        rationale_parts.append(f"City match: {lead.city}")

    # Signals (25 pts)
    if lead.is_hiring:
        score += 15
        rationale_parts.append("Active hiring signal")
    if enriched.has_ecommerce:
        score += 10
        rationale_parts.append(f"Ecommerce platform: {enriched.ecommerce_platform}")

    # Data quality (15 pts)
    if lead.phone_e164:
        score += 5
    if lead.email:
        score += 5
    if enriched.has_website:
        score += 5

    # Company size (10 pts)
    if query.icp.company_size:
        score += 5  # We don't have size data usually at this stage

    total = min(100, score)
    icp_score = min(100, score * 0.8)
    intent_score = min(100, (15 if lead.is_hiring else 0) + (10 if enriched.has_ecommerce else 0))

    # Talking points
    talking_points = []
    if lead.is_hiring:
        talking_points.append(f"You're hiring actively — a strong growth signal")
    if enriched.has_website:
        talking_points.append("Your online presence shows digital readiness")
    if lead.country == "SA":
        talking_points.append("Saudi-based companies are our primary focus market")

    talking_points_ar = []
    if lead.is_hiring:
        talking_points_ar.append("التوظيف النشط لديكم يشير إلى نمو — نستطيع مساعدتكم بأدوات CRM متخصصة")
    if enriched.has_website:
        talking_points_ar.append("تواجدكم الرقمي القوي يسهّل التكامل مع منظومتنا")
    if lead.country == "SA":
        talking_points_ar.append("تركيزنا الأساسي على السوق السعودي يتيح لنا فهم احتياجاتكم بعمق")

    rationale = "; ".join(rationale_parts) if rationale_parts else "Basic scoring based on available data"
    rationale_ar = f"تقييم بناءً على: {' + '.join(rationale_parts)}" if rationale_parts else "تقييم أساسي"

    return {
        "icp_score": round(icp_score, 1),
        "intent_score": round(intent_score, 1),
        "total_score": round(total, 1),
        "score_rationale": rationale,
        "score_rationale_ar": rationale_ar,
        "talking_points": talking_points[:3],
        "talking_points_ar": talking_points_ar[:3],
        "model": "rule_based",
    }


async def _llm_score(
    enriched: EnrichedLead,
    query: DiscoveryQuery,
    client: httpx.AsyncClient,
) -> dict:
    """Score a single lead using Groq LLM."""
    lead = enriched.normalized_lead

    # Determine language for response
    has_arabic_name = bool(lead.company_name_ar) or (
        lead.company_name and any("\u0600" <= c <= "\u06FF" for c in lead.company_name)
    )
    use_arabic = has_arabic_name or query.language == "ar"

    system_prompt = SCORING_SYSTEM_PROMPT_AR if use_arabic else SCORING_SYSTEM_PROMPT_EN

    # Build lead description
    lead_desc = f"""الشركة: {lead.company_name}
{f"الاسم بالعربي: {lead.company_name_ar}" if lead.company_name_ar else ""}
القطاع: {lead.industry or "غير محدد"}
الدولة: {lead.country} | المدينة: {lead.city or "غير محدد"}
الهاتف: {"نعم" if lead.phone_e164 else "لا"}
الإيميل: {"نعم" if lead.email else "لا"}
الموقع: {"نعم" if enriched.has_website else "لا"}
LinkedIn: {"نعم" if enriched.linkedin_url or lead.linkedin_url else "لا"}
التوظيف النشط: {"نعم — " + ", ".join(lead.hiring_roles[:3]) if lead.is_hiring else "لا"}
منصة تجارة إلكترونية: {enriched.ecommerce_platform or "لا"}
"""

    icp_desc = f"""ICP المستهدف:
القطاعات: {", ".join(query.icp.industries)}
الدول: {", ".join(query.icp.geo.countries)}
المدن: {", ".join(query.icp.geo.cities) if query.icp.geo.cities else "الكل"}
الإشارات المطلوبة: {", ".join(query.icp.signals) if query.icp.signals else "أي"}
"""

    user_message = f"{icp_desc}\n\nتقييم هذه الشركة:\n{lead_desc}"

    resp = await client.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.2,
            "max_tokens": 500,
            "response_format": {"type": "json_object"},
        },
        timeout=20.0,
    )
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    result = json.loads(content)
    result["model"] = GROQ_MODEL
    return result


async def score_lead(
    enriched: EnrichedLead,
    query: DiscoveryQuery,
    client: Optional[httpx.AsyncClient] = None,
) -> ScoredLead:
    """Score a single enriched lead."""
    score_data = {}

    if GROQ_API_KEY and client:
        try:
            score_data = await _llm_score(enriched, query, client)
        except Exception as e:
            logger.warning(f"[scoring] LLM scoring failed for {enriched.normalized_lead.company_name}: {e}")
            score_data = _rule_based_score(enriched, query)
    else:
        score_data = _rule_based_score(enriched, query)

    scored = ScoredLead(
        enriched_lead=enriched,
        icp_score=float(score_data.get("icp_score", 0)),
        intent_score=float(score_data.get("intent_score", 0)),
        total_score=float(score_data.get("total_score", 0)),
        score_rationale=score_data.get("score_rationale"),
        score_rationale_ar=score_data.get("score_rationale_ar"),
        talking_points=score_data.get("talking_points", [])[:3],
        talking_points_ar=score_data.get("talking_points_ar", [])[:3],
        scoring_model=score_data.get("model", "rule_based"),
    )
    scored.set_tier()
    return scored


async def score_leads(
    enriched_leads: List[EnrichedLead],
    query: DiscoveryQuery,
    concurrency: int = 5,
) -> List[ScoredLead]:
    """Score all enriched leads. Uses LLM batch with concurrency limit."""
    semaphore = asyncio.Semaphore(concurrency)

    async def _bounded_score(enriched: EnrichedLead, client: httpx.AsyncClient) -> ScoredLead:
        async with semaphore:
            return await score_lead(enriched, query, client)

    if GROQ_API_KEY:
        async with httpx.AsyncClient(timeout=30.0) as client:
            results = await asyncio.gather(
                *[_bounded_score(lead, client) for lead in enriched_leads],
                return_exceptions=False,
            )
    else:
        results = await asyncio.gather(
            *[score_lead(lead, query, client=None) for lead in enriched_leads],
            return_exceptions=False,
        )

    logger.info(f"[scoring] Scored {len(results)} leads")
    return results
