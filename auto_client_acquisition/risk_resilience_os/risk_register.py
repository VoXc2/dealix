"""Risk taxonomy — twelve strategic risk families (design inputs, not blockers)."""

from __future__ import annotations

RISK_TAXONOMY_CATEGORIES: tuple[str, ...] = (
    "data_risk",
    "privacy_risk",
    "ai_output_risk",
    "agent_autonomy_risk",
    "channel_risk",
    "claim_risk",
    "client_risk",
    "delivery_risk",
    "partner_risk",
    "financial_risk",
    "market_risk",
    "strategic_drift_risk",
)

RISK_REGISTER_METADATA_FIELDS: tuple[str, ...] = (
    "owner",
    "severity",
    "likelihood",
    "control",
    "early_warning_signal",
    "response_plan",
    "test_or_checklist",
)


def risk_taxonomy_category_valid(category: str) -> bool:
    return category in RISK_TAXONOMY_CATEGORIES


def risk_register_metadata_complete(fields_present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [f for f in RISK_REGISTER_METADATA_FIELDS if f not in fields_present]
    return not missing, tuple(missing)
