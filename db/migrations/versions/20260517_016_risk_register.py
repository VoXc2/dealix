"""Risk Register table.

Revision ID: 016
Revises: 015
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "016"
down_revision: Union[str, Sequence[str], None] = "015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "risks",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("owner", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("severity", sa.String(length=16), nullable=False, server_default="medium"),
        sa.Column("likelihood", sa.String(length=16), nullable=False, server_default="medium"),
        sa.Column("control", sa.Text(), nullable=False, server_default=""),
        sa.Column("early_warning_signal", sa.Text(), nullable=False, server_default=""),
        sa.Column("response_plan", sa.Text(), nullable=False, server_default=""),
        sa.Column("test_or_checklist", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="open"),
        sa.Column("linked_deal_id", sa.String(length=64), nullable=True),
        sa.Column("linked_customer_id", sa.String(length=64), nullable=True),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risks_tenant_id", "risks", ["tenant_id"])
    op.create_index("ix_risks_category", "risks", ["category"])
    op.create_index("ix_risks_severity", "risks", ["severity"])
    op.create_index("ix_risks_status", "risks", ["status"])
    op.create_index("ix_risks_linked_deal_id", "risks", ["linked_deal_id"])
    op.create_index("ix_risks_linked_customer_id", "risks", ["linked_customer_id"])
    op.create_index("ix_risks_deleted_at", "risks", ["deleted_at"])
    op.create_index("ix_risks_tenant_status", "risks", ["tenant_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_risks_tenant_status", table_name="risks")
    op.drop_index("ix_risks_deleted_at", table_name="risks")
    op.drop_index("ix_risks_linked_customer_id", table_name="risks")
    op.drop_index("ix_risks_linked_deal_id", table_name="risks")
    op.drop_index("ix_risks_status", table_name="risks")
    op.drop_index("ix_risks_severity", table_name="risks")
    op.drop_index("ix_risks_category", table_name="risks")
    op.drop_index("ix_risks_tenant_id", table_name="risks")
    op.drop_table("risks")
