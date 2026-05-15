"""ROI OS — ROI snapshots.

Companion to ``auto_client_acquisition/roi_os/`` (Wave 16). The runtime
spine uses the JSONL ROI ledger; this table is the DB-backed upgrade
path.

Migration 014.
Down revision: 013 (eval_runs).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "014"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "013"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "roi_snapshots",
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("customer_id", sa.String(length=128), nullable=False),
        sa.Column("window_days", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("agent_runs", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("grounded_answers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("eval_pass_rate", sa.Float(), nullable=False, server_default="0"),
        sa.Column(
            "knowledge_grounding_rate", sa.Float(), nullable=False, server_default="0"
        ),
        sa.Column(
            "verified_value_sar", sa.Float(), nullable=False, server_default="0"
        ),
        sa.Column(
            "estimated_value_sar", sa.Float(), nullable=False, server_default="0"
        ),
        sa.Column("llm_cost_sar", sa.Float(), nullable=False, server_default="0"),
        sa.Column("net_roi_sar", sa.Float(), nullable=False, server_default="0"),
        sa.Column("lines", sa.JSON(), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("snapshot_id", name="pk_roi_snapshots"),
    )
    op.create_index(
        "ix_roi_snapshots_customer",
        "roi_snapshots",
        ["customer_id", "occurred_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_roi_snapshots_customer", table_name="roi_snapshots")
    op.drop_table("roi_snapshots")
