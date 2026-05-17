"""Layer 7 — Improvement Decision (experiments + improvement backlog).

The founder runs at most 3 experiments per week. ``select_experiments``
enforces that cap. The improvement backlog is suggest-only — items are
``proposed`` until a human approves them (mirrors the suggest-only
discipline of the existing Self-Improvement OS).
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    Experiment,
    ImprovementItem,
)

MAX_EXPERIMENTS_PER_WEEK = 3

# Default experiment templates — used when the caller supplies none.
DEFAULT_EXPERIMENTS: list[tuple[str, str, str, int]] = [
    ("exp_icp", "If we focus on one ICP, reply rate rises.",
     "reply_rate + meeting_rate", 7),
    ("exp_cta", "If the CTA is 'Risk Score' vs 'Proof Pack', booking rate changes.",
     "conversion_to_booking", 7),
    ("exp_offer", "If we lead with a 499 SAR starter, paid conversion rises.",
     "paid_conversion + client_quality", 7),
]


def select_experiments(inputs: AssuranceInputs) -> list[Experiment]:
    """Return this week's experiments (max 3). Raises ValueError if the
    caller supplies more than the weekly cap — focus is enforced."""
    supplied = inputs.experiments
    if len(supplied) > MAX_EXPERIMENTS_PER_WEEK:
        raise ValueError(
            f"max {MAX_EXPERIMENTS_PER_WEEK} experiments per week; "
            f"got {len(supplied)} — focus, do not scatter"
        )
    if supplied:
        return [
            Experiment(
                id=str(e.get("id", f"exp_{i}")),
                hypothesis=str(e.get("hypothesis", "")),
                metric=str(e.get("metric", "")),
                timebox_days=int(e.get("timebox_days", 7)),
                decision=str(e.get("decision", "pending")),
            )
            for i, e in enumerate(supplied)
        ]
    return [
        Experiment(eid, hyp, metric, days, "pending")
        for eid, hyp, metric, days in DEFAULT_EXPERIMENTS
    ]


def build_improvement_backlog(inputs: AssuranceInputs) -> list[ImprovementItem]:
    """Map caller-supplied improvement items into the backlog. Items stay
    ``proposed`` until a human approves — never auto-applied."""
    backlog: list[ImprovementItem] = []
    for i, item in enumerate(inputs.improvement_items):
        status = str(item.get("status", "proposed"))
        if status not in ("proposed", "approved", "done"):
            status = "proposed"
        backlog.append(ImprovementItem(
            id=str(item.get("id", f"imp_{i}")),
            source=str(item.get("source", "weekly_review")),
            title=str(item.get("title", "")),
            recommended_action=str(item.get("recommended_action", "")),
            status=status,
        ))
    return backlog
