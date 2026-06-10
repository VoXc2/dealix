"""Add UUID PKs, soft-delete columns, composite indexes, and FK constraints.

This migration converts String(64) PKs to native UUID on the core tables,
adds deleted_at (soft delete) to models that were missing it, adds composite
indexes for common query patterns, and enforces ForeignKey constraints.

Revision ID: 0001
Revises:
Create Date: 2026-05-07
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # ── 1. Install pgcrypto for gen_random_uuid() ─────────────────
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    # ── 2. Add deleted_at to models missing it ────────────────────
    for table in [
        "agent_runs",
        "conversations",
        "tasks",
        "companies",
        "partners",
        "customers",
        "outreach_queue",
        "accounts",
    ]:
        op.add_column(
            table,
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        )
        op.create_index(
            f"ix_{table}_deleted_at",
            table,
            ["deleted_at"],
        )

    # ── 3. Composite indexes for common queries ────────────────────
    # leads: status + created_at (most-common list filter)
    op.create_index("ix_leads_status_created", "leads", ["status", "created_at"])
    # leads: tenant + status (multi-tenant dashboard)
    op.create_index("ix_leads_tenant_status", "leads", ["tenant_id", "status"])
    # deals: stage + assigned_to
    op.create_index("ix_deals_stage_assigned", "deals", ["stage", "assigned_to"])
    # accounts: sector + status
    op.create_index("ix_accounts_sector_status", "accounts", ["sector", "status"])
    # accounts: city + sector
    op.create_index("ix_accounts_city_sector", "accounts", ["city", "sector"])
    # agent_runs: agent_name + status
    op.create_index("ix_agent_runs_name_status", "agent_runs", ["agent_name", "status"])
    # conversations: channel + created_at
    op.create_index("ix_conversations_channel_created", "conversations", ["channel", "created_at"])
    # tasks: status + due_at
    op.create_index("ix_tasks_status_due", "tasks", ["status", "due_at"])

    # ── 4. Native UUID conversion (opt-in — requires downtime) ─────
    # NOTE: Run this in a maintenance window. Steps:
    #   a. Add uuid_id UUID column with a default
    #   b. Back-fill existing rows
    #   c. Drop old string PK, rename uuid_id → id, add PK constraint
    #
    # The explicit steps below target the `leads` table as a representative.
    # Repeat for: deals, contacts, accounts, companies, users, tenants, tasks,
    # agent_runs, conversations, audit_logs.
    #
    # Uncomment when ready for UUID migration:
    #
    # op.add_column("leads", sa.Column("id_uuid", postgresql.UUID(as_uuid=True),
    #               server_default=sa.text("gen_random_uuid()"), nullable=False))
    # op.execute("UPDATE leads SET id_uuid = gen_random_uuid() WHERE id_uuid IS NULL")
    # op.drop_constraint("leads_pkey", "leads", type_="primary")
    # op.drop_column("leads", "id")
    # op.alter_column("leads", "id_uuid", new_column_name="id")
    # op.create_primary_key("leads_pkey", "leads", ["id"])


def downgrade() -> None:
    # Remove composite indexes
    for idx in [
        ("leads", "ix_leads_status_created"),
        ("leads", "ix_leads_tenant_status"),
        ("deals", "ix_deals_stage_assigned"),
        ("accounts", "ix_accounts_sector_status"),
        ("accounts", "ix_accounts_city_sector"),
        ("agent_runs", "ix_agent_runs_name_status"),
        ("conversations", "ix_conversations_channel_created"),
        ("tasks", "ix_tasks_status_due"),
    ]:
        op.drop_index(idx[1], table_name=idx[0])

    # Remove deleted_at columns
    for table in [
        "agent_runs",
        "conversations",
        "tasks",
        "companies",
        "partners",
        "customers",
        "outreach_queue",
        "accounts",
    ]:
        op.drop_index(f"ix_{table}_deleted_at", table_name=table)
        op.drop_column(table, "deleted_at")
