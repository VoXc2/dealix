"""Claim compliance — statuses for client-facing and case materials."""

from __future__ import annotations

CLAIM_STATUSES: tuple[str, ...] = ("UNSUPPORTED", "ESTIMATED", "OBSERVED", "VERIFIED")


def claim_status_valid(status: str) -> bool:
    return status in CLAIM_STATUSES


def claim_allowed_in_client_output(status: str) -> bool:
    """UNSUPPORTED must not ship to clients."""
    return status != "UNSUPPORTED"


def claim_allowed_in_case_safe_summary(status: str, *, client_permission: bool) -> bool:
    return status == "VERIFIED" and client_permission
