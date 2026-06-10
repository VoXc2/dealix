"""ROI discipline — estimated vs observed vs verified."""

from __future__ import annotations

from enum import StrEnum


class RoiConfidence(StrEnum):
    ESTIMATED = "estimated"
    OBSERVED = "observed"
    VERIFIED = "verified"


def roi_safe_for_public_case(confidence: RoiConfidence) -> bool:
    """Only verified outcomes should anchor public case studies."""
    return confidence is RoiConfidence.VERIFIED


def roi_observed_ok_for_internal_report(confidence: RoiConfidence) -> bool:
    """Observed metrics are fine inside delivery / governance packs — not as advertising."""
    return confidence in (RoiConfidence.OBSERVED, RoiConfidence.VERIFIED)


def roi_must_label_distinct(
    estimated_used: bool,
    verified_claimed: bool,
) -> tuple[bool, tuple[str, ...]]:
    """Block ambiguous mixing when both estimated and verified are presented as one claim."""
    if estimated_used and verified_claimed:
        return False, ("separate_estimated_and_verified_labels_required",)
    return True, ()
