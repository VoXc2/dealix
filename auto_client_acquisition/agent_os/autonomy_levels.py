"""Agent autonomy levels — L0 through L5.

MVP default: L1 (Draft-Assisted). L4+ requires explicit per-session
founder approval. L5 (Fully Autonomous) is banned in MVP.
"""
from __future__ import annotations

from enum import IntEnum


class AutonomyLevel(IntEnum):
    L0_HUMAN_ONLY = 0
    L1_DRAFT_ASSISTED = 1
    L2_REVIEW_REQUIRED = 2
    L3_CONDITIONAL_AUTO = 3
    L4_AUTO_WITH_AUDIT = 4
    L5_FULLY_AUTONOMOUS = 5


MVP_MAX_AUTONOMY = AutonomyLevel.L3_CONDITIONAL_AUTO
MVP_BANNED_LEVELS = frozenset({AutonomyLevel.L5_FULLY_AUTONOMOUS})


def requires_per_session_approval(level: AutonomyLevel | int) -> bool:
    """L4+ always requires explicit founder approval per session."""
    return int(level) >= int(AutonomyLevel.L4_AUTO_WITH_AUDIT)


def is_mvp_allowed(level: AutonomyLevel | int) -> bool:
    return int(level) <= int(MVP_MAX_AUTONOMY) and int(level) not in {int(l) for l in MVP_BANNED_LEVELS}


__all__ = [
    "AutonomyLevel",
    "MVP_BANNED_LEVELS",
    "MVP_MAX_AUTONOMY",
    "is_mvp_allowed",
    "requires_per_session_approval",
]
