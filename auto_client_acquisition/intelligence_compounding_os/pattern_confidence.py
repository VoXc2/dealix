"""Pattern Confidence — Low / Medium / High based on occurrence count."""

from __future__ import annotations

from enum import Enum


class PatternConfidence(str, Enum):
    LOW = "low"        # 1..2
    MEDIUM = "medium"  # 3..5
    HIGH = "high"      # 6+


def classify_confidence(occurrences: int) -> PatternConfidence:
    if occurrences <= 0:
        raise ValueError("occurrences_must_be_positive")
    if occurrences <= 2:
        return PatternConfidence.LOW
    if occurrences <= 5:
        return PatternConfidence.MEDIUM
    return PatternConfidence.HIGH
