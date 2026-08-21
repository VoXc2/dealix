"""Public commercial-surface contracts for the quote-only first launch.

The current launch has one customer path:
Free Mini Diagnostic -> qualified discovery -> quote-only 30-day
Revenue Command Pilot -> verified proof -> evidence-based expansion.

These tests deliberately reject the retired fixed-price/self-serve ladder and
prevent capability pages from becoming parallel commercial products.
"""

from __future__ import annotations

from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"
RETIRED_PRICE_TOKENS = ("499", "1500", "1,500", "2999", "2,999", "7999", "7,999", "12000", "12,000")
RETIRED_TIER_NAMES = (
    "Revenue Proof Sprint",
    "Growth OS",
    "Scale OS",
    "Executive Command Center",
    "Data Pack",
)


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


def test_public_commercial_pages_exist() -> None:
    for name in (
        "pricing.html",
        "services.html",
        "checkout.html",
        "checkout-success.html",
        "llms.txt",
    ):
        assert (LANDING / name).exists(), name


def test_pricing_page_exposes_one_quote_only_launch_path() -> None:
    html = _read("pricing.html")
    for required in (
        "Free Mini Diagnostic",
        "Revenue Command Pilot — 30 يومًا",
        "Quote-only",
        "30-day Pilot",
        "Weekly Proof Pack",
        "Final Proof Pack",
        "NO_LIVE_CHARGE",
        "لا Checkout حي",
    ):
        assert required in html, required
    assert 'href="/diagnostic.html"' in html
    assert 'href="/proof.html"' in html


def test_pricing_page_has_no_retired_price_ladder_or_checkout_cta() -> None:
    html = _read("pricing.html")
    for token in RETIRED_PRICE_TOKENS:
        assert token not in html, token
    for name in RETIRED_TIER_NAMES:
        assert name not in html, name
    assert "/checkout.html?tier=" not in html
    assert "إكمال الاشتراك" not in html
    assert "VAT 15%" not in html
    assert "SLA 99.9%" not in html
    assert "price-lock" not in html


def test_services_page_is_capability_map_under_one_product() -> None:
    html = _read("services.html")
    for required in (
        "One Product",
        "Dealix منتج واحد",
        "Revenue + Proof + Command",
        "Free Mini Diagnostic",
        "Revenue Command Pilot — 30 يومًا",
        "Company Brain + Business Graph",
        "Daily Executive Command",
        "Governed Execution",
        "Proof + Learning + Model Router",
    ):
        assert required in html, required
    assert "سلّم العروض" not in html
    assert "Saudi Opportunity Snapshot" not in html
    assert "AI Company OS Setup" not in html
    assert "Partner & Distributor Desk" not in html
    assert "Revenue Proof Sprint" not in html
    assert 'href="/diagnostic.html"' in html
    assert 'href="/pricing.html"' in html
    assert "sami.assiri11@gmail.com" not in html


def test_checkout_is_hard_blocked_before_named_customer_quote() -> None:
    html = _read("checkout.html")
    for required in (
        "NO_LIVE_CHARGE",
        "QUOTE_ONLY",
        "NO_PUBLIC_FIXED_PRICE",
        "NO_SELF_SERVE_CHECKOUT",
        "REQUEST ≠ QUOTE ≠ INVOICE ≠ PAYMENT ≠ REVENUE",
    ):
        assert required in html, required
    assert "/diagnostic.html" in html
    assert "/proof.html" in html


def test_checkout_has_no_payment_intent_or_customer_input_form() -> None:
    html = _read("checkout.html")
    assert "/api/v1/payment-ops/invoice-intent" not in html
    assert "TIERS=" not in html
    assert "fetch(" not in html
    assert "<form" not in html
    assert "amount_sar" not in html
    assert "bank_transfer_manual" not in html
    for token in RETIRED_PRICE_TOKENS:
        assert token not in html, token


def test_checkout_success_is_a_legacy_fail_closed_surface() -> None:
    html = _read("checkout-success.html")
    for required in (
        "Checkout العام غير مفعّل",
        "NO_LIVE_CHARGE",
        "NO_PUBLIC_FIXED_PRICE",
        "NO_SELF_SERVE_CHECKOUT",
        "REQUEST ≠ QUOTE ≠ INVOICE ≠ PAYMENT ≠ REVENUE",
    ):
        assert required in html, required
    assert "request_id" not in html
    assert "tier-label" not in html
    assert "amount-shown" not in html
    assert "payment_received" not in html
    for token in RETIRED_PRICE_TOKENS:
        assert token not in html, token


def test_robots_txt_disallows_checkout_pages() -> None:
    robots = _read("robots.txt")
    assert "Disallow: /checkout.html" in robots
    assert "Disallow: /checkout-success.html" in robots


def test_llms_txt_lists_current_hard_gates() -> None:
    llms = _read("llms.txt")
    for gate in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_LINKEDIN_AUTOMATION",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
        "NO_UNAPPROVED_TESTIMONIAL",
        "NO_UNPROVEN_COMPLIANCE_CLAIM",
    ):
        assert gate in llms, gate


def test_llms_txt_matches_quote_only_authority() -> None:
    llms = _read("llms.txt")
    for required in (
        "Saudi-first AI Business Operating System",
        "Revenue + Proof + Command",
        "Free Mini Diagnostic",
        "Revenue Command Pilot — 30 days",
        "no public fixed first-launch price",
        "no public self-serve checkout",
        "founder-approved named-customer quote",
    ):
        assert required.lower() in llms.lower(), required
    for token in RETIRED_PRICE_TOKENS:
        assert token not in llms, token
    for name in RETIRED_TIER_NAMES:
        assert name not in llms, name
    assert "Saudi data residency" not in llms
    assert "Pricing is **transparent**" not in llms


def test_llms_txt_does_not_claim_payment_intent_is_public_offer() -> None:
    llms = _read("llms.txt")
    assert "POST /api/v1/payment-ops/invoice-intent" not in llms
    assert "VAT 15% included" not in llms
    assert "full refund" not in llms.lower()
