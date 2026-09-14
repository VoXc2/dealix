"""Minimal telemetry extension: trace/case/effect metadata on existing stack.

No new observability stack. Merges kernel metadata into the redacted
payload of auto_client_acquisition.agent_observability.record_trace.
"""

from __future__ import annotations

from typing import Any


def extend_trace_payload(
    *,
    trace_id: str,
    case_id: str,
    effect_class: str,
    sector: str = "",
    channel: str = "",
    response_state: str = "",
) -> dict[str, Any]:
    return {
        "kernel_trace_id": trace_id,
        "kernel_case_id": case_id,
        "kernel_effect_class": effect_class,
        "kernel_sector": sector,
        "kernel_channel": channel,
        "kernel_response_state": response_state,
    }


def record_kernel_trace(
    *,
    agent_name: str = "customer_ops_kernel",
    action_mode: str = "draft_only",
    trace_id: str,
    case_id: str,
    effect_class: str,
    sector: str = "",
    channel: str = "",
    response_state: str = "",
    guardrail_result: str = "ok",
    approval_status: str = "pending",
) -> Any:
    """Never raises: falls back to a local dict if the canonical stack
    is unavailable in the current runtime (tests, minimal envs)."""
    from datetime import UTC, datetime

    payload = extend_trace_payload(
        trace_id=trace_id,
        case_id=case_id,
        effect_class=effect_class,
        sector=sector,
        channel=channel,
        response_state=response_state,
    )
    try:
        from auto_client_acquisition.agent_observability import record_trace

        return record_trace(
            agent_name=agent_name,
            action_mode=action_mode,  # type: ignore[arg-type]
            workflow="customer_ops_kernel",
            input_kind="customer_ops_event",
            output_kind=response_state,
            guardrail_result=guardrail_result,
            approval_status=approval_status,
            payload=payload,
        )
    except Exception:
        return {
            "trace_id": trace_id,
            "agent_name": agent_name,
            "workflow": "customer_ops_kernel",
            "action_mode": action_mode,
            "redacted_payload": payload,
            "timestamp": datetime.now(UTC).isoformat(),
            "fallback": True,
        }
