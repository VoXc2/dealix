"""Referral program — Wave 14D.1 (promoted to Alembic in Wave 14J).

Companion to `api/routers/referral_program.py` (W13.13) +
`auto_client_acquisition/partnership_os/referral_store.py` (W14D.1).

Alembic owns the schema so Railway's `release: alembic upgrade head`
applies it automatically on deploy.

Migration 010.
Down revision: 009 (customer_webhooks).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "010"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "009"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    # referral_codes — one-time codes issued to existing paying customers.
    op.create_table(
        "referral_codes",
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("referrer_id", sa.String(length=64), nullable=False),
        sa.Column(
            "plan_required",
            sa.String(length=64),
            nullable=True,
            server_default="managed_revenue_ops_starter",
        ),
        sa.Column(
            "credit_sar", sa.Integer(), nullable=False, server_default="5000"
        ),
        sa.Column(
            "discount_pct", sa.Integer(), nullable=False, server_default="50"
        ),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "is_revoked",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("code", name="pk_referral_codes"),
    )
    op.create_index(
        "ix_referral_codes_referrer", "referral_codes", ["referrer_id"]
    )

    # referrals — referrer → referred customer link + credit state.
    op.create_table(
        "referrals",
        sa.Column("referral_id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("referrer_id", sa.String(length=64), nullable=False),
        sa.Column("referred_id", sa.String(length=64), nullable=False),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("referred_invoice_id", sa.String(length=64), nullable=True),
        sa.Column(
            "referred_first_amount_sar", sa.Integer(), nullable=True
        ),
        sa.Column("declined_reason", sa.String(length=256), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "credit_issued_at", sa.DateTime(timezone=True), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["code"], ["referral_codes.code"], name="fk_referrals_code"
        ),
        sa.PrimaryKeyConstraint("referral_id", name="pk_referrals"),
        sa.UniqueConstraint(
            "referrer_id", "referred_id", name="uq_referrals_referrer_referred"
        ),
    )
    op.create_index("ix_referrals_status", "referrals", ["status"])
    op.create_index("ix_referrals_referrer", "referrals", ["referrer_id"])
    op.create_index("ix_referrals_referred", "referrals", ["referred_id"])

    # referral_payouts — credit applications against future invoices.
    op.create_table(
        "referral_payouts",
        sa.Column("payout_id", sa.String(length=64), nullable=False),
        sa.Column("referral_id", sa.String(length=64), nullable=False),
        sa.Column("credit_sar", sa.Integer(), nullable=False),
        sa.Column(
            "applied_to_invoice_id", sa.String(length=64), nullable=True
        ),
        sa.Column(
            "applied_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["referral_id"],
            ["referrals.referral_id"],
            name="fk_referral_payouts_referral",
        ),
        sa.PrimaryKeyConstraint("payout_id", name="pk_referral_payouts"),
    )
    op.create_index(
        "ix_referral_payouts_referral", "referral_payouts", ["referral_id"]
    )


def downgrade() -> None:
    op.drop_index(
        "ix_referral_payouts_referral", table_name="referral_payouts"
    )
    op.drop_table("referral_payouts")

    op.drop_index("ix_referrals_referred", table_name="referrals")
    op.drop_index("ix_referrals_referrer", table_name="referrals")
    op.drop_index("ix_referrals_status", table_name="referrals")
    op.drop_table("referrals")

    op.drop_index("ix_referral_codes_referrer", table_name="referral_codes")
    op.drop_table("referral_codes")
