"""Commercial truth contracts for retired public checkout surfaces.

The current first-launch authority is deliberately fail-closed:
Free Mini Diagnostic -> qualified discovery -> named-customer quote ->
30-day Revenue Command Pilot. Public checkout/payment initiation is retired.
These tests prevent the older TEST invoice-intent flow from reappearing.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / "landing" / "checkout.html"
SUCCESS = ROOT / "landing" / "checkout-success.html"

FORBIDDEN_PUBLIC_CLAIMS = (
    "حتّى 2,500 lead/شهر",
    "Lead غير محدود",
    "SLA 99.9%",
    "دعم خلال 4 ساعات",
    "Next Best Offer تلقائي",
    "WhatsApp approval flow",
    "Moyasar invoicing مدمج",
    "الفاتورة جاهزة",
    "سيتواصل معك المؤسس خلال 24 ساعة",
    "Proof Pack جاهز يوم 7",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkout_is_explicitly_quote_only_not_live_revenue() -> None:
    text = _text(CHECKOUT)
    for required in (
        "NO_LIVE_CHARGE",
        "QUOTE_ONLY",
        "NO_PUBLIC_FIXED_PRICE",
        "NO_SELF_SERVE_CHECKOUT",
        "REQUEST ≠ QUOTE ≠ INVOICE ≠ PAYMENT ≠ REVENUE",
        "Free Mini Diagnostic",
    ):
        assert required in text
    assert "لا يوجد Checkout عام" in text
    assert "لا يُسجل الإيراد إلا بعد دليل payment_received" in text


def test_success_page_is_a_fail_closed_legacy_surface() -> None:
    text = _text(SUCCESS)
    for required in (
        "Checkout العام غير مفعّل",
        "NO_LIVE_CHARGE",
        "NO_PUBLIC_FIXED_PRICE",
        "NO_SELF_SERVE_CHECKOUT",
        "REQUEST ≠ QUOTE ≠ INVOICE ≠ PAYMENT ≠ REVENUE",
        "لم يتم إنشاء Invoice أو Payment request",
        "لم يتم خصم أي مبلغ",
        "لم يبدأ تنفيذ خدمة",
    ):
        assert required in text
    assert "request_id" not in text
    assert "invoice_id" not in text
    assert "test_request_recorded" not in text


def test_unverified_capacity_sla_and_automation_claims_are_absent() -> None:
    combined = _text(CHECKOUT) + "\n" + _text(SUCCESS)
    for claim in FORBIDDEN_PUBLIC_CLAIMS:
        assert claim.casefold() not in combined.casefold()


def test_retired_payment_request_flow_cannot_reappear() -> None:
    combined = _text(CHECKOUT) + "\n" + _text(SUCCESS)
    for retired in (
        "/api/v1/payment-ops/invoice-intent",
        "bank_transfer_manual",
        "TIERS=",
        "amount_sar",
        "test_request_recorded",
        "وضع TEST",
    ):
        assert retired not in combined
    assert "<form" not in _text(CHECKOUT)
    assert "fetch(" not in _text(CHECKOUT)


def test_checkout_routes_back_to_diagnostic_not_payment() -> None:
    checkout = _text(CHECKOUT)
    success = _text(SUCCESS)
    assert 'href="/diagnostic.html"' in checkout
    assert 'href="/diagnostic.html"' in success
    assert "qualified discovery" in success.lower()
    assert "quote-only 30-day Revenue Command Pilot" in success
