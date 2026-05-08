"""Add tenant_id to revenue_events for strict isolation in Revenue Memory.

Revision ID: 005_revenue_events_tenant
Revises: 004_merge_heads
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005_revenue_events_tenant"
down_revision: Union[str, None] = "004_merge_heads"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "revenue_events",
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
    )
    op.create_index(
        "ix_revevt_tenant_occurred",
        "revenue_events",
        ["tenant_id", "occurred_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_revevt_tenant_occurred", table_name="revenue_events")
    op.drop_column("revenue_events", "tenant_id")
