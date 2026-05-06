"""Weekly rollup over daily loop outputs."""
from __future__ import annotations

from typing import Any


def build_weekly_learning(last_daily_loops: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize last N daily snapshots — deterministic."""
    best_segment = "unknown"
    if last_daily_loops:
        top = last_daily_loops[-1].get("top_3_targets") or []
        if top:
            best_segment = str(top[0].get("label_ar") or top[0])
    return {
        "schema_version": 1,
        "best_segment_guess": best_segment,
        "experiments_to_review": 1,
        "next_week_focus_ar": "كرّر أفضل مسار دافئ مع موافقة يدوية",
        "action_mode": "suggest_only",
    }
