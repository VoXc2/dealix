"""ManagedOpsAgent — runs weekly managed operations cycle."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.base import HermesAgent
from dealix.hermes.tools.analysis_tools import analyze_revenue_trend, generate_executive_summary
from dealix.hermes.tools.crm_tools import list_open_deals, log_activity
from dealix.hermes.tools.scoring_tools import score_account_health

logger = structlog.get_logger(__name__)

_SYSTEM = """\
You are the Dealix Managed Ops Agent — you run the weekly operations cycle for clients on the
2,999-4,999 SAR/month managed tier.

Weekly ops cycle:
1. Health check all accounts — score every account and flag at-risk ones.
2. Review open deals — check pipeline velocity and stalled deals.
3. Analyse revenue trend — detect week-over-week shifts.
4. Prioritise actions — rank interventions by impact.
5. Log all completed activities in CRM.
6. Generate weekly ops report for client delivery.

Be systematic. Flag risks clearly (CRITICAL / AT_RISK / HEALTHY). Always log activities.
"""


class ManagedOpsAgent(HermesAgent):
    """Runs weekly managed operations cycle (2,999-4,999 SAR/mo tier)."""

    name = "managed_ops"
    description = "Runs weekly managed operations cycle (2,999-4,999 SAR/mo tier)"

    def __init__(self, config=None) -> None:
        super().__init__(config)
        self.register_hermes_tool(
            name="score_account_health",
            description="Score account health from activity, MRR, and NPS.",
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
            name="list_open_deals",
            description="List open CRM deals.",
            properties={
                "limit": {"type": "integer", "description": "Max number of deals to return"},
            },
            required=[],
            fn=list_open_deals,
        )
        self.register_hermes_tool(
            name="log_activity",
            description="Log a CRM activity (call, email, meeting, note, task).",
            properties={
                "entity_id": {"type": "string"},
                "activity_type": {"type": "string"},
                "notes": {"type": "string"},
            },
            required=["entity_id", "activity_type"],
            fn=log_activity,
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
            name="generate_executive_summary",
            description="Generate weekly executive summary.",
            properties={
                "metrics": {"type": "object"},
                "period": {"type": "string"},
            },
            required=["metrics", "period"],
            fn=generate_executive_summary,
        )

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        tenant_id = input_data.get("tenant_id", "tenant_unknown")
        accounts = input_data.get("accounts", [])
        monthly_data = input_data.get("monthly_data", [])
        week_label = input_data.get("week_label", datetime.now(UTC).strftime("W%W %Y"))

        user_msg = (
            f"Run the weekly managed ops cycle for tenant: {tenant_id}\n"
            f"Week: {week_label}\n"
            f"Accounts to check: {len(accounts)}\n"
            f"Revenue data months: {len(monthly_data)}\n\n"
            "Health-check all accounts, review pipeline, flag risks, prioritise actions, "
            "log activities, and generate the weekly report."
        )

        result = await self.run_with_tools(system=_SYSTEM, user_msg=user_msg, context=input_data)

        logger.info(
            "managed_ops_complete",
            tenant_id=tenant_id,
            week=week_label,
            tokens=result.get("usage", {}).get("total_tokens", 0),
        )
        return {
            "status": "complete",
            "agent": self.name,
            "tenant_id": tenant_id,
            "week_label": week_label,
            "weekly_report": result.get("response", ""),
            "completed_at": datetime.now(UTC).isoformat(),
            "usage": result.get("usage", {}),
        }
