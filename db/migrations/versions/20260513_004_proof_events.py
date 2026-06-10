"""proof_events ledger — append-only Proof Pack evidence chain
جدول أحداث Proof — سجل ثابت للأدلّة الدائمة

Revision ID: 004
Revises: 003
Create Date: 2026-05-13 00:00:00.000000

Why
- Article 3 Law 2: "No proof → no claim". Every Proof Pack assertion must
  be traceable to a real event with evidence_id, customer attestation,
  and a verifiable level (L1 Internal Draft → L5 Revenue Evidence).
- Master Plan V.B #1 lists this as the highest-leverage piece of "smart
  enough to run with API keys" — Proof Packs become generative once this
  table exists.
- Constitution Article 8 Revenue Truth: payment evidence required for L5;
  without DB persistence the audit chain breaks across restarts.

Changes
- Create proof_events table (append-only — no UPDATE/DELETE in app code).
- Indexes on (tenant_id, customer_handle, created_at) for portal queries.
- Index on (event_type, level) for KPI rollups (L4+ outcomes, L5 revenue).
- Soft delete via deleted_at (PDPL right-to-be-forgotten).
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "proof_events",
        # Identity
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("customer_handle", sa.String(length=80), nullable=False),
        # Classification
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("service_id", sa.String(length=64), nullable=True),
        sa.Column(
            "level",
            sa.String(length=4),
            nullable=False,
            server_default="L1",
        ),
        # Content
        sa.Column("claim", sa.Text(), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default="{}"),
        sa.Column("evidence_url", sa.String(length=512), nullable=True),
        sa.Column("evidence_hash", sa.String(length=128), nullable=True),
        # Visibility + consent
        sa.Column(
            "customer_visible",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "publish_consent",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("consent_signature", sa.String(length=256), nullable=True),
        # Approvals
        sa.Column("approved_by", sa.String(length=128), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        # Lifecycle
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        # Constraints
        sa.PrimaryKeyConstraint("event_id"),
        sa.CheckConstraint(
            "level IN ('L1', 'L2', 'L3', 'L4', 'L5')",
            name="ck_proof_events_level",
        ),
    )
    op.create_index(
        "ix_proof_events_tenant_customer_created",
        "proof_events",
        ["tenant_id", "customer_handle", "created_at"],
    )
    op.create_index(
        "ix_proof_events_type_level",
        "proof_events",
        ["event_type", "level"],
    )
    op.create_index(
        "ix_proof_events_service",
        "proof_events",
        ["service_id"],
    )
    op.create_index(
        "ix_proof_events_visible_published",
        "proof_events",
        ["customer_visible", "publish_consent"],
    )


def downgrade() -> None:
    op.drop_index("ix_proof_events_visible_published", table_name="proof_events")
    op.drop_index("ix_proof_events_service", table_name="proof_events")
    op.drop_index("ix_proof_events_type_level", table_name="proof_events")
    op.drop_index("ix_proof_events_tenant_customer_created", table_name="proof_events")
    op.drop_table("proof_events")
