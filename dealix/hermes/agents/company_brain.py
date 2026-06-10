"""CompanyBrainAgent — strategic company knowledge synthesis."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.analysis_tools import (
    analyze_revenue_trend,
    calculate_ltv_cac,
    generate_executive_summary,
    identify_growth_levers,
)
from dealix.hermes.tools.saudi_tools import get_saudi_market_context

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Company Brain Agent — the strategic intelligence layer for a B2B company.

Your synthesis covers:
1. Situation analysis — current state across revenue, data, market position.
2. Strategic options — 3 distinct paths forward with trade-offs.
3. Recommended actions — top 5 actions with priority, owner, and timeline.
4. Risk register — top 3 strategic risks with mitigation.
5. 90-day roadmap — milestones and success metrics.

Output: a comprehensive strategic briefing. Be direct, specific, and actionable.
Reference Saudi Vision 2030 context where relevant. Cite all numbers.
"""


class CompanyBrainAgent(HermesAgent):
    """Strategic company knowledge — synthesises all data into decisions."""

    name = "company_brain"
    description = "Strategic company knowledge — synthesises all data into decisions"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="generate_executive_summary",
            description="Generate executive summary from metrics.",
            properties={
                "metrics": {"type": "object"},
                "period": {"type": "string"},
            },
            required=["metrics", "period"],
            fn=generate_executive_summary,
        )
        self.register_hermes_tool(
            name="identify_growth_levers",
            description="Identify top growth levers for the company.",
            properties={
                "company_data": {"type": "object"},
            },
            required=["company_data"],
            fn=identify_growth_levers,
        )
        self.register_hermes_tool(
            name="calculate_ltv_cac",
            description="Calculate LTV, CAC, and unit economics.",
            properties={
                "revenue_data": {"type": "object"},
                "cost_data": {"type": "object"},
            },
            required=["revenue_data", "cost_data"],
            fn=calculate_ltv_cac,
        )
        self.register_hermes_tool(
            name="analyze_revenue_trend",
            description="Analyse revenue trends.",
            properties={
                "monthly_data": {"type": "array", "items": {"type": "object"}},
            },
            required=["monthly_data"],
            fn=analyze_revenue_trend,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Saudi market context for strategic positioning.",
            properties={
                "industry": {"type": "string"},
            },
            required=["industry"],
            fn=get_saudi_market_context,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        company_name = input_data.get("company_name", "Client")
        industry = input_data.get("industry", "technology")
        period = input_data.get("period", "Q2 2026")
        metrics = input_data.get("metrics", {})

        user_msg = (
            f"Build a strategic synthesis for: {company_name}\n"
            f"Industry: {industry} | Period: {period}\n"
            f"Metrics available: {list(metrics.keys())}\n\n"
            "Produce: situation analysis, 3 strategic options, top 5 recommended actions, "
            "risk register, and a 90-day roadmap. Use all tools."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "company_brain_complete",
            company=company_name,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "company_name": company_name,
            "strategic_synthesis": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
