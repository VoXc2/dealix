"""Autonomy levels — numeric ladder (0 read-only … 5 fully autonomous).

L0-L4 are governed and permitted in the MVP. L5 (fully autonomous, no
audit gate) is blocked under MVP doctrine and must be rejected on card
creation.
"""

from __future__ import annotations

from enum import IntEnum


class AutonomyLevel(IntEnum):
    READ_ONLY = 0
    ANALYZE = 1
    DRAFT = 2
    RECOMMEND = 3
    QUEUE_FOR_APPROVAL = 4
    # Named ladder rungs (aliases at the same numeric positions plus L5).
    L0_READ_ONLY = 0
    L1_ANALYZE = 1
    L2_DRAFT = 2
    L3_RECOMMEND = 3
    L4_AUTO_WITH_AUDIT = 4
    L5_FULLY_AUTONOMOUS = 5


# L4 and above require a named kill-switch owner.
_REQUIRES_KILL_SWITCH_OWNER = AutonomyLevel.L4_AUTO_WITH_AUDIT

# L5 is not permitted in the MVP.
_MVP_MAX_AUTONOMY = AutonomyLevel.L4_AUTO_WITH_AUDIT


def requires_kill_switch_owner(level: AutonomyLevel) -> bool:
    return int(level) >= int(_REQUIRES_KILL_SWITCH_OWNER)


def autonomy_allowed_in_mvp(level: AutonomyLevel) -> bool:
    return int(level) <= int(_MVP_MAX_AUTONOMY)


__all__ = [
    "AutonomyLevel",
    "autonomy_allowed_in_mvp",
    "requires_kill_switch_owner",
]
