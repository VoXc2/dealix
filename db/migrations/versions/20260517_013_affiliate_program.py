"""Affiliate / Partner Commission Machine — schema.

Companion to `api/routers/affiliate_program.py` and
`auto_client_acquisition/partnership_os/affiliate_store.py`.

External affiliates/partners earn CASH commissions on referred deals,
paid only after a recorded invoice_paid event, with a 30-day clawback
window. Distinct from the customer-referral program in migration 010.

The JSONL store is the runtime source of truth today; this migration
lands the Postgres schema so the store can swap to asyncpg with no API
change. Raw SQL reference: `db/migrations/013_affiliate_program.sql`.

Migration 013.
Down revision: 012 (value_ledger_and_operational_streams).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "013"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "012"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    # affiliate_partners — external affiliates/partners and their score/tier.
    op.create_table(
        "affiliate_partners",
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("email_hash", sa.String(length=32), nullable=True),
        sa.Column(
            "partner_category",
            sa.String(length=32),
            nullable=False,
            server_default="other",
        ),
        sa.Column("audience_type", sa.String(length=64), nullable=True),
        sa.Column("region", sa.String(length=64), nullable=True),
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "score_breakdown",
            sa.JSON(),
            nullable=False,
            server_default="{}",
        ),
        sa.Column("tier", sa.String(length=16), nullable=True),
        sa.Column(
            "status", sa.String(length=16), nullable=False, server_default="scored"
        ),
        sa.Column(
            "disclosure_accepted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("plan_text", sa.Text(), nullable=True),
        sa.Column("rejected_reason", sa.String(length=256), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("scored_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("partner_id", name="pk_affiliate_partners"),
    )
    op.create_index(
        "ix_affiliate_partners_status", "affiliate_partners", ["status"]
    )

    # affiliate_partner_links — APT- referral codes issued on approval.
    op.create_table(
        "affiliate_partner_links",
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("tier", sa.String(length=16), nullable=False),
        sa.Column(
            "is_revoked", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["partner_id"],
            ["affiliate_partners.partner_id"],
            name="fk_affiliate_links_partner",
        ),
        sa.PrimaryKeyConstraint("code", name="pk_affiliate_partner_links"),
    )
    op.create_index(
        "ix_affiliate_links_partner", "affiliate_partner_links", ["partner_id"]
    )

    # affiliate_referrals — leads submitted by partners.
    op.create_table(
        "affiliate_referrals",
        sa.Column("affiliate_referral_id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("lead_company", sa.String(length=255), nullable=False),
        sa.Column("lead_email_hash", sa.String(length=32), nullable=True),
        sa.Column(
            "status", sa.String(length=16), nullable=False, server_default="submitted"
        ),
        sa.Column(
            "qualified", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "disclosure_present",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("decline_reason", sa.String(length=256), nullable=True),
        sa.Column("invoice_id", sa.String(length=64), nullable=True),
        sa.Column(
            "deal_amount_sar", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("qualified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("invoice_paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["code"],
            ["affiliate_partner_links.code"],
            name="fk_affiliate_referrals_code",
        ),
        sa.PrimaryKeyConstraint(
            "affiliate_referral_id", name="pk_affiliate_referrals"
        ),
        sa.UniqueConstraint(
            "code", "lead_email_hash", name="uq_affiliate_referrals_code_lead"
        ),
    )
    op.create_index(
        "ix_affiliate_referrals_partner", "affiliate_referrals", ["partner_id"]
    )
    op.create_index(
        "ix_affiliate_referrals_status", "affiliate_referrals", ["status"]
    )

    # affiliate_commissions — cash commission, gated on invoice_paid.
    op.create_table(
        "affiliate_commissions",
        sa.Column("commission_id", sa.String(length=64), nullable=False),
        sa.Column(
            "affiliate_referral_id", sa.String(length=64), nullable=False
        ),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("tier", sa.String(length=16), nullable=False),
        sa.Column("pct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "base_amount_sar", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "commission_sar", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "status",
            sa.String(length=16),
            nullable=False,
            server_default="calculated",
        ),
        sa.Column("clawback_deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("clawback_reason", sa.String(length=256), nullable=True),
        sa.Column(
            "calculated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("payout_id", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["affiliate_referral_id"],
            ["affiliate_referrals.affiliate_referral_id"],
            name="fk_affiliate_commissions_referral",
        ),
        sa.PrimaryKeyConstraint("commission_id", name="pk_affiliate_commissions"),
        sa.UniqueConstraint(
            "affiliate_referral_id",
            name="uq_affiliate_commissions_referral",
        ),
    )
    op.create_index(
        "ix_affiliate_commissions_partner",
        "affiliate_commissions",
        ["partner_id"],
    )
    op.create_index(
        "ix_affiliate_commissions_status",
        "affiliate_commissions",
        ["status"],
    )

    # affiliate_payouts — settled cash payouts to partners.
    op.create_table(
        "affiliate_payouts",
        sa.Column("payout_id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("commission_ids", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("total_sar", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("method", sa.String(length=32), nullable=True),
        sa.Column("reference", sa.String(length=128), nullable=True),
        sa.Column(
            "status", sa.String(length=16), nullable=False, server_default="pending"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["partner_id"],
            ["affiliate_partners.partner_id"],
            name="fk_affiliate_payouts_partner",
        ),
        sa.PrimaryKeyConstraint("payout_id", name="pk_affiliate_payouts"),
    )
    op.create_index(
        "ix_affiliate_payouts_partner", "affiliate_payouts", ["partner_id"]
    )

    # affiliate_approved_assets — vetted partner-facing messaging.
    op.create_table(
        "affiliate_approved_assets",
        sa.Column("asset_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("lang", sa.String(length=8), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("asset_id", name="pk_affiliate_approved_assets"),
    )

    # affiliate_compliance_events — disclosure / spam / abuse events.
    op.create_table(
        "affiliate_compliance_events",
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("partner_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column(
            "severity", sa.String(length=16), nullable=False, server_default="low"
        ),
        sa.Column("detail", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint(
            "event_id", name="pk_affiliate_compliance_events"
        ),
    )
    op.create_index(
        "ix_affiliate_compliance_partner",
        "affiliate_compliance_events",
        ["partner_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_affiliate_compliance_partner",
        table_name="affiliate_compliance_events",
    )
    op.drop_table("affiliate_compliance_events")

    op.drop_table("affiliate_approved_assets")

    op.drop_index("ix_affiliate_payouts_partner", table_name="affiliate_payouts")
    op.drop_table("affiliate_payouts")

    op.drop_index(
        "ix_affiliate_commissions_status", table_name="affiliate_commissions"
    )
    op.drop_index(
        "ix_affiliate_commissions_partner", table_name="affiliate_commissions"
    )
    op.drop_table("affiliate_commissions")

    op.drop_index(
        "ix_affiliate_referrals_status", table_name="affiliate_referrals"
    )
    op.drop_index(
        "ix_affiliate_referrals_partner", table_name="affiliate_referrals"
    )
    op.drop_table("affiliate_referrals")

    op.drop_index(
        "ix_affiliate_links_partner", table_name="affiliate_partner_links"
    )
    op.drop_table("affiliate_partner_links")

    op.drop_index(
        "ix_affiliate_partners_status", table_name="affiliate_partners"
    )
    op.drop_table("affiliate_partners")
