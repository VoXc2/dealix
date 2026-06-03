"""Analysis tool functions — revenue trends, cohorts, LTV/CAC, executive summaries."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


async def analyze_revenue_trend(monthly_data: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute growth rate, MoM changes, and a simple linear forecast."""
    if not monthly_data:
        return {
            "status": "no_data",
            "growth_rate_pct": 0.0,
            "mom_changes": [],
            "forecast_3m": [],
            "alert_flags": ["insufficient_data"],
        }

    revenues = [float(d.get("revenue_sar", 0)) for d in monthly_data]
    months = [d.get("month", "") for d in monthly_data]

    mom_changes: list[dict[str, Any]] = []
    for i in range(1, len(revenues)):
        prev = revenues[i - 1]
        curr = revenues[i]
        change_pct = round((curr - prev) / prev * 100, 2) if prev > 0 else 0.0
        mom_changes.append({
            "month": months[i],
            "revenue_sar": curr,
            "change_pct": change_pct,
            "direction": "up" if change_pct > 0 else ("down" if change_pct < 0 else "flat"),
        })

    overall_growth = (
        round((revenues[-1] - revenues[0]) / revenues[0] * 100, 2)
        if len(revenues) >= 2 and revenues[0] > 0
        else 0.0
    )

    avg_delta = (revenues[-1] - revenues[0]) / max(1, len(revenues) - 1)
    forecast_3m = [
        {"offset_months": i, "projected_revenue_sar": round(max(0.0, revenues[-1] + avg_delta * i), 2)}
        for i in range(1, 4)
    ]

    alert_flags: list[str] = []
    if len(mom_changes) >= 2 and all(c["change_pct"] < 0 for c in mom_changes[-2:]):
        alert_flags.append("consecutive_revenue_decline")
    if revenues[-1] < revenues[0] * 0.8:
        alert_flags.append("revenue_below_starting_point_20pct")
    if overall_growth > 50:
        alert_flags.append("high_growth_validate_sustainability")

    logger.info("revenue_trend_analyzed", months=len(monthly_data), overall_growth=overall_growth)
    return {
        "status": "analyzed",
        "period_months": len(monthly_data),
        "first_month": months[0] if months else "",
        "last_month": months[-1] if months else "",
        "first_revenue_sar": revenues[0],
        "last_revenue_sar": revenues[-1],
        "growth_rate_pct": overall_growth,
        "avg_monthly_revenue_sar": round(sum(revenues) / len(revenues), 2),
        "mom_changes": mom_changes,
        "forecast_3m": forecast_3m,
        "alert_flags": alert_flags,
    }


