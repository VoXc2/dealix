"""Runtime safety repository with explicit failure propagation."""

from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.control_plane_os.repositories import ControlPlaneRepository
from auto_client_acquisition.runtime_safety_os.schemas import (
    CircuitBreakerState,
    KillSwitchState,
)


class RuntimeSafetyRepository:
    def __init__(self, *, breaker_threshold: int = 3) -> None:
        self._breaker_threshold = breaker_threshold
        self._kill_switches: dict[tuple[str, str], KillSwitchState] = {}
        self._breakers: dict[tuple[str, str], CircuitBreakerState] = {}

    def engage_kill_switch(self, *, tenant_id: str, target_id: str, reason: str) -> KillSwitchState:
        state = KillSwitchState(
            tenant_id=tenant_id,
            target_id=target_id,
            is_active=True,
            reason=reason,
            activated_at=datetime.now(UTC),
        )
        self._kill_switches[(tenant_id, target_id)] = state
        return state

    def kill_switch_active(self, *, tenant_id: str, target_id: str) -> bool:
        state = self._kill_switches.get((tenant_id, target_id))
        return bool(state and state.is_active)

    def propagate_kill_switch_to_control_plane(
        self,
        *,
        tenant_id: str,
        target_id: str,
        run_id: str,
        control_plane: ControlPlaneRepository,
        actor: str = "runtime_safety",
    ) -> None:
        if not self.kill_switch_active(tenant_id=tenant_id, target_id=target_id):
            raise ValueError("kill_switch_not_active")
        control_plane.pause_run(tenant_id=tenant_id, run_id=run_id, actor=actor)

    def register_failure(self, *, tenant_id: str, key: str) -> CircuitBreakerState:
        current = self._breakers.get((tenant_id, key))
        failures = 1 if current is None else current.failures + 1
        state = CircuitBreakerState(
            tenant_id=tenant_id,
            key=key,
            failures=failures,
            threshold=self._breaker_threshold,
            is_open=failures >= self._breaker_threshold,
            updated_at=datetime.now(UTC),
        )
        self._breakers[(tenant_id, key)] = state
        return state

    def get_breaker(self, *, tenant_id: str, key: str) -> CircuitBreakerState | None:
        return self._breakers.get((tenant_id, key))

    def clear_for_test(self) -> None:
        self._kill_switches.clear()
        self._breakers.clear()


__all__ = ["RuntimeSafetyRepository"]
