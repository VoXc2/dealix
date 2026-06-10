"""Agentic operations board — high-level signals to decisions."""

from __future__ import annotations

from auto_client_acquisition.agentic_operations_os.agent_permissions import agent_tool_forbidden


def board_decision_for_tool_request(*, agent_name: str, requested_tool: str) -> tuple[str, str]:
    """Return (decision, rationale) for an agent requesting a tool."""
    if agent_tool_forbidden(requested_tool):
        return (
            "deny_permission_keep_draft_only",
            f"{agent_name}: forbidden tool {requested_tool}; escalate to approval center product signal",
        )
    return ("evaluate_under_governance_runtime", "tool_not_on_forbidden_list")
