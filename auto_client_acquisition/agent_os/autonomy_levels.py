"""Autonomy ladder for governed agents (L0 read-only … L5 fully autonomous).

L5 is defined but blocked in the MVP — no agent may run fully autonomous.
L4+ requires a named kill-switch owner. Doctrine: no AI agent without owner,
scope, and audit.
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


DEFAULT_AUTONOMY: AutonomyLevel = AutonomyLevel.L2_DRAFT


def coerce_autonomy(value: int | AutonomyLevel) -> AutonomyLevel:
    """Normalise an int or AutonomyLevel into an AutonomyLevel.

    Raises ValueError when the value is outside the L0–L5 ladder.
    """
    try:
        return AutonomyLevel(int(value))
    except (ValueError, TypeError) as exc:
        msg = f"autonomy_level out of range (expected 0-5): {value!r}"
        raise ValueError(msg) from exc


def autonomy_blocked_in_mvp(level: int | AutonomyLevel) -> bool:
    """L5 (fully autonomous) is not permitted in the MVP."""
    return coerce_autonomy(level) >= AutonomyLevel.L5_FULLY_AUTONOMOUS


def requires_kill_switch_owner(level: int | AutonomyLevel) -> bool:
    """L4 and above must name a human kill-switch owner."""
    return coerce_autonomy(level) >= AutonomyLevel.L4_AUTO_WITH_AUDIT


__all__ = [
    "DEFAULT_AUTONOMY",
    "AutonomyLevel",
    "autonomy_blocked_in_mvp",
    "coerce_autonomy",
    "requires_kill_switch_owner",
]
