"""Agent Registry table — doctrine #9 (owner + scope + audit).

Revision ID: 015
Revises: 014
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "015"
down_revision: Union[str, Sequence[str], None] = "014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agent_registry",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("agent_name", sa.String(length=64), nullable=False),
        sa.Column("owner", sa.String(length=128), nullable=False),
        sa.Column("scope", sa.Text(), nullable=False),
        sa.Column("allowed_tools", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("risk_class", sa.String(length=32), nullable=False, server_default="draft_only"),
        sa.Column("audit_hook", sa.String(length=128), nullable=False, server_default="default_audit_hook"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("agent_name", name="uq_agent_registry_agent_name"),
    )
    op.create_index("ix_agent_registry_agent_name", "agent_registry", ["agent_name"])
    op.create_index("ix_agent_registry_risk_class", "agent_registry", ["risk_class"])
    op.create_index("ix_agent_registry_enabled", "agent_registry", ["enabled"])


def downgrade() -> None:
    op.drop_index("ix_agent_registry_enabled", table_name="agent_registry")
    op.drop_index("ix_agent_registry_risk_class", table_name="agent_registry")
    op.drop_index("ix_agent_registry_agent_name", table_name="agent_registry")
    op.drop_table("agent_registry")
