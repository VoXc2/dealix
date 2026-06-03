"""A won deal must hand off to customer success (and delivery) before work."""

from core.safety.commercial import won_deal_handoff


def test_won_deal_without_cs_handoff_fails():
    deal = {"stage": "won", "delivery_handoff": True, "customer_success_handoff": False}
    res = won_deal_handoff(deal)
    assert res.allowed is False
    assert "won_deal_requires_customer_success_handoff" in res.reasons


def test_won_deal_with_both_handoffs_passes():
    deal = {"stage": "won", "delivery_handoff": True, "customer_success_handoff": True}
    res = won_deal_handoff(deal)
    assert res.allowed is True


def test_open_deal_not_gated():
    res = won_deal_handoff({"stage": "proposal"})
    assert res.allowed is True
