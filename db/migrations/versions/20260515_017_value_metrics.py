"""Create value_metrics table.

Revision ID: 017
Revises: 016
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

__all__ = ["branch_labels", "depends_on", "down_revision", "revision"]

revision: str = "017"
down_revision: str | Sequence[str] | None = "016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "value_metrics",
        sa.Column("metric_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("metric_name", sa.Text(), nullable=False),
        sa.Column("tier", sa.Text(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False, server_default="0"),
        sa.Column("source_ref", sa.Text(), nullable=True),
        sa.Column("confirmation_ref", sa.Text(), nullable=True),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_value_metrics_tenant_run", "value_metrics", ["tenant_id", "run_id"])


def downgrade() -> None:
    op.drop_index("idx_value_metrics_tenant_run", table_name="value_metrics")
    op.drop_table("value_metrics")
