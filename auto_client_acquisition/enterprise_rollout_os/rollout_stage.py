"""Enterprise rollout stages — Land through Institutionalize."""

from __future__ import annotations

ROLLOUT_STAGES: tuple[str, ...] = (
    "land",
    "prove",
    "adopt",
    "operate",
    "expand",
    "standardize",
    "institutionalize",
)


def rollout_stage_index(stage: str) -> int | None:
    try:
        return ROLLOUT_STAGES.index(stage)
    except ValueError:
        return None


def rollout_next_stage(current: str) -> str | None:
    idx = rollout_stage_index(current)
    if idx is None or idx + 1 >= len(ROLLOUT_STAGES):
        return None
    return ROLLOUT_STAGES[idx + 1]
