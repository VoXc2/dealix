"""Enterprise control plane: control_events table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "011"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "010"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "control_events",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("source_module", sa.String(length=128), nullable=False),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("subject_type", sa.String(length=128), nullable=True),
        sa.Column("subject_id", sa.String(length=128), nullable=True),
        sa.Column("run_id", sa.String(length=64), nullable=True),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("decision", sa.String(length=64), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("payload", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("redacted", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id", name="pk_control_events"),
    )
    op.create_index("idx_control_events_tenant_run", "control_events", ["tenant_id", "run_id"])
    op.create_index("idx_control_events_tenant_time", "control_events", ["tenant_id", "occurred_at"])


def downgrade() -> None:
    op.drop_index("idx_control_events_tenant_time", table_name="control_events")
    op.drop_index("idx_control_events_tenant_run", table_name="control_events")
    op.drop_table("control_events")
