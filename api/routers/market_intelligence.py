"""Market Intelligence API Router.

Saudi B2B market signals, sector rankings, and opportunity intelligence.
Public endpoints for growth — no auth required for read-only sector data.

Prefix: /api/v1/market-intelligence
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Query

from dealix.commercial.market_intelligence import MarketIntelligenceEngine

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/market-intelligence", tags=["Analytics"])

_engine = MarketIntelligenceEngine()


@router.get("/signals")
async def get_market_signals(
    urgency: str | None = Query(default=None, description="Filter: HIGH | MEDIUM | LOW"),
    sector: str | None = Query(default=None, description="Filter by sector key"),
) -> dict[str, Any]:
    """Get Saudi market signals by urgency and/or sector.

    Returns curated signals from public Saudi market research (2025-2026).
    Signals are NOT scraped — sourced from public research and regulatory announcements.
    """
    signals = _engine.get_all_signals(urgency_filter=urgency, sector_filter=sector)
    return {
        "count": len(signals),
        "signals": [s.model_dump() for s in signals],
        "source_note_ar": "من بحث عام مُعتمد — ليس scraping",
        "source_note_en": "From approved public research — not scraping",
    }


@router.get("/sector-ranking")
async def get_sector_ranking() -> dict[str, Any]:
    """Returns Saudi B2B sectors ranked by AI operations opportunity.

    Scoring: pain intensity × AI adoption gap × avg deal value.
    """
    ranking = _engine.get_sector_ranking()
    return {
        "ranking": ranking,
        "methodology_ar": "الترتيب بناءً على: شدة الألم × فجوة تبني AI × متوسط قيمة الصفقة",
        "methodology_en": "Ranked by: pain intensity × AI adoption gap × average deal value",
        "note_ar": "هذه تقديرات قطاعية — ليست ضمانات نتائج",
        "note_en": "These are sector estimates — not guaranteed outcomes",
    }


@router.get("/sector/{sector}")
async def get_sector_intelligence(sector: str) -> dict[str, Any]:
    """Get detailed intelligence for a specific Saudi B2B sector."""
    intel = _engine.get_sector_intelligence(sector)
    if not intel:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found. Available: b2b_saas, agency, healthcare_clinic, real_estate, logistics, fintech, engineering",
        )
    return intel.model_dump()


@router.get("/why-now/{sector}")
async def get_why_now(sector: str) -> dict[str, Any]:
    """Get a concise 'Why Act Now' brief for a sector — for use in proposals."""
    brief = _engine.get_why_now_brief(sector)
    return {
        "sector": sector,
        "why_now_ar": brief["ar"],
        "why_now_en": brief["en"],
        "governance_note": "تُستخدم في العروض التجارية — تتطلب مراجعة المؤسس قبل الإرسال",
    }


@router.get("/opportunities/top")
async def get_top_opportunities() -> dict[str, Any]:
    """Returns top 3 highest-opportunity sectors with entry recommendations."""
    ranking = _engine.get_sector_ranking()
    top3 = ranking[:3]
    return {
        "top_opportunities": top3,
        "action_ar": "هذه القطاعات تمثل أعلى ROI للوقت المستثمر في التنقيب",
        "action_en": "These sectors represent the highest ROI on prospecting time invested",
    }
