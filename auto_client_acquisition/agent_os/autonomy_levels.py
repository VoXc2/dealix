"""Autonomy levels — numeric ladder for governed agents.

L0 read-only … L4 auto-with-audit (internal). L5 fully autonomous is
defined but blocked in the MVP and rejected at card creation.
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


# Highest level permitted in the MVP; L5 is reserved and rejected.
MAX_AUTONOMY_MVP: AutonomyLevel = AutonomyLevel.L4_AUTO_WITH_AUDIT

# Levels that require a named kill-switch owner before a card is valid.
KILL_SWITCH_REQUIRED_FROM: AutonomyLevel = AutonomyLevel.L4_AUTO_WITH_AUDIT


def autonomy_allowed_mvp(level: AutonomyLevel | int) -> bool:
    return int(level) <= int(MAX_AUTONOMY_MVP)


def autonomy_requires_kill_switch(level: AutonomyLevel | int) -> bool:
    return int(level) >= int(KILL_SWITCH_REQUIRED_FROM)


__all__ = [
    "KILL_SWITCH_REQUIRED_FROM",
    "MAX_AUTONOMY_MVP",
    "AutonomyLevel",
    "autonomy_allowed_mvp",
    "autonomy_requires_kill_switch",
]
