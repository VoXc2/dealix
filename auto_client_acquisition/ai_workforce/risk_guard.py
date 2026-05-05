"""Aggregate per-task risk into a workforce-run summary."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_workforce.schemas import AgentTask, RiskLevel


def summarize_risks(tasks: list[AgentTask]) -> dict[str, Any]:
    """Counts per risk_level + a list of blocked-action descriptors."""
    counts: dict[str, int] = {lvl.value: 0 for lvl in RiskLevel}
    blocked: list[dict[str, Any]] = []

    for task in tasks or []:
        # Pydantic stores the enum value as a string when use_enum_values=True.
        lvl = task.risk_level if isinstance(task.risk_level, str) else task.risk_level.value
        counts[lvl] = counts.get(lvl, 0) + 1
        if task.action_mode == "blocked" or lvl == RiskLevel.BLOCKED.value:
            blocked.append({
                "agent_id": task.agent_id,
                "reason_en": task.action_summary_en,
                "reason_ar": task.action_summary_ar,
            })

    return {
        "counts": counts,
        "blocked_actions": blocked,
        "total_tasks": sum(counts.values()),
    }
