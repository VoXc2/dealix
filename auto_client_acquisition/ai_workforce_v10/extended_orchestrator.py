"""Extended orchestrator — wraps existing run_workforce_goal.

Adds Planner BEFORE the existing run + Reviewer AFTER. The existing
ComplianceGuardAgent already runs LAST inside ``run_workforce_goal``;
we just attach the planner + reviewer envelopes around it.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_workforce import (
    WorkforceGoal,
    run_workforce_goal,
)
from auto_client_acquisition.ai_workforce_v10.planner_agent import run_planner
from auto_client_acquisition.ai_workforce_v10.reviewer_agent import run_reviewer
from auto_client_acquisition.ai_workforce_v10.schemas import (
    PlannerOutput,
    ReviewerOutput,
)

_GUARDRAILS: dict[str, bool] = {
    "no_llm_calls": True,
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "memory_never_crosses_customers": True,
}


def run_workforce_v10(goal: WorkforceGoal) -> dict[str, Any]:
    """Run the v10 envelope: Planner → existing run → Reviewer."""
    # 1. Plan (deterministic, no side effects)
    planner: PlannerOutput = run_planner(
        getattr(goal, "goal_ar", "") or "",
        getattr(goal, "goal_en", "") or "",
        available_agents=None,
    )

    # 2. Existing v7 run (compliance veto runs internally as last step).
    try:
        run = run_workforce_goal(goal)
        run_dump = run.model_dump(mode="json")
    except Exception as exc:
        run_dump = {
            "_error": True,
            "_type": type(exc).__name__,
            "task_plan": [],
            "guardrails": dict(_GUARDRAILS),
        }

    # 3. Reviewer pass on the produced task outputs
    prior_outputs: list[dict] = []
    for task in run_dump.get("task_plan") or []:
        if isinstance(task, dict):
            payload = dict(task.get("output") or {})
            payload["_action_summary_en"] = task.get("action_summary_en", "")
            prior_outputs.append(payload)
    reviewer: ReviewerOutput = run_reviewer(prior_outputs)

    return {
        "planner": planner.model_dump(mode="json"),
        "workforce_run": run_dump,
        "reviewer": reviewer.model_dump(mode="json"),
        "guardrails": dict(_GUARDRAILS),
    }
