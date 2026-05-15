"""Enterprise control plane: value_metrics table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "017"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "016"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "value_metrics",
        sa.Column("metric_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("metric_name", sa.String(length=128), nullable=False),
        sa.Column("metric_type", sa.String(length=32), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="SAR"),
        sa.Column("source_ref", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.PrimaryKeyConstraint("metric_id", name="pk_value_metrics"),
    )
    op.create_index("idx_value_metrics_tenant_run", "value_metrics", ["tenant_id", "run_id"])


def downgrade() -> None:
    op.drop_index("idx_value_metrics_tenant_run", table_name="value_metrics")
    op.drop_table("value_metrics")
