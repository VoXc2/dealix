"""Runtime governance fabric: policy + approval + reversibility + audit."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.accountability import AuditRecord, record_audit_event
from auto_client_acquisition.platform.approval_engine import create_approval_request
from auto_client_acquisition.platform.policy_engine import (
    ActionRisk,
    PolicyDecision,
    evaluate_policy,
)
from auto_client_acquisition.platform.reversibility import (
    ReversibleExecution,
    register_reversible_execution,
)


@dataclass(frozen=True, slots=True)
class RuntimeActionRequest:
    action_id: str
    action_name: str
    actor: str
    is_external: bool
    risk: ActionRisk
    permissions: tuple[str, ...]
    requires_data_access: bool
    now_epoch: int
    trace_id: str = ''
    rollback_steps: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RuntimeActionResult:
    decision: PolicyDecision
    reasons: tuple[str, ...]
    approval_request_id: str
    audit_event_id: str
    reversible_registered: bool


def govern_action(request: RuntimeActionRequest) -> RuntimeActionResult:
    evaluation = evaluate_policy(
        action_name=request.action_name,
        is_external=request.is_external,
        risk=request.risk,
        permissions=request.permissions,
        requires_data_access=request.requires_data_access,
    )

    approval_request_id = ''
    if evaluation.decision == PolicyDecision.APPROVAL_REQUIRED:
        approval_request_id = f'approval:{request.action_id}'
        create_approval_request(
            request_id=approval_request_id,
            action_name=request.action_name,
            requester=request.actor,
            now_epoch=request.now_epoch,
        )

    reversible_registered = False
    if evaluation.decision == PolicyDecision.ALLOW and request.rollback_steps:
        register_reversible_execution(
            ReversibleExecution(
                action_id=request.action_id,
                rollback_steps=request.rollback_steps,
                executed_at_epoch=request.now_epoch,
            )
        )
        reversible_registered = True

    audit_event_id = f'audit:{request.action_id}'
    record_audit_event(
        AuditRecord(
            event_id=audit_event_id,
            action_name=request.action_name,
            decision=evaluation.decision.value,
            actor=request.actor,
            reasons=evaluation.reasons,
            timestamp_epoch=request.now_epoch,
            trace_id=request.trace_id,
        )
    )

    return RuntimeActionResult(
        decision=evaluation.decision,
        reasons=evaluation.reasons,
        approval_request_id=approval_request_id,
        audit_event_id=audit_event_id,
        reversible_registered=reversible_registered,
    )


__all__ = ['RuntimeActionRequest', 'RuntimeActionResult', 'govern_action']
