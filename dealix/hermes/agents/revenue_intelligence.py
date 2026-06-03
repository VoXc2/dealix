"""RevenueIntelligenceAgent — analyses revenue patterns and forecasts growth."""

from __future__ import annotations

from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.analysis_tools import (
    analyze_revenue_trend,
    calculate_ltv_cac,
    generate_cohort_analysis,
    generate_executive_summary,
    identify_growth_levers,
)

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Revenue Intelligence Agent — a world-class SaaS revenue analyst.

Your job is to:
1. Analyse monthly revenue trends (MoM growth, declines, anomalies).
2. Run cohort analysis to understand retention.
3. Calculate LTV/CAC to assess unit economics.
4. Identify the top growth levers.
5. Synthesise everything into an executive summary.

Use all available tools. Flag alerts proactively. Always cite specific numbers.
Output a structured analysis with: Metrics, Trends, Unit Economics, Growth Levers, and Executive Summary.
"""


class RevenueIntelligenceAgent(HermesAgent):
    """Analyses revenue patterns, forecasts growth, and identifies levers."""

    name = "revenue_intelligence"
    description = "Analyses revenue patterns and forecasts growth for B2B companies"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="analyze_revenue_trend",
            description="Analyse MoM revenue trends, compute growth rate, and forecast 3 months.",
            properties={
                "monthly_data": {
                    "type": "array",
                    "description": "List of {month: 'YYYY-MM', revenue_sar: float}",
                    "items": {"type": "object"},
                },
            },
            required=["monthly_data"],
            fn=analyze_revenue_trend,
        )
        self.register_hermes_tool(
            name="generate_cohort_analysis",
            description="Analyse customer retention by cohort month.",
            properties={
                "cohort_data": {
                    "type": "array",
                    "description": "List of cohort records with cohort_month, month_offset, mrr, customer_id",
                    "items": {"type": "object"},
                },
            },
            required=["cohort_data"],
            fn=generate_cohort_analysis,
        )
        self.register_hermes_tool(
            name="calculate_ltv_cac",
            description="Calculate LTV, CAC, LTV:CAC ratio, and payback period.",
            properties={
                "revenue_data": {"type": "object", "description": "avg_mrr_sar, churn_rate_monthly, gross_margin_pct"},
                "cost_data": {"type": "object", "description": "total_sales_marketing_sar, new_customers_acquired"},
            },
            required=["revenue_data", "cost_data"],
            fn=calculate_ltv_cac,
        )
        self.register_hermes_tool(
            name="identify_growth_levers",
            description="Identify top 5 growth levers with estimated revenue uplift.",
            properties={
                "company_data": {"type": "object", "description": "Company metrics dict"},
            },
            required=["company_data"],
            fn=identify_growth_levers,
        )
        self.register_hermes_tool(
            name="generate_executive_summary",
            description="Generate bilingual AR/EN executive summary from metrics.",
            properties={
                "metrics": {"type": "object", "description": "Key metrics dict"},
                "period": {"type": "string", "description": "Reporting period e.g. 'Q2 2026'"},
            },
            required=["metrics", "period"],
            fn=generate_executive_summary,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        company_data = input_data.get("company_data", {})
        period = input_data.get("period", "Q2 2026")
        monthly_data = input_data.get("monthly_data", [])
        cohort_data = input_data.get("cohort_data", [])

        user_msg = (
            f"Analyse the revenue intelligence for this company.\n"
            f"Period: {period}\n"
            f"Company profile: {company_data}\n"
            f"Monthly revenue data: {monthly_data[:12]}\n"
            f"Cohort data available: {len(cohort_data)} records\n\n"
            "Use all tools to produce a complete revenue intelligence report."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)
        logger.info("revenue_intelligence_complete", period=period, tokens=result.get("usage", {}).get("total_tokens", 0))

        return {
            "status": "complete",
            "agent": self.name,
            "period": period,
            "analysis": result.get("response", ""),
            "usage": result.get("usage", {}),
        }
