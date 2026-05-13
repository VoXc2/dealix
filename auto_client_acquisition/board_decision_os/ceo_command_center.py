"""CEO Command Center — top-five decisions for the week."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorityDecision:
    priority: int      # 1..5
    decision: str      # the decision-type code from board_decision_os
    target: str
    reason: str

    def __post_init__(self) -> None:
        if not 1 <= self.priority <= 5:
            raise ValueError("priority_must_be_1_to_5")


@dataclass(frozen=True)
class CEOCommandCenterTopFive:
    period: str
    decisions: tuple[PriorityDecision, ...]

    def __post_init__(self) -> None:
        if len(self.decisions) != 5:
            raise ValueError("top_five_requires_exactly_five_decisions")
        priorities = sorted(d.priority for d in self.decisions)
        if priorities != [1, 2, 3, 4, 5]:
            raise ValueError("top_five_priorities_must_be_1_through_5")
