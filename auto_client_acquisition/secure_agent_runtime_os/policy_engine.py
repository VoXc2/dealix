"""Runtime policy engine — deterministic allow/deny for tools."""

from __future__ import annotations

from auto_client_acquisition.agent_os.tool_permissions import tool_allowed_mvp
from auto_client_acquisition.secure_agent_runtime_os.agent_states import AgentRuntimeState
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import kill_switch_active


def runtime_policy_allows_tool(
    tool: str,
    *,
    runtime_state: AgentRuntimeState,
) -> tuple[bool, str]:
    if kill_switch_active():
        return False, "kill_switch_active"
    if runtime_state in (AgentRuntimeState.RESTRICTED, AgentRuntimeState.ESCALATED, AgentRuntimeState.PAUSED, AgentRuntimeState.KILLED):
        return False, f"runtime_state:{runtime_state.value}"
    if not tool_allowed_mvp(tool):
        return False, "tool_not_on_mvp_allow_list"
    return True, "allow"


__all__ = ["runtime_policy_allows_tool"]
