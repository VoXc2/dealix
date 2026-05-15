"""Create agent_mesh_agents table.

Revision ID: 014
Revises: 013
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agent_mesh_agents",
        sa.Column("agent_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("owner", sa.Text(), nullable=False),
        sa.Column(
            "capabilities",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("trust_tier", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("autonomy_level", sa.Integer(), nullable=False),
        sa.Column("endpoint", sa.Text(), nullable=True),
        sa.Column("composite_score", sa.Float(), nullable=True),
        sa.Column(
            "tool_permissions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_agent_mesh_tenant_status", "agent_mesh_agents", ["tenant_id", "status"])


def downgrade() -> None:
    op.drop_index("idx_agent_mesh_tenant_status", table_name="agent_mesh_agents")
    op.drop_table("agent_mesh_agents")
