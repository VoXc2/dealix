"""activity_events hypertable — T5f time-series

Revision ID: 007
Revises: 006
Create Date: 2026-05-22 00:00:00.000000

Adds activity_events (per-tenant touch log) and turns it into a
TimescaleDB hypertable when the extension is present. On vanilla
Postgres or SQLite the table is a normal one — queries still work,
just without partitioning.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _is_postgres() -> bool:
    return op.get_bind().dialect.name == "postgresql"


def upgrade() -> None:
    op.create_table(
        "activity_events",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("user_id", sa.String(64), nullable=True),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=True),
        sa.Column("verb", sa.String(64), nullable=False),
        sa.Column("source", sa.String(64), nullable=False, server_default="api"),
        sa.Column("metadata", sa.JSON, nullable=False, server_default="{}"),
        sa.Column(
            "occurred_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ix_ae_tenant_occurred", "activity_events", ["tenant_id", "occurred_at"])
    op.create_index("ix_ae_entity", "activity_events", ["entity_type", "entity_id"])
    op.create_index("ix_ae_verb", "activity_events", ["verb"])

    if _is_postgres():
        # TimescaleDB hypertable — partition on occurred_at.
        op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")
        op.execute(
            "SELECT create_hypertable('activity_events', 'occurred_at', "
            "if_not_exists => TRUE)"
        )


def downgrade() -> None:
    if _is_postgres():
        # Hypertable is implicitly dropped with the underlying table.
        pass
    op.drop_index("ix_ae_verb", "activity_events")
    op.drop_index("ix_ae_entity", "activity_events")
    op.drop_index("ix_ae_tenant_occurred", "activity_events")
    op.drop_table("activity_events")
