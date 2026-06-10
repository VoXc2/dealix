"""Transformation gap (DTG) — feasibility table for next move."""

from __future__ import annotations

from typing import Literal

TransformationDecision = Literal[
    "sprint_now",
    "diagnostic_first",
    "quick_win",
    "deprioritize",
]


def transformation_decision(*, gap_high: bool, feasibility_high: bool) -> TransformationDecision:
    if gap_high and feasibility_high:
        return "sprint_now"
    if gap_high and not feasibility_high:
        return "diagnostic_first"
    if not gap_high and feasibility_high:
        return "quick_win"
    return "deprioritize"
