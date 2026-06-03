"""LeadIntelligenceAgent — qualifies, scores, and enriches B2B leads for the Saudi market."""

from __future__ import annotations

from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.data_tools import enrich_company_data
from dealix.hermes.tools.saudi_tools import get_saudi_market_context
from dealix.hermes.tools.scoring_tools import prioritize_leads, score_lead

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Lead Intelligence Agent — a B2B revenue expert specialising in the Saudi market.

Your job is to:
1. Enrich each lead with Saudi market context.
2. Score every lead for ICP fit using score_lead.
3. Prioritise the full list using prioritize_leads.
4. Return tier classifications (A/B/C) and recommended actions.

Always use the tools provided. Think step-by-step. After processing all leads, synthesise a
ranked list with next-action recommendations for each tier.
"""


class LeadIntelligenceAgent(HermesAgent):
    """Qualifies, scores, and enriches B2B leads for the Saudi market."""

    name = "lead_intelligence"
    description = "Qualifies, scores, and enriches B2B leads for Saudi market"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="score_lead",
            description="Score a B2B lead for ICP fit (0-100). Returns tier A/B/C and recommended offer.",
            properties={
                "company": {"type": "string", "description": "Company name"},
                "industry": {"type": "string", "description": "Industry vertical"},
                "revenue_sar": {"type": "number", "description": "Annual revenue in SAR"},
                "employees": {"type": "integer", "description": "Number of employees"},
            },
            required=["company", "industry", "revenue_sar", "employees"],
            fn=score_lead,
        )
        self.register_hermes_tool(
            name="enrich_company_data",
            description="Enrich a company profile with Saudi market data (MISA, LinkedIn, Vision 2030).",
            properties={
                "company_name": {"type": "string", "description": "Company name"},
                "cr_number": {"type": "string", "description": "Saudi CR number (optional)"},
            },
            required=["company_name"],
            fn=enrich_company_data,
        )
        self.register_hermes_tool(
            name="prioritize_leads",
            description="Rank a list of scored leads by priority score and assign tiers.",
            properties={
                "leads": {
                    "type": "array",
                    "description": "List of lead dicts with icp_score and value_sar fields",
                    "items": {"type": "object"},
                },
            },
            required=["leads"],
            fn=prioritize_leads,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Return Vision 2030 context, opportunity score, and growth catalysts for an industry.",
            properties={
                "industry": {"type": "string", "description": "Industry vertical (e.g. fintech, energy)"},
            },
            required=["industry"],
            fn=get_saudi_market_context,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        leads = input_data.get("leads", [])
        goal = input_data.get("goal", "Score and prioritise all leads for outreach")

        if not leads:
            return {
                "status": "no_leads",
                "ranked_leads": [],
                "tier_summary": {"A": 0, "B": 0, "C": 0},
                "recommended_actions": [],
                "total_processed": 0,
            }

        user_msg = (
            f"Goal: {goal}\n\n"
            f"Leads to process ({len(leads)} total):\n"
            + "\n".join(
                f"- {l.get('company', 'Unknown')} | Industry: {l.get('industry', 'N/A')} "
                f"| Revenue: {l.get('revenue_sar', 0):,.0f} SAR "
                f"| Employees: {l.get('employees', 0)}"
                for l in leads[:20]
            )
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)
        response_text = result.get("response", "")

        logger.info(
            "lead_intelligence_complete",
            leads_processed=len(leads),
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "leads_processed": len(leads),
            "analysis": response_text,
            "usage": result.get("usage", {}),
        }
