"""payments table — Moyasar webhook persistence + reconciliation source of truth
جدول المدفوعات — مصدر الحقيقة للمطابقة والتدقيق

Revision ID: 005
Revises: 004
Create Date: 2026-05-12 18:30:00.000000

Why
- The Moyasar webhook handler in api/routers/pricing.py currently only logs
  events. Without a persistent payments table:
    * scripts/reconcile_moyasar.py cannot detect drift between Moyasar and DB
    * accounting cannot answer "who paid what when" from the operational store
    * refunds/disputes have no canonical local trail
- PDPL Art. 11 retention requires we control payment records explicitly,
  not rely on Moyasar API forever.

Changes (additive only — safe to apply during live traffic)
- Create payments table (CREATE TABLE IF NOT EXISTS via Alembic)
- Unique constraint on (provider, provider_payment_id) for idempotency
- Composite index on (status, created_at) for reconciliation scans
- No data backfill — historical payments stay only in Moyasar's API
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("provider", sa.String(length=32), nullable=False, server_default="moyasar"),
        sa.Column("provider_payment_id", sa.String(length=128), nullable=False),
        sa.Column("plan", sa.String(length=64), nullable=True),
        sa.Column("amount_halalas", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="SAR"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("customer_handle", sa.String(length=128), nullable=True),
        sa.Column("last_event_id", sa.String(length=128), nullable=True),
        sa.Column("last_event_type", sa.String(length=64), nullable=True),
        sa.Column("raw_event", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("error_reason", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["tenant_id"], ["tenants.id"],
            name="fk_payments_tenant_id",
            ondelete="SET NULL",
        ),
        sa.UniqueConstraint("provider", "provider_payment_id", name="uq_payments_provider_id"),
    )
    op.create_index("ix_payments_tenant_id", "payments", ["tenant_id"])
    op.create_index("ix_payments_provider", "payments", ["provider"])
    op.create_index("ix_payments_provider_payment_id", "payments", ["provider_payment_id"])
    op.create_index("ix_payments_plan", "payments", ["plan"])
    op.create_index("ix_payments_status", "payments", ["status"])
    op.create_index("ix_payments_email", "payments", ["email"])
    op.create_index("ix_payments_customer_handle", "payments", ["customer_handle"])
    op.create_index("ix_payments_created_at", "payments", ["created_at"])
    op.create_index("ix_payments_status_created_at", "payments", ["status", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_payments_status_created_at", table_name="payments")
    op.drop_index("ix_payments_created_at", table_name="payments")
    op.drop_index("ix_payments_customer_handle", table_name="payments")
    op.drop_index("ix_payments_email", table_name="payments")
    op.drop_index("ix_payments_status", table_name="payments")
    op.drop_index("ix_payments_plan", table_name="payments")
    op.drop_index("ix_payments_provider_payment_id", table_name="payments")
    op.drop_index("ix_payments_provider", table_name="payments")
    op.drop_index("ix_payments_tenant_id", table_name="payments")
    op.drop_table("payments")
