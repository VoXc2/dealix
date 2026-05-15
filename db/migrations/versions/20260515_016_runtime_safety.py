"""Create runtime_safety_kill_switches and runtime_safety_circuit_breakers tables.

Revision ID: 016
Revises: 015
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "016"
down_revision: Union[str, Sequence[str], None] = "015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "runtime_safety_kill_switches",
        sa.Column("switch_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("target_id", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "idx_runtime_safety_switch_tenant_target",
        "runtime_safety_kill_switches",
        ["tenant_id", "target_id"],
    )

    op.create_table(
        "runtime_safety_circuit_breakers",
        sa.Column("breaker_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("breaker_key", sa.Text(), nullable=False),
        sa.Column("failures", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("threshold", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("is_open", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "idx_runtime_safety_breaker_tenant_key",
        "runtime_safety_circuit_breakers",
        ["tenant_id", "breaker_key"],
    )


def downgrade() -> None:
    op.drop_index("idx_runtime_safety_breaker_tenant_key", table_name="runtime_safety_circuit_breakers")
    op.drop_table("runtime_safety_circuit_breakers")
    op.drop_index("idx_runtime_safety_switch_tenant_target", table_name="runtime_safety_kill_switches")
    op.drop_table("runtime_safety_kill_switches")
