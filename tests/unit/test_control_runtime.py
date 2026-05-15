"""Control runtime kernel tests."""

from __future__ import annotations

from auto_client_acquisition.observability_v10 import _reset_v10_buffer, list_v10_traces
from auto_client_acquisition.orchestrator.control_runtime import (
    build_control_envelope,
    emit_control_trace,
)
from auto_client_acquisition.orchestrator.policies import AutonomyMode, default_policy


def test_control_runtime_allow_for_safe_action() -> None:
    policy = default_policy("c1")
    policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
    policy.require_human_for_first_send = False

    env = build_control_envelope(
        actor_id="system",
        customer_id="c1",
        workflow_id="wf_1",
        step_id="step_send",
        agent_id="outreach",
        action_type="send_message",
        policy=policy,
        risk_factors={"is_first_send_to_account": False, "deal_value_sar": 5000},
    )
    assert env.decision == "allow"
    assert env.approval_required is False
    assert env.permission_ok is True


def test_control_runtime_requires_approval_when_policy_demands() -> None:
    policy = default_policy("c1")
    policy.autonomy_mode = AutonomyMode.DRAFT_APPROVE

    env = build_control_envelope(
        actor_id="system",
        customer_id="c1",
        workflow_id="wf_1",
        step_id="step_send",
        agent_id="outreach",
        action_type="send_message",
        policy=policy,
        risk_factors={},
    )
    assert env.decision == "require_approval"
    assert env.approval_required is True
    assert env.approval_reason is not None


def test_control_runtime_blocks_unknown_action_type() -> None:
    policy = default_policy("c1")
    env = build_control_envelope(
        actor_id="system",
        customer_id="c1",
        workflow_id="wf_1",
        step_id="step_unknown",
        agent_id="ops",
        action_type="totally_unknown_action",
        policy=policy,
        risk_factors={},
    )
    assert env.decision == "block"
    assert env.permission_ok is False


def test_emit_control_trace_records_observability_trace() -> None:
    _reset_v10_buffer()
    policy = default_policy("c1")
    env = build_control_envelope(
        actor_id="system",
        customer_id="c1",
        workflow_id="wf_1",
        step_id="step_send",
        agent_id="outreach",
        action_type="send_message",
        policy=policy,
        risk_factors={},
    )
    emit_control_trace(
        env,
        correlation_id="cor_kernel_1",
        stage="requested",
        approval_status="pending",
    )
    rows = list_v10_traces(limit=10)
    assert len(rows) == 1
    assert rows[0].correlation_id == "cor_kernel_1"
    assert rows[0].redacted_payload.get("stage") == "requested"
