"""Institutional Control Plane primitives (System 56)."""

from __future__ import annotations

from dataclasses import dataclass

RUNTIME_OPERATIONS: tuple[str, ...] = (
    "stop",
    "reroute",
    "rollback",
    "policy_patch",
    "trace",
)


@dataclass(frozen=True, slots=True)
class WorkflowControlState:
    workflow_id: str
    policy_version: str
    trace_id: str
    can_stop: bool
    can_reroute: bool
    can_rollback: bool
    can_policy_patch: bool
    checkpoint_id: str


def control_plane_ready(state: WorkflowControlState) -> tuple[bool, tuple[str, ...]]:
    """Control plane is ready only when all runtime levers exist."""
    blockers: list[str] = []
    if not state.workflow_id.strip():
        blockers.append("workflow_id_missing")
    if not state.policy_version.strip():
        blockers.append("policy_version_missing")
    if not state.trace_id.strip():
        blockers.append("trace_id_missing")
    if not state.can_stop:
        blockers.append("stop_not_available")
    if not state.can_reroute:
        blockers.append("reroute_not_available")
    if not state.can_policy_patch:
        blockers.append("policy_patch_not_available")
    if not state.can_rollback:
        blockers.append("rollback_not_available")
    if state.can_rollback and not state.checkpoint_id.strip():
        blockers.append("rollback_checkpoint_missing")
    return len(blockers) == 0, tuple(blockers)


def runtime_operation_allowed(state: WorkflowControlState, operation: str) -> bool:
    """Check if an operation is allowed for the workflow runtime."""
    op = operation.strip().lower()
    if op == "stop":
        return state.can_stop
    if op == "reroute":
        return state.can_reroute
    if op == "rollback":
        return state.can_rollback and bool(state.checkpoint_id.strip())
    if op == "policy_patch":
        return state.can_policy_patch
    if op == "trace":
        return bool(state.trace_id.strip())
    return False
