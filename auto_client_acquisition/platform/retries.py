"""Retry policy primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPlan:
    max_attempts: int
    backoff_seconds: tuple[int, ...]


def build_retry_plan(*, max_attempts: int, base_delay: int = 1, factor: int = 2, cap: int = 60) -> RetryPlan:
    delays: list[int] = []
    delay = base_delay
    for _ in range(max_attempts):
        delays.append(min(delay, cap))
        delay *= factor
    return RetryPlan(max_attempts=max_attempts, backoff_seconds=tuple(delays))


def should_retry(*, attempt: int, max_attempts: int, error_code: str, retryable_errors: tuple[str, ...]) -> bool:
    if attempt >= max_attempts:
        return False
    return error_code in retryable_errors


__all__ = ['RetryPlan', 'build_retry_plan', 'should_retry']
