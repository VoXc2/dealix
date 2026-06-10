"""SprintOrchestratorAgent — executes the 7-day Revenue Intelligence Sprint."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.analysis_tools import analyze_revenue_trend, generate_executive_summary
from dealix.hermes.tools.commercial_tools import build_commercial_proof_pack, run_commercial_sprint
from dealix.hermes.tools.data_tools import generate_data_passport, score_data_quality
from dealix.hermes.tools.saudi_tools import get_saudi_market_context
from dealix.hermes.tools.scoring_tools import score_lead

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Sprint Orchestrator — you run the 7-day Revenue Intelligence Sprint.

Sprint structure:
  Day 1: Source Passport + DQ Score — assess data quality baseline.
  Day 2: Account Scoring — ICP fit for all accounts.
  Day 3: Revenue Trend Analysis — historical patterns and forecasts.
  Day 4: Market Context — Vision 2030 and Saudi market positioning.
  Day 5: Growth Lever Identification — top 5 revenue levers.
  Day 6: Proof Pack Assembly — evidence for ROI claims.
  Day 7: Executive Summary + Delivery — final client-ready output.

For each day: use the relevant tools, record findings, and build toward the final report.
Your output must include a day-by-day findings log and a final sprint_report dict.
"""


class SprintOrchestratorAgent(HermesAgent):
    """Executes the 7-day Revenue Intelligence Sprint (499 SAR offer)."""

    name = "sprint_orchestrator"
    description = "Executes the 7-day Revenue Intelligence Sprint (499 SAR offer)"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="score_data_quality",
            description="Score the quality of a dataset (0-100) across completeness, consistency, uniqueness.",
            properties={
                "records": {"type": "array", "description": "List of record dicts", "items": {"type": "object"}},
                "fields": {"type": "array", "description": "Field names to assess", "items": {"type": "string"}},
            },
            required=["records", "fields"],
            fn=score_data_quality,
        )
        self.register_hermes_tool(
            name="generate_data_passport",
            description="Generate a structured data passport report for a tenant.",
            properties={
                "tenant_id": {"type": "string", "description": "Tenant identifier"},
            },
            required=["tenant_id"],
            fn=generate_data_passport,
        )
        self.register_hermes_tool(
            name="score_lead",
            description="Score a B2B lead for ICP fit (0-100).",
            properties={
                "company": {"type": "string"},
                "industry": {"type": "string"},
                "revenue_sar": {"type": "number"},
                "employees": {"type": "integer"},
            },
            required=["company", "industry", "revenue_sar", "employees"],
            fn=score_lead,
        )
        self.register_hermes_tool(
            name="analyze_revenue_trend",
            description="Analyse MoM revenue trends and produce 3-month forecast.",
            properties={
                "monthly_data": {"type": "array", "items": {"type": "object"}},
            },
            required=["monthly_data"],
            fn=analyze_revenue_trend,
        )
        self.register_hermes_tool(
            name="get_saudi_market_context",
            description="Return Vision 2030 context and market size for an industry.",
            properties={
                "industry": {"type": "string"},
            },
            required=["industry"],
            fn=get_saudi_market_context,
        )
        self.register_hermes_tool(
            name="generate_executive_summary",
            description="Generate executive summary from metrics dict.",
            properties={
                "metrics": {"type": "object"},
                "period": {"type": "string"},
            },
            required=["metrics", "period"],
            fn=generate_executive_summary,
        )
        self.register_hermes_tool(
            name="run_commercial_sprint",
            description="Execute all 7 days of the Revenue Intelligence Sprint via the commercial SprintOrchestrator.",
            properties={
                "engagement_id": {"type": "string", "description": "Unique sprint engagement ID"},
                "customer_id": {"type": "string", "description": "Customer identifier"},
                "customer_name": {"type": "string", "description": "Customer company name"},
                "sector": {"type": "string", "description": "Business sector"},
                "pain_summary": {"type": "string", "description": "Summary of customer pain points"},
                "founder_approved": {"type": "boolean", "description": "Whether founder has approved this sprint"},
            },
            required=["engagement_id", "customer_id"],
            fn=run_commercial_sprint,
        )
        self.register_hermes_tool(
            name="build_commercial_proof_pack",
            description="Build a proof pack with evidence of ROI for Day 6 of the sprint.",
            properties={
                "account_id": {"type": "string"},
                "company_name": {"type": "string"},
                "events": {"type": "array", "items": {"type": "object"}, "description": "Proof events/evidence"},
                "approved_by_founder": {"type": "boolean"},
                "customer_consent": {"type": "boolean"},
            },
            required=["account_id", "company_name"],
            fn=build_commercial_proof_pack,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        tenant_id = input_data.get("tenant_id", "tenant_unknown")
        company_name = input_data.get("company_name", "Client Company")
        industry = input_data.get("industry", "technology")
        monthly_data = input_data.get("monthly_data", [])
        records = input_data.get("records", [])
        sprint_id = input_data.get("sprint_id", f"SPRINT-{tenant_id[:6].upper()}")

        user_msg = (
            f"Execute the full 7-day Revenue Intelligence Sprint for:\n"
            f"Client: {company_name} | Industry: {industry} | Tenant ID: {tenant_id}\n"
            f"Sprint ID: {sprint_id}\n\n"
            f"Available data: {len(records)} records, {len(monthly_data)} months of revenue data.\n\n"
            "Work through each day systematically. Use all available tools. "
            "Return day-by-day findings and a comprehensive final sprint report."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "sprint_orchestrator_complete",
            sprint_id=sprint_id,
            company=company_name,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "sprint_id": sprint_id,
            "company_name": company_name,
            "sprint_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
