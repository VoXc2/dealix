"""Business unit scorecard — documented dimensions."""

from __future__ import annotations

from typing import Final

BUSINESS_UNIT_SCORECARD_FIELDS: Final[tuple[str, ...]] = (
    "revenue",
    "retainers",
    "playbook_maturity",
    "product_module_usage",
    "proof_library",
    "owner_readiness",
    "venture_score",
)
