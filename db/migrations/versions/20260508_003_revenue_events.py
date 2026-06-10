"""revenue_events append-only event log
جدول أحداث الإيرادات — السجل الثابت لذاكرة الإيرادات

Revision ID: 003
Revises: 002
Create Date: 2026-05-08 00:00:00.000000

Changes:
  - Create revenue_events table (append-only event store for Revenue Memory)
  - Indexes on (customer_id, occurred_at), (subject_type, subject_id),
    (event_type), (correlation_id)
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "revenue_events",
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("customer_id", sa.String(length=64), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("subject_type", sa.String(length=64), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default="{}"),
        sa.Column("causation_id", sa.String(length=64), nullable=True),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("actor", sa.String(length=128), nullable=False, server_default="system"),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_index(
        "ix_revevt_customer_occurred",
        "revenue_events",
        ["customer_id", "occurred_at"],
    )
    op.create_index(
        "ix_revevt_subject",
        "revenue_events",
        ["subject_type", "subject_id"],
    )
    op.create_index("ix_revevt_event_type", "revenue_events", ["event_type"])
    op.create_index("ix_revevt_correlation", "revenue_events", ["correlation_id"])


def downgrade() -> None:
    op.drop_index("ix_revevt_correlation", table_name="revenue_events")
    op.drop_index("ix_revevt_event_type", table_name="revenue_events")
    op.drop_index("ix_revevt_subject", table_name="revenue_events")
    op.drop_index("ix_revevt_customer_occurred", table_name="revenue_events")
    op.drop_table("revenue_events")
