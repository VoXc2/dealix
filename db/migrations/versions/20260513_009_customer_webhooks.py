"""Customer webhooks table — Dealix→customer event delivery (W12.1).

Migration 009.
Down revision: 008 (sector_reports).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "009"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "008"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "customer_webhook_subscriptions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("secret", sa.String(length=128), nullable=False),
        sa.Column("event_types", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_delivery_at", sa.DateTime(), nullable=True),
        sa.Column("last_delivery_status", sa.String(length=32), nullable=True),
        sa.Column("consecutive_failures", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["tenant_id"], ["tenants.id"], ondelete="CASCADE",
            name="fk_cwh_tenant_id",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_customer_webhook_subscriptions"),
    )
    op.create_index("ix_cwh_tenant_id", "customer_webhook_subscriptions", ["tenant_id"])
    op.create_index(
        "ix_cwh_tenant_active",
        "customer_webhook_subscriptions",
        ["tenant_id", "is_active"],
    )
    op.create_index(
        "ix_cwh_is_active",
        "customer_webhook_subscriptions",
        ["is_active"],
    )

    op.create_table(
        "customer_webhook_deliveries",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("subscription_id", sa.String(length=64), nullable=False),
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("delivered_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("response_status", sa.Integer(), nullable=True),
        sa.Column("response_body_preview", sa.String(length=500), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["subscription_id"], ["customer_webhook_subscriptions.id"],
            ondelete="CASCADE",
            name="fk_cwd_subscription_id",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_customer_webhook_deliveries"),
        sa.UniqueConstraint(
            "subscription_id", "event_id", name="uq_webhook_subscription_event"
        ),
    )
    op.create_index("ix_cwd_subscription_id", "customer_webhook_deliveries", ["subscription_id"])
    op.create_index("ix_cwd_event_id", "customer_webhook_deliveries", ["event_id"])
    op.create_index("ix_cwd_event_type", "customer_webhook_deliveries", ["event_type"])
    op.create_index("ix_cwd_delivered_at", "customer_webhook_deliveries", ["delivered_at"])
    op.create_index(
        "ix_cwd_event_type_created",
        "customer_webhook_deliveries",
        ["event_type", "delivered_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_cwd_event_type_created", table_name="customer_webhook_deliveries")
    op.drop_index("ix_cwd_delivered_at", table_name="customer_webhook_deliveries")
    op.drop_index("ix_cwd_event_type", table_name="customer_webhook_deliveries")
    op.drop_index("ix_cwd_event_id", table_name="customer_webhook_deliveries")
    op.drop_index("ix_cwd_subscription_id", table_name="customer_webhook_deliveries")
    op.drop_table("customer_webhook_deliveries")

    op.drop_index("ix_cwh_is_active", table_name="customer_webhook_subscriptions")
    op.drop_index("ix_cwh_tenant_active", table_name="customer_webhook_subscriptions")
    op.drop_index("ix_cwh_tenant_id", table_name="customer_webhook_subscriptions")
    op.drop_table("customer_webhook_subscriptions")
