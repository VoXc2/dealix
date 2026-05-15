"""AI Agent control + output QA bands — MVP autonomy cap."""

from __future__ import annotations

MVP_AUTONOMY_LEVEL_MAX = 3
_AUTONOMY_ABSOLUTE_MAX = 6


def agent_autonomy_allowed_in_mvp(level: int) -> bool:
    """Dealix MVP allows autonomy levels 0–3 only."""
    return 0 <= level <= MVP_AUTONOMY_LEVEL_MAX


def agent_autonomy_level_valid(level: int) -> bool:
    return 0 <= level <= _AUTONOMY_ABSOLUTE_MAX


def ai_output_qa_band(score: int) -> str:
    if score >= 90:
        return "client_ready"
    if score >= 80:
        return "review"
    if score >= 70:
        return "revise"
    return "reject"
