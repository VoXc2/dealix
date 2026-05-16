"""Recovery strategy selector for workflow failures."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.compensation_logic import (
    CompensationAction,
    build_compensation_plan,
)
from auto_client_acquisition.platform.retries import RetryPlan, build_retry_plan


@dataclass(frozen=True, slots=True)
class RecoveryOutcome:
    recovered: bool
    strategy: str
    retry_plan: RetryPlan
    compensation_steps: tuple[str, ...]


def execute_recovery(
    *,
    failure_code: str,
    retryable_errors: tuple[str, ...],
    executed_actions: tuple[CompensationAction, ...],
) -> RecoveryOutcome:
    retry_plan = build_retry_plan(max_attempts=3)
    if failure_code in retryable_errors:
        return RecoveryOutcome(
            recovered=True,
            strategy='retry',
            retry_plan=retry_plan,
            compensation_steps=(),
        )
    compensation = build_compensation_plan(executed_actions)
    return RecoveryOutcome(
        recovered=False,
        strategy='compensate',
        retry_plan=retry_plan,
        compensation_steps=compensation,
    )


__all__ = ['RecoveryOutcome', 'execute_recovery']
