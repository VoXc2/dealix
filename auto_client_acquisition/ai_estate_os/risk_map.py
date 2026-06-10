"""Risk map scoring for AI estate."""

from __future__ import annotations


def estate_risk_band(score: int) -> str:
    if score >= 70:
        return "critical_review"
    if score >= 40:
        return "elevated"
    return "managed"


__all__ = ["estate_risk_band"]
