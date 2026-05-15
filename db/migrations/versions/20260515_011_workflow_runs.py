"""workflow_runs — durable persistence for the workflow_os_v10 state machine
جدول تشغيلات سير العمل — تخزين دائم لآلة الحالة

Revision ID: 011
Revises: 010
Create Date: 2026-05-15 00:00:00.000000

Why
- workflow_os_v10 runs lived only in an in-process dict (``_RUN_BUFFER``), so a
  restart lost every in-flight run and a run could not be resumed across
  processes. The 7-Day Revenue Intelligence Sprint runs as a workflow with a
  governance gate and founder approval — it must survive a restart.
- AI OS Gap Analysis, Phase A: persist WorkflowRun to Postgres
  (docs/architecture/AI_OS_GAP_ANALYSIS.md).

Changes
- Create workflow_runs table. The full run (step_history, idempotency keys,
  checkpoint) is stored in a JSONB ``checkpoint`` column and round-trips
  through save_checkpoint / restore_checkpoint.
- Index on (state, updated_at) to find resumable runs (paused_for_approval,
  retrying); index on workflow_id for per-definition queries.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "workflow_runs",
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("workflow_id", sa.String(length=64), nullable=False),
        sa.Column("customer_handle", sa.String(length=80), nullable=False),
        sa.Column(
            "state",
            sa.String(length=32),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "current_step",
            sa.String(length=128),
            nullable=False,
            server_default="",
        ),
        sa.Column("checkpoint", JSONB, nullable=False, server_default="{}"),
        sa.Column(
            "schema_version",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index(
        "ix_workflow_runs_state_updated",
        "workflow_runs",
        ["state", "updated_at"],
    )
    op.create_index(
        "ix_workflow_runs_workflow_id",
        "workflow_runs",
        ["workflow_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_workflow_runs_workflow_id", table_name="workflow_runs")
    op.drop_index("ix_workflow_runs_state_updated", table_name="workflow_runs")
    op.drop_table("workflow_runs")
