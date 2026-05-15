"""SQLAlchemy 2.0 model for the workflow_runs table.

Durable persistence for the workflow_os_v10 state machine. One row per
WorkflowRun; the full run (steps, idempotency keys, checkpoint) is stored
in the JSONB ``checkpoint`` column and round-trips through
``save_checkpoint`` / ``restore_checkpoint``.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.utils import utcnow
from db.models import Base


class WorkflowRunRecord(Base):
    """Durable row mirroring a workflow_os_v10 WorkflowRun."""

    __tablename__ = "workflow_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    workflow_id: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_handle: Mapped[str] = mapped_column(String(80), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    current_step: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    checkpoint: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_workflow_runs_state_updated", "state", "updated_at"),
        Index("ix_workflow_runs_workflow_id", "workflow_id"),
    )
