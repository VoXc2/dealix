"""Workflow intelligence — manual steps and productization heuristics."""

from __future__ import annotations

WORKFLOW_INTELLIGENCE_SIGNALS: tuple[str, ...] = (
    "manual_step_repeats",
    "hours_per_project",
    "revenue_linked",
    "risk_reducing",
    "testable",
    "reusable",
)


def workflow_productization_candidate(
    *,
    manual_step_repeats: int,
    hours_per_project: float,
    revenue_linked: bool,
    risk_reducing: bool,
    testable: bool,
    reusable: bool,
) -> bool:
    """Heuristic: repeated manual + time + commercial/risk attributes."""
    return (
        manual_step_repeats >= 3
        and hours_per_project >= 2.0
        and revenue_linked
        and risk_reducing
        and testable
        and reusable
    )
