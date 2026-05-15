"""Enterprise control plane: agent_mesh_agents table."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "014"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "013"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "agent_mesh_agents",
        sa.Column("agent_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("owner", sa.String(length=128), nullable=False),
        sa.Column("capabilities", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("trust_tier", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("autonomy_level", sa.Integer(), nullable=False),
        sa.Column("endpoint", sa.String(length=255), nullable=True),
        sa.Column("composite_score", sa.Float(), nullable=True),
        sa.Column("tool_permissions", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("agent_id", name="pk_agent_mesh_agents"),
    )
    op.create_index("idx_agent_mesh_tenant_status", "agent_mesh_agents", ["tenant_id", "status"])


def downgrade() -> None:
    op.drop_index("idx_agent_mesh_tenant_status", table_name="agent_mesh_agents")
    op.drop_table("agent_mesh_agents")
