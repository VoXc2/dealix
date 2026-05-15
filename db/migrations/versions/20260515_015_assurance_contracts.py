"""Enterprise control plane: assurance_contracts table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "015"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "014"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "assurance_contracts",
        sa.Column("contract_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("contract_type", sa.String(length=64), nullable=False),
        sa.Column("agent_id", sa.String(length=64), nullable=False),
        sa.Column("action_type", sa.String(length=128), nullable=False),
        sa.Column("may_see", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("may_propose", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("may_execute", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("precondition_checks", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("rollback_plan", sa.Text(), nullable=True),
        sa.Column("is_external", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_irreversible", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("contract_id", name="pk_assurance_contracts"),
    )
    op.create_index(
        "idx_assurance_contracts_tenant_agent_action",
        "assurance_contracts",
        ["tenant_id", "agent_id", "action_type"],
    )


def downgrade() -> None:
    op.drop_index("idx_assurance_contracts_tenant_agent_action", table_name="assurance_contracts")
    op.drop_table("assurance_contracts")
