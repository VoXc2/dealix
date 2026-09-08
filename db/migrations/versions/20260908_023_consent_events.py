"""Create the append-only durable outbound consent event ledger.

Revision ID: 20260908_023_consent_events
Revises: 20260905_022_approval_center_snapshots
Create Date: 2026-09-08

Applying this migration to production remains a separate governed DB action.
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260908_023_consent_events"
down_revision: str | Sequence[str] | None = "20260905_022_approval_center_snapshots"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "outbound_consent_events",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("event_key", sa.String(length=128), nullable=False),
        sa.Column("tenant_scope", sa.String(length=128), nullable=False),
        sa.Column("contact_id", sa.String(length=128), nullable=True),
        sa.Column("recipient", sa.String(length=320), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("purpose", sa.String(length=64), nullable=False),
        sa.Column("state", sa.String(length=16), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("evidence_ref", sa.String(length=512), nullable=True),
        sa.Column("evidence_digest", sa.String(length=128), nullable=True),
        sa.Column("policy_version", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "channel IN ('email', 'whatsapp', 'sms')",
            name="ck_outbound_consent_events_channel",
        ),
        sa.CheckConstraint(
            "purpose IN ('direct_marketing', 'partner_discovery', 'customer_success', 'support', 'transactional')",
            name="ck_outbound_consent_events_purpose",
        ),
        sa.CheckConstraint(
            "state IN ('granted', 'withdrawn')",
            name="ck_outbound_consent_events_state",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_key", name="uq_outbound_consent_events_event_key"),
    )
    op.create_index(
        "ix_outbound_consent_events_authority",
        "outbound_consent_events",
        ["tenant_scope", "recipient", "channel", "purpose", "occurred_at"],
        unique=False,
    )
    op.create_index(
        "ix_outbound_consent_events_contact",
        "outbound_consent_events",
        ["tenant_scope", "contact_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_outbound_consent_events_contact",
        table_name="outbound_consent_events",
    )
    op.drop_index(
        "ix_outbound_consent_events_authority",
        table_name="outbound_consent_events",
    )
    op.drop_table("outbound_consent_events")
