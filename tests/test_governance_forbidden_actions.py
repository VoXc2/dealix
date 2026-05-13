"""Governance OS — forbidden claims and approval matrix tests.

اختبارات Governance OS — الادعاءات الممنوعة ومصفوفة الموافقات.

Guards `dealix/trust/forbidden_claims.py` and `dealix/trust/approval_matrix.py`:
banned phrases are flagged in Arabic and English, the approval matrix returns
CSM for OUTBOUND_EMAIL at evidence L2, and lower evidence escalates the role.
"""
from __future__ import annotations

import pytest

pytest.importorskip("pydantic", reason="pydantic required for governance modules")


def test_arabic_guarantee_phrase_is_blocked():
    from dealix.trust.forbidden_claims import scan_text

    scan = scan_text("نضمن لك أفضل النتائج في المملكة")
    assert scan.has_forbidden is True
    assert any(h.language == "ar" for h in scan.hits)


def test_english_guarantee_phrase_is_blocked():
    from dealix.trust.forbidden_claims import scan_text

    scan = scan_text("we guarantee outstanding outcomes")
    assert scan.has_forbidden is True
    assert any(h.language == "en" for h in scan.hits)


def test_best_in_saudi_phrase_is_blocked():
    from dealix.trust.forbidden_claims import scan_text

    scan = scan_text("the best in saudi consulting firm")
    assert scan.has_forbidden is True


def test_risk_free_phrase_is_blocked():
    from dealix.trust.forbidden_claims import assert_clean

    with pytest.raises(ValueError):
        assert_clean("our service is risk-free and proven")


def test_clean_marketing_message_passes():
    """Negative path — a neutral, professional message must pass."""
    from dealix.trust.forbidden_claims import assert_clean, scan_text

    text = "Our team delivers measurable outcomes for Saudi enterprises."
    assert scan_text(text).has_forbidden is False
    assert_clean(text)  # should not raise


def test_outbound_email_evidence_l2_requires_csm():
    from dealix.trust.approval_matrix import (
        ActionKind,
        ApproverRole,
        required_approver,
    )

    req = required_approver(ActionKind.OUTBOUND_EMAIL, evidence_level=2)
    assert req.approver == ApproverRole.CSM
    assert req.min_evidence_level == 2


def test_low_evidence_escalates_to_higher_role():
    from dealix.trust.approval_matrix import (
        ActionKind,
        ApproverRole,
        required_approver,
    )

    # OUTBOUND_EMAIL min L2 → at L1 should escalate from CSM to HEAD_CS.
    req = required_approver(ActionKind.OUTBOUND_EMAIL, evidence_level=1)
    assert req.approver == ApproverRole.HEAD_CS
    assert "Escalated" in req.reason_en


def test_policy_override_always_requires_ceo():
    from dealix.trust.approval_matrix import (
        ActionKind,
        ApproverRole,
        required_approver,
    )

    req = required_approver(ActionKind.POLICY_OVERRIDE, evidence_level=5)
    assert req.approver == ApproverRole.CEO
