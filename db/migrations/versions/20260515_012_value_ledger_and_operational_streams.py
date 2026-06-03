"""Value ledger events + operational JSONL stream mirror tables.

Revision ID: 012
Revises: 011
Create Date: 2026-05-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "012"
down_revision: Union[str, Sequence[str], None] = "011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "value_ledger_events",
        sa.Column("event_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("tier", sa.Text(), nullable=False),
        sa.Column("source_ref", sa.Text(), nullable=False, server_default=""),
        sa.Column("confirmation_ref", sa.Text(), nullable=False, server_default=""),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_index("ix_value_ledger_events_tenant", "value_ledger_events", ["tenant_id"])
    op.create_index("ix_value_ledger_events_occurred", "value_ledger_events", ["occurred_at"])

    op.create_table(
        "operational_event_streams",
        sa.Column("stream_id", sa.Text(), nullable=False),
        sa.Column("event_id", sa.Text(), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("stream_id", "event_id"),
    )
    op.create_index(
        "ix_operational_event_streams_stream_occurred",
        "operational_event_streams",
        ["stream_id", "occurred_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_operational_event_streams_stream_occurred", table_name="operational_event_streams")
    op.drop_table("operational_event_streams")
    op.drop_index("ix_value_ledger_events_occurred", table_name="value_ledger_events")
    op.drop_index("ix_value_ledger_events_tenant", table_name="value_ledger_events")
    op.drop_table("value_ledger_events")
