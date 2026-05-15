"""System 26 — Organizational Control Plane core primitives."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class WorkflowControlState:
    """Deterministic control state for one workflow execution."""

    workflow_id: str
    route: str
    policy_version: str
    status: str
    trace_id: str
    checkpoints: tuple[str, ...]
    current_checkpoint_index: int


def create_workflow(
    *, workflow_id: str, route: str, policy_version: str, trace_id: str
) -> WorkflowControlState:
    if not workflow_id.strip():
        raise ValueError("workflow_id_required")
    if not route.strip():
        raise ValueError("route_required")
    if not policy_version.strip():
        raise ValueError("policy_version_required")
    if not trace_id.strip():
        raise ValueError("trace_id_required")
    return WorkflowControlState(
        workflow_id=workflow_id.strip(),
        route=route.strip(),
        policy_version=policy_version.strip(),
        status="running",
        trace_id=trace_id.strip(),
        checkpoints=(),
        current_checkpoint_index=-1,
    )


def append_checkpoint(state: WorkflowControlState, checkpoint_id: str) -> WorkflowControlState:
    checkpoint = checkpoint_id.strip()
    if not checkpoint:
        raise ValueError("checkpoint_id_required")
    checkpoints = (*state.checkpoints, checkpoint)
    return replace(state, checkpoints=checkpoints, current_checkpoint_index=len(checkpoints) - 1)


def observe_workflow(state: WorkflowControlState) -> dict[str, object]:
    current_checkpoint = (
        state.checkpoints[state.current_checkpoint_index]
        if state.current_checkpoint_index >= 0
        else None
    )
    return {
        "workflow_id": state.workflow_id,
        "monitorable": True,
        "stoppable": True,
        "rollbackable": bool(state.checkpoints),
        "traceable": True,
        "policy_mutable": True,
        "reroutable": True,
        "status": state.status,
        "route": state.route,
        "policy_version": state.policy_version,
        "trace_id": state.trace_id,
        "current_checkpoint": current_checkpoint,
    }


def stop_workflow(state: WorkflowControlState) -> WorkflowControlState:
    return replace(state, status="stopped")


def rollback_workflow(state: WorkflowControlState, checkpoint_id: str) -> WorkflowControlState:
    checkpoint = checkpoint_id.strip()
    if checkpoint not in state.checkpoints:
        raise ValueError("checkpoint_not_found")
    return replace(
        state,
        status="rolled_back",
        current_checkpoint_index=state.checkpoints.index(checkpoint),
    )


def reroute_workflow(state: WorkflowControlState, new_route: str) -> WorkflowControlState:
    route = new_route.strip()
    if not route:
        raise ValueError("new_route_required")
    return replace(state, route=route)


def update_workflow_policy(
    state: WorkflowControlState, policy_version: str
) -> WorkflowControlState:
    policy = policy_version.strip()
    if not policy:
        raise ValueError("policy_version_required")
    return replace(state, policy_version=policy)
