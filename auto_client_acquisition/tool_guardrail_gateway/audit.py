"""Audit — every gate decision recorded via radar_events."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call


def audit_decision(
    *,
    tool_name: str,
    decision: dict[str, Any],
    customer_handle: str | None = None,
) -> None:
    """Record a guardrail decision into radar_events. Never raises."""
    def fn():
        from auto_client_acquisition.radar_events import record_event
        event_type = "unsafe_action_blocked" if not decision.get("passed", True) else "approval_requested"
        record_event(
            event_type=event_type,
            customer_handle=customer_handle,
            payload={
                "tool_name": tool_name,
                "passed": decision.get("passed"),
                "reasons": decision.get("reasons", []),
                "severity": decision.get("severity", "info"),
            },
        )
    safe_call(name="audit_decision", fn=fn, fallback=None)
