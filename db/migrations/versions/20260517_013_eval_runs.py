"""Evals OS — eval runs + results.

Companion to ``auto_client_acquisition/evals_os/`` (Wave 16). The runtime
spine uses the JSONL eval ledger; these tables are the DB-backed upgrade
path.

Migration 013.
Down revision: 012 (agent_loop_traces).
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "013"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "012"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "eval_runs",
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("customer_id", sa.String(length=128), nullable=False),
        sa.Column("suite_id", sa.String(length=64), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pass_rate", sa.Float(), nullable=False, server_default="0"),
        sa.Column(
            "regression_detected",
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
        sa.PrimaryKeyConstraint("run_id", name="pk_eval_runs"),
    )
    op.create_index(
        "ix_eval_runs_customer_suite",
        "eval_runs",
        ["customer_id", "suite_id", "occurred_at"],
    )

    op.create_table(
        "eval_results",
        sa.Column("result_id", sa.String(length=64), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("case_id", sa.String(length=128), nullable=False),
        sa.Column("suite_id", sa.String(length=64), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("failures", sa.JSON(), nullable=True),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["run_id"], ["eval_runs.run_id"], name="fk_eval_results_run"
        ),
        sa.PrimaryKeyConstraint("result_id", name="pk_eval_results"),
    )
    op.create_index("ix_eval_results_run", "eval_results", ["run_id"])


def downgrade() -> None:
    op.drop_index("ix_eval_results_run", table_name="eval_results")
    op.drop_table("eval_results")

    op.drop_index("ix_eval_runs_customer_suite", table_name="eval_runs")
    op.drop_table("eval_runs")
