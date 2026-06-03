"""A positive reply routes to booking/WhatsApp/proof — never straight to payment."""
from _util import decide

SAFE_ROUTES = ["booking", "whatsapp_welcome", "proof_pack_review", "readiness_scan"]
UNSAFE_ROUTES = ["direct_payment", "send_payment_link"]


def test_positive_reply_to_payment_is_rejected():
    assert decide({"event": "positive_reply", "proposed_route": "direct_payment"}) == "reject"


def test_positive_reply_to_safe_routes_is_allowed():
    for route in SAFE_ROUTES:
        assert decide({"event": "positive_reply", "proposed_route": route}) == "allow", route


def test_unsafe_routes_all_rejected():
    for route in UNSAFE_ROUTES:
        assert decide({"event": "positive_reply", "proposed_route": route}) == "reject", route
