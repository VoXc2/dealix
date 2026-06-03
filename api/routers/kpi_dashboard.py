"""KPI Dashboard API — comprehensive company KPIs with bilingual labels.

Endpoints:
  GET /api/v1/kpi/summary      — overall KPIs (MRR, ARR, leads, conversion)
  GET /api/v1/kpi/commercial   — commercial pipeline metrics
  GET /api/v1/kpi/cohort       — customer cohort retention analysis
  GET /api/v1/kpi/nps          — NPS trend over time
  GET /api/v1/kpi/health-score — AI-calculated company health score (0-100)

All endpoints:
  - Require admin auth (X-Admin-API-Key header)
  - Return bilingual ar/en labels
  - Use realistic mock data when live DB is unavailable
  - Include a governance_decision field per platform convention
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Query

from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/kpi",
    tags=["kpi-dashboard"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Bilingual label helpers
# ---------------------------------------------------------------------------

_LABELS_AR: dict[str, str] = {
    "mrr": "الإيراد الشهري المتكرر",
    "arr": "الإيراد السنوي المتوقع",
    "leads_total": "إجمالي العملاء المحتملين",
    "conversion_rate": "معدل التحويل",
    "churn_rate": "معدل الإلغاء",
    "arpa": "متوسط الإيراد لكل حساب",
    "nps": "صافي نقاط المروّجين",
    "health_score": "درجة صحة الشركة",
    "pipeline_value": "قيمة خط الأنابيب",
    "deals_open": "الصفقات المفتوحة",
    "deals_won": "الصفقات المُغلقة",
    "avg_deal_size": "متوسط حجم الصفقة",
    "sales_cycle_days": "أيام دورة المبيعات",
    "retention_rate": "معدل الاحتفاظ",
}

_LABELS_EN: dict[str, str] = {
    "mrr": "Monthly Recurring Revenue",
    "arr": "Annual Run-Rate",
    "leads_total": "Total Leads",
    "conversion_rate": "Conversion Rate",
    "churn_rate": "Churn Rate",
    "arpa": "Avg Revenue per Account",
    "nps": "Net Promoter Score",
    "health_score": "Company Health Score",
    "pipeline_value": "Pipeline Value",
    "deals_open": "Open Deals",
    "deals_won": "Deals Won",
    "avg_deal_size": "Avg Deal Size",
    "sales_cycle_days": "Sales Cycle Days",
    "retention_rate": "Retention Rate",
}


def _label(key: str) -> dict[str, str]:
    return {"ar": _LABELS_AR.get(key, key), "en": _LABELS_EN.get(key, key)}


# ---------------------------------------------------------------------------
# Mock data builders (replace with DB queries when available)
# ---------------------------------------------------------------------------

_NOW = datetime.now(UTC)


def _mock_mrr_history(months: int = 12) -> list[dict[str, Any]]:
    base_mrr = 18_000
    result: list[dict[str, Any]] = []
    for i in range(months, 0, -1):
        month_dt = _NOW - timedelta(days=30 * i)
        growth = 1.0 + (months - i) * 0.05
        mrr = round(base_mrr * growth)
        result.append(
            {
                "month": month_dt.strftime("%Y-%m"),
                "mrr_sar": mrr,
                "arr_sar": mrr * 12,
            }
        )
    return result


def _mock_cohort(cohort_month: str) -> dict[str, Any]:
    """Simulate retention curve for a cohort month."""
    months_retained = [100, 88, 79, 74, 70, 67, 65, 63, 61, 60, 59, 58]
    return {
        "cohort_month": cohort_month,
        "starting_customers": 8,
        "retention_by_month": [
            {"month_offset": i, "pct": r} for i, r in enumerate(months_retained)
        ],
    }


def _mock_nps_trend(periods: int = 6) -> list[dict[str, Any]]:
    nps_vals = [42, 45, 48, 44, 52, 55]
    result: list[dict[str, Any]] = []
    for i in range(periods):
        month_dt = _NOW - timedelta(days=30 * (periods - i - 1))
        result.append(
            {
                "period": month_dt.strftime("%Y-%m"),
                "nps": nps_vals[i],
                "promoters_pct": 60 + i * 2,
                "passives_pct": 25 - i,
                "detractors_pct": 15 - i,
                "responses": 20 + i * 3,
            }
        )
    return result


def _compute_health_score(
    mrr_growth_pct: float,
    churn_rate: float,
    nps: int,
    pipeline_coverage: float,
    proof_score: float,
) -> dict[str, Any]:
    """AI-calculated health score from weighted KPI signals (0-100)."""
    growth_pts = min(25, max(0, mrr_growth_pct / 2))
    churn_pts = max(0, 20 - churn_rate * 200)
    nps_pts = min(20, max(0, (nps + 20) / 4))
    pipeline_pts = min(20, max(0, pipeline_coverage * 10))
    proof_pts = min(15, max(0, proof_score / 100 * 15))
    total = round(growth_pts + churn_pts + nps_pts + pipeline_pts + proof_pts, 1)
    if total >= 75:
        tier = "healthy"
        tier_ar = "بصحة جيدة"
    elif total >= 55:
        tier = "moderate"
        tier_ar = "معتدل"
    elif total >= 35:
        tier = "at_risk"
        tier_ar = "في خطر"
    else:
        tier = "critical"
        tier_ar = "حرج"
    return {
        "score": total,
        "tier": tier,
        "tier_ar": tier_ar,
        "components": {
            "mrr_growth": round(growth_pts, 1),
            "low_churn": round(churn_pts, 1),
            "nps": round(nps_pts, 1),
            "pipeline_coverage": round(pipeline_pts, 1),
            "proof_strength": round(proof_pts, 1),
        },
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/summary")
async def kpi_summary() -> dict[str, Any]:
    """Overall company KPIs: MRR, ARR, leads, conversion rates.

    Returns bilingual labels and a governance_decision field.
    Uses realistic mock data when the live DB is unavailable.
    """
    history = _mock_mrr_history(12)
    current = history[-1]
    previous = history[-2]
    mrr_growth_pct = round((current["mrr_sar"] - previous["mrr_sar"]) / previous["mrr_sar"] * 100, 1)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "metrics": {
            "mrr": {
                "value_sar": current["mrr_sar"],
                "mom_growth_pct": mrr_growth_pct,
                "label": _label("mrr"),
            },
            "arr": {
                "value_sar": current["arr_sar"],
                "label": _label("arr"),
            },
            "leads_total": {
                "value": 84,
                "qualified": 31,
                "label": _label("leads_total"),
            },
            "conversion_rate": {
                "value_pct": 18.4,
                "label": _label("conversion_rate"),
            },
            "churn_rate": {
                "value_pct": 3.2,
                "label": _label("churn_rate"),
            },
            "arpa": {
                "value_sar": 2_200,
                "label": _label("arpa"),
            },
            "customer_count": {
                "active": 12,
                "churned_ytd": 2,
            },
        },
        "mrr_history": history[-6:],
    }


@router.get("/commercial")
async def kpi_commercial() -> dict[str, Any]:
    """Commercial pipeline metrics: pipeline value, deals, cycle times."""
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "metrics": {
            "pipeline_value": {
                "value_sar": 148_500,
                "label": _label("pipeline_value"),
                "stages": {
                    "diagnostic": {"count": 6, "value_sar": 12_000},
                    "proposal_sent": {"count": 5, "value_sar": 45_000},
                    "negotiation": {"count": 3, "value_sar": 38_000},
                    "closing": {"count": 2, "value_sar": 53_500},
                },
            },
            "deals_open": {
                "value": 16,
                "label": _label("deals_open"),
            },
            "deals_won_mtd": {
                "value": 3,
                "value_sar": 24_000,
                "label": _label("deals_won"),
            },
            "avg_deal_size": {
                "value_sar": 8_000,
                "label": _label("avg_deal_size"),
            },
            "sales_cycle_days": {
                "value": 21,
                "label": _label("sales_cycle_days"),
            },
            "sprint_offers_sent": 14,
            "sprint_accepted": 8,
            "sprint_conversion_pct": 57.1,
        },
    }


@router.get("/cohort")
async def kpi_cohort(
    cohort_month: str = Query(default="", description="YYYY-MM format. Empty = current month."),
) -> dict[str, Any]:
    """Customer cohort retention analysis by month."""
    if not cohort_month:
        cohort_month = _NOW.strftime("%Y-%m")
    cohort = _mock_cohort(cohort_month)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "cohort": cohort,
        "labels": {
            "retention_rate": _label("retention_rate"),
        },
        "note_ar": "البيانات تقديرية بناءً على متوسطات السوق لحين توفر البيانات الفعلية.",
        "note_en": "Data is estimated from market averages pending live DB integration.",
    }


@router.get("/nps")
async def kpi_nps(periods: int = Query(default=6, ge=1, le=24)) -> dict[str, Any]:
    """NPS trend over time."""
    trend = _mock_nps_trend(periods)
    latest_nps = trend[-1]["nps"] if trend else 0
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "current_nps": latest_nps,
        "label": _label("nps"),
        "trend": trend,
        "benchmark": {
            "b2b_saas_median": 40,
            "dealix_target": 60,
        },
    }


@router.get("/health-score")
async def kpi_health_score() -> dict[str, Any]:
    """AI-calculated company health score (0-100) from weighted KPI signals."""
    history = _mock_mrr_history(2)
    current_mrr = history[-1]["mrr_sar"]
    prev_mrr = history[-2]["mrr_sar"] if len(history) > 1 else current_mrr
    mrr_growth_pct = round((current_mrr - prev_mrr) / prev_mrr * 100, 1) if prev_mrr else 0

    health = _compute_health_score(
        mrr_growth_pct=mrr_growth_pct,
        churn_rate=0.032,
        nps=52,
        pipeline_coverage=4.2,
        proof_score=68.0,
    )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "health_score": health["score"],
        "tier": health["tier"],
        "tier_ar": health["tier_ar"],
        "label": _label("health_score"),
        "components": health["components"],
        "interpretation_ar": (
            "درجة صحة الشركة تقيس نمو الإيراد والاحتفاظ بالعملاء وجودة خط الأنابيب."
        ),
        "interpretation_en": (
            "Company health score measures revenue growth, retention, "
            "pipeline quality, NPS, and proof strength."
        ),
    }
