"""
Safe-action gateway invariants.

Verifies the ActionMode enum completeness and that the bilingual classifier
respects the gateway contract: nothing leaks past a BLOCKED decision.
"""

from __future__ import annotations

from auto_client_acquisition.safety import ActionMode, classify_intent


def test_action_mode_has_exactly_five_modes() -> None:
    assert {m.value for m in ActionMode} == {
        "suggest_only",
        "draft_only",
        "approval_required",
        "approved_execute",
        "blocked",
    }


def test_blocked_decision_has_no_bundle() -> None:
    """When action_mode==BLOCKED the operator must NOT recommend a bundle."""
    d = classify_intent("أبي أرسل واتساب لأرقام مشتريها")
    assert d.action_mode == ActionMode.BLOCKED
    assert d.recommended_bundle is None
    assert d.blocked_reasons


def test_blocked_decision_includes_safe_alternatives() -> None:
    d = classify_intent("cold whatsapp blast")
    assert d.action_mode == ActionMode.BLOCKED
    assert "linkedin_manual_warm_intro" in d.safe_alternatives
    assert "inbound_wa_me_link" in d.safe_alternatives
    assert "opt_in_form" in d.safe_alternatives
    assert "email_draft_with_approval" in d.safe_alternatives
    assert "customer_initiated_whatsapp" in d.safe_alternatives


def test_blocked_decision_provides_reason_in_both_languages() -> None:
    d = classify_intent("أبي البوت يشطح على الناس بالواتساب")
    assert d.action_mode == ActionMode.BLOCKED
    assert d.reason_ar
    assert d.reason_en


def test_default_recommendation_is_approval_required_not_execute() -> None:
    """A safe recommendation must require human approval — never auto-execute."""
    d = classify_intent("I need more B2B leads")
    assert d.action_mode in {
        ActionMode.SUGGEST_ONLY,
        ActionMode.DRAFT_ONLY,
        ActionMode.APPROVAL_REQUIRED,
    }
    assert d.action_mode != ActionMode.APPROVED_EXECUTE
