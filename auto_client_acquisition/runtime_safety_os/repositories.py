"""Runtime safety repository (kill switch + circuit breaker)."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from auto_client_acquisition.agent_mesh_os.repositories import InMemoryAgentMeshRepository
from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.runtime_safety_os.schemas import CircuitBreakerState, KillSwitchState


class InMemoryRuntimeSafetyRepository:
    def __init__(self) -> None:
        self._kill_switches: dict[tuple[str, str], KillSwitchState] = {}
        self._breakers: dict[tuple[str, str], CircuitBreakerState] = {}

    def engage_kill_switch(
        self,
        *,
        tenant_id: str,
        agent_id: str,
        actor: str,
        reason: str,
        agent_repo: InMemoryAgentMeshRepository | None = None,
        control_repo: InMemoryControlPlaneRepository | None = None,
        run_id: str = "",
    ) -> KillSwitchState:
        state = KillSwitchState(
            tenant_id=tenant_id,
            agent_id=agent_id,
            enabled=True,
            reason=reason,
            activated_by=actor,
        )
        self._kill_switches[(tenant_id, agent_id)] = state
        if agent_repo is not None:
            try:
                agent_repo.isolate_agent(tenant_id=tenant_id, agent_id=agent_id)
            except ValueError:
                pass
        if control_repo is not None and run_id:
            control_repo.pause_run(
                tenant_id=tenant_id,
                run_id=run_id,
                actor=actor,
                reason=f"kill_switch:{reason}",
            )
        return state

    def get_kill_switch(self, *, tenant_id: str, agent_id: str) -> KillSwitchState | None:
        return self._kill_switches.get((tenant_id, agent_id))

    def record_failure(
        self,
        *,
        tenant_id: str,
        breaker_key: str,
        threshold: int = 3,
    ) -> CircuitBreakerState:
        key = (tenant_id, breaker_key)
        existing = self._breakers.get(key)
        if existing is None:
            existing = CircuitBreakerState(tenant_id=tenant_id, breaker_key=breaker_key, threshold=threshold)
        failure_count = existing.failure_count + 1
        status = "open" if failure_count >= threshold else "closed"
        updated = replace(
            existing,
            failure_count=failure_count,
            threshold=threshold,
            status=status,
            updated_at=datetime.now(UTC).isoformat(),
        )
        self._breakers[key] = updated
        return updated

    def is_circuit_open(self, *, tenant_id: str, breaker_key: str) -> bool:
        state = self._breakers.get((tenant_id, breaker_key))
        return bool(state and state.status == "open")
