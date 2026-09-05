"""Create the durable Approval Center snapshot and merge current heads.

Revision ID: 20260905_022_approval_center_snapshots
Revises: 20260823_021_collaboration_events, 20260815_020_governed_orchestrator_state
Create Date: 2026-09-05

Applying this migration to production remains a separate governed operation.
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260905_022_approval_center_snapshots"
down_revision: str | Sequence[str] | None = (
    "20260823_021_collaboration_events",
    "20260815_020_governed_orchestrator_state",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "approval_center_snapshots",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column(
            "data",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("approval_center_snapshots")
