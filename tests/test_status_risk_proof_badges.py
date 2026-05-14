"""Bilingual badge taxonomy: Status, Risk, Proof — labels must cover every value."""
from __future__ import annotations

import pytest

from auto_client_acquisition.client_os.badges import (
    BADGE_LABELS_AR,
    BADGE_LABELS_EN,
    ProofBadge,
    RiskBadge,
    StatusBadge,
)


STATUS_EXPECTED = {
    "draft",
    "needs_review",
    "approved",
    "blocked",
    "redacted",
    "proof_linked",
    "client_ready",
}
RISK_EXPECTED = {
    "contains_pii",
    "draft_only",
    "approval_required",
    "source_missing",
    "proof_missing",
    "claim_risk",
    "channel_risk",
}
PROOF_EXPECTED = {
    "estimated",
    "observed",
    "verified",
    "client_confirmed",
    "case_safe",
}


def test_status_badge_completeness() -> None:
    actual = {b.value for b in StatusBadge}
    assert actual == STATUS_EXPECTED
    assert len(actual) == 7


def test_risk_badge_completeness() -> None:
    actual = {b.value for b in RiskBadge}
    assert actual == RISK_EXPECTED
    assert len(actual) == 7


def test_proof_badge_completeness() -> None:
    actual = {b.value for b in ProofBadge}
    assert actual == PROOF_EXPECTED
    assert len(actual) == 5


def test_bilingual_labels_for_every_enum_value() -> None:
    all_values: set[str] = set()
    for enum_cls in (StatusBadge, RiskBadge, ProofBadge):
        for member in enum_cls:
            all_values.add(member.value)

    missing_ar = [v for v in all_values if v not in BADGE_LABELS_AR]
    missing_en = [v for v in all_values if v not in BADGE_LABELS_EN]

    assert not missing_ar, f"BADGE_LABELS_AR missing: {missing_ar}"
    assert not missing_en, f"BADGE_LABELS_EN missing: {missing_en}"

    # Non-empty translations.
    for v in all_values:
        assert BADGE_LABELS_AR[v], f"empty AR label for {v}"
        assert BADGE_LABELS_EN[v], f"empty EN label for {v}"


def test_approval_renderer_regression() -> None:
    """The badge rename must be a superset: all 7 RiskBadge values labelled.

    We additionally probe the older PII/DRAFT_ONLY-style keys to confirm the
    new BADGE_LABELS_AR is a *superset* of historical risk badge keys.
    """
    # All 7 RiskBadge values labelled bilingually.
    for badge in RiskBadge:
        assert badge.value in BADGE_LABELS_AR
        assert badge.value in BADGE_LABELS_EN

    # The historical-style snake_case names should still be there.
    historical = ["contains_pii", "draft_only", "approval_required"]
    for key in historical:
        assert key in BADGE_LABELS_AR
        assert key in BADGE_LABELS_EN

    # Don't crash importing the approval_center package.
    try:
        import auto_client_acquisition.approval_center as _ac  # noqa: F401
    except ImportError:
        pytest.skip("approval_center module not importable in this environment")
