"""Enterprise rollout — 7 canonical stages."""

from __future__ import annotations

from enum import IntEnum


class RolloutStage(IntEnum):
    LAND = 1
    PROVE = 2
    ADOPT = 3
    OPERATE = 4
    EXPAND = 5
    STANDARDIZE = 6
    INSTITUTIONALIZE = 7


ROLLOUT_STAGES: tuple[RolloutStage, ...] = tuple(RolloutStage)
