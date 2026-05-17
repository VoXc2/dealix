"""Content Assets store table.

Revision ID: 019
Revises: 018
Create Date: 2026-05-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "019"
down_revision: Union[str, Sequence[str], None] = "018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "content_assets",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("asset_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("uri", sa.String(length=2048), nullable=False, server_default=""),
        sa.Column("template_id", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("approved_by", sa.String(length=128), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("linked_deal_id", sa.String(length=64), nullable=True),
        sa.Column("checksum", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_content_assets_tenant_id", "content_assets", ["tenant_id"])
    op.create_index("ix_content_assets_asset_type", "content_assets", ["asset_type"])
    op.create_index("ix_content_assets_template_id", "content_assets", ["template_id"])
    op.create_index("ix_content_assets_status", "content_assets", ["status"])
    op.create_index("ix_content_assets_linked_deal_id", "content_assets", ["linked_deal_id"])
    op.create_index("ix_content_assets_deleted_at", "content_assets", ["deleted_at"])
    op.create_index("ix_content_assets_tenant_status", "content_assets", ["tenant_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_content_assets_tenant_status", table_name="content_assets")
    op.drop_index("ix_content_assets_deleted_at", table_name="content_assets")
    op.drop_index("ix_content_assets_linked_deal_id", table_name="content_assets")
    op.drop_index("ix_content_assets_status", table_name="content_assets")
    op.drop_index("ix_content_assets_template_id", table_name="content_assets")
    op.drop_index("ix_content_assets_asset_type", table_name="content_assets")
    op.drop_index("ix_content_assets_tenant_id", table_name="content_assets")
    op.drop_table("content_assets")
