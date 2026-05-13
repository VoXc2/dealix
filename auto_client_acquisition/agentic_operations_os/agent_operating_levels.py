"""Agent Operating Levels — 0..7."""

from __future__ import annotations

from enum import IntEnum


class AgentOperatingLevel(IntEnum):
    L0_NO_AGENT = 0
    L1_ASSISTANT = 1
    L2_DRAFTING = 2
    L3_RECOMMENDATION = 3
    L4_APPROVAL_QUEUE = 4
    L5_INTERNAL_EXECUTION = 5
    L6_EXTERNAL_ACTION = 6
    L7_AUTONOMOUS_EXTERNAL = 7


AGENT_OPERATING_LEVELS: tuple[AgentOperatingLevel, ...] = tuple(AgentOperatingLevel)


def is_mvp_allowed(level: AgentOperatingLevel) -> bool:
    """MVP allows levels 1..4. Level 7 is forbidden constitutionally."""

    if level is AgentOperatingLevel.L7_AUTONOMOUS_EXTERNAL:
        return False
    return AgentOperatingLevel.L1_ASSISTANT <= level <= AgentOperatingLevel.L4_APPROVAL_QUEUE
