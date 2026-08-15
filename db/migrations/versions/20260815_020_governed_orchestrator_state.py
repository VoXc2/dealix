"""Durable multi-node state for the governed orchestrator.

Revision ID: 20260815_020_governed_orchestrator_state
Revises: 20260723_019_knowledge_accumulator_storage
Create Date: 2026-08-15
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260815_020_governed_orchestrator_state"
down_revision: str | None = "20260723_019_knowledge_accumulator_storage"
branch_labels: str | None = None
depends_on: str | None = None


def _alembic_revision_metadata() -> tuple[str, str | None, str | None, str | None]:
    """Expose the module globals that Alembic reads through introspection."""
    return revision, down_revision, branch_labels, depends_on


def upgrade() -> None:
    _alembic_revision_metadata()
    op.add_column("workflow_runs", sa.Column("idempotency_key", sa.Text(), nullable=True))
    op.add_column(
        "workflow_runs",
        sa.Column("version", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )
    op.add_column("workflow_runs", sa.Column("lease_owner", sa.Text(), nullable=True))
    op.add_column(
        "workflow_runs",
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute(
        "UPDATE workflow_runs SET idempotency_key = run_id WHERE idempotency_key IS NULL"
    )
    op.alter_column("workflow_runs", "idempotency_key", nullable=False)
    op.create_unique_constraint(
        "uq_workflow_runs_tenant_idempotency",
        "workflow_runs",
        ["tenant_id", "customer_id", "workflow_id", "idempotency_key"],
    )
    op.create_index(
        "ix_workflow_runs_lease_expiry",
        "workflow_runs",
        ["lease_expires_at"],
    )

    op.create_table(
        "orchestrator_tasks",
        sa.Column("task_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("customer_id", sa.Text(), nullable=False),
        sa.Column("agent_id", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("step_id", sa.Text(), nullable=False),
        sa.Column(
            "payload",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column(
            "requires_approval",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("approval_reason", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.Text(), nullable=True),
        sa.Column("causation_task_id", sa.Text(), nullable=True),
        sa.Column("parent_workflow_id", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("result", JSONB, nullable=True),
        sa.Column(
            "retries",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "max_retries",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("2"),
        ),
        sa.Column(
            "version",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("claim_owner", sa.Text(), nullable=True),
        sa.Column("claim_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("task_id"),
        sa.UniqueConstraint(
            "tenant_id",
            "correlation_id",
            "step_id",
            name="uq_orchestrator_tasks_tenant_run_step",
        ),
    )
    op.create_index("ix_orchestrator_tasks_tenant", "orchestrator_tasks", ["tenant_id"])
    op.create_index(
        "ix_orchestrator_tasks_customer",
        "orchestrator_tasks",
        ["tenant_id", "customer_id"],
    )
    op.create_index(
        "ix_orchestrator_tasks_run",
        "orchestrator_tasks",
        ["tenant_id", "correlation_id"],
    )
    op.create_index(
        "ix_orchestrator_tasks_claimable",
        "orchestrator_tasks",
        ["tenant_id", "status", "claim_expires_at"],
    )


def downgrade() -> None:
    _alembic_revision_metadata()
    op.drop_index("ix_orchestrator_tasks_claimable", table_name="orchestrator_tasks")
    op.drop_index("ix_orchestrator_tasks_run", table_name="orchestrator_tasks")
    op.drop_index("ix_orchestrator_tasks_customer", table_name="orchestrator_tasks")
    op.drop_index("ix_orchestrator_tasks_tenant", table_name="orchestrator_tasks")
    op.drop_table("orchestrator_tasks")

    op.drop_index("ix_workflow_runs_lease_expiry", table_name="workflow_runs")
    op.drop_constraint(
        "uq_workflow_runs_tenant_idempotency",
        "workflow_runs",
        type_="unique",
    )
    op.drop_column("workflow_runs", "lease_expires_at")
    op.drop_column("workflow_runs", "lease_owner")
    op.drop_column("workflow_runs", "version")
    op.drop_column("workflow_runs", "idempotency_key")
