"""Scoring tool functions — ICP fit, account health, deal probability."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

# ICP scoring weights
_ICP_WEIGHTS: dict[str, float] = {
    "industry_fit": 0.30,
    "revenue_fit": 0.25,
    "employee_fit": 0.20,
    "region_fit": 0.15,
    "growth_signal": 0.10,
}

# Target ICP industry verticals for Saudi B2B
_TARGET_INDUSTRIES: frozenset[str] = frozenset(
    {
        "technology",
        "financial_services",
        "healthcare",
        "retail",
        "logistics",
        "manufacturing",
        "education",
        "real_estate",
    }
)


def _score_revenue(revenue_sar: float) -> float:
    """Score revenue fit on 0-1 scale targeting 1M-50M SAR sweet spot."""
    if 1_000_000 <= revenue_sar <= 50_000_000:
        return 1.0
    if 500_000 <= revenue_sar < 1_000_000:
        return 0.7
    if 50_000_000 < revenue_sar <= 200_000_000:
        return 0.6
    if revenue_sar < 500_000:
        return 0.3
    return 0.4


def _score_employees(employees: int) -> float:
    """Score headcount fit on 0-1 scale targeting 10-500 employees."""
    if 10 <= employees <= 500:
        return 1.0
    if 500 < employees <= 1_000:
        return 0.7
    if 5 <= employees < 10:
        return 0.6
    if employees > 1_000:
        return 0.5
    return 0.2


async def score_lead(
    company: str,
    industry: str,
    revenue_sar: float,
    employees: int,
) -> dict[str, Any]:
    """Compute an ICP fit score (0-100) for a B2B lead.

    Parameters
    ----------
    company:
        Company name for identification.
    industry:
        Industry vertical of the company.
    revenue_sar:
        Annual revenue in Saudi Riyals.
    employees:
        Total employee headcount.

    Returns
    -------
    dict
        ICP score, tier (A/B/C), and per-dimension breakdown.
    """
    industry_fit = 1.0 if industry.lower() in _TARGET_INDUSTRIES else 0.3
    revenue_fit = _score_revenue(revenue_sar)
    employee_fit = _score_employees(employees)
    # Assume region and growth signal as neutral defaults (0.7) without more data
    region_fit = 0.7
    growth_signal = 0.7

    weighted = (
        industry_fit * _ICP_WEIGHTS["industry_fit"]
        + revenue_fit * _ICP_WEIGHTS["revenue_fit"]
        + employee_fit * _ICP_WEIGHTS["employee_fit"]
        + region_fit * _ICP_WEIGHTS["region_fit"]
        + growth_signal * _ICP_WEIGHTS["growth_signal"]
    )
    score = round(weighted * 100, 1)

    if score >= 75:
        tier = "A"
        recommendation = "high_priority_outreach"
    elif score >= 50:
        tier = "B"
        recommendation = "nurture_sequence"
    else:
        tier = "C"
        recommendation = "low_priority_monitor"

    logger.info("lead_scored", company=company, score=score, tier=tier)
    return {
        "company": company,
        "icp_score": score,
        "tier": tier,
        "recommendation": recommendation,
        "breakdown": {
            "industry_fit": round(industry_fit * 100, 1),
            "revenue_fit": round(revenue_fit * 100, 1),
            "employee_fit": round(employee_fit * 100, 1),
            "region_fit": round(region_fit * 100, 1),
            "growth_signal": round(growth_signal * 100, 1),
        },
        "scored_at": datetime.now(UTC).isoformat(),
    }


async def score_account_health(
    account_id: str,
    last_activity_days: int,
    mrr: float,
    nps: int,
) -> dict[str, Any]:
    """Compute account health score combining activity, revenue, and satisfaction.

    Parameters
    ----------
    account_id:
        Unique account identifier.
    last_activity_days:
        Days since last meaningful interaction.
    mrr:
        Monthly recurring revenue in SAR.
    nps:
        Net Promoter Score (-100 to +100).

    Returns
    -------
    dict
        Health score (0-100), risk level, and recommended action.
    """
    # Activity score: 100 if active today, decays toward 0 at 90 days
    activity_score = max(0.0, 1.0 - (last_activity_days / 90.0))

    # MRR score: 0 at 0, 1.0 at 20K SAR+
    mrr_score = min(1.0, mrr / 20_000.0)

    # NPS score: map -100..+100 → 0..1
    nps_score = (min(100, max(-100, nps)) + 100) / 200.0

    health = round((activity_score * 0.40 + mrr_score * 0.35 + nps_score * 0.25) * 100, 1)

    if health >= 70:
        risk_level = "healthy"
        action = "upsell_opportunity"
    elif health >= 45:
        risk_level = "at_risk"
        action = "proactive_check_in"
    else:
        risk_level = "critical"
        action = "urgent_intervention"

    logger.info("account_health_scored", account_id=account_id, health=health, risk=risk_level)
    return {
        "account_id": account_id,
        "health_score": health,
        "risk_level": risk_level,
        "recommended_action": action,
        "breakdown": {
            "activity_score": round(activity_score * 100, 1),
            "mrr_score": round(mrr_score * 100, 1),
            "nps_score": round(nps_score * 100, 1),
        },
        "inputs": {
            "last_activity_days": last_activity_days,
            "mrr_sar": mrr,
            "nps": nps,
        },
        "scored_at": datetime.now(UTC).isoformat(),
    }


async def prioritize_leads(leads: list[dict[str, Any]]) -> dict[str, Any]:
    """Rank a list of leads by ICP fit and engagement potential.

    Parameters
    ----------
    leads:
        List of lead dicts. Each must include at minimum: company, industry,
        revenue_sar, employees.

    Returns
    -------
    dict
        Ranked lead list with scores, tiers, and reasoning.
    """
    if not leads:
        return {"ranked_leads": [], "total": 0, "tier_summary": {"A": 0, "B": 0, "C": 0}}

    scored: list[dict[str, Any]] = []
    for lead in leads:
        result = await score_lead(
            company=lead.get("company", "Unknown"),
            industry=lead.get("industry", "other"),
            revenue_sar=float(lead.get("revenue_sar", 0)),
            employees=int(lead.get("employees", 0)),
        )
        merged = {**lead, **result}
        scored.append(merged)

    ranked = sorted(scored, key=lambda x: x.get("icp_score", 0), reverse=True)

    tier_summary: dict[str, int] = {"A": 0, "B": 0, "C": 0}
    for lead in ranked:
        t = lead.get("tier", "C")
        tier_summary[t] = tier_summary.get(t, 0) + 1

    logger.info("leads_prioritized", total=len(ranked))
    return {
        "ranked_leads": ranked,
        "total": len(ranked),
        "tier_summary": tier_summary,
        "top_lead": ranked[0].get("company") if ranked else None,
    }


async def calculate_deal_probability(deal_data: dict[str, Any]) -> dict[str, Any]:
    """Estimate close probability for a CRM deal.

    Parameters
    ----------
    deal_data:
        Dict with keys: stage, value_sar, age_days, last_activity_days,
        has_demo (bool), has_proposal (bool), champion_identified (bool).

    Returns
    -------
    dict
        Probability (0-100), confidence band, and recommended next action.
    """
    stage_base: dict[str, float] = {
        "prospect": 0.05,
        "qualified": 0.15,
        "proposal": 0.35,
        "negotiation": 0.60,
        "closed_won": 1.0,
        "closed_lost": 0.0,
    }

    stage = deal_data.get("stage", "prospect")
    base_prob = stage_base.get(stage, 0.10)

    # Positive signals
    if deal_data.get("has_demo"):
        base_prob = min(1.0, base_prob + 0.10)
    if deal_data.get("has_proposal"):
        base_prob = min(1.0, base_prob + 0.10)
    if deal_data.get("champion_identified"):
        base_prob = min(1.0, base_prob + 0.15)

    # Negative signals
    age_days = int(deal_data.get("age_days", 0))
    last_activity = int(deal_data.get("last_activity_days", 0))
    if age_days > 60:
        base_prob = max(0.0, base_prob - 0.10)
    if last_activity > 14:
        base_prob = max(0.0, base_prob - 0.08)

    probability = round(base_prob * 100, 1)

    if probability >= 60:
        next_action = "schedule_closing_call"
    elif probability >= 30:
        next_action = "send_proposal_or_follow_up"
    elif probability >= 10:
        next_action = "qualify_further_or_nurture"
    else:
        next_action = "deprioritize_or_close_lost"

    logger.info(
        "deal_probability_calculated",
        stage=stage,
        probability=probability,
        next_action=next_action,
    )
    return {
        "probability": probability,
        "stage": stage,
        "confidence": "medium",
        "next_action": next_action,
        "signals": {
            "has_demo": deal_data.get("has_demo", False),
            "has_proposal": deal_data.get("has_proposal", False),
            "champion_identified": deal_data.get("champion_identified", False),
            "age_days": age_days,
            "last_activity_days": last_activity,
        },
    }


__all__ = [
    "score_lead",
    "score_account_health",
    "prioritize_leads",
    "calculate_deal_probability",
]
