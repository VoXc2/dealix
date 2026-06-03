"""Dealix Transformation Gap (DTG) — target vs current capability; sprint routing."""

from __future__ import annotations

from enum import StrEnum


class SprintOpportunity(StrEnum):
    """Heuristic routing from gap × feasibility (each 0–100)."""

    BEST_SPRINT = "best_sprint_opportunity"  # high gap + high feasibility
    DIAGNOSTIC_FIRST = "diagnostic_first"
    QUICK_WIN = "quick_win"
    DEPRIORITIZE = "deprioritize"


def transformation_gap(current_capability: float, target_capability: float) -> float:
    """DTG on same 0–100 scale as capabilities."""
    return max(0.0, float(target_capability) - float(current_capability))


def classify_sprint_opportunity(*, gap: float, feasibility: float) -> SprintOpportunity:
    """
    gap / feasibility are 0–100.
    High gap + high feasibility → best sprint; high gap + low feasibility → diagnostic; etc.
    """
    high_g = gap >= 55
    low_g = gap < 35
    high_f = feasibility >= 60
    low_f = feasibility < 45

    if high_g and high_f:
        return SprintOpportunity.BEST_SPRINT
    if high_g and low_f:
        return SprintOpportunity.DIAGNOSTIC_FIRST
    if low_g and high_f:
        return SprintOpportunity.QUICK_WIN
    return SprintOpportunity.DEPRIORITIZE
