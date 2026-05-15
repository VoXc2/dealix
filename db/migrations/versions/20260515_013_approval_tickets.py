"""Create approval_tickets table.

Revision ID: 013
Revises: 012
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

__all__ = ["branch_labels", "depends_on", "down_revision", "revision"]

revision: str = "013"
down_revision: str | Sequence[str] | None = "012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "approval_tickets",
        sa.Column("ticket_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requested_by", sa.Text(), nullable=False),
        sa.Column("source_module", sa.Text(), nullable=False),
        sa.Column("subject_type", sa.Text(), nullable=True),
        sa.Column("subject_id", sa.Text(), nullable=True),
        sa.Column("run_id", sa.Text(), nullable=True),
        sa.Column("state", sa.Text(), nullable=False),
        sa.Column("granted_by", sa.Text(), nullable=True),
        sa.Column("rejected_by", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_approval_tickets_tenant_state", "approval_tickets", ["tenant_id", "state"])


def downgrade() -> None:
    op.drop_index("idx_approval_tickets_tenant_state", table_name="approval_tickets")
    op.drop_table("approval_tickets")
