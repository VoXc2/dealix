"""PII / sensitivity classification helpers (taxonomy, not ML detection)."""

from __future__ import annotations

PII_SENSITIVITY_LEVELS: tuple[str, ...] = ("low", "medium", "high")


def pii_sensitivity_valid(level: str) -> bool:
    return level in PII_SENSITIVITY_LEVELS


def external_blocked_without_passport_permission(*, passport_external_allowed: bool) -> bool:
    """Passport says external not allowed → block external execution."""
    return not passport_external_allowed


def pii_plus_external_requires_approval(*, contains_pii: bool, external_action_requested: bool) -> bool:
    """PII present and external action requested → human approval path required."""
    return contains_pii and external_action_requested
