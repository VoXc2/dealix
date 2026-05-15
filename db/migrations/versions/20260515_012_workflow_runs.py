"""Enterprise control plane: workflow_runs table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "012"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "011"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "workflow_runs",
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("workflow_id", sa.String(length=128), nullable=False),
        sa.Column("customer_id", sa.String(length=128), nullable=True),
        sa.Column("state", sa.String(length=64), nullable=False),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("parent_run_id", sa.String(length=64), nullable=True),
        sa.Column("current_step", sa.String(length=128), nullable=True),
        sa.Column("attached_policy_ids", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("run_id", name="pk_workflow_runs"),
    )
    op.create_index("idx_workflow_runs_tenant_state", "workflow_runs", ["tenant_id", "state"])


def downgrade() -> None:
    op.drop_index("idx_workflow_runs_tenant_state", table_name="workflow_runs")
    op.drop_table("workflow_runs")
