"""Merge Alembic heads: UUID branch (0001) + Saudi auth/compliance branch (003).

Revision ID: 004_merge_heads
Revises: 0001, 003
Create Date: 2026-05-08

The repo had two independent roots (0001 vs 001→002→003). This revision
unifies history so `alembic upgrade head` applies both lineages exactly once.
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "004_merge_heads"
down_revision: Union[str, tuple[str, ...], None] = ("0001", "003")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op merge — both parent branches already applied their DDL."""
    pass


def downgrade() -> None:
    """Merge points cannot be split safely; no-op."""
    pass
