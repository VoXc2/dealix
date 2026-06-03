"""QA review scoring stub — deterministic rubric hook."""

from __future__ import annotations

from typing import Any


def qa_delivery_score(*, checklist_done: int, checklist_total: int, blockers: int) -> dict[str, Any]:
    if checklist_total <= 0:
        score = 0.0
    else:
        base = 100.0 * (checklist_done / checklist_total)
        score = max(0.0, base - blockers * 15.0)
    return {
        "score": round(score, 1),
        "checklist_done": checklist_done,
        "checklist_total": checklist_total,
        "blockers": blockers,
        "passes_minimum": score >= 85.0,
    }
