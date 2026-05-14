"""Kill switch — revokes an agent's tools immediately + sets KILLED state.

Effects:
  1. agent_registry.kill_agent(agent_id, reason) → status=KILLED
  2. friction_log emits a high-severity event (already wired in kill_agent)
  3. auditability_os records an INCIDENT event (already wired in kill_agent)

This module is the canonical entry point for runtime supervisors / dashboards.
"""
from __future__ import annotations

from typing import Any


def activate_kill_switch(*, agent_id: str, reason: str) -> dict[str, Any]:
    """Activate the kill switch. Returns a result dict suitable for an
    API response."""
    if not agent_id:
        return {"activated": False, "reason_code": "missing_agent_id"}
    if not reason or not reason.strip():
        return {"activated": False, "reason_code": "missing_reason"}

    from auto_client_acquisition.agent_os.agent_registry import kill_agent

    card = kill_agent(agent_id, reason)
    if card is None:
        return {
            "activated": False,
            "reason_code": "agent_not_found",
            "agent_id": agent_id,
        }
    return {
        "activated": True,
        "agent_id": agent_id,
        "status": card.status,
        "killed_at": card.last_updated_at,
        "kill_switch_owner": card.kill_switch_owner,
        "governance_decision": "block",
    }


__all__ = ["activate_kill_switch"]
