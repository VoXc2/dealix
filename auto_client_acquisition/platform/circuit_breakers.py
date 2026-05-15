"""Simple circuit breaker state machine."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CircuitState(StrEnum):
    CLOSED = 'closed'
    OPEN = 'open'
    HALF_OPEN = 'half_open'


@dataclass(slots=True)
class CircuitBreaker:
    name: str
    failure_threshold: int = 5
    recovery_timeout_seconds: int = 30
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_epoch: int = 0

    def record_success(self) -> None:
        self.state = CircuitState.CLOSED
        self.failure_count = 0

    def record_failure(self, *, now_epoch: int) -> None:
        self.failure_count += 1
        self.last_failure_epoch = now_epoch
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def allow_request(self, *, now_epoch: int) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if now_epoch - self.last_failure_epoch >= self.recovery_timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True


__all__ = ['CircuitBreaker', 'CircuitState']
