"""Kill switch — global runtime flag plus per-agent kill via the registry.

``activate_kill_switch()`` with no arguments trips the in-process global
flag (legacy behaviour). Called with an ``agent_id`` it kills that agent
in the agent registry and returns a structured result dict.
"""

from __future__ import annotations

from typing import Any

_KILLED: bool = False


def kill_switch_active() -> bool:
    return _KILLED


def activate_kill_switch(
    *,
    agent_id: str | None = None,
    reason: str = "",
) -> dict[str, Any] | None:
    """Activate the kill switch.

    With no ``agent_id`` the global runtime flag is set and ``None`` is
    returned. With an ``agent_id`` the named agent is killed in the
    registry and a result dict is returned.
    """
    global _KILLED
    if agent_id is None:
        _KILLED = True
        return None

    from auto_client_acquisition.agent_os import kill_agent

    if not (reason and reason.strip()):
        return {
            "activated": False,
            "reason_code": "reason_required",
            "agent_id": agent_id,
        }
    killed = kill_agent(agent_id, reason=reason)
    if killed is None:
        return {
            "activated": False,
            "reason_code": "agent_not_found",
            "agent_id": agent_id,
        }
    return {
        "activated": True,
        "agent_id": agent_id,
        "status": killed.status,
        "reason": killed.killed_reason,
    }


def reset_kill_switch_for_tests() -> None:
    global _KILLED
    _KILLED = False


__all__ = ["activate_kill_switch", "kill_switch_active", "reset_kill_switch_for_tests"]
