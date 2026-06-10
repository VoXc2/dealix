"""MarketIntelAgent — Saudi market intelligence, competitors, Vision 2030 alignment."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.analysis_tools import analyze_revenue_trend, identify_growth_levers
from dealix.hermes.tools.data_tools import calculate_tam_sam_som
from dealix.hermes.tools.saudi_tools import get_saudi_market_context

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Market Intelligence Agent — a Saudi B2B market expert.

Your analysis covers:
1. Market sizing — TAM, SAM, SOM for the client's target segment.
2. Vision 2030 alignment — relevant programs, funding opportunities, and mandates.
3. Competitive landscape — market positioning and differentiation angles.
4. Growth drivers — macro trends creating demand in this sector.
5. Opportunity mapping — where to play and how to win.

Output: structured market intelligence report with actionable insights.
Cite specific Saudi market data. Reference Vision 2030 programs by name.
"""


class MarketIntelAgent(HermesAgent):
    """Saudi market intelligence — competitors, trends, Vision 2030 alignment."""

    name = "market_intel"
    description = "Saudi market intelligence — competitors, trends, Vision 2030 alignment"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="calculate_tam_sam_som",
            description="Estimate TAM, SAM, SOM for a Saudi market segment.",
            properties={
                "industry": {"type": "string"},
                "region": {"type": "string"},
                "segment": {"type": "string"},
            },
            required=["industry", "region", "segment"],
            fn=calculate_tam_sam_som,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Vision 2030 context and market intelligence for an industry.",
            properties={
                "industry": {"type": "string"},
            },
            required=["industry"],
            fn=get_saudi_market_context,
        )
        self.register_hermes_tool(
            name="analyze_revenue_trend",
            description="Analyse revenue trend data for market benchmarking.",
            properties={
                "monthly_data": {"type": "array", "items": {"type": "object"}},
            },
            required=["monthly_data"],
            fn=analyze_revenue_trend,
        )
        self.register_hermes_tool(
            name="identify_growth_levers",
            description="Identify growth levers from company data.",
            properties={
                "company_data": {"type": "object"},
            },
            required=["company_data"],
            fn=identify_growth_levers,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        industry = input_data.get("industry", "technology")
        region = input_data.get("region", "nationwide")
        segment = input_data.get("segment", "sme")
        company_name = input_data.get("company_name", "Client")

        user_msg = (
            f"Generate a Saudi market intelligence report for: {company_name}\n"
            f"Industry: {industry} | Region: {region} | Segment: {segment}\n\n"
            "Cover: market sizing (TAM/SAM/SOM), Vision 2030 alignment, competitive landscape, "
            "growth drivers, and a specific opportunity map. Use all available tools."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "market_intel_complete",
            industry=industry,
            company=company_name,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "industry": industry,
            "region": region,
            "market_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
