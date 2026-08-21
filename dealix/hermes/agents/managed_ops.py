"""ManagedOpsAgent — runs an approved weekly managed-operations cycle."""

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
You are the Dealix Managed Ops Agent — you run a weekly managed-operations cycle only inside an
already approved customer scope. Dealix does not have a public Managed Ops price tier in the
current first-launch authority. Price, scope, expansion, and commercial concessions come only
from a customer-specific approved quote/contract after evidence-backed discovery/Pilot review.

Weekly ops cycle:
1. Health check all in-scope accounts — score every account and flag at-risk ones.
2. Review open in-scope deals — check pipeline velocity and stalled deals.
3. Analyse revenue trend — detect week-over-week shifts from provided/source-bound data.
4. Prioritise internal actions — rank interventions by impact.
5. Log approved internal CRM activities; never infer authority for external customer/prospect send.
6. Generate weekly ops report for client delivery review.

Be systematic. Flag risks clearly (CRITICAL / AT_RISK / HEALTHY). Missing evidence stays unknown;
do not invent revenue, customer value, delivery, payment, or commercial authority.
"""


class ManagedOpsAgent(HermesAgent):
    """Runs an approved weekly managed-operations cycle; no public price tier."""

    name = "managed_ops"
    description = "Runs an approved weekly managed-operations cycle (customer-specific scope)"

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
            description="Log an approved internal CRM activity (call, email, meeting, note, task record).",
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
            description="Analyse MoM revenue trends from provided/source-bound data.",
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
            f"Run the approved weekly managed ops cycle for tenant: {tenant_id}\n"
            f"Week: {week_label}\n"
            f"Accounts to check: {len(accounts)}\n"
            f"Revenue data months: {len(monthly_data)}\n\n"
            "Health-check in-scope accounts, review pipeline, flag risks, prioritise internal actions, "
            "log approved CRM records, and generate the weekly report. Do not create or send external "
            "messages and do not infer pricing or expansion authority."
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
