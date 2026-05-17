"""Append-only Evidence Events ledger table.

Revision ID: 013
Revises: 012
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "013"
down_revision: Union[str, Sequence[str], None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "evidence_events",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("approval_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("linked_asset", sa.String(length=128), nullable=True),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("signature", sa.String(length=128), nullable=False, server_default="UNSIGNED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_events_event_type", "evidence_events", ["event_type"])
    op.create_index("ix_evidence_events_source", "evidence_events", ["source"])
    op.create_index("ix_evidence_events_approval_required", "evidence_events", ["approval_required"])
    op.create_index("ix_evidence_events_linked_asset", "evidence_events", ["linked_asset"])
    op.create_index("ix_evidence_events_actor", "evidence_events", ["actor"])
    op.create_index("ix_evidence_events_created_at", "evidence_events", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_evidence_events_created_at", table_name="evidence_events")
    op.drop_index("ix_evidence_events_actor", table_name="evidence_events")
    op.drop_index("ix_evidence_events_linked_asset", table_name="evidence_events")
    op.drop_index("ix_evidence_events_approval_required", table_name="evidence_events")
    op.drop_index("ix_evidence_events_source", table_name="evidence_events")
    op.drop_index("ix_evidence_events_event_type", table_name="evidence_events")
    op.drop_table("evidence_events")
