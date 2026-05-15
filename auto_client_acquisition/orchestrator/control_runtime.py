"""Unified control runtime envelope for orchestrator actions.

This module gives one deterministic decision surface for:
identity -> permissions -> policy/risk -> approval mode -> observability trace.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.observability_v10 import record_v10_trace
from auto_client_acquisition.orchestrator.policies import ACTION_TYPES, Policy, requires_approval


@dataclass(frozen=True, slots=True)
class ControlRuntimeEnvelope:
    actor_id: str
    customer_id: str
    workflow_id: str
    step_id: str
    agent_id: str
    action_type: str
    decision: str
    approval_required: bool
    approval_reason: str | None
    risk_level: str
    risk_score: float
    permission_ok: bool
    identity_ok: bool


def _risk_score_from_factors(risk_factors: dict[str, Any]) -> float:
    score = 0.0
    if risk_factors.get("is_first_send_to_account"):
        score += 0.2
    if risk_factors.get("contains_legal_topic"):
        score += 0.3
    if float(risk_factors.get("deal_value_sar", 0) or 0) >= 100_000:
        score += 0.4
    followup = int(risk_factors.get("consecutive_followup_index", 0) or 0)
    if followup >= 3:
        score += 0.2
    return max(0.0, min(1.0, round(score, 3)))


def _risk_level(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.3:
        return "medium"
    return "low"


def build_control_envelope(
    *,
    actor_id: str,
    customer_id: str,
    workflow_id: str,
    step_id: str,
    agent_id: str,
    action_type: str,
    policy: Policy,
    risk_factors: dict[str, Any],
) -> ControlRuntimeEnvelope:
    """Compute one governance envelope for the proposed action."""
    identity_ok = bool(str(actor_id or "").strip())
    permission_ok = action_type in ACTION_TYPES
    risk_score = _risk_score_from_factors(risk_factors)
    risk_level = _risk_level(risk_score)

    approval_required, approval_reason = requires_approval(
        action_type=action_type,
        policy=policy,
        risk_factors=risk_factors,
    )

    if not identity_ok or not permission_ok or not str(customer_id or "").strip():
        decision = "block"
    elif approval_required:
        decision = "require_approval"
    else:
        decision = "allow"

    return ControlRuntimeEnvelope(
        actor_id=actor_id or "system",
        customer_id=customer_id,
        workflow_id=workflow_id,
        step_id=step_id,
        agent_id=agent_id,
        action_type=action_type,
        decision=decision,
        approval_required=approval_required,
        approval_reason=approval_reason,
        risk_level=risk_level,
        risk_score=risk_score,
        permission_ok=permission_ok,
        identity_ok=identity_ok,
    )


def emit_control_trace(
    envelope: ControlRuntimeEnvelope,
    *,
    correlation_id: str,
    stage: str,
    approval_status: str,
    extra_payload: dict[str, Any] | None = None,
) -> None:
    """Emit one observability-v10 trace for governance/runtime visibility."""
    payload = {
        "stage": stage,
        "action_type": envelope.action_type,
        "decision": envelope.decision,
        "approval_reason": envelope.approval_reason or "",
        "permission_ok": envelope.permission_ok,
        "identity_ok": envelope.identity_ok,
    }
    if extra_payload:
        payload.update(extra_payload)
    record_v10_trace(
        {
            "correlation_id": correlation_id,
            "customer_id": envelope.customer_id,
            "agent_id": envelope.agent_id,
            "workflow_id": envelope.workflow_id,
            "action_mode": envelope.decision,
            "approval_status": approval_status,
            "risk_level": envelope.risk_level,
            "model_name": "orchestrator_control_runtime_v1",
            "prompt_version": "kernel_v1",
            "input_tokens": 0,
            "output_tokens": 0,
            "estimated_cost_usd": 0.0,
            "latency_ms": 0.0,
            "risk_score": envelope.risk_score,
            "proof_event_id": "",
            "redacted_payload": payload,
        },
    )


__all__ = ["ControlRuntimeEnvelope", "build_control_envelope", "emit_control_trace"]
