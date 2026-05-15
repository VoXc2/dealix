"""Kill switch — global runtime flag plus per-agent kill.

``activate_kill_switch()`` with no arguments trips the in-process global
flag (legacy runtime supervision). Called with ``agent_id`` and ``reason``
it kills a single registered agent and returns a structured result.
"""

from __future__ import annotations

from typing import Any

_KILLED: bool = False


def kill_switch_active() -> bool:
    return _KILLED


def reset_kill_switch_for_tests() -> None:
    global _KILLED
    _KILLED = False


def activate_kill_switch(
    *,
    agent_id: str | None = None,
    reason: str = "",
) -> dict[str, Any]:
    """Trip the kill switch.

    With no ``agent_id`` the global runtime flag is set. With an
    ``agent_id`` the named agent is moved to ``killed`` in the registry.
    """
    global _KILLED

    if agent_id is None:
        _KILLED = True
        return {"activated": True, "scope": "global", "reason": reason}

    if not reason.strip():
        return {
            "activated": False,
            "reason_code": "reason_required",
            "agent_id": agent_id,
        }

    from auto_client_acquisition.agent_os.agent_registry import get_agent, kill_agent

    if get_agent(agent_id) is None:
        return {
            "activated": False,
            "reason_code": "agent_not_found",
            "agent_id": agent_id,
        }

    updated = kill_agent(agent_id, reason=reason)
    if updated is None:
        return {
            "activated": False,
            "reason_code": "agent_not_found",
            "agent_id": agent_id,
        }
    return {
        "activated": True,
        "scope": "agent",
        "agent_id": agent_id,
        "status": updated.status,
        "reason": reason,
    }


__all__ = ["activate_kill_switch", "kill_switch_active", "reset_kill_switch_for_tests"]
