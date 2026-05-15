"""Enterprise control plane: runtime safety tables."""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "016"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "015"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "runtime_safety_kill_switches",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("agent_id", sa.String(length=64), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("activated_by", sa.String(length=128), nullable=True),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("tenant_id", "agent_id", name="pk_runtime_safety_kill_switches"),
    )
    op.create_table(
        "runtime_safety_circuit_breakers",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("breaker_key", sa.String(length=128), nullable=False),
        sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("threshold", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="closed"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("tenant_id", "breaker_key", name="pk_runtime_safety_circuit_breakers"),
    )


def downgrade() -> None:
    op.drop_table("runtime_safety_circuit_breakers")
    op.drop_table("runtime_safety_kill_switches")
