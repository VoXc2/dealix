"""Enterprise control plane: approval_tickets table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "013"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "012"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "approval_tickets",
        sa.Column("ticket_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("action_type", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requested_by", sa.String(length=128), nullable=False),
        sa.Column("source_module", sa.String(length=128), nullable=False),
        sa.Column("subject_type", sa.String(length=128), nullable=True),
        sa.Column("subject_id", sa.String(length=128), nullable=True),
        sa.Column("run_id", sa.String(length=64), nullable=True),
        sa.Column("state", sa.String(length=64), nullable=False),
        sa.Column("granted_by", sa.String(length=128), nullable=True),
        sa.Column("rejected_by", sa.String(length=128), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("ticket_id", name="pk_approval_tickets"),
    )
    op.create_index("idx_approval_tickets_tenant_state", "approval_tickets", ["tenant_id", "state"])


def downgrade() -> None:
    op.drop_index("idx_approval_tickets_tenant_state", table_name="approval_tickets")
    op.drop_table("approval_tickets")
