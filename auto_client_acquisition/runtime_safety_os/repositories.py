"""Runtime safety controls: kill switch, sandbox, and canary state."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id

if TYPE_CHECKING:
    from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class SandboxRun:
    sandbox_id: str
    tenant_id: str
    run_id: str
    status: str = "active"
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class CanaryRollout:
    rollout_id: str
    tenant_id: str
    target_agent_id: str
    status: str = "planned"
    blast_radius_pct: float = 0.0
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class KillSwitchState:
    tenant_id: str
    agent_id: str
    isolated: bool
    reason: str
    triggered_by: str
    triggered_at: datetime = field(default_factory=_now)


class InMemoryRuntimeSafetyRepository:
    def __init__(self) -> None:
        self._kill_switches: dict[tuple[str, str], KillSwitchState] = {}

    def activate_kill_switch(
        self,
        *,
        tenant_id: str | None,
        agent_id: str,
        reason: str,
        triggered_by: str,
    ) -> KillSwitchState:
        tid = resolve_tenant_id(tenant_id)
        state = KillSwitchState(
            tenant_id=tid,
            agent_id=agent_id,
            isolated=True,
            reason=reason,
            triggered_by=triggered_by,
        )
        self._kill_switches[(tid, agent_id)] = state
        return state

    def is_agent_isolated(self, *, tenant_id: str | None, agent_id: str) -> bool:
        tid = resolve_tenant_id(tenant_id)
        state = self._kill_switches.get((tid, agent_id))
        return bool(state and state.isolated)

    def isolate_agent_and_pause_run(
        self,
        *,
        tenant_id: str | None,
        agent_id: str,
        run_id: str,
        reason: str,
        triggered_by: str,
        control_plane: "InMemoryControlPlaneRepository",
    ) -> KillSwitchState:
        tid = resolve_tenant_id(tenant_id)
        state = self.activate_kill_switch(
            tenant_id=tid,
            agent_id=agent_id,
            reason=reason,
            triggered_by=triggered_by,
        )
        control_plane.pause_run(tenant_id=tid, run_id=run_id, actor=triggered_by, reason=reason)
        control_plane.append_event(
            tenant_id=tid,
            event_type="runtime_safety.kill_switch.activated",
            source_module="runtime_safety",
            actor=triggered_by,
            subject_type="agent",
            subject_id=agent_id,
            run_id=run_id,
            decision="isolated",
            payload={"reason": reason},
        )
        return replace(state)


__all__ = [
    "CanaryRollout",
    "InMemoryRuntimeSafetyRepository",
    "KillSwitchState",
    "SandboxRun",
]
