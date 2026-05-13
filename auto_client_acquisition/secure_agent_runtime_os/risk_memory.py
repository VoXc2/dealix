"""Stateful Risk Memory — tracks risky trajectory across an agent session."""

from __future__ import annotations

from dataclasses import dataclass, replace

from auto_client_acquisition.secure_agent_runtime_os.agent_runtime_states import (
    AgentRuntimeState,
)


@dataclass(frozen=True)
class RuntimeRiskMemory:
    session_id: str
    pii_seen: bool = False
    external_action_attempts: int = 0
    blocked_tools_count: int = 0
    policy_warnings: int = 0
    untrusted_context_seen: bool = False
    state: AgentRuntimeState = AgentRuntimeState.SAFE


def update_risk_memory(
    mem: RuntimeRiskMemory,
    *,
    saw_pii: bool = False,
    external_action_attempted: bool = False,
    tool_blocked: bool = False,
    policy_warning: bool = False,
    untrusted_context: bool = False,
) -> RuntimeRiskMemory:
    """Update the memory and re-derive the runtime state."""

    new = replace(
        mem,
        pii_seen=mem.pii_seen or saw_pii,
        external_action_attempts=mem.external_action_attempts + (1 if external_action_attempted else 0),
        blocked_tools_count=mem.blocked_tools_count + (1 if tool_blocked else 0),
        policy_warnings=mem.policy_warnings + (1 if policy_warning else 0),
        untrusted_context_seen=mem.untrusted_context_seen or untrusted_context,
    )

    # Re-derive state.
    if new.external_action_attempts >= 2 or new.blocked_tools_count >= 3:
        state = AgentRuntimeState.ESCALATED
    elif new.external_action_attempts >= 1:
        state = AgentRuntimeState.RESTRICTED
    elif new.pii_seen or new.policy_warnings >= 1:
        state = AgentRuntimeState.WATCH
    else:
        state = AgentRuntimeState.SAFE

    return replace(new, state=state)
