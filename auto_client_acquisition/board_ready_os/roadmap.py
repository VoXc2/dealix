"""Board-ready roadmap — six engine phases."""

from __future__ import annotations

BOARD_ROADMAP_PHASES: tuple[str, ...] = (
    "proof_engine",
    "retainer_engine",
    "productization_engine",
    "enterprise_trust_engine",
    "distribution_engine",
    "holding_engine",
)

_PHASE_MILESTONE_COUNTS: tuple[int, ...] = (6, 5, 5, 6, 5, 5)


def board_roadmap_phase_name(phase_index_1_based: int) -> str:
    if not 1 <= phase_index_1_based <= len(BOARD_ROADMAP_PHASES):
        msg = f"phase_index_1_based must be 1..{len(BOARD_ROADMAP_PHASES)}"
        raise ValueError(msg)
    return BOARD_ROADMAP_PHASES[phase_index_1_based - 1]


def board_roadmap_milestone_count(phase_index_1_based: int) -> int:
    if not 1 <= phase_index_1_based <= len(_PHASE_MILESTONE_COUNTS):
        msg = f"phase_index_1_based must be 1..{len(_PHASE_MILESTONE_COUNTS)}"
        raise ValueError(msg)
    return _PHASE_MILESTONE_COUNTS[phase_index_1_based - 1]
