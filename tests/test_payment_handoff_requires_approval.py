"""Payment handoff requires explicit human approval + a qualified opportunity."""

from core.safety.commercial import payment_handoff


def test_payment_handoff_without_approval_fails():
    res = payment_handoff({"qualified": True, "approved_by_human": False})
    assert res.allowed is False
    assert "payment_handoff_requires_human_approval" in res.reasons


def test_payment_handoff_unqualified_fails():
    res = payment_handoff({"qualified": False, "approved_by_human": True})
    assert res.allowed is False
    assert "payment_handoff_requires_qualified_opportunity" in res.reasons


def test_payment_handoff_with_approval_and_qualified_allowed():
    res = payment_handoff({"qualified": True, "approved_by_human": True})
    assert res.allowed is True
    assert res.requires_human is True
