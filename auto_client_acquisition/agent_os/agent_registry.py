"""Agent registry — JSONL store of AgentCards.

Path: $DEALIX_AGENT_REGISTRY_PATH (default var/agent-registry.jsonl).
Mirrors the friction_log / value_ledger / capital_ledger pattern.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus

_DEFAULT_PATH = "var/agent-registry.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AGENT_REGISTRY_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _read_all() -> list[dict[str, Any]]:
    path = _path()
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
    return out


def _rewrite(rows: list[dict[str, Any]]) -> None:
    path = _path()
    _ensure_dir(path)
    with _lock:
        path.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""),
            encoding="utf-8",
        )


def register_agent(card: AgentCard) -> AgentCard:
    """Register a new agent. Refuses if agent_id already exists (idempotency
    by caller — call update_status to change state)."""
    if not card.agent_id:
        raise ValueError("agent_id is required")
    rows = _read_all()
    if any(r.get("agent_id") == card.agent_id for r in rows):
        raise ValueError(f"agent_id {card.agent_id!r} already registered")
    card.last_updated_at = datetime.now(timezone.utc).isoformat()
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(card.to_dict(), ensure_ascii=False) + "\n")
    return card


def get_agent(agent_id: str) -> AgentCard | None:
    for r in _read_all():
        if r.get("agent_id") == agent_id:
            return AgentCard(**r)
    return None


def list_agents(*, status: str | None = None, owner: str | None = None) -> list[AgentCard]:
    out: list[AgentCard] = []
    for r in _read_all():
        if status and r.get("status") != status:
            continue
        if owner and r.get("owner") != owner:
            continue
        out.append(AgentCard(**r))
    return out


def update_status(agent_id: str, new_status: str | AgentStatus) -> AgentCard | None:
    """Transition an agent's status. Returns updated card or None if not found."""
    new_status_value = (
        new_status.value if isinstance(new_status, AgentStatus) else str(new_status)
    )
    rows = _read_all()
    updated: AgentCard | None = None
    for r in rows:
        if r.get("agent_id") == agent_id:
            r["status"] = new_status_value
            r["last_updated_at"] = datetime.now(timezone.utc).isoformat()
            updated = AgentCard(**r)
            break
    if updated:
        _rewrite(rows)
    return updated


def kill_agent(agent_id: str, reason: str) -> AgentCard | None:
    """Activate kill switch. Sets status to KILLED + records reason in notes."""
    if not reason:
        raise ValueError("reason is required for kill_agent")
    rows = _read_all()
    updated: AgentCard | None = None
    for r in rows:
        if r.get("agent_id") == agent_id:
            r["status"] = AgentStatus.KILLED.value
            r["last_updated_at"] = datetime.now(timezone.utc).isoformat()
            r["notes"] = (
                (r.get("notes", "") or "")
                + f"\n[killed at {r['last_updated_at']}] {reason}"
            ).strip()
            updated = AgentCard(**r)
            break
    if updated:
        _rewrite(rows)

        # Emit friction + audit events.
        try:
            from auto_client_acquisition.friction_log.store import emit as emit_friction
            emit_friction(
                customer_id="dealix_internal",
                kind="manual_override",
                severity="high",
                workflow_id=f"agent:{agent_id}",
                notes=f"kill_switch_activated:{reason[:120]}",
            )
        except Exception:  # noqa: BLE001
            pass
        try:
            from auto_client_acquisition.auditability_os.audit_event import (
                AuditEventKind,
                record_event,
            )
            record_event(
                customer_id="dealix_internal",
                kind=AuditEventKind.INCIDENT,
                actor=updated.kill_switch_owner or updated.owner,
                summary=f"agent {agent_id} killed: {reason[:200]}",
            )
        except Exception:  # noqa: BLE001
            pass
    return updated


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "clear_for_test",
    "get_agent",
    "kill_agent",
    "list_agents",
    "register_agent",
    "update_status",
]
