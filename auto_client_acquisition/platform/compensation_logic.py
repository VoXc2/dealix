"""Compensation plan generation for reversible execution."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompensationAction:
    action_id: str
    undo_action: str
    reversible: bool = True


def build_compensation_plan(executed_actions: tuple[CompensationAction, ...]) -> tuple[str, ...]:
    plan: list[str] = []
    for action in reversed(executed_actions):
        plan.append(action.undo_action if action.reversible else 'manual_intervention_required')
    return tuple(plan)


def compensation_coverage(executed_actions: tuple[CompensationAction, ...]) -> float:
    if not executed_actions:
        return 1.0
    reversible = sum(1 for action in executed_actions if action.reversible)
    return round(reversible / len(executed_actions), 4)


__all__ = ['CompensationAction', 'build_compensation_plan', 'compensation_coverage']
