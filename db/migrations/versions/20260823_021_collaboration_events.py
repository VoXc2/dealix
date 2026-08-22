"""Allow durable Collaboration OS events in Communication OS storage.

Revision ID: 20260823_021_collaboration_events
Revises: 20260812_020_tenant_scope_conversations_tasks
Create Date: 2026-08-23

This migration expands the existing communication_hub_snapshots collection
check constraint. It does not introduce a parallel table or source of truth.
Applying this migration to production remains a separate governed operation.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260823_021_collaboration_events"
down_revision: str | None = "20260812_020_tenant_scope_conversations_tasks"
branch_labels: str | None = None
depends_on: str | None = None

_CONSTRAINT = "ck_communication_hub_collection"
_TABLE = "communication_hub_snapshots"


def upgrade() -> None:
    op.drop_constraint(_CONSTRAINT, _TABLE, type_="check")
    op.create_check_constraint(
        _CONSTRAINT,
        _TABLE,
        sa.text("collection IN ('contact_log', 'sequences', 'collaboration_events')"),
    )
    op.execute(
        """
        INSERT INTO communication_hub_snapshots (collection, data)
        VALUES ('collaboration_events', '[]'::jsonb)
        ON CONFLICT (collection) DO NOTHING
        """
    )


def downgrade() -> None:
    # Fail closed rather than silently deleting durable collaboration history.
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM communication_hub_snapshots
                WHERE collection = 'collaboration_events'
                  AND data <> '[]'::jsonb
            ) THEN
                RAISE EXCEPTION
                    'Cannot downgrade: collaboration_events contains durable data';
            END IF;
        END $$;
        """
    )
    op.execute(
        "DELETE FROM communication_hub_snapshots "
        "WHERE collection = 'collaboration_events' AND data = '[]'::jsonb"
    )
    op.drop_constraint(_CONSTRAINT, _TABLE, type_="check")
    op.create_check_constraint(
        _CONSTRAINT,
        _TABLE,
        sa.text("collection IN ('contact_log', 'sequences')"),
    )
