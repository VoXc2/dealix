"""Saudi compliance: zatca_invoices + consent_requests tables
نظام التوافق السعودي: جداول فواتير ZATCA + طلبات الموافقة PDPL

Revision ID: 002
Revises: 001
Create Date: 2026-05-07 00:00:00.000000

Changes:
  - Create zatca_invoices table (ZATCA Phase 2 e-invoice records)
  - Create consent_requests table (PDPL Art. 5 consent request tracking)
  - Add pdpl_erasure columns to contacts table (if missing)
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Create zatca_invoices table ────────────────────────────────
    # ZATCA Phase 2 e-invoice record (clearance + reporting).
    op.create_table(
        "zatca_invoices",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("deal_id", sa.String(length=64), nullable=True),
        sa.Column("customer_id", sa.String(length=64), nullable=True),
        sa.Column("invoice_number", sa.String(length=128), nullable=False),
        sa.Column("invoice_type", sa.String(length=32), nullable=False, server_default="simplified"),
        # invoice_type: "simplified" (B2C) | "standard" (B2B)
        sa.Column("issue_date", sa.String(length=10), nullable=True),    # YYYY-MM-DD
        sa.Column("issue_time", sa.String(length=8), nullable=True),     # HH:MM:SS
        sa.Column("seller_vat_number", sa.String(length=20), nullable=True),
        sa.Column("buyer_vat_number", sa.String(length=20), nullable=True),
        sa.Column("buyer_name", sa.String(length=255), nullable=True),
        sa.Column("subtotal_sar", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("vat_amount_sar", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("total_sar", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("vat_rate", sa.Numeric(precision=5, scale=4), nullable=True, server_default="0.15"),
        sa.Column("line_items", JSONB, nullable=True),
        # ZATCA API response fields
        sa.Column("zatca_xml_b64", sa.Text, nullable=True),
        sa.Column("qr_code_b64", sa.Text, nullable=True),
        sa.Column("zatca_status", sa.String(length=32), nullable=False, server_default="draft"),
        # draft | pending_clearance | cleared | reported | rejected | error
        sa.Column("zatca_response", JSONB, nullable=True),
        sa.Column("zatca_cleared_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invoice_number", name="uq_zatca_invoice_number"),
    )
    op.create_index("ix_zatca_invoices_tenant_id", "zatca_invoices", ["tenant_id"])
    op.create_index("ix_zatca_invoices_invoice_number", "zatca_invoices", ["invoice_number"])
    op.create_index("ix_zatca_invoices_zatca_status", "zatca_invoices", ["zatca_status"])
    op.create_index("ix_zatca_invoices_created_at", "zatca_invoices", ["created_at"])
    op.create_index("ix_zatca_invoices_deal_id", "zatca_invoices", ["deal_id"])

    # ── Create consent_requests table ─────────────────────────────
    # PDPL Art. 5 consent request dispatch tracking.
    op.create_table(
        "consent_requests",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("contact_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        # channel: email | whatsapp | sms
        sa.Column("purpose", sa.String(length=64), nullable=False),
        # purpose: service_delivery | legal_obligation | legitimate_interest | explicit_consent
        sa.Column("status", sa.String(length=32), nullable=False, server_default="sent"),
        # status: sent | delivered | responded_grant | responded_revoke | expired
        sa.Column("consent_url", sa.String(length=500), nullable=True),
        sa.Column("locale", sa.String(length=8), nullable=False, server_default="ar"),
        sa.Column("responded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response_kind", sa.String(length=16), nullable=True),
        # response_kind: grant | revoke
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_consent_requests_contact_id", "consent_requests", ["contact_id"])
    op.create_index("ix_consent_requests_tenant_id", "consent_requests", ["tenant_id"])
    op.create_index("ix_consent_requests_channel", "consent_requests", ["channel"])
    op.create_index("ix_consent_requests_purpose", "consent_requests", ["purpose"])
    op.create_index("ix_consent_requests_status", "consent_requests", ["status"])
    op.create_index("ix_consent_requests_created_at", "consent_requests", ["created_at"])
    op.create_index(
        "ix_consent_requests_contact_channel",
        "consent_requests",
        ["contact_id", "channel", "purpose"],
    )

    # ── Add PDPL erasure columns to contacts (if they don't exist) ─
    # These are added as nullable columns — no data migration needed.
    # The try/except guards against re-running on a DB that already has them.
    try:
        op.add_column(
            "contacts",
            sa.Column(
                "pdpl_erasure_requested_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
        )
    except Exception:
        pass  # Column already exists

    try:
        op.add_column(
            "contacts",
            sa.Column(
                "pdpl_erased_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
        )
    except Exception:
        pass  # Column already exists

    try:
        op.add_column(
            "contacts",
            sa.Column(
                "consent_status",
                sa.String(length=32),
                nullable=True,
                server_default="unknown",
            ),
        )
    except Exception:
        pass  # Column already exists


def downgrade() -> None:
    # Remove PDPL columns from contacts
    try:
        op.drop_column("contacts", "consent_status")
    except Exception:
        pass
    try:
        op.drop_column("contacts", "pdpl_erased_at")
    except Exception:
        pass
    try:
        op.drop_column("contacts", "pdpl_erasure_requested_at")
    except Exception:
        pass

    # Drop consent_requests table
    op.drop_index("ix_consent_requests_contact_channel", table_name="consent_requests")
    op.drop_index("ix_consent_requests_created_at", table_name="consent_requests")
    op.drop_index("ix_consent_requests_status", table_name="consent_requests")
    op.drop_index("ix_consent_requests_purpose", table_name="consent_requests")
    op.drop_index("ix_consent_requests_channel", table_name="consent_requests")
    op.drop_index("ix_consent_requests_tenant_id", table_name="consent_requests")
    op.drop_index("ix_consent_requests_contact_id", table_name="consent_requests")
    op.drop_table("consent_requests")

    # Drop zatca_invoices table
    op.drop_index("ix_zatca_invoices_deal_id", table_name="zatca_invoices")
    op.drop_index("ix_zatca_invoices_created_at", table_name="zatca_invoices")
    op.drop_index("ix_zatca_invoices_zatca_status", table_name="zatca_invoices")
    op.drop_index("ix_zatca_invoices_invoice_number", table_name="zatca_invoices")
    op.drop_index("ix_zatca_invoices_tenant_id", table_name="zatca_invoices")
    op.drop_table("zatca_invoices")
