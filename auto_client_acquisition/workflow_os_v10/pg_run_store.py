"""Durable Postgres backend for workflow runs.

Async-only — used by the API / orchestration layer so a run survives a
process restart and can be resumed. The in-process sync state machine keeps
using the in-memory store (see ``run_store``); this backend is a write-through
mirror plus a way to rehydrate runs after a restart.

A run round-trips losslessly through ``save_checkpoint`` / ``restore_checkpoint``
— the ``checkpoint`` JSONB column holds the full serialized run.
"""

from __future__ import annotations

from sqlalchemy import select

from auto_client_acquisition.workflow_os_v10.checkpoint import (
    restore_checkpoint,
    save_checkpoint,
)
from auto_client_acquisition.workflow_os_v10.schemas import WorkflowRun
from core.utils import utcnow
from db.models_workflow_runs import WorkflowRunRecord
from db.session import get_session


async def save_run(run: WorkflowRun) -> None:
    """Upsert a run into the workflow_runs table (write-through)."""
    checkpoint = save_checkpoint(run)
    async with get_session() as session:
        record = await session.get(WorkflowRunRecord, run.run_id)
        if record is None:
            record = WorkflowRunRecord(
                run_id=run.run_id,
                created_at=run.created_at,
            )
            session.add(record)
        record.workflow_id = run.workflow_id
        record.customer_handle = run.customer_handle
        record.state = run.state
        record.current_step = run.current_step
        record.checkpoint = checkpoint
        record.updated_at = utcnow()


async def load_run(run_id: str) -> WorkflowRun | None:
    """Rehydrate a run from Postgres, or None if it is not stored."""
    async with get_session() as session:
        record = await session.get(WorkflowRunRecord, run_id)
        if record is None:
            return None
        return restore_checkpoint(dict(record.checkpoint))


async def list_runs_by_state(state: str, *, limit: int = 100) -> list[WorkflowRun]:
    """Load runs in a given state — e.g. resumable ``paused_for_approval`` runs."""
    async with get_session() as session:
        stmt = (
            select(WorkflowRunRecord)
            .where(WorkflowRunRecord.state == state)
            .order_by(WorkflowRunRecord.updated_at)
            .limit(limit)
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [restore_checkpoint(dict(r.checkpoint)) for r in rows]
