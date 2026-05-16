"""Organizational learning loop."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningCycle:
    cycle_id: str
    lessons: tuple[str, ...]
    adopted_actions: tuple[str, ...]


def run_org_learning_cycle(
    *, cycle_id: str, recommendations: tuple[str, ...], optimization_actions: tuple[str, ...]
) -> LearningCycle:
    lessons = tuple(f'lesson_from:{item}' for item in recommendations)
    return LearningCycle(cycle_id=cycle_id, lessons=lessons, adopted_actions=optimization_actions)


__all__ = ['LearningCycle', 'run_org_learning_cycle']
