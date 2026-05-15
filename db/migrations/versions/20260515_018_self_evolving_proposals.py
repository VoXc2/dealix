"""Enterprise control plane: self_evolving_proposals table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "018"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "017"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "self_evolving_proposals",
        sa.Column("proposal_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("proposed_by", sa.String(length=128), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False, server_default="proposed"),
        sa.Column("approval_ticket_id", sa.String(length=64), nullable=True),
        sa.Column("approved_by", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("proposal_id", name="pk_self_evolving_proposals"),
    )
    op.create_index("idx_self_evolving_tenant_state", "self_evolving_proposals", ["tenant_id", "state"])


def downgrade() -> None:
    op.drop_index("idx_self_evolving_tenant_state", table_name="self_evolving_proposals")
    op.drop_table("self_evolving_proposals")
