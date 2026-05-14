"""Risk-related scoring bands — deterministic thresholds."""

from __future__ import annotations


def ai_output_qa_band(score: int) -> str:
    """QA score 0–100 → operating band for client-facing outputs."""
    if score >= 90:
        return "client_ready"
    if score >= 80:
        return "review"
    if score >= 70:
        return "revise"
    return "reject"


def autonomy_level_allowed_in_mvp(level: int) -> bool:
    """Dealix MVP: autonomy levels 0–3 only."""
    return 0 <= level <= 3
