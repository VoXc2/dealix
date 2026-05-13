"""Claim Compliance — classify and gate marketing claims."""

from __future__ import annotations

from enum import Enum


class ClaimStatus(str, Enum):
    UNSUPPORTED = "unsupported"
    ESTIMATED = "estimated"
    OBSERVED = "observed"
    VERIFIED = "verified"


def classify_claim_status(
    *,
    has_baseline: bool,
    has_observation: bool,
    has_client_confirmation: bool,
) -> ClaimStatus:
    if has_client_confirmation:
        return ClaimStatus.VERIFIED
    if has_observation:
        return ClaimStatus.OBSERVED
    if has_baseline:
        return ClaimStatus.ESTIMATED
    return ClaimStatus.UNSUPPORTED


def can_use_in_marketing(status: ClaimStatus) -> bool:
    """Only VERIFIED claims may be used in public marketing."""

    return status is ClaimStatus.VERIFIED


def can_use_in_sales(status: ClaimStatus) -> bool:
    """OBSERVED + VERIFIED may be used in private sales conversations."""

    return status in {ClaimStatus.OBSERVED, ClaimStatus.VERIFIED}
