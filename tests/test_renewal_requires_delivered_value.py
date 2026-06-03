"""Renewal requires evidence of delivered value + completed delivery."""

from core.safety.commercial import renewal_allowed


def test_renewal_without_delivered_value_fails():
    res = renewal_allowed({"delivered_value": False, "delivery_completed": True})
    assert res.allowed is False
    assert "renewal_requires_delivered_value" in res.reasons


def test_renewal_without_completed_delivery_fails():
    res = renewal_allowed({"delivered_value": True, "delivery_completed": False})
    assert res.allowed is False
    assert "renewal_requires_completed_delivery" in res.reasons


def test_renewal_with_value_and_completion_allowed():
    res = renewal_allowed({"delivered_value": True, "delivery_completed": True})
    assert res.allowed is True
