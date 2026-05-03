"""
Service Session — state machine for executing one purchased service.

States (forward-only with explicit transitions):
    new
      → waiting_inputs       (intake form sent; waiting on customer)
      → in_progress          (Dealix is doing the work)
      → needs_approval       (drafts/policy items waiting on customer approval)
      → ready_to_deliver     (all approvals collected; deliverables built)
      → delivered            (PDF/links shared with the customer)
      → proof_generated      (Proof Pack assembled in the ledger)
      → upgrade_pending      (waiting on customer's upgrade decision)
      → closed               (terminal — keep for audit only)

Each transition records who triggered it + when. SLA breach is computed by
sla_tracker.py against the contract's sla_hours.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition.service_tower.contracts import get_contract
from db.models import ServiceSessionRecord


# Canonical transitions. The validator in `transition()` enforces these.
_ALLOWED: dict[str, set[str]] = {
    "new":              {"waiting_inputs", "in_progress", "closed"},
    "waiting_inputs":   {"in_progress", "closed"},
    "in_progress":      {"needs_approval", "ready_to_deliver", "closed"},
    "needs_approval":   {"in_progress", "ready_to_deliver", "closed"},
    "ready_to_deliver": {"delivered", "closed"},
    "delivered":        {"proof_generated", "closed"},
    "proof_generated":  {"upgrade_pending", "closed"},
    "upgrade_pending":  {"closed"},
    "closed":           set(),
}

TERMINAL_STATES: tuple[str, ...] = ("closed",)
DELIVERED_STATES: tuple[str, ...] = ("delivered", "proof_generated", "upgrade_pending", "closed")


def _new_id() -> str:
    return f"svc_{uuid.uuid4().hex[:14]}"


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC for TIMESTAMP cols


async def open_session(
    session: AsyncSession,
    *,
    service_id: str,
    customer_id: str | None = None,
    partner_id: str | None = None,
    owner: str | None = None,
    inputs: dict[str, Any] | None = None,
) -> ServiceSessionRecord:
    """Create a new ServiceSession in state 'new'."""
    contract = get_contract(service_id)
    if contract is None:
        raise ValueError(f"unknown service_id: {service_id}")
    sla = int(contract.sla_hours or 168)
    deadline = _now() + timedelta(hours=sla)
    row = ServiceSessionRecord(
        id=_new_id(),
        service_id=service_id,
        customer_id=customer_id,
        partner_id=partner_id,
        status="new",
        owner=owner,
        deadline_at=deadline,
        sla_target_hours=sla,
        next_step="capture_inputs",
        inputs_json=dict(inputs or {}),
        deliverables_json=[],
    )
    session.add(row)
    return row


async def transition(
    session: AsyncSession,
    *,
    session_id: str,
    to_status: str,
    actor: str = "system",
    next_step: str | None = None,
    deliverables: list[dict[str, Any]] | None = None,
    proof_pack_url: str | None = None,
) -> ServiceSessionRecord:
    """Move a session to a new state. Raises ValueError if illegal."""
    row = (await session.execute(
        select(ServiceSessionRecord).where(ServiceSessionRecord.id == session_id)
    )).scalar_one_or_none()
    if row is None:
        raise ValueError(f"session_not_found: {session_id}")
    allowed = _ALLOWED.get(row.status, set())
    if to_status not in allowed:
        raise ValueError(
            f"illegal_transition from {row.status!r} to {to_status!r}; "
            f"allowed: {sorted(allowed) or 'none (terminal)'}"
        )
    row.status = to_status
    if next_step is not None:
        row.next_step = next_step
    if deliverables is not None:
        row.deliverables_json = list(deliverables)
    if proof_pack_url is not None:
        row.proof_pack_url = proof_pack_url
    if to_status == "delivered":
        row.delivered_at = _now()
    if to_status == "closed":
        row.closed_at = _now()
    # Append actor history
    meta = dict(row.meta_json or {})
    history = list(meta.get("transition_history") or [])
    history.append({
        "to": to_status,
        "actor": actor,
        "at": _now().isoformat(),
    })
    meta["transition_history"] = history
    row.meta_json = meta
    return row


async def get(session: AsyncSession, session_id: str) -> ServiceSessionRecord | None:
    return (await session.execute(
        select(ServiceSessionRecord).where(ServiceSessionRecord.id == session_id)
    )).scalar_one_or_none()


async def list_for_customer(
    session: AsyncSession,
    customer_id: str,
) -> list[ServiceSessionRecord]:
    q = (
        select(ServiceSessionRecord)
        .where(ServiceSessionRecord.customer_id == customer_id)
        .order_by(ServiceSessionRecord.started_at.desc())
    )
    return list((await session.execute(q)).scalars().all())


def allowed_transitions(current_status: str) -> list[str]:
    return sorted(_ALLOWED.get(current_status, set()))
