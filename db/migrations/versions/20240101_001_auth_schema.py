"""auth schema - tenants, users, roles, refresh tokens, invites

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

Changes:
  - Add system_role column to users table
  - Make users.tenant_id nullable (for system super_admin users)
  - Create refresh_tokens table (session management)
  - Create user_invites table (invite flow)
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Alter users table ──────────────────────────────────────────

    # Make tenant_id nullable (super_admin users may not belong to a tenant)
    op.alter_column(
        "users",
        "tenant_id",
        existing_type=sa.String(length=64),
        nullable=True,
    )

    # Add system_role column
    op.add_column(
        "users",
        sa.Column("system_role", sa.String(length=32), nullable=True),
    )
    op.create_index("ix_users_system_role", "users", ["system_role"])

    # ── Create refresh_tokens table ────────────────────────────────

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("device_info", sa.String(length=512), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])
    op.create_index("ix_refresh_tokens_token_hash", "refresh_tokens", ["token_hash"])
    op.create_index("ix_refresh_tokens_expires_at", "refresh_tokens", ["expires_at"])
    op.create_index(
        "ix_refresh_user_expires",
        "refresh_tokens",
        ["user_id", "expires_at"],
    )

    # ── Create user_invites table ──────────────────────────────────

    op.create_table(
        "user_invites",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.String(length=64), nullable=True),
        sa.Column("invited_by", sa.String(length=64), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "email", name="uq_invite_tenant_email"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_user_invites_tenant_id", "user_invites", ["tenant_id"])
    op.create_index("ix_user_invites_email", "user_invites", ["email"])
    op.create_index("ix_user_invites_token_hash", "user_invites", ["token_hash"])
    op.create_index("ix_user_invites_expires_at", "user_invites", ["expires_at"])
    op.create_index("ix_user_invites_invited_by", "user_invites", ["invited_by"])


def downgrade() -> None:
    # Drop new tables
    op.drop_index("ix_user_invites_invited_by", table_name="user_invites")
    op.drop_index("ix_user_invites_expires_at", table_name="user_invites")
    op.drop_index("ix_user_invites_token_hash", table_name="user_invites")
    op.drop_index("ix_user_invites_email", table_name="user_invites")
    op.drop_index("ix_user_invites_tenant_id", table_name="user_invites")
    op.drop_table("user_invites")

    op.drop_index("ix_refresh_user_expires", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_expires_at", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_token_hash", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")

    # Remove users additions
    op.drop_index("ix_users_system_role", table_name="users")
    op.drop_column("users", "system_role")
    op.alter_column("users", "tenant_id", existing_type=sa.String(length=64), nullable=False)
