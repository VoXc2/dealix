"""Budget enforcement — sums estimates, picks an action."""
from __future__ import annotations

from auto_client_acquisition.llm_gateway_v10.schemas import (
    BudgetPolicy,
    CostEstimate,
)


def enforce_budget(
    estimates: list[CostEstimate],
    policy: BudgetPolicy,
) -> dict:
    """Sum ``estimates`` and decide whether the run may proceed.

    Returns a plain dict with::

        within_budget: bool
        total_usd: float
        action: "proceed" | "warn_founder" | "pause_for_approval" | "hard_stop"
        breached: "per_run" | "per_customer" | "per_agent" | "monthly" | None

    Defensive — accepts an empty list (returns proceed/0.0) and never raises.
    """
    try:
        total = round(
            sum(float(getattr(e, "estimated_usd", 0.0) or 0.0) for e in (estimates or [])),
            6,
        )
        per_run = float(policy.per_run_budget_usd)
        per_cust = float(policy.per_customer_budget_usd)
        per_agent = float(policy.per_agent_budget_usd)
        monthly = float(policy.monthly_founder_budget_usd)

        # Monthly cap is the outermost — never overrun.
        if total > monthly:
            return {
                "within_budget": False,
                "total_usd": total,
                "action": "hard_stop",
                "breached": "monthly",
            }
        if total > per_cust:
            return {
                "within_budget": False,
                "total_usd": total,
                "action": "hard_stop",
                "breached": "per_customer",
            }
        if total > per_run:
            return {
                "within_budget": False,
                "total_usd": total,
                "action": "hard_stop",
                "breached": "per_run",
            }
        if total > per_agent:
            return {
                "within_budget": True,
                "total_usd": total,
                "action": "warn_founder",
                "breached": "per_agent",
            }
        return {
            "within_budget": True,
            "total_usd": total,
            "action": "proceed",
            "breached": None,
        }
    except Exception:
        return {
            "within_budget": False,
            "total_usd": 0.0,
            "action": "hard_stop",
            "breached": "per_run",
        }
