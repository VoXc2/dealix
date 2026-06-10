"""Future: read normalized ledger rows from stores. Today: ledger names registry only."""

from __future__ import annotations

from typing import Final

LEDGER_NAMES: Final[tuple[str, ...]] = (
    "ai_run",
    "audit",
    "proof",
    "capital",
    "productization",
    "client_health",
    "unit_performance",
    "partner",
    "venture_signal",
)
