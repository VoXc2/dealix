"""Runtime controller — deterministic transitions when risks or kill switch fire."""

from __future__ import annotations

from auto_client_acquisition.secure_agent_runtime_os.agent_states import AgentRuntimeState
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import kill_switch_active
from auto_client_acquisition.secure_agent_runtime_os.risk_memory import recent_risks


def evaluate_runtime_state(agent_id: str, *, forbidden_tool_attempt: bool) -> AgentRuntimeState:
    if kill_switch_active():
        return AgentRuntimeState.KILLED
    if forbidden_tool_attempt:
        return AgentRuntimeState.RESTRICTED
    risks = recent_risks(agent_id)
    if len(risks) >= 5:
        return AgentRuntimeState.ESCALATED
    if risks:
        return AgentRuntimeState.WATCH
    return AgentRuntimeState.SAFE


__all__ = ["evaluate_runtime_state"]
