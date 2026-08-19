"""Add tenant ownership columns for autonomous conversations and tasks.

Revision ID: 20260812_020_tenant_scope_conversations_tasks
Revises: 20260815_020_governed_orchestrator_state
Create Date: 2026-08-12

This is the schema tranche for #1070. On the current repository lineage it is
sequenced after the governed-orchestrator state revision so the combined graph
keeps a single Alembic head. The columns are intentionally nullable because
historical rows cannot be assigned to a tenant safely without an evidence-backed
backfill. Runtime code must stamp tenant_id on all new rows and scope every
read/update before this migration is approved for production.
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

__all__ = (
    "revision",
    "down_revision",
    "branch_labels",
    "depends_on",
    "upgrade",
    "downgrade",
)

revision: str = "20260812_020_tenant_scope_conversations_tasks"
down_revision: str | None = "20260815_020_governed_orchestrator_state"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "conversations",
        sa.Column("tenant_id", sa.String(64), nullable=True),
    )
    op.create_foreign_key(
        "fk_conversations_tenant_id_tenants",
        "conversations",
        "tenants",
        ["tenant_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_conversations_tenant_created",
        "conversations",
        ["tenant_id", "created_at"],
        unique=False,
    )

    op.add_column(
        "tasks",
        sa.Column("tenant_id", sa.String(64), nullable=True),
    )
    op.create_foreign_key(
        "fk_tasks_tenant_id_tenants",
        "tasks",
        "tenants",
        ["tenant_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_tasks_tenant_status_due",
        "tasks",
        ["tenant_id", "status", "due_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_tasks_tenant_status_due", table_name="tasks")
    op.drop_constraint(
        "fk_tasks_tenant_id_tenants",
        "tasks",
        type_="foreignkey",
    )
    op.drop_column("tasks", "tenant_id")

    op.drop_index("ix_conversations_tenant_created", table_name="conversations")
    op.drop_constraint(
        "fk_conversations_tenant_id_tenants",
        "conversations",
        type_="foreignkey",
    )
    op.drop_column("conversations", "tenant_id")
