"""Agent Runtime — loop traces + steps.

Companion to ``auto_client_acquisition/agent_loop_os/`` (Wave 16). The
runtime spine uses the JSONL agent-loop ledger; these tables are the
DB-backed upgrade path.

Migration 012.
Down revision: 011 (knowledge_chunks).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "012"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "011"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "agent_loop_traces",
        sa.Column("loop_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("customer_id", sa.String(length=128), nullable=False),
        sa.Column("goal", sa.Text(), nullable=False),
        sa.Column("final_answer", sa.Text(), nullable=False, server_default=""),
        sa.Column("terminated_reason", sa.String(length=32), nullable=False),
        sa.Column("iteration_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tool_call_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "insufficient_evidence",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("loop_id", name="pk_agent_loop_traces"),
    )
    op.create_index(
        "ix_agent_loop_traces_customer",
        "agent_loop_traces",
        ["customer_id", "occurred_at"],
    )

    op.create_table(
        "agent_loop_steps",
        sa.Column("step_id", sa.String(length=64), nullable=False),
        sa.Column("loop_id", sa.String(length=64), nullable=False),
        sa.Column("iteration", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("thought", sa.Text(), nullable=False, server_default=""),
        sa.Column("tool_name", sa.String(length=64), nullable=True),
        sa.Column("observation", sa.Text(), nullable=False, server_default=""),
        sa.Column("error", sa.String(length=512), nullable=True),
        sa.ForeignKeyConstraint(
            ["loop_id"],
            ["agent_loop_traces.loop_id"],
            name="fk_agent_loop_steps_loop",
        ),
        sa.PrimaryKeyConstraint("step_id", name="pk_agent_loop_steps"),
    )
    op.create_index("ix_agent_loop_steps_loop", "agent_loop_steps", ["loop_id"])


def downgrade() -> None:
    op.drop_index("ix_agent_loop_steps_loop", table_name="agent_loop_steps")
    op.drop_table("agent_loop_steps")

    op.drop_index("ix_agent_loop_traces_customer", table_name="agent_loop_traces")
    op.drop_table("agent_loop_traces")
