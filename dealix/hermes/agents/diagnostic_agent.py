"""DiagnosticAgent — free diagnostic that identifies top 3 revenue gaps."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.analysis_tools import analyze_revenue_trend, identify_growth_levers
from dealix.hermes.tools.commercial_tools import run_commercial_diagnostic
from dealix.hermes.tools.data_tools import score_data_quality
from dealix.hermes.tools.scoring_tools import score_account_health

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Diagnostic Agent — you identify the top 3 revenue gaps in 15 minutes.

Your diagnostic process:
1. Score data quality — poor data is always a gap.
2. Check account health — flag at-risk accounts.
3. Analyse revenue trend — identify decline signals.
4. Identify growth levers — surface quick wins.
5. Use run_commercial_diagnostic for a full structured revenue gap report when company and sector context are available.

Output format (JSON-compatible):
- gaps: list of top 3 revenue gaps with impact estimate
- quick_wins: list of top 3 actions completable in < 30 days
- recommended_offer: which Dealix service tier addresses the gaps
- roi_estimate: estimated annual revenue uplift from fixing the top gap

Be specific, cite numbers, and prioritise by impact.
"""


class DiagnosticAgent(HermesAgent):
    """Free diagnostic — identifies top 3 revenue gaps in 15 minutes."""

    name = "diagnostic_agent"
    description = "Free diagnostic — identifies top 3 revenue gaps in 15 minutes"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="score_data_quality",
            description="Score dataset quality (0-100).",
            properties={
                "records": {"type": "array", "items": {"type": "object"}},
                "fields": {"type": "array", "items": {"type": "string"}},
            },
            required=["records", "fields"],
            fn=score_data_quality,
        )
        self.register_hermes_tool(
            name="score_account_health",
            description="Score a CRM account's health (0-100) from activity, MRR, and NPS.",
            properties={
                "account_id": {"type": "string"},
                "last_activity_days": {"type": "integer"},
                "mrr": {"type": "number"},
                "nps": {"type": "integer"},
            },
            required=["account_id", "last_activity_days", "mrr", "nps"],
            fn=score_account_health,
        )
        self.register_hermes_tool(
            name="analyze_revenue_trend",
            description="Analyse MoM revenue trends.",
            properties={
                "monthly_data": {"type": "array", "items": {"type": "object"}},
            },
            required=["monthly_data"],
            fn=analyze_revenue_trend,
        )
        self.register_hermes_tool(
            name="identify_growth_levers",
            description="Identify top 5 revenue growth levers.",
            properties={
                "company_data": {"type": "object"},
            },
            required=["company_data"],
            fn=identify_growth_levers,
        )
        self.register_hermes_tool(
            name="run_commercial_diagnostic",
            description="Run the full commercial DiagnosticEngine to generate a structured revenue gap report.",
            properties={
                "company_name": {"type": "string", "description": "Company to diagnose"},
                "sector": {"type": "string", "description": "Business sector, e.g. b2b_services, healthcare, retail"},
                "pain_points": {"type": "array", "items": {"type": "string"}, "description": "Known pain points"},
                "notes": {"type": "string", "description": "Additional context"},
            },
            required=["company_name"],
            fn=run_commercial_diagnostic,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        company_name = input_data.get("company_name", "Client")
        records = input_data.get("records", [])
        monthly_data = input_data.get("monthly_data", [])
        accounts = input_data.get("accounts", [])

        user_msg = (
            f"Run a quick revenue diagnostic for: {company_name}\n\n"
            f"Available: {len(records)} CRM records, "
            f"{len(monthly_data)} months revenue data, "
            f"{len(accounts)} accounts.\n\n"
            "Identify the top 3 revenue gaps, 3 quick wins, recommend a Dealix service, "
            "and estimate ROI. Use all diagnostic tools."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "diagnostic_complete",
            company=company_name,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "company_name": company_name,
            "diagnostic_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
