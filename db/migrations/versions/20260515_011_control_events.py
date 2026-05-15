"""Create control_events table for enterprise control plane.

Revision ID: 011
Revises: 010
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

__all__ = ["branch_labels", "depends_on", "down_revision", "revision"]

revision: str = "011"
down_revision: str | Sequence[str] | None = "010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "control_events",
        sa.Column("id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("source_module", sa.Text(), nullable=False),
        sa.Column("actor", sa.Text(), nullable=False),
        sa.Column("subject_type", sa.Text(), nullable=True),
        sa.Column("subject_id", sa.Text(), nullable=True),
        sa.Column("run_id", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.Text(), nullable=True),
        sa.Column("decision", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("redacted", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("idx_control_events_tenant_run", "control_events", ["tenant_id", "run_id"])
    op.create_index("idx_control_events_tenant_time", "control_events", ["tenant_id", "occurred_at"])
    op.create_index("idx_control_events_type", "control_events", ["event_type"])


def downgrade() -> None:
    op.drop_index("idx_control_events_type", table_name="control_events")
    op.drop_index("idx_control_events_tenant_time", table_name="control_events")
    op.drop_index("idx_control_events_tenant_run", table_name="control_events")
    op.drop_table("control_events")
