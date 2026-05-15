"""Cost tracking endpoint (W11.2).

Public read-only endpoint surfacing aggregate cost telemetry: infrastructure
+ per-customer cost-to-serve + LLM provider usage. Used for:

  - Investor diligence (cost-to-serve breakdown by tier)
  - Customer transparency (admin shows their consumption + our cost)
  - Internal margin tracking (compare to financial model)

  GET /api/v1/cost-tracking/summary
      Aggregate this-month costs across infrastructure, LLM providers,
      data adapters. Admin-only (sensitive operational data).

  GET /api/v1/cost-tracking/per-tier
      Cost-per-customer breakdown by plan tier (pilot/starter/growth/scale).
      Public read-only (drives the v4 §3 financial model transparency).

All costs are expressed in halalas (1 SAR = 100 halalas) so the response
matches the unit used in api/routers/pricing.py PLANS.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/cost-tracking", tags=["cost-tracking"])

# ── Cost model (halalas/month per tier) ──────────────────────────
# Calibrated from v3 §1 financial model + actual provider quotas.
# Source of truth: financial_model in docs/sales-kit/dealix_financial_model.md

INFRASTRUCTURE_FIXED_HALALAS_PER_MONTH = 172_500   # 1,725 SAR (Railway + Redis + Postgres + Sentry + Langfuse)

# Per-customer variable cost components (halalas/month)
TIER_VARIABLE_COSTS = {
    "pilot": {
        "llm_inference":   500,   # 5 SAR     (50 LLM calls × 0.10 SAR avg)
        "lead_adapters":   500,   # 5 SAR     (Hunter quota share + Maps + Firecrawl)
        "moyasar_fees":    100,   # 1 SAR     (transaction fees on 499 pilot)
        "support_time":   2000,   # 20 SAR    (founder time amortized)
        "total_per_pilot": 3100,  # 31 SAR    per 7-day pilot
    },
    "starter": {
        "llm_inference":  3000,   # 30 SAR    (200 leads × 0.15 SAR scoring + replies)
        "lead_adapters":  2000,   # 20 SAR
        "moyasar_fees":    300,   # 3 SAR     (subscription processing)
        "support_time":   5000,   # 50 SAR    (CS time)
        "infra_share":    1725,   # 17 SAR    (infrastructure attribution)
        "total_per_month": 12025, # 120 SAR/mo
    },
    "growth": {
        "llm_inference": 15000,   # 150 SAR   (1000 leads + heavy AI workforce usage)
        "lead_adapters":  8000,   # 80 SAR
        "moyasar_fees":    900,   # 9 SAR
        "support_time":  10000,   # 100 SAR
        "infra_share":    1725,   # 17 SAR
        "total_per_month": 35625, # 356 SAR/mo
    },
    "scale": {
        "llm_inference": 60000,   # 600 SAR   (5000 leads, full agent workforce)
        "lead_adapters": 25000,   # 250 SAR
        "moyasar_fees":   2400,   # 24 SAR
        "support_time":  30000,   # 300 SAR
        "infra_share":    1725,   # 17 SAR
        "total_per_month": 119125, # 1,191 SAR/mo
    },
}

TIER_PRICE_HALALAS_PER_MONTH = {
    "pilot":    49900,
    "starter":  99900,
    "growth":  299900,
    "scale":   799900,
}


def _margin_breakdown(tier: str) -> dict[str, Any]:
    if tier not in TIER_VARIABLE_COSTS:
        return {}
    cost = TIER_VARIABLE_COSTS[tier]
    total_cost_key = (
        "total_per_pilot" if tier == "pilot" else "total_per_month"
    )
    cost_halalas = cost[total_cost_key]
    price_halalas = TIER_PRICE_HALALAS_PER_MONTH[tier]
    gross_profit = price_halalas - cost_halalas
    gross_margin_pct = round(
        (gross_profit / price_halalas) * 100, 1
    ) if price_halalas > 0 else 0.0

    return {
        "tier": tier,
        "price_halalas": price_halalas,
        "price_sar": price_halalas // 100,
        "total_cost_halalas": cost_halalas,
        "total_cost_sar": cost_halalas // 100,
        "gross_profit_halalas": gross_profit,
        "gross_profit_sar": gross_profit // 100,
        "gross_margin_pct": gross_margin_pct,
        "cost_breakdown_halalas": {
            k: v for k, v in cost.items() if not k.startswith("total")
        },
    }


@router.get("/per-tier")
async def cost_per_tier() -> dict[str, Any]:
    """Public cost-to-serve breakdown per tier. Drives v4 §3 transparency.

    No PII, no per-customer data — only model parameters. Returns the
    same numbers the financial model in docs/sales-kit uses.
    """
    return {
        "currency": "SAR",
        "unit": "halalas (1 SAR = 100 halalas)",
        "infrastructure_fixed_halalas_per_month": INFRASTRUCTURE_FIXED_HALALAS_PER_MONTH,
        "infrastructure_fixed_sar_per_month": INFRASTRUCTURE_FIXED_HALALAS_PER_MONTH // 100,
        "tiers": {
            tier: _margin_breakdown(tier) for tier in TIER_VARIABLE_COSTS
        },
        "note": (
            "Cost figures are model parameters, not actuals. Margin "
            "varies by customer (LLM usage spikes, etc.). Source of "
            "truth: docs/sales-kit/dealix_financial_model.md."
        ),
        "model_version": "1.0",
        "last_calibrated": "2026-05-13",
    }


@router.get(
    "/summary",
    dependencies=[Depends(require_admin_key)],
)
async def cost_summary() -> dict[str, Any]:
    """Admin-only aggregate cost telemetry this month.

    Stub: real telemetry requires Langfuse + Moyasar usage exports.
    Returns the model parameters in the meantime so dashboards have
    a stable schema to render against.
    """
    now = datetime.now(UTC)
    return {
        "period": {
            "month": now.strftime("%Y-%m"),
            "generated_at": now.isoformat(),
        },
        "infrastructure": {
            "fixed_halalas": INFRASTRUCTURE_FIXED_HALALAS_PER_MONTH,
            "fixed_sar": INFRASTRUCTURE_FIXED_HALALAS_PER_MONTH // 100,
            "components": [
                "Railway hosting",
                "Postgres (managed)",
                "Redis (managed)",
                "Sentry (free tier through Y1)",
                "Langfuse (LLM observability)",
            ],
        },
        "llm_providers": {
            "status": "telemetry_not_yet_wired",
            "note": "Awaits Langfuse cost export integration; this commit "
                    "establishes schema. Plan: Q3 2026 after customer #5.",
        },
        "data_adapters": {
            "status": "telemetry_not_yet_wired",
            "providers": [
                "Google Search/CSE quota share",
                "Google Maps quota share",
                "Hunter.io 50/day free tier",
                "Firecrawl on-demand",
                "Wappalyzer",
            ],
        },
        "warning": (
            "Aggregate cost telemetry is a stub. Real numbers require "
            "wired provider exports. Tier model parameters above are "
            "the authoritative source until Q3 2026."
        ),
    }
