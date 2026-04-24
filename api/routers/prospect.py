"""
Prospect discovery endpoint — public, rate-limited.

POST /api/v1/prospect/discover
    body: {"icp": str, "use_case": "sales|partnership|collaboration|investor|b2c_audience", "count": 10}
    returns: ProspectResult JSON

POST /api/v1/prospect/demo
    returns: a canned demo result (no LLM call) for instant landing UI preview
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.agents.prospector import (
    MAX_COUNT,
    USE_CASES,
    ProspectorAgent,
)

router = APIRouter(prefix="/api/v1/prospect", tags=["prospect"])
log = logging.getLogger(__name__)

_agent = ProspectorAgent()


@router.get("/use-cases")
async def list_use_cases() -> dict[str, Any]:
    return {"use_cases": USE_CASES, "max_count": MAX_COUNT}


@router.post("/discover")
async def discover(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    icp = str(body.get("icp") or "").strip()
    use_case = str(body.get("use_case") or "sales").strip().lower()
    count = int(body.get("count") or 10)

    if len(icp) < 20:
        raise HTTPException(
            status_code=400,
            detail="icp_too_short: provide at least 20 characters describing your ideal customer",
        )
    if len(icp) > 2000:
        raise HTTPException(
            status_code=400,
            detail="icp_too_long: keep ICP under 2000 characters",
        )
    if use_case not in USE_CASES:
        raise HTTPException(
            status_code=400,
            detail=f"unknown_use_case: {use_case}. Valid: {list(USE_CASES.keys())}",
        )
    if count < 1 or count > MAX_COUNT:
        raise HTTPException(
            status_code=400,
            detail=f"count_out_of_range: 1..{MAX_COUNT}",
        )

    try:
        result = await _agent.run(icp=icp, use_case=use_case, count=count)
    except Exception as exc:
        log.exception("prospector_failed use_case=%s count=%d", use_case, count)
        raise HTTPException(
            status_code=502,
            detail="prospector_error",
        ) from exc

    return result.to_dict()


@router.post("/demo")
async def demo() -> dict[str, Any]:
    """Canned demo response for landing UI preview. No LLM call."""
    return {
        "use_case": "sales",
        "icp": "شركات SaaS سعودية B2B بحجم 20-100 موظف تبيع للمطاعم",
        "count_requested": 3,
        "count_returned": 3,
        "search_notes": "نتائج توضيحية — جرب الواجهة الحقيقية للحصول على قائمة مخصصة لمواصفاتك.",
        "leads": [
            {
                "company_ar": "فودكس",
                "company_en": "Foodics",
                "industry": "SaaS للمطاعم",
                "est_size": "200-1000",
                "website": "https://www.foodics.com",
                "linkedin": "https://www.linkedin.com/company/foodics",
                "decision_maker_hints": ["Ahmad Al-Zaini — CEO", "Mosab Alothmani — Co-founder"],
                "signals": ["جولة Series C بـ $170M 2025", "توسع في الخليج وشمال أفريقيا"],
                "outreach_opening": "أحمد، مبروك Series C — 170M = فرصة مضاعفة السرعة في onboarding العملاء الجدد.",
                "fit_score": 92,
                "confidence": 90,
                "evidence": "شركة SaaS سعودية واضحة، تستهدف restaurant operators، بحجم يطابق الـ ICP.",
            },
            {
                "company_ar": "رُكاز",
                "company_en": "Rekaz",
                "industry": "SaaS للـ SMB",
                "est_size": "10-50",
                "website": "https://rekaz.io",
                "linkedin": None,
                "decision_maker_hints": ["Abdullah Al-Shalan — Founder"],
                "signals": ["منصة متخصصة في إدارة المستودعات للتجار"],
                "outreach_opening": "عبدالله، رُكاز تبني الطبقة التشغيلية للتاجر السعودي — هذا تماماً مكان AI sales rep بالعربي.",
                "fit_score": 85,
                "confidence": 75,
                "evidence": "SMB-focused SaaS سعودي ضمن الحجم المطلوب.",
            },
            {
                "company_ar": "زد",
                "company_en": "Zid",
                "industry": "E-commerce Platform",
                "est_size": "200-1000",
                "website": "https://zid.sa",
                "linkedin": "https://www.linkedin.com/company/zidsa",
                "decision_maker_hints": ["Sultan Mofarreh — Co-founder"],
                "signals": ["منافس لسلة مع 15K تاجر+", "ركّز على SMB merchants"],
                "outreach_opening": "سلطان، 15K تاجر = فرصة توزيع هائلة لـ AI sales rep داخل zid marketplace.",
                "fit_score": 88,
                "confidence": 85,
                "evidence": "منصة تجارة إلكترونية سعودية راسخة ضمن الحجم المطلوب.",
            },
        ],
    }
