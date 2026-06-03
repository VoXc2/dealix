"""Sector Reports persistence — R4 monetization (W8.2).

Adds the sector_reports table so generated reports survive across
process restarts. Pairs with api/routers/sector_intel.py update that
writes to + reads from this table.

Revision: 008
Down revision: 007 (tenant_themes)
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# Alembic introspects these via runtime; mark explicit for static analyzers.
__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "008"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "007"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "sector_reports",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("sector", sa.String(length=64), nullable=False),
        sa.Column("customer_handle", sa.String(length=64), nullable=True),
        sa.Column("price_sar", sa.Integer(), nullable=False),
        sa.Column("period_start", sa.String(length=32), nullable=True),
        sa.Column("period_end", sa.String(length=32), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("payment_status", sa.String(length=32),
                  nullable=False, server_default="pending"),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_sector_reports"),
    )
    op.create_index("ix_sector_reports_sector", "sector_reports", ["sector"])
    op.create_index(
        "ix_sector_reports_customer_handle", "sector_reports", ["customer_handle"]
    )
    op.create_index(
        "ix_sector_reports_payment_status", "sector_reports", ["payment_status"]
    )
    op.create_index(
        "ix_sector_reports_created_at", "sector_reports", ["created_at"]
    )
    op.create_index(
        "ix_sector_reports_sector_created",
        "sector_reports",
        ["sector", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_sector_reports_sector_created", table_name="sector_reports")
    op.drop_index("ix_sector_reports_created_at", table_name="sector_reports")
    op.drop_index("ix_sector_reports_payment_status", table_name="sector_reports")
    op.drop_index("ix_sector_reports_customer_handle", table_name="sector_reports")
    op.drop_index("ix_sector_reports_sector", table_name="sector_reports")
    op.drop_table("sector_reports")
