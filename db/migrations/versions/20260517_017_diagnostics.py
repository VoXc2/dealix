"""Diagnostics store table.

Revision ID: 017
Revises: 016
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "017"
down_revision: Union[str, Sequence[str], None] = "016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "diagnostics",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("subject_type", sa.String(length=64), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("diagnostic_type", sa.String(length=64), nullable=False),
        sa.Column("findings", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("severity", sa.String(length=16), nullable=False, server_default="low"),
        sa.Column("recommendations", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("run_by", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_diagnostics_tenant_id", "diagnostics", ["tenant_id"])
    op.create_index("ix_diagnostics_subject_type", "diagnostics", ["subject_type"])
    op.create_index("ix_diagnostics_subject_id", "diagnostics", ["subject_id"])
    op.create_index("ix_diagnostics_diagnostic_type", "diagnostics", ["diagnostic_type"])
    op.create_index("ix_diagnostics_severity", "diagnostics", ["severity"])
    op.create_index("ix_diagnostics_created_at", "diagnostics", ["created_at"])
    op.create_index("ix_diagnostics_deleted_at", "diagnostics", ["deleted_at"])
    op.create_index("ix_diagnostics_subject", "diagnostics", ["subject_type", "subject_id"])


def downgrade() -> None:
    op.drop_index("ix_diagnostics_subject", table_name="diagnostics")
    op.drop_index("ix_diagnostics_deleted_at", table_name="diagnostics")
    op.drop_index("ix_diagnostics_created_at", table_name="diagnostics")
    op.drop_index("ix_diagnostics_severity", table_name="diagnostics")
    op.drop_index("ix_diagnostics_diagnostic_type", table_name="diagnostics")
    op.drop_index("ix_diagnostics_subject_id", table_name="diagnostics")
    op.drop_index("ix_diagnostics_subject_type", table_name="diagnostics")
    op.drop_index("ix_diagnostics_tenant_id", table_name="diagnostics")
    op.drop_table("diagnostics")
