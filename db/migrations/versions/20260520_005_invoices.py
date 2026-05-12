"""invoices table — T4e webhook landing zone

Revision ID: 005
Revises: 004
Create Date: 2026-05-20 00:00:00.000000

Changes:
  - Create invoices table to land Stripe + Moyasar webhook events as
    first-class rows (replacing the AuditLogRecord-as-invoice-store
    pattern used since T0).
  - Composite unique (provider, external_id) so the same vendor event
    can't double-insert.
  - Composite index (tenant_id, provider) for fast per-tenant listing.
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
        "invoices",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("external_id", sa.String(128), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("amount_minor", sa.Integer, nullable=False, server_default="0"),
        sa.Column("currency", sa.String(8), nullable=False, server_default="SAR"),
        sa.Column(
            "issued_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ix_invoices_tenant_id", "invoices", ["tenant_id"])
    op.create_index("ix_invoices_provider", "invoices", ["provider"])
    op.create_index("ix_invoices_external_id", "invoices", ["external_id"])
    op.create_index("ix_invoices_status", "invoices", ["status"])
    op.create_index("ix_invoices_issued_at", "invoices", ["issued_at"])
    op.create_index("ix_invoice_tenant_provider", "invoices", ["tenant_id", "provider"])
    op.create_unique_constraint(
        "uq_invoice_provider_external", "invoices", ["provider", "external_id"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_invoice_provider_external", "invoices", type_="unique")
    op.drop_index("ix_invoice_tenant_provider", "invoices")
    op.drop_index("ix_invoices_issued_at", "invoices")
    op.drop_index("ix_invoices_status", "invoices")
    op.drop_index("ix_invoices_external_id", "invoices")
    op.drop_index("ix_invoices_provider", "invoices")
    op.drop_index("ix_invoices_tenant_id", "invoices")
    op.drop_table("invoices")
