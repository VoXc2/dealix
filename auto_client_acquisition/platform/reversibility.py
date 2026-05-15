"""Reversible execution registry."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class ReversibleExecution:
    action_id: str
    rollback_steps: tuple[str, ...]
    executed_at_epoch: int
    rolled_back: bool = False


_EXECUTIONS: dict[str, ReversibleExecution] = {}


def register_reversible_execution(execution: ReversibleExecution) -> None:
    _EXECUTIONS[execution.action_id] = execution


def rollback_execution(action_id: str) -> tuple[bool, tuple[str, ...]]:
    execution = _EXECUTIONS.get(action_id)
    if execution is None:
        return False, ('execution_not_found',)
    if execution.rolled_back:
        return True, execution.rollback_steps
    _EXECUTIONS[action_id] = replace(execution, rolled_back=True)
    return True, execution.rollback_steps


def clear_executions_for_tests() -> None:
    _EXECUTIONS.clear()


__all__ = [
    'ReversibleExecution',
    'clear_executions_for_tests',
    'register_reversible_execution',
    'rollback_execution',
]
