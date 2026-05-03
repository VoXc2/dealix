"""
Proof Ledger — append-only log of Revenue Work Units (proof events).

The ledger is the source of truth for "what Dealix actually did this week".
Every Pilot, Growth OS sprint, or Data-to-Revenue session emits proof events
into this ledger; the Proof Pack Builder summarizes them into the weekly PDF.

This module is the WRITE side. Reading + summarization lives in
proof_pack_builder.py.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition.revenue_company_os.revenue_work_units import (
    base_revenue_impact,
    is_valid_unit,
    label_for,
    weight_for,
)
from db.models import ProofEventRecord

log = logging.getLogger(__name__)


def _new_id() -> str:
    return f"prf_{uuid.uuid4().hex[:14]}"


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC for TIMESTAMP cols


async def record(
    session: AsyncSession,
    *,
    unit_type: str,
    customer_id: str | None = None,
    partner_id: str | None = None,
    service_id: str | None = None,
    session_id: str | None = None,
    revenue_impact_sar: float | None = None,
    actor: str = "system",
    approval_required: bool = False,
    approved: bool = False,
    risk_level: str = "low",
    label_ar: str | None = None,
    meta: dict[str, Any] | None = None,
) -> ProofEventRecord:
    """Append a single proof event. Validates unit_type. Returns the row.

    Caller is responsible for committing the session — the ledger does not
    commit so it can be batched with the producing transaction.
    """
    if not is_valid_unit(unit_type):
        raise ValueError(f"unknown unit_type: {unit_type!r}")
    if risk_level not in ("low", "medium", "high"):
        raise ValueError(f"risk_level must be low/medium/high, got {risk_level!r}")

    row = ProofEventRecord(
        id=_new_id(),
        customer_id=customer_id,
        partner_id=partner_id,
        service_id=service_id,
        session_id=session_id,
        unit_type=unit_type,
        label_ar=label_ar or label_for(unit_type),
        revenue_impact_sar=(
            float(revenue_impact_sar)
            if revenue_impact_sar is not None
            else base_revenue_impact(unit_type)
        ),
        weight=weight_for(unit_type),
        actor=actor,
        approval_required=approval_required,
        approved=approved,
        risk_level=risk_level,
        occurred_at=_now(),
        meta_json=dict(meta or {}),
    )
    session.add(row)
    return row


async def record_batch(
    session: AsyncSession,
    items: list[dict[str, Any]],
) -> list[ProofEventRecord]:
    """Convenience: emit many events in one transaction."""
    rows: list[ProofEventRecord] = []
    for item in items:
        rows.append(await record(session, **item))
    return rows


async def fetch_for_customer(
    session: AsyncSession,
    customer_id: str,
    *,
    since: datetime | None = None,
    limit: int = 500,
) -> list[ProofEventRecord]:
    q = select(ProofEventRecord).where(ProofEventRecord.customer_id == customer_id)
    if since:
        q = q.where(ProofEventRecord.occurred_at >= since)
    q = q.order_by(ProofEventRecord.occurred_at.desc()).limit(limit)
    return list((await session.execute(q)).scalars().all())


async def fetch_for_partner(
    session: AsyncSession,
    partner_id: str,
    *,
    since: datetime | None = None,
    limit: int = 1000,
) -> list[ProofEventRecord]:
    q = select(ProofEventRecord).where(ProofEventRecord.partner_id == partner_id)
    if since:
        q = q.where(ProofEventRecord.occurred_at >= since)
    q = q.order_by(ProofEventRecord.occurred_at.desc()).limit(limit)
    return list((await session.execute(q)).scalars().all())


async def fetch_for_session(
    session: AsyncSession,
    service_session_id: str,
) -> list[ProofEventRecord]:
    q = (
        select(ProofEventRecord)
        .where(ProofEventRecord.session_id == service_session_id)
        .order_by(ProofEventRecord.occurred_at.asc())
    )
    return list((await session.execute(q)).scalars().all())
