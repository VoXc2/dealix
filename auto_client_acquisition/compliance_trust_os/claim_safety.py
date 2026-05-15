"""Claim safety — forbidden commercial patterns + re-export claim status gates."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.claim_compliance import (
    CLAIM_STATUSES,
    claim_allowed_in_case_safe_summary,
    claim_allowed_in_client_output,
    claim_status_valid,
)

FORBIDDEN_CLAIM_PATTERNS: tuple[str, ...] = (
    "guaranteed_sales",
    "guaranteed_leads",
    "strongest_ai_in_market",
    "unverified_roi_percentage",
    "case_study_without_permission",
)


def forbidden_claim_pattern_listed(pattern: str) -> bool:
    return pattern in FORBIDDEN_CLAIM_PATTERNS


def claim_estimated_requires_caveat(status: str) -> bool:
    """ESTIMATED claims must carry explicit caveat in client-facing materials."""
    return status == "ESTIMATED"


__all__ = (
    "CLAIM_STATUSES",
    "FORBIDDEN_CLAIM_PATTERNS",
    "claim_allowed_in_case_safe_summary",
    "claim_allowed_in_client_output",
    "claim_estimated_requires_caveat",
    "claim_status_valid",
    "forbidden_claim_pattern_listed",
)
