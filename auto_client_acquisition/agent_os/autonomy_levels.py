"""Autonomy levels — numeric ladder (0 read-only … 5 fully autonomous).

Levels L0..L3 cover the original read/analyze/draft/recommend ladder.
L4 adds automated execution under a mandatory audit trail and kill switch.
L5 (fully autonomous, no human gate) is reserved and blocked in the MVP.
"""

from __future__ import annotations

from enum import IntEnum


class AutonomyLevel(IntEnum):
    L0_READ_ONLY = 0
    L1_ANALYZE = 1
    L2_DRAFT = 2
    L3_RECOMMEND = 3
    L4_AUTO_WITH_AUDIT = 4
    L5_FULLY_AUTONOMOUS = 5

    # Legacy names retained as aliases for existing callers.
    READ_ONLY = 0
    ANALYZE = 1
    DRAFT = 2
    RECOMMEND = 3
    QUEUE_FOR_APPROVAL = 4


# Highest autonomy permitted in the MVP — L5 is reserved.
MAX_AUTONOMY_LEVEL_MVP: AutonomyLevel = AutonomyLevel.L4_AUTO_WITH_AUDIT


__all__ = ["MAX_AUTONOMY_LEVEL_MVP", "AutonomyLevel"]
