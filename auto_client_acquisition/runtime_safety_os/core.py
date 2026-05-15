"""System 31 — the Enterprise Safety Engine.

Runtime operational safety: circuit breakers, kill switches, execution limits
and policy boundaries. Any agent or workflow can be halted instantly.

Every transition asserts its preconditions and raises `SafetyError` loudly on
an invalid operation — a kill switch must never silently fail to engage
(`no_silent_failures`). Engaging a kill switch propagates: it isolates the
target agent in the mesh and pauses the target run in the control plane.
"""

from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.agent_mesh_os.core import get_agent_mesh
from auto_client_acquisition.control_plane_os.core import get_control_plane
from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit
from auto_client_acquisition.control_plane_os.schemas import RunState
from auto_client_acquisition.runtime_safety_os.schemas import (
    CircuitBreaker,
    CircuitState,
    ExecutionLimit,
    KillSwitch,
    SafetyVerdict,
)

_MODULE = "runtime_safety_os"


class SafetyError(RuntimeError):
    """Raised on an invalid safety operation — never swallowed."""


class SafetyEngine:
    """Circuit breakers, kill switches and execution limits for the control plane."""

    def __init__(self) -> None:
        self._breakers: dict[str, CircuitBreaker] = {}
        self._kill_switches: dict[str, KillSwitch] = {}
        self._limits: dict[str, ExecutionLimit] = {}

    # ── checks ───────────────────────────────────────────────────
    def check(self, *, target: str, action_type: str = "") -> SafetyVerdict:
        """Decide whether a target may act, given breakers + kill switches."""
        if not target.strip():
            raise SafetyError("safety check requires a non-empty target")
        barriers: list[str] = []
        if self._active_kill_switch(target) is not None:
            barriers.append("kill_switch")
        breaker = self._breakers.get(target)
        if breaker is not None and breaker.state == CircuitState.OPEN:
            barriers.append("circuit_open")
        allowed = not barriers
        return SafetyVerdict(
            target=target,
            allowed=allowed,
            barriers_hit=barriers,
            reason="clear" if allowed else f"blocked by: {', '.join(barriers)}",
        )

    # ── circuit breakers ─────────────────────────────────────────
    def record_failure(self, target: str, *, threshold: int = 3) -> CircuitBreaker:
        """Record a failure for a target; trip the breaker at the threshold."""
        if not target.strip():
            raise SafetyError("record_failure requires a non-empty target")
        breaker = self._breakers.get(target)
        if breaker is None:
            breaker = CircuitBreaker(target=target, threshold=threshold)
            self._breakers[target] = breaker
        breaker.failure_count += 1
        if (
            breaker.failure_count >= breaker.threshold
            and breaker.state != CircuitState.OPEN
        ):
            breaker.state = CircuitState.OPEN
            breaker.opened_at = datetime.now(UTC)
            emit(
                event_type=ControlEventType.CIRCUIT_OPENED,
                source_module=_MODULE,
                subject_type="circuit_breaker",
                subject_id=target,
                decision="deny",
                payload={"failure_count": breaker.failure_count},
            )
        return breaker

    def reset_breaker(self, target: str) -> CircuitBreaker:
        breaker = self._breakers.get(target)
        if breaker is None:
            raise SafetyError(f"no circuit breaker for target: {target}")
        breaker.state = CircuitState.CLOSED
        breaker.failure_count = 0
        breaker.opened_at = None
        emit(
            event_type=ControlEventType.CIRCUIT_CLOSED,
            source_module=_MODULE,
            subject_type="circuit_breaker",
            subject_id=target,
        )
        return breaker

    def list_breakers(self) -> list[CircuitBreaker]:
        return list(self._breakers.values())

    # ── kill switches ────────────────────────────────────────────
    def engage_kill_switch(
        self, *, target: str, actor: str = "system", reason: str = ""
    ) -> KillSwitch:
        """Engage an emergency stop. Raises if the target is empty.

        Propagates: isolates the target agent in the mesh and pauses the
        target run in the control plane.
        """
        if not target.strip():
            raise SafetyError("kill switch requires a non-empty target")
        switch = KillSwitch(target=target, engaged_by=actor, reason=reason)
        self._kill_switches[switch.switch_id] = switch
        emit(
            event_type=ControlEventType.KILL_SWITCH_ENGAGED,
            source_module=_MODULE,
            actor=actor,
            subject_type="kill_switch",
            subject_id=target,
            decision="deny",
            payload={"reason": reason, "switch_id": switch.switch_id},
        )
        self._propagate_stop(target, actor)
        return switch

    def release_kill_switch(
        self, switch_id: str, *, actor: str = "system"
    ) -> KillSwitch:
        """Release an engaged kill switch. Raises if unknown or already released."""
        switch = self._kill_switches.get(switch_id)
        if switch is None:
            raise SafetyError(f"kill switch not found: {switch_id}")
        if not switch.engaged:
            raise SafetyError(f"kill switch {switch_id} is already released")
        switch.engaged = False
        switch.released_at = datetime.now(UTC)
        emit(
            event_type=ControlEventType.KILL_SWITCH_RELEASED,
            source_module=_MODULE,
            actor=actor,
            subject_type="kill_switch",
            subject_id=switch.target,
            payload={"switch_id": switch_id},
        )
        return switch

    def list_kill_switches(self, *, engaged_only: bool = False) -> list[KillSwitch]:
        switches = list(self._kill_switches.values())
        if engaged_only:
            switches = [s for s in switches if s.engaged]
        return switches

    # ── execution limits ─────────────────────────────────────────
    def set_execution_limit(self, limit: ExecutionLimit) -> ExecutionLimit:
        self._limits[limit.target] = limit
        emit(
            event_type=ControlEventType.EXECUTION_LIMIT_SET,
            source_module=_MODULE,
            subject_type="execution_limit",
            subject_id=limit.target,
            payload={
                "max_actions_per_hour": limit.max_actions_per_hour,
                "max_concurrency": limit.max_concurrency,
            },
        )
        return limit

    def get_execution_limit(self, target: str) -> ExecutionLimit | None:
        return self._limits.get(target)

    def status(self, target: str) -> dict[str, object]:
        verdict = self.check(target=target)
        return {
            "verdict": verdict.model_dump(mode="json"),
            "breaker": (
                self._breakers[target].model_dump(mode="json")
                if target in self._breakers
                else None
            ),
            "execution_limit": (
                self._limits[target].model_dump(mode="json")
                if target in self._limits
                else None
            ),
            "active_kill_switches": [
                s.switch_id
                for s in self._kill_switches.values()
                if s.engaged and s.target == target
            ],
        }

    # ── internals ────────────────────────────────────────────────
    def _active_kill_switch(self, target: str) -> KillSwitch | None:
        for switch in self._kill_switches.values():
            if switch.engaged and switch.target == target:
                return switch
        return None

    def _propagate_stop(self, target: str, actor: str) -> None:
        mesh = get_agent_mesh()
        if mesh.get_agent(target) is not None:
            mesh.isolate_agent(target, actor=actor, reason="kill switch engaged")
        control_plane = get_control_plane()
        run = control_plane.get_run(target)
        if run is not None and run.state in (
            RunState.RUNNING.value,
            RunState.REGISTERED.value,
        ):
            control_plane.pause(target, actor=actor)


_ENGINE: SafetyEngine | None = None


def get_safety_engine() -> SafetyEngine:
    """Return the process-scoped safety engine singleton."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SafetyEngine()
    return _ENGINE


def reset_safety_engine() -> None:
    """Test helper: drop the cached engine."""
    global _ENGINE
    _ENGINE = None


__all__ = [
    "SafetyEngine",
    "SafetyError",
    "get_safety_engine",
    "reset_safety_engine",
]
