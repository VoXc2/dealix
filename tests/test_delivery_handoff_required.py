"""A won deal cannot move into execution without a delivery handoff."""

from core.safety.commercial import won_deal_handoff


def test_won_deal_without_delivery_handoff_fails():
    deal = {"won": True, "delivery_handoff": False, "customer_success_handoff": True}
    res = won_deal_handoff(deal)
    assert res.allowed is False
    assert "won_deal_requires_delivery_handoff" in res.reasons


def test_won_deal_with_delivery_handoff_ok():
    deal = {"won": True, "delivery_handoff": True, "customer_success_handoff": True}
    assert won_deal_handoff(deal).allowed is True
