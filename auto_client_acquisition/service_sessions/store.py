"""Service session in-memory + JSONL store.

Schema: ServiceSessionRecord from full_ops_contracts.schemas.
Persistence: append-only JSONL at data/service_sessions.jsonl.

This is the Article 11 minimum. When the first paid customer is
signed, swap to Postgres ORM following proof_ledger/postgres_backend.py.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import (
    ServiceSessionRecord,
    ServiceType,
    SessionStatus,
)
from auto_client_acquisition.service_sessions.lifecycle import advance_session

_JSONL_PATH = os.path.join("data", "service_sessions.jsonl")
_INDEX: dict[str, ServiceSessionRecord] = {}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(rec: ServiceSessionRecord) -> None:
    _ensure_dir()
    _INDEX[rec.session_id] = rec
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(rec.model_dump_json() + "\n")


def start_session(
    *,
    customer_handle: str,
    service_type: ServiceType,
    inputs: dict[str, Any] | None = None,
) -> ServiceSessionRecord:
    rec = ServiceSessionRecord(
        session_id=f"sess_{uuid.uuid4().hex[:10]}",
        customer_handle=customer_handle,
        service_type=service_type,
        status="draft",
        inputs=inputs or {},
        next_step={
            "action": "request_approval_to_activate",
            "owner": "founder",
        },
    )
    _persist(rec)
    return rec


def get_session(session_id: str) -> ServiceSessionRecord | None:
    return _INDEX.get(session_id)


def list_sessions(
    *,
    customer_handle: str | None = None,
    status: SessionStatus | None = None,
    limit: int = 50,
) -> list[ServiceSessionRecord]:
    sessions = list(_INDEX.values())
    if customer_handle:
        sessions = [s for s in sessions if s.customer_handle == customer_handle]
    if status:
        sessions = [s for s in sessions if s.status == status]
    return sorted(sessions, key=lambda s: s.started_at, reverse=True)[:limit]


def transition_session(
    *,
    session_id: str,
    target: SessionStatus,
    approval_id: str | None = None,
) -> tuple[ServiceSessionRecord | None, str]:
    """Advance a session through its state machine.

    Returns (record, reason). record is None if transition rejected.
    """
    rec = _INDEX.get(session_id)
    if rec is None:
        return (None, "session_not_found")

    allowed, reason = advance_session(
        current=rec.status,
        target=target,
        approval_id=approval_id,
    )
    if not allowed:
        return (None, reason)

    if approval_id and approval_id not in rec.approval_ids:
        rec.approval_ids.append(approval_id)
    rec.status = target
    if target == "complete":
        rec.completed_at = datetime.now(timezone.utc)

    # Update next_step for clarity
    next_step_map: dict[SessionStatus, dict[str, Any]] = {
        "draft": {"action": "request_approval_to_activate", "owner": "founder"},
        "waiting_for_approval": {"action": "founder_approves", "owner": "founder"},
        "active": {"action": "execute_deliverables", "owner": "csm_or_founder"},
        "delivered": {"action": "build_proof_pack", "owner": "system"},
        "proof_pending": {"action": "request_customer_signoff", "owner": "founder"},
        "complete": {"action": "consider_upsell", "owner": "founder"},
        "blocked": {"action": "founder_review_unblock", "owner": "founder"},
    }
    rec.next_step = next_step_map.get(target)

    _persist(rec)
    return (rec, reason)


def attach_deliverable(
    *,
    session_id: str,
    deliverable: dict[str, Any],
) -> ServiceSessionRecord | None:
    """Attach an artifact (proof_event_id, file uri, link, etc.) to a session."""
    rec = _INDEX.get(session_id)
    if rec is None:
        return None
    rec.deliverables.append(deliverable)
    if "proof_event_id" in deliverable:
        rec.proof_event_ids.append(deliverable["proof_event_id"])
    _persist(rec)
    return rec


def complete_session(*, session_id: str) -> tuple[ServiceSessionRecord | None, str]:
    """Shortcut: advance proof_pending → complete."""
    return transition_session(session_id=session_id, target="complete")
