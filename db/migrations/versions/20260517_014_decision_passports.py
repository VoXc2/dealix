"""Append-only Decision Passport store table.

Revision ID: 014
Revises: 013
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "decision_passports",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("lead_id", sa.String(length=64), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("schema_version", sa.String(length=16), nullable=False, server_default="1.1"),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("approved_by", sa.String(length=128), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("proof_target", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("owner", sa.String(length=64), nullable=False, server_default="founder"),
        sa.Column("priority_bucket", sa.String(length=32), nullable=False, server_default="P2_NURTURE"),
        sa.Column("measurable_impact", sa.Text(), nullable=False, server_default=""),
        sa.Column("evidence_event_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("signature", sa.String(length=128), nullable=False, server_default="UNSIGNED"),
        sa.Column("passport_json", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_decision_passports_tenant_id", "decision_passports", ["tenant_id"])
    op.create_index("ix_decision_passports_lead_id", "decision_passports", ["lead_id"])
    op.create_index("ix_decision_passports_priority_bucket", "decision_passports", ["priority_bucket"])
    op.create_index("ix_decision_passports_created_at", "decision_passports", ["created_at"])
    op.create_index("ix_decision_passports_tenant_lead", "decision_passports", ["tenant_id", "lead_id"])


def downgrade() -> None:
    op.drop_index("ix_decision_passports_tenant_lead", table_name="decision_passports")
    op.drop_index("ix_decision_passports_created_at", table_name="decision_passports")
    op.drop_index("ix_decision_passports_priority_bucket", table_name="decision_passports")
    op.drop_index("ix_decision_passports_lead_id", table_name="decision_passports")
    op.drop_index("ix_decision_passports_tenant_id", table_name="decision_passports")
    op.drop_table("decision_passports")
