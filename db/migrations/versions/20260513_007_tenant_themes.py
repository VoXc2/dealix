"""Tenant themes — white-label CSS overrides per tenant (W7.5).

Wires the W3.2 CSS variable scaffold to a real DB-backed config:
each subscribing customer/agency can override brand palette,
display name, fonts, logo, custom domain.

Revision: 007
Down revision: 006 (the merge head)
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# Alembic reads these via runtime introspection (same pattern as 006).
__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "007"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "006"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "tenant_themes",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("brand_primary", sa.String(length=32), nullable=False, server_default="#0f172a"),
        sa.Column("brand_accent", sa.String(length=32), nullable=False, server_default="#10b981"),
        sa.Column("brand_muted", sa.String(length=32), nullable=False, server_default="#64748b"),
        sa.Column("brand_surface", sa.String(length=32), nullable=False, server_default="#ffffff"),
        sa.Column("brand_bg", sa.String(length=32), nullable=False, server_default="#f8fafc"),
        sa.Column("font_arabic", sa.String(length=128), nullable=False,
                  server_default="IBM Plex Sans Arabic"),
        sa.Column("font_english", sa.String(length=128), nullable=False, server_default="Inter"),
        sa.Column("logo_url", sa.String(length=512), nullable=True),
        sa.Column("favicon_url", sa.String(length=512), nullable=True),
        sa.Column("display_name", sa.String(length=128), nullable=False, server_default="Dealix"),
        sa.Column("custom_domain", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["tenant_id"], ["tenants.id"],
            ondelete="CASCADE",
            name="fk_tenant_themes_tenant_id",
        ),
        sa.PrimaryKeyConstraint("tenant_id", name="pk_tenant_themes"),
    )
    op.create_index(
        "ix_tenant_themes_custom_domain",
        "tenant_themes",
        ["custom_domain"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_tenant_themes_custom_domain", table_name="tenant_themes")
    op.drop_table("tenant_themes")
