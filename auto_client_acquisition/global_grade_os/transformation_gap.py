"""Dealix Transformation Gap (DTG) — per-axis decision matrix.

See ``docs/global_grade/TRANSFORMATION_GAP.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from auto_client_acquisition.global_grade_os.capability_index import (
    DCIAxis,
    DCIMaturity,
)


class Feasibility(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DTGRecommendation(str, Enum):
    SPRINT_NOW = "sprint_now"
    DIAGNOSTIC_FIRST = "diagnostic_first"
    QUICK_WIN = "quick_win"
    DEPRIORITIZE = "deprioritize"


@dataclass(frozen=True)
class DTGEntry:
    axis: DCIAxis
    current: DCIMaturity
    target: DCIMaturity
    feasibility: Feasibility

    def gap(self) -> int:
        return int(self.target) - int(self.current)


def recommend_for_gap(entry: DTGEntry) -> DTGRecommendation:
    """Apply the doctrine decision matrix to a single DTG entry."""

    gap = entry.gap()
    high_gap = gap >= 2
    high_feasibility = entry.feasibility is Feasibility.HIGH

    if high_gap and high_feasibility:
        return DTGRecommendation.SPRINT_NOW
    if high_gap and not high_feasibility:
        return DTGRecommendation.DIAGNOSTIC_FIRST
    if (not high_gap) and high_feasibility:
        return DTGRecommendation.QUICK_WIN
    return DTGRecommendation.DEPRIORITIZE
