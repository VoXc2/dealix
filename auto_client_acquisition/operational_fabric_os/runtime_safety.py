"""System 31 — Runtime safety controls."""

from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class RuntimeSafetyPolicy:
    failure_threshold: int = 3
    execution_limit: int = 500
    high_risk_actions: frozenset[str] = field(
        default_factory=lambda: frozenset({"send_external_message", "delete_data"})
    )

    def __post_init__(self) -> None:
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold_invalid")
        if self.execution_limit < 1:
            raise ValueError("execution_limit_invalid")


@dataclass(frozen=True)
class RuntimeSafetyState:
    kill_switch_active: bool = False
    circuit_open: bool = False
    consecutive_failures: int = 0
    execution_count: int = 0
    isolated_agents: frozenset[str] = field(default_factory=frozenset)


def activate_kill_switch(state: RuntimeSafetyState) -> RuntimeSafetyState:
    return replace(state, kill_switch_active=True)


def isolate_agent(state: RuntimeSafetyState, agent_id: str) -> RuntimeSafetyState:
    agent = agent_id.strip()
    if not agent:
        raise ValueError("agent_id_required")
    return replace(state, isolated_agents=state.isolated_agents | {agent})


def rollback_permitted(_state: RuntimeSafetyState) -> bool:
    return True


def register_execution(
    state: RuntimeSafetyState,
    policy: RuntimeSafetyPolicy,
    *,
    action_name: str,
    success: bool,
    agent_id: str,
    requested_risk: str = "low",
) -> tuple[RuntimeSafetyState, bool, str]:
    action = action_name.strip()
    agent = agent_id.strip()
    risk = requested_risk.strip().lower()
    if not action:
        raise ValueError("action_name_required")
    if not agent:
        raise ValueError("agent_id_required")

    if state.kill_switch_active:
        return state, False, "kill_switch_active"
    if state.circuit_open:
        return state, False, "circuit_breaker_open"
    if agent in state.isolated_agents:
        return state, False, "agent_isolated"
    if state.execution_count >= policy.execution_limit:
        return state, False, "execution_limit_reached"
    if action in policy.high_risk_actions and risk == "high":
        return state, False, "high_risk_action_blocked"

    next_count = state.execution_count + 1
    next_failures = state.consecutive_failures + (0 if success else 1)
    next_circuit = next_failures >= policy.failure_threshold
    if success:
        next_failures = 0
    return (
        replace(
            state,
            execution_count=next_count,
            consecutive_failures=next_failures,
            circuit_open=next_circuit,
        ),
        True,
        "allowed",
    )
