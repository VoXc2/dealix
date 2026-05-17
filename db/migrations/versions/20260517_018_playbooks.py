"""Playbooks store table.

Revision ID: 018
Revises: 017
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "018"
down_revision: Union[str, Sequence[str], None] = "017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "playbooks",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("vertical", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("stage", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("steps", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("entry_criteria", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("exit_criteria", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("owner", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_playbooks_tenant_id", "playbooks", ["tenant_id"])
    op.create_index("ix_playbooks_name", "playbooks", ["name"])
    op.create_index("ix_playbooks_vertical", "playbooks", ["vertical"])
    op.create_index("ix_playbooks_status", "playbooks", ["status"])
    op.create_index("ix_playbooks_deleted_at", "playbooks", ["deleted_at"])
    op.create_index("ix_playbooks_tenant_vertical", "playbooks", ["tenant_id", "vertical"])


def downgrade() -> None:
    op.drop_index("ix_playbooks_tenant_vertical", table_name="playbooks")
    op.drop_index("ix_playbooks_deleted_at", table_name="playbooks")
    op.drop_index("ix_playbooks_status", table_name="playbooks")
    op.drop_index("ix_playbooks_vertical", table_name="playbooks")
    op.drop_index("ix_playbooks_name", table_name="playbooks")
    op.drop_index("ix_playbooks_tenant_id", table_name="playbooks")
    op.drop_table("playbooks")
