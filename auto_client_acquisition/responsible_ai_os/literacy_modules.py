"""AI Literacy modules — enablement as part of the product."""

from __future__ import annotations

LITERACY_MODULE_IDS: tuple[str, ...] = (
    "ai_for_executives",
    "ai_for_sales_operators",
    "ai_governance_basics",
    "data_readiness_for_ai",
    "responsible_ai_outreach",
    "company_brain_usage",
)


def literacy_modules_complete(completed: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [m for m in LITERACY_MODULE_IDS if m not in completed]
    return not missing, tuple(missing)
