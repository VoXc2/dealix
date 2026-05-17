"""Affiliate & Partner machine — partner application columns + 6 new tables.

Revision ID: 013
Revises: 012
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "013"
down_revision: Union[str, Sequence[str], None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Extend the existing `partners` table ───────────────────────
    op.add_column("partners", sa.Column("country", sa.String(length=64), nullable=True))
    op.add_column("partners", sa.Column("audience_type", sa.String(length=64), nullable=True))
    op.add_column(
        "partners",
        sa.Column("audience_size", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("partners", sa.Column("main_channel", sa.String(length=64), nullable=True))
    op.add_column(
        "partners",
        sa.Column("partner_score", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("partners", sa.Column("tier", sa.String(length=32), nullable=True))
    op.add_column("partners", sa.Column("referral_code", sa.String(length=32), nullable=True))
    op.add_column(
        "partners",
        sa.Column("disclosure_accepted", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("partners", sa.Column("applied_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("partners", sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("partners", sa.Column("approved_by", sa.String(length=64), nullable=True))
    op.create_unique_constraint("uq_partners_referral_code", "partners", ["referral_code"])

    # ── partner_links ──────────────────────────────────────────────
    op.create_table(
        "partner_links",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("utm_source", sa.String(length=64), nullable=True),
        sa.Column("utm_medium", sa.String(length=64), nullable=True),
        sa.Column("utm_campaign", sa.String(length=64), nullable=True),
        sa.Column("target_url", sa.String(length=512), nullable=False, server_default=""),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_partner_links_partner_id", "partner_links", ["partner_id"])
    op.create_index("ix_partner_links_code", "partner_links", ["code"])
    op.create_index("ix_partner_links_deleted_at", "partner_links", ["deleted_at"])

    # ── partner_referrals ──────────────────────────────────────────
    op.create_table(
        "partner_referrals",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("link_id", sa.String(length=64), nullable=True),
        sa.Column("lead_id", sa.String(length=64), nullable=True),
        sa.Column("deal_id", sa.String(length=64), nullable=True),
        sa.Column("contact_email_hash", sa.String(length=64), nullable=True),
        sa.Column("stage", sa.String(length=32), nullable=False, server_default="submitted"),
        sa.Column("qualified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_partner_referrals_partner_id", "partner_referrals", ["partner_id"])
    op.create_index("ix_partner_referrals_link_id", "partner_referrals", ["link_id"])
    op.create_index("ix_partner_referrals_lead_id", "partner_referrals", ["lead_id"])
    op.create_index("ix_partner_referrals_deal_id", "partner_referrals", ["deal_id"])
    op.create_index(
        "ix_partner_referrals_contact_email_hash", "partner_referrals", ["contact_email_hash"]
    )
    op.create_index("ix_partner_referrals_stage", "partner_referrals", ["stage"])
    op.create_index("ix_partner_referrals_deleted_at", "partner_referrals", ["deleted_at"])

    # ── partner_commissions ────────────────────────────────────────
    op.create_table(
        "partner_commissions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("referral_id", sa.String(length=64), nullable=True),
        sa.Column("deal_id", sa.String(length=64), nullable=True),
        sa.Column("tier", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("basis_amount_sar", sa.Float(), nullable=False, server_default="0"),
        sa.Column("rate", sa.Float(), nullable=False, server_default="0"),
        sa.Column("amount_sar", sa.Float(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("invoice_paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_partner_commissions_partner_id", "partner_commissions", ["partner_id"])
    op.create_index("ix_partner_commissions_referral_id", "partner_commissions", ["referral_id"])
    op.create_index("ix_partner_commissions_deal_id", "partner_commissions", ["deal_id"])
    op.create_index("ix_partner_commissions_status", "partner_commissions", ["status"])
    op.create_index("ix_partner_commissions_deleted_at", "partner_commissions", ["deleted_at"])

    # ── partner_payouts ────────────────────────────────────────────
    op.create_table(
        "partner_payouts",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("period", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("commission_ids", sa.JSON(), nullable=False),
        sa.Column("total_sar", sa.Float(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("partner_invoice_ref", sa.String(length=128), nullable=True),
        sa.Column("marked_paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("marked_paid_by", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_partner_payouts_partner_id", "partner_payouts", ["partner_id"])
    op.create_index("ix_partner_payouts_status", "partner_payouts", ["status"])
    op.create_index("ix_partner_payouts_deleted_at", "partner_payouts", ["deleted_at"])

    # ── partner_approved_assets ────────────────────────────────────
    op.create_table(
        "partner_approved_assets",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("asset_type", sa.String(length=64), nullable=False),
        sa.Column("locale", sa.String(length=8), nullable=False, server_default="ar"),
        sa.Column("title", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("allowed_claims", sa.JSON(), nullable=False),
        sa.Column("forbidden_claims", sa.JSON(), nullable=False),
        sa.Column("version", sa.String(length=16), nullable=False, server_default="1.0"),
        sa.Column("approved", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_partner_approved_assets_asset_type", "partner_approved_assets", ["asset_type"]
    )
    op.create_index(
        "ix_partner_approved_assets_deleted_at", "partner_approved_assets", ["deleted_at"]
    )

    # ── partner_compliance_events ──────────────────────────────────
    op.create_table(
        "partner_compliance_events",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False, server_default="low"),
        sa.Column("evidence_ref", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_partner_compliance_events_partner_id", "partner_compliance_events", ["partner_id"]
    )
    op.create_index(
        "ix_partner_compliance_events_kind", "partner_compliance_events", ["kind"]
    )
    op.create_index(
        "ix_partner_compliance_events_deleted_at", "partner_compliance_events", ["deleted_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_partner_compliance_events_deleted_at", table_name="partner_compliance_events")
    op.drop_index("ix_partner_compliance_events_kind", table_name="partner_compliance_events")
    op.drop_index("ix_partner_compliance_events_partner_id", table_name="partner_compliance_events")
    op.drop_table("partner_compliance_events")

    op.drop_index("ix_partner_approved_assets_deleted_at", table_name="partner_approved_assets")
    op.drop_index("ix_partner_approved_assets_asset_type", table_name="partner_approved_assets")
    op.drop_table("partner_approved_assets")

    op.drop_index("ix_partner_payouts_deleted_at", table_name="partner_payouts")
    op.drop_index("ix_partner_payouts_status", table_name="partner_payouts")
    op.drop_index("ix_partner_payouts_partner_id", table_name="partner_payouts")
    op.drop_table("partner_payouts")

    op.drop_index("ix_partner_commissions_deleted_at", table_name="partner_commissions")
    op.drop_index("ix_partner_commissions_status", table_name="partner_commissions")
    op.drop_index("ix_partner_commissions_deal_id", table_name="partner_commissions")
    op.drop_index("ix_partner_commissions_referral_id", table_name="partner_commissions")
    op.drop_index("ix_partner_commissions_partner_id", table_name="partner_commissions")
    op.drop_table("partner_commissions")

    op.drop_index("ix_partner_referrals_deleted_at", table_name="partner_referrals")
    op.drop_index("ix_partner_referrals_stage", table_name="partner_referrals")
    op.drop_index("ix_partner_referrals_contact_email_hash", table_name="partner_referrals")
    op.drop_index("ix_partner_referrals_deal_id", table_name="partner_referrals")
    op.drop_index("ix_partner_referrals_lead_id", table_name="partner_referrals")
    op.drop_index("ix_partner_referrals_link_id", table_name="partner_referrals")
    op.drop_index("ix_partner_referrals_partner_id", table_name="partner_referrals")
    op.drop_table("partner_referrals")

    op.drop_index("ix_partner_links_deleted_at", table_name="partner_links")
    op.drop_index("ix_partner_links_code", table_name="partner_links")
    op.drop_index("ix_partner_links_partner_id", table_name="partner_links")
    op.drop_table("partner_links")

    op.drop_constraint("uq_partners_referral_code", "partners", type_="unique")
    op.drop_column("partners", "approved_by")
    op.drop_column("partners", "approved_at")
    op.drop_column("partners", "applied_at")
    op.drop_column("partners", "disclosure_accepted")
    op.drop_column("partners", "referral_code")
    op.drop_column("partners", "tier")
    op.drop_column("partners", "partner_score")
    op.drop_column("partners", "main_channel")
    op.drop_column("partners", "audience_size")
    op.drop_column("partners", "audience_type")
    op.drop_column("partners", "country")
