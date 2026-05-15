"""Tenant-scoped agent isolation — the runtime-safety kill path.

The global ``kill_switch`` is process-wide; this module adds the
granular control the enterprise plane needs: isolating a *single*
agent within a *single* tenant, and — crucially — pausing the
workflow run that agent was driving so a killed agent cannot leave a
run live. Isolation is recorded as evidence for the run trace.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

_LOCK = threading.Lock()
# (tenant_id, agent_id) -> isolation record
_ISOLATED: dict[tuple[str, str], dict[str, Any]] = {}


def is_agent_isolated(tenant_id: str, agent_id: str) -> bool:
    """Has this agent been isolated within this tenant?"""
    with _LOCK:
        return (tenant_id, agent_id) in _ISOLATED


def isolate_agent(
    *,
    tenant_id: str,
    agent_id: str,
    reason: str,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Isolate an agent and pause its run (if any).

    Returns a result dict: ``isolated`` is always True on success;
    ``run_paused`` is True when an associated run was paused.
    """
    if not tenant_id.strip() or not agent_id.strip():
        raise ValueError("tenant_id and agent_id are required to isolate an agent")
    if not reason.strip():
        raise ValueError("isolation requires a reason")

    record = {
        "tenant_id": tenant_id,
        "agent_id": agent_id,
        "reason": reason,
        "run_id": run_id or "",
        "isolated_at": datetime.now(UTC).isoformat(),
    }
    with _LOCK:
        _ISOLATED[(tenant_id, agent_id)] = record

    run_paused = False
    if run_id:
        from auto_client_acquisition.institutional_control_os.run_registry import (
            RunRegistryError,
            pause_run,
        )

        try:
            pause_run(run_id, tenant_id=tenant_id, reason=f"agent_isolated:{agent_id}")
            run_paused = True
        except RunRegistryError:
            run_paused = False

    # Record the isolation as evidence on the run trace.
    try:
        from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
            EvidenceType,
        )
        from auto_client_acquisition.evidence_control_plane_os.evidence_store import record

        record(
            tenant_id=tenant_id,
            evidence_type=EvidenceType.RISK.value,
            client_id=tenant_id,
            summary=f"Agent {agent_id} isolated: {reason}",
            actor_type="runtime_safety",
            actor_id=agent_id,
            run_id=run_id or "",
        )
    except Exception:  # evidence is best-effort, never blocks isolation
        pass

    return {
        "isolated": True,
        "tenant_id": tenant_id,
        "agent_id": agent_id,
        "run_id": run_id or "",
        "run_paused": run_paused,
        "reason": reason,
    }


def release_agent(tenant_id: str, agent_id: str) -> bool:
    """Lift isolation for an agent. Returns True if it was isolated."""
    with _LOCK:
        return _ISOLATED.pop((tenant_id, agent_id), None) is not None


def list_isolated(tenant_id: str | None = None) -> list[dict[str, Any]]:
    """Isolation records, optionally scoped to one tenant."""
    with _LOCK:
        rows = list(_ISOLATED.values())
    if tenant_id is not None:
        rows = [r for r in rows if r["tenant_id"] == tenant_id]
    return rows


def clear_isolation_for_tests() -> None:
    with _LOCK:
        _ISOLATED.clear()


__all__ = [
    "clear_isolation_for_tests",
    "is_agent_isolated",
    "isolate_agent",
    "list_isolated",
    "release_agent",
]
