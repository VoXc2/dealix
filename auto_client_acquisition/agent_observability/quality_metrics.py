"""
Quality Metrics — compute the KPIs the user listed (Quality bucket).

  draft_acceptance_rate
  unsafe_suggestion_rate
  override_rate
  hallucination_reports
  complaint_rate

Inputs are proof events + objection events + support tickets +
unsafe_action records. Pure function.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


def compute(
    *,
    proof_events,
    objection_events,
    tickets,
    unsafe_actions,
) -> dict[str, Any]:
    proof_events = list(proof_events or [])
    objection_events = list(objection_events or [])
    tickets = list(tickets or [])
    unsafe_actions = list(unsafe_actions or [])

    by_unit: Counter[str] = Counter()
    for e in proof_events:
        by_unit[e.unit_type] += 1

    drafts_total   = by_unit.get("draft_created", 0)
    drafts_approved = by_unit.get("approval_collected", 0)

    objections_total = len(objection_events)
    objections_lost  = sum(1 for o in objection_events if o.outcome == "lost")

    complaint_tickets = sum(
        1 for t in tickets
        if (t.priority in ("P0", "P1")) or (t.category in ("billing_dispute", "privacy", "angry"))
    )

    high_severity_blocked = sum(1 for u in unsafe_actions if u.severity == "high")

    return {
        "draft_acceptance_rate": _safe_div(drafts_approved, drafts_total),
        "unsafe_suggestion_rate": _safe_div(high_severity_blocked, max(drafts_total, len(proof_events))),
        "override_rate":          _safe_div(objections_lost, objections_total),
        "hallucination_reports":  high_severity_blocked,
        "complaint_rate":         _safe_div(complaint_tickets, max(len(tickets), 1)),
        "samples": {
            "drafts_total":      drafts_total,
            "drafts_approved":   drafts_approved,
            "objections_total":  objections_total,
            "tickets_total":     len(tickets),
            "unsafe_blocked":    len(unsafe_actions),
        },
    }


def _safe_div(num: int, den: int) -> float:
    if den <= 0:
        return 0.0
    return round(num / den, 4)
