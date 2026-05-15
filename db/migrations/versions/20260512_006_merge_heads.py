"""merge orphan revision 0001 with main chain at 005 — joins multiple alembic heads

Revision ID: 006
Revises: 005, 0001
Create Date: 2026-05-12 20:30:00.000000

Why
- Two root revisions exist in this project: `0001` (uuid_softdelete_indexes)
  and `001` (auth_schema). The `0001` chain stops at itself; the `001` chain
  grew to `001 → 002 → 003 → 004 → 005`.
- `alembic upgrade head` (singular) fails with "multiple heads" until they're
  joined. CI / Railway deploy / scripts/check_alembic_heads.sh all assume a
  single head.
- This is a no-op merge revision (no schema change). It only updates the
  alembic_version table to declare both ancestors as joined.

Operator note
- After this is in main, both head revisions are reachable from a single tip.
  `alembic upgrade head` works again. `alembic downgrade` from `006` returns
  to both `0001` and `005` in their respective branches.
"""

from __future__ import annotations

from typing import Sequence, Union

# Alembic reads these module-level names via runtime introspection
# (script.py.mako template + ScriptDirectory.walk_revisions). Static
# analyzers cannot see that use, so they flag them as unused — they
# are not. `__all__` makes the export explicit.
__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "006"  # noqa: F841 — read by Alembic via introspection
down_revision: Union[str, Sequence[str], None] = ("005", "0001")  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    # No schema changes. This revision exists solely to merge two
    # previously-disjoint head revisions in the alembic graph.
    pass


def downgrade() -> None:
    pass
