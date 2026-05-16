"""Agent registration, versioning, and rollback contracts."""

from __future__ import annotations

from dataclasses import dataclass, replace

from auto_client_acquisition.platform.agent_lifecycle import AgentLifecycleState


@dataclass(frozen=True, slots=True)
class AgentRegistration:
    agent_id: str
    version: str
    owner: str
    permissions: tuple[str, ...]
    memory_scope: str
    lifecycle: AgentLifecycleState
    observable: bool
    rollbackable: bool


_AGENTS: dict[str, AgentRegistration] = {}
_AGENT_HISTORY: dict[str, list[AgentRegistration]] = {}


def _version_tuple(version: str) -> tuple[int, int, int]:
    parts = version.split('.')
    if len(parts) != 3:
        raise ValueError('version_must_be_semver')
    return tuple(int(p) for p in parts)  # type: ignore[return-value]


def register_agent(agent: AgentRegistration, *, allow_replace: bool = False) -> None:
    if not agent.agent_id.strip() or not agent.owner.strip() or not agent.memory_scope.strip():
        raise ValueError('invalid_agent_registration')
    existing = _AGENTS.get(agent.agent_id)
    if existing is not None and not allow_replace:
        raise ValueError('agent_already_registered')
    if existing is not None and _version_tuple(agent.version) <= _version_tuple(existing.version):
        raise ValueError('version_must_increase')
    _AGENTS[agent.agent_id] = agent
    _AGENT_HISTORY.setdefault(agent.agent_id, []).append(agent)


def get_agent(agent_id: str) -> AgentRegistration | None:
    return _AGENTS.get(agent_id)


def list_agents() -> tuple[AgentRegistration, ...]:
    return tuple(_AGENTS.values())


def suspend_agent(agent_id: str) -> None:
    agent = _AGENTS.get(agent_id)
    if agent is None:
        raise KeyError('agent_not_found')
    _AGENTS[agent_id] = replace(agent, lifecycle=AgentLifecycleState.SUSPENDED)
    _AGENT_HISTORY.setdefault(agent_id, []).append(_AGENTS[agent_id])


def rollback_agent(agent_id: str, version: str) -> AgentRegistration:
    history = _AGENT_HISTORY.get(agent_id, [])
    for candidate in reversed(history):
        if candidate.version == version:
            _AGENTS[agent_id] = candidate
            _AGENT_HISTORY[agent_id].append(candidate)
            return candidate
    raise ValueError('rollback_version_not_found')


def clear_agent_registry_for_tests() -> None:
    _AGENTS.clear()
    _AGENT_HISTORY.clear()


__all__ = [
    'AgentRegistration',
    'clear_agent_registry_for_tests',
    'get_agent',
    'list_agents',
    'register_agent',
    'rollback_agent',
    'suspend_agent',
]
