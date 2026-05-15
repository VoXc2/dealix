"""Global kill switch flag (in-process; callers persist externally for production)."""

from __future__ import annotations

from typing import Any

_KILLED: bool = False


def kill_switch_active() -> bool:
    return _KILLED


def activate_kill_switch(
    *,
    agent_id: str | None = None,
    reason: str = "",
) -> dict[str, Any]:
    """Activate the in-process kill switch.

    When ``agent_id`` is supplied the named agent is also transitioned to the
    KILLED status in the agent registry. Returns a result record describing the
    outcome. Calling with no arguments only raises the global flag.
    """
    global _KILLED
    _KILLED = True

    if agent_id is None:
        return {"activated": True, "reason_code": "global_kill_switch"}

    from auto_client_acquisition.agent_os import get_agent, kill_agent

    if not reason.strip():
        raise ValueError("reason is required to activate the kill switch for an agent")

    if get_agent(agent_id) is None:
        return {
            "activated": False,
            "reason_code": "agent_not_found",
            "agent_id": agent_id,
        }

    killed = kill_agent(agent_id, reason=reason)
    return {
        "activated": True,
        "reason_code": "agent_killed",
        "agent_id": agent_id,
        "status": killed.status if killed is not None else None,
        "reason": reason,
    }


def reset_kill_switch_for_tests() -> None:
    global _KILLED
    _KILLED = False


__all__ = ["activate_kill_switch", "kill_switch_active", "reset_kill_switch_for_tests"]
