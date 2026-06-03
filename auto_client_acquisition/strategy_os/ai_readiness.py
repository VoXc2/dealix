"""Deterministic AI readiness rollup + next commercial sprint hint (no LLM)."""

from __future__ import annotations

from enum import StrEnum
from typing import Any


class RecommendedNextService(StrEnum):
    """Symbolic next step aligned with ``commercial_engagements`` runners."""

    LEAD_INTELLIGENCE_SPRINT = "lead_intelligence_sprint"
    SUPPORT_DESK_SPRINT = "support_desk_sprint"
    QUICK_WIN_OPS = "quick_win_ops"


_DEFAULT_WEIGHTS: dict[str, float] = {
    "data": 0.25,
    "process": 0.25,
    "governance": 0.25,
    "people": 0.125,
    "tech": 0.125,
}


def compute_ai_readiness(
    axes: dict[str, float],
    *,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    ``axes`` values are clamped to 0–1. Weighted average → ``readiness_score``.

    ``recommended_next_service`` prefers fixing the weakest pillar first:
    data/governance → lead intelligence; weak process → quick win ops;
    strong across → support desk sprint as operational polish.
    """
    w = {**_DEFAULT_WEIGHTS, **(weights or {})}
    clamped: dict[str, float] = {}
    acc = 0.0
    denom = 0.0
    for key, wt in w.items():
        if wt <= 0:
            continue
        raw = float(axes.get(key, 0.0))
        v = max(0.0, min(1.0, raw))
        clamped[key] = v
        acc += v * wt
        denom += wt

    readiness_score = round(acc / denom, 4) if denom > 0 else 0.0

    data = clamped.get("data", 1.0)
    gov = clamped.get("governance", 1.0)
    proc = clamped.get("process", 1.0)

    if data < 0.55 or (data <= gov and data <= proc and data < 0.7):
        rec: RecommendedNextService = RecommendedNextService.LEAD_INTELLIGENCE_SPRINT
    elif gov < 0.55:
        rec = RecommendedNextService.LEAD_INTELLIGENCE_SPRINT
    elif proc < 0.55:
        rec = RecommendedNextService.QUICK_WIN_OPS
    elif readiness_score >= 0.72:
        rec = RecommendedNextService.SUPPORT_DESK_SPRINT
    else:
        rec = RecommendedNextService.LEAD_INTELLIGENCE_SPRINT

    return {
        "axes": clamped,
        "readiness_score": readiness_score,
        "recommended_next_service": rec.value,
    }
