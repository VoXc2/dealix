"""Customer Health Scoring API Router.

Provides AI-powered customer health scores across 6 dimensions.
All endpoints require admin authentication (X-Admin-API-Key).

Prefix: /api/v1/customer-health
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException

from dealix.commercial.customer_health import CustomerHealthEngine, HealthInput

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/customer-health", tags=["Customers"])

_ADMIN_KEY = os.getenv("DEALIX_ADMIN_API_KEY", "")


def _require_admin(x_api_key: str = Header(default="", alias="X-Admin-API-Key")) -> None:
    if not _ADMIN_KEY:
        return
    if x_api_key != _ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin API key")


_engine = CustomerHealthEngine()


@router.post("/score")
async def score_customer_health(
    inp: HealthInput,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Calculate AI-powered health score for a single customer.

    Returns overall score (0-100), health tier (CHAMPION/HEALTHY/AT_RISK/CRITICAL/CHURNED),
    6-dimension breakdown, churn probability, and action items.
    """
    report = _engine.calculate(inp)
    return report.to_dict()


@router.post("/score/batch")
async def score_customers_batch(
    payload: dict[str, Any],
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Score multiple customers in one request.

    Body: {"customers": [<HealthInput>, ...]}
    Returns sorted list by overall_score ascending (most at-risk first).
    """
    customers_raw = payload.get("customers", [])
    if not customers_raw or not isinstance(customers_raw, list):
        raise HTTPException(status_code=400, detail="'customers' array required")
    if len(customers_raw) > 100:
        raise HTTPException(status_code=400, detail="Max 100 customers per batch")

    reports = []
    errors = []
    for i, c in enumerate(customers_raw):
        try:
            inp = HealthInput(**c)
            report = _engine.calculate(inp)
            reports.append(report.to_dict())
        except Exception as exc:
            log.warning("batch_score_error index=%d type=%s", i, type(exc).__name__)
            errors.append({"index": i, "error": "Validation error — check field types and required fields"})

    # Sort by score ascending (most at-risk first)
    reports.sort(key=lambda r: r["overall_score"])

    at_risk = [r for r in reports if r["overall_score"] < 50]
    champions = [r for r in reports if r["overall_score"] >= 85]

    return {
        "total": len(reports),
        "errors": errors,
        "summary": {
            "champions_count": len(champions),
            "at_risk_count": len(at_risk),
            "avg_health_score": round(
                sum(r["overall_score"] for r in reports) / len(reports), 1
            ) if reports else 0,
        },
        "reports": reports,
        "generated_at": datetime.now(UTC).isoformat(),
    }


@router.get("/tiers")
async def get_health_tiers() -> dict[str, Any]:
    """Returns the 5 health tier definitions and scoring criteria."""
    from dealix.commercial.customer_health import HEALTH_TIERS
    return {
        "tiers": [
            {
                "name": tier,
                "range": {"min": lo, "max": hi},
                "action_ar": _tier_action_ar(tier),
                "action_en": _tier_action_en(tier),
            }
            for tier, (lo, hi) in HEALTH_TIERS.items()
        ],
        "dimensions": [
            {"name_ar": "مستوى التفاعل", "name_en": "Engagement", "weight": 0.20},
            {"name_ar": "جودة التسليم", "name_en": "Delivery Quality", "weight": 0.25},
            {"name_ar": "الصحة المالية", "name_en": "Financial Health", "weight": 0.20},
            {"name_ar": "رضا العميل", "name_en": "Customer Satisfaction", "weight": 0.20},
            {"name_ar": "تبني المنتج", "name_en": "Product Adoption", "weight": 0.10},
            {"name_ar": "مؤشرات الخطر", "name_en": "Risk Indicators", "weight": 0.05},
        ],
    }


@router.get("/sector-benchmarks")
async def get_sector_benchmarks() -> dict[str, Any]:
    """Returns health benchmarks by Saudi B2B sector."""
    from dealix.commercial.customer_health import SECTOR_BENCHMARKS
    return {
        "benchmarks": [
            {
                "sector": sector,
                "avg_health_score": data["avg_health"],
                "churn_risk_threshold": data["churn_risk_threshold"],
            }
            for sector, data in SECTOR_BENCHMARKS.items()
        ],
        "note_ar": "هذه معدلات مرجعية من بيانات قطاع B2B السعودي — ليست ضمانات نتائج",
        "note_en": "These are reference benchmarks from Saudi B2B sector data — not guaranteed outcomes",
    }


def _tier_action_ar(tier: str) -> str:
    actions = {
        "CHAMPION": "اطلب شهادة + قدّم upsell",
        "HEALTHY": "حافظ على الزخم الأسبوعي",
        "AT_RISK": "تدخل استباقي — جلسة طارئة خلال 48 ساعة",
        "CRITICAL": "خطة إنقاذ عاجلة — تواصل اليوم",
        "CHURNED": "تدخل عميق أو خروج مُدار بشكل محترم",
    }
    return actions.get(tier, "")


def _tier_action_en(tier: str) -> str:
    actions = {
        "CHAMPION": "Request testimonial + present upsell",
        "HEALTHY": "Maintain weekly momentum",
        "AT_RISK": "Proactive intervention — emergency session within 48 hours",
        "CRITICAL": "Urgent rescue plan — contact today",
        "CHURNED": "Deep intervention or managed respectful exit",
    }
    return actions.get(tier, "")