async def generate_cohort_analysis(cohort_data: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze customer cohort retention and revenue expansion."""
    if not cohort_data:
        return {"cohorts": [], "avg_retention_12m": 0.0, "best_cohort": None, "worst_cohort": None}

    cohorts: dict[str, dict[str, Any]] = {}
    for record in cohort_data:
        cm = record.get("cohort_month", "unknown")
        offset = int(record.get("month_offset", 0))
        mrr = float(record.get("mrr", 0))
        cid = record.get("customer_id", "")
        if cm not in cohorts:
            cohorts[cm] = {"offsets": {}, "customers": set()}
        cohorts[cm]["offsets"].setdefault(offset, []).append(mrr)
        cohorts[cm]["customers"].add(cid)

    summaries: list[dict[str, Any]] = []
    for cm, info in cohorts.items():
        offsets = info["offsets"]
        starting = len(offsets.get(0, []))
        m12 = len(offsets.get(12, []))
        retention_12m = (m12 / starting * 100) if starting else 0.0
        s_mrr = sum(offsets.get(0, []))
        c_mrr = sum(offsets.get(max(offsets.keys()), [])) if offsets else 0.0
        expansion = (c_mrr / s_mrr * 100 - 100) if s_mrr else 0.0
        summaries.append({
            "cohort_month": cm,
            "starting_customers": starting,
            "retention_12m_pct": round(retention_12m, 1),
            "starting_mrr_sar": s_mrr,
            "latest_mrr_sar": c_mrr,
            "expansion_pct": round(expansion, 1),
        })

    summaries.sort(key=lambda x: x["cohort_month"])
    retentions = [c["retention_12m_pct"] for c in summaries if c["retention_12m_pct"] > 0]
    avg_ret = sum(retentions) / len(retentions) if retentions else 0.0
    best = max(summaries, key=lambda x: x["retention_12m_pct"], default=None)
    worst = min(summaries, key=lambda x: x["retention_12m_pct"], default=None)

    logger.info("cohort_analysis_generated", cohort_count=len(summaries))
    return {
        "cohorts": summaries,
        "avg_retention_12m": round(avg_ret, 1),
        "best_cohort": best.get("cohort_month") if best else None,
        "worst_cohort": worst.get("cohort_month") if worst else None,
    }


async def calculate_ltv_cac(
    revenue_data: dict[str, Any],
    cost_data: dict[str, Any],
) -> dict[str, Any]:
    """Calculate LTV, CAC, and related SaaS health metrics."""
    avg_mrr = float(revenue_data.get("avg_mrr_sar", 0))
    avg_contract_months = float(revenue_data.get("avg_contract_months", 12))
    churn_monthly = float(revenue_data.get("churn_rate_monthly", 0.05))
    gross_margin = float(revenue_data.get("gross_margin_pct", 0.70))

    sales_marketing = float(cost_data.get("total_sales_marketing_sar", 1))
    new_customers = max(1, int(cost_data.get("new_customers_acquired", 1)))

    ltv = ((avg_mrr * gross_margin) / churn_monthly) if churn_monthly > 0 else (avg_mrr * gross_margin * avg_contract_months)
    cac = sales_marketing / new_customers
    ltv_cac_ratio = ltv / max(1, cac)
    monthly_margin = avg_mrr * gross_margin
    payback_months = cac / monthly_margin if monthly_margin > 0 else 0

    if ltv_cac_ratio >= 3:
        health, interpretation = "healthy", "Business is generating strong returns on customer acquisition."
    elif ltv_cac_ratio >= 1:
        health, interpretation = "marginal", "Returns are positive but acquisition costs are high relative to lifetime value."
    else:
        health, interpretation = "unhealthy", "CAC exceeds LTV — acquisition strategy requires immediate review."

    logger.info("ltv_cac_calculated", ltv=ltv, cac=cac, ratio=round(ltv_cac_ratio, 2))
    return {
        "ltv_sar": round(ltv, 2),
        "cac_sar": round(cac, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "payback_months": round(payback_months, 1),
        "health": health,
        "interpretation": interpretation,
        "gross_margin_pct": round(gross_margin * 100, 1),
        "churn_rate_monthly_pct": round(churn_monthly * 100, 2),
    }


async def generate_executive_summary(
    metrics: dict[str, Any],
    period: str,
) -> dict[str, Any]:
    """Generate a structured executive summary from a metrics dict."""
    highlights: list[str] = []
    risks: list[str] = []

    revenue = float(metrics.get("revenue_sar", 0) or metrics.get("mrr_sar", 0))
    growth = float(metrics.get("growth_rate_pct", 0))
    churn = float(metrics.get("churn_rate_pct", 0))
    nps = metrics.get("nps")
    new_customers = int(metrics.get("new_customers", 0))

    if growth > 0:
        highlights.append(f"Revenue growth of {growth:.1f}% recorded.")
    elif growth < -5:
        risks.append(f"Revenue declined {abs(growth):.1f}% — action required.")

    if churn > 5:
        risks.append(f"Churn rate {churn:.1f}% exceeds healthy threshold of 5%.")
    elif churn > 0:
        highlights.append(f"Churn rate controlled at {churn:.1f}%.")

    if nps is not None:
        nps_val = int(nps)
        if nps_val >= 50:
            highlights.append(f"NPS {nps_val} — strong customer advocacy.")
        elif nps_val < 0:
            risks.append(f"NPS {nps_val} — customer satisfaction requires attention.")

    if new_customers > 0:
        highlights.append(f"{new_customers} new customers acquired.")

    rating = "strong" if not risks and len(highlights) >= 2 else ("moderate" if len(risks) <= 1 else "needs_attention")
    rev_str = f"SAR {revenue:,.0f}. " if revenue > 0 else ""
    headline = f"{rev_str}Period: {period} — Performance: {rating.upper()}."

    logger.info("executive_summary_generated", period=period, rating=rating)
    return {
        "headline": headline,
        "period": period,
        "performance_rating": rating,
        "highlights": highlights[:5],
        "risks": risks[:5],
        "metrics_snapshot": metrics,
        "generated_at": datetime.now(UTC).isoformat(),
    }


async def identify_growth_levers(company_data: dict[str, Any]) -> dict[str, Any]:
    """Identify top growth levers based on company profile and metrics."""
    levers: list[dict[str, Any]] = []

    churn = float(company_data.get("churn_rate", 0.05))
    if churn > 0.05:
        levers.append({
            "lever": "reduce_churn",
            "impact": "high",
            "effort": "medium",
            "rationale": f"Monthly churn {churn*100:.1f}% — 1pp reduction drives significant LTV uplift.",
            "action": "Implement proactive customer success program.",
            "priority": 1,
        })

    if not company_data.get("has_crm"):
        levers.append({
            "lever": "crm_implementation",
            "impact": "high",
            "effort": "medium",
            "rationale": "No CRM detected — pipeline visibility is limited.",
            "action": "Deploy CRM with lead scoring within 30 days.",
            "priority": 2,
        })

    if not company_data.get("has_data_infra"):
        levers.append({
            "lever": "data_infrastructure",
            "impact": "high",
            "effort": "high",
            "rationale": "Data infrastructure gaps limit analytics and AI capabilities.",
            "action": "Build unified data model and quality baseline.",
            "priority": 3,
        })

    revenue = float(company_data.get("revenue_sar", 0))
    employees = int(company_data.get("employees", 0))
    if employees > 0 and revenue / employees < 200_000:
        levers.append({
            "lever": "revenue_per_employee",
            "impact": "medium",
            "effort": "high",
            "rationale": "Revenue per employee below 200K SAR — productivity gap exists.",
            "action": "Automate high-volume manual processes.",
            "priority": 4,
        })

    if company_data.get("vision_2030_aligned"):
        levers.append({
            "lever": "vision_2030_positioning",
            "impact": "medium",
            "effort": "low",
            "rationale": "Company is aligned with Vision 2030 sectors — leverage for enterprise deals.",
            "action": "Create Vision 2030 alignment narrative for enterprise pitch.",
            "priority": 5,
        })

    nps = int(company_data.get("nps", 0))
    if nps >= 40:
        levers.append({
            "lever": "referral_program",
            "impact": "medium",
            "effort": "low",
            "rationale": f"NPS {nps} indicates satisfied customers — activate referral engine.",
            "action": "Launch structured referral incentive program.",
            "priority": 6,
        })

    levers.sort(key=lambda x: x["priority"])
    logger.info("growth_levers_identified", count=len(levers))
    return {
        "growth_levers": levers[:5],
        "total_levers_identified": len(levers),
        "top_priority": levers[0]["lever"] if levers else None,
        "quick_wins": [l for l in levers if l["effort"] == "low"][:3],
    }


__all__ = [
    "analyze_revenue_trend",
    "generate_cohort_analysis",
    "calculate_ltv_cac",
    "generate_executive_summary",
    "identify_growth_levers",
]
