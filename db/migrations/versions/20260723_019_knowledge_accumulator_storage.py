"""Durable Knowledge and Research OS snapshot storage.

Revision ID: 20260723_019_knowledge_accumulator_storage
Revises: 20260723_018_communication_hub_storage
Create Date: 2026-07-23
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

__all__ = (
    "revision",
    "down_revision",
    "branch_labels",
    "depends_on",
    "upgrade",
    "downgrade",
)

revision: str = "20260723_019_knowledge_accumulator_storage"
down_revision: str | None = "20260723_018_communication_hub_storage"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "knowledge_accumulator_snapshots",
        sa.Column("collection", sa.String(32), primary_key=True),
        sa.Column(
            "data",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "collection = 'entries'",
            name="ck_knowledge_accumulator_collection",
        ),
    )
    # Explicit JSONB literal keeps both online migration and ``--sql`` offline
    # rendering deterministic; Alembic cannot literal-render Python lists for JSONB.
    op.execute(
        """
        INSERT INTO knowledge_accumulator_snapshots (collection, data)
        VALUES ('entries', '[]'::jsonb)
        """
    )


def downgrade() -> None:
    op.drop_table("knowledge_accumulator_snapshots")
