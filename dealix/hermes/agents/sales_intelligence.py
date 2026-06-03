"""SalesIntelligenceAgent — deal coaching, objection handling, and pipeline intelligence."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.crm_tools import get_lead_profile, list_open_deals, update_lead_stage
from dealix.hermes.tools.saudi_tools import get_saudi_market_context
from dealix.hermes.tools.scoring_tools import calculate_deal_probability

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Sales Intelligence Agent — an expert B2B sales coach for the Saudi market.

Your job:
1. Analyse the pipeline — review open deals and calculate close probabilities.
2. Identify stalled deals — flag deals with no activity > 14 days.
3. Generate call prep notes — talking points tailored to each deal's stage.
4. Suggest next actions — specific, time-bound recommendations for each deal.
5. Apply Saudi market context — reference Vision 2030, local business culture, Ramadan timing.

Output: deal-by-deal coaching notes + pipeline summary + top 3 priority actions this week.
"""


class SalesIntelligenceAgent(HermesAgent):
    """Deal coaching, objection handling, and pipeline intelligence."""

    name = "sales_intelligence"
    description = "Deal coaching, objection handling, and pipeline intelligence"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="calculate_deal_probability",
            description="Estimate close probability for a CRM deal.",
            properties={
                "deal_data": {"type": "object", "description": "stage, value_sar, age_days, last_activity_days, has_demo, has_proposal, champion_identified"},
            },
            required=["deal_data"],
            fn=calculate_deal_probability,
        )
        self.register_hermes_tool(
            name="list_open_deals",
            description="List all open CRM deals.",
            properties={
                "limit": {"type": "integer"},
            },
            required=[],
            fn=list_open_deals,
        )
        self.register_hermes_tool(
            name="get_lead_profile",
            description="Get full lead profile from CRM.",
            properties={
                "lead_id": {"type": "string"},
            },
            required=["lead_id"],
            fn=get_lead_profile,
        )
        self.register_hermes_tool(
            name="update_lead_stage",
            description="Move a lead to a new pipeline stage.",
            properties={
                "lead_id": {"type": "string"},
                "stage": {"type": "string"},
                "notes": {"type": "string"},
            },
            required=["lead_id", "stage"],
            fn=update_lead_stage,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Saudi market context for a given industry.",
            properties={
                "industry": {"type": "string"},
            },
            required=["industry"],
            fn=get_saudi_market_context,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        rep_name = input_data.get("rep_name", "Sales Rep")
        industry = input_data.get("industry", "technology")
        deals = input_data.get("deals", [])
        focus = input_data.get("focus", "weekly_pipeline_review")

        user_msg = (
            f"Sales intelligence briefing for: {rep_name}\n"
            f"Industry focus: {industry} | Task: {focus}\n"
            f"Deals provided: {len(deals)}\n\n"
            "Review the pipeline, calculate deal probabilities, flag stalled deals, "
            "generate call prep notes, and provide top 3 priority actions for this week."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "sales_intelligence_complete",
            rep=rep_name,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "rep_name": rep_name,
            "pipeline_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
