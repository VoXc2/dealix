"""Autonomy levels — numeric ladder (0 read-only … 4 recommend + approval queue)."""

from __future__ import annotations

from enum import IntEnum


class AutonomyLevel(IntEnum):
    READ_ONLY = 0
    ANALYZE = 1
    DRAFT = 2
    RECOMMEND = 3
    QUEUE_FOR_APPROVAL = 4


__all__ = ["AutonomyLevel"]
