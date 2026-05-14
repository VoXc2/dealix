"""Track B2 — Pricing → Checkout flow assertions.

Verifies:
- /checkout.html exists with all 5 priced tiers (sprint, growth, scale, partner, enterprise)
- /checkout-success.html exists and reads invoice_id from URL
- /pricing.html CTAs route to /checkout.html?tier=X
- NO_LIVE_CHARGE banner is visible on checkout.html
- VAT 15% wording present
- Footer trust badges present (polish rule)
"""

from __future__ import annotations

import re
from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


# ─── Files exist ──────────────────────────────────────────────────────


def test_checkout_html_exists():
    assert (LANDING / "checkout.html").exists()


def test_checkout_success_html_exists():
    assert (LANDING / "checkout-success.html").exists()


# ─── Checkout page content ────────────────────────────────────────────


def test_checkout_html_lists_all_pricing_tiers():
    html = _read("checkout.html")
    for key in ("sprint", "growth", "scale", "partner", "enterprise"):
        assert f"{key}:" in html or f'"{key}"' in html, f"checkout.html missing tier {key!r}"


def test_checkout_html_includes_amount_for_each_priced_tier():
    """Defensive: ensures the 4 priced tiers retain their canonical SAR amounts."""
    html = _read("checkout.html")
    for amount in ("499", "2999", "7999", "12000"):
        assert amount in html, f"checkout.html missing amount {amount!r}"


def test_checkout_html_has_no_live_charge_banner():
    html = _read("checkout.html")
    assert "NO_LIVE_CHARGE" in html, "checkout.html must visibly cite NO_LIVE_CHARGE"
    assert "TEST" in html, "checkout.html must label test mode"


def test_checkout_html_has_vat_wording():
    html = _read("checkout.html")
    assert "VAT" in html or "ضريبة" in html, "checkout.html must mention VAT"
    assert "15%" in html, "checkout.html must show 15% VAT figure"


def test_checkout_html_has_footer_trust_badges():
    html = _read("checkout.html")
    for badge in ("Saudi-PDPL", "Approval-first", "Proof-backed"):
        assert badge in html, f"checkout.html missing footer badge {badge!r}"


def test_checkout_html_posts_to_payment_ops_endpoint():
    html = _read("checkout.html")
    assert "/api/v1/payment-ops/invoice-intent" in html, (
        "checkout.html must integrate with existing payment_ops API"
    )


def test_checkout_html_handles_enterprise_tier_separately():
    html = _read("checkout.html")
    # Enterprise tier should redirect to mailto, not call invoice-intent
    assert "mailto:sales@dealix.sa" in html, (
        "checkout.html should provide mailto fallback for Enterprise"
    )


# ─── Checkout success page ────────────────────────────────────────────


def test_checkout_success_reads_invoice_id_from_url():
    html = _read("checkout-success.html")
    assert "invoice_id" in html, "checkout-success.html must read invoice_id query param"


def test_checkout_success_shows_vat_breakdown():
    html = _read("checkout-success.html")
    assert "VAT 15%" in html or "15%" in html, "success page should show VAT breakdown"


def test_checkout_success_has_no_live_charge_disclaimer():
    html = _read("checkout-success.html")
    assert "NO_LIVE_CHARGE" in html, "success page must reaffirm NO_LIVE_CHARGE"


def test_checkout_success_has_footer_trust_badges():
    html = _read("checkout-success.html")
    for badge in ("Saudi-PDPL", "Approval-first", "Proof-backed"):
        assert badge in html, f"checkout-success.html missing footer badge {badge!r}"


# ─── Pricing page wiring ──────────────────────────────────────────────


def test_pricing_ctas_route_to_checkout():
    html = _read("pricing.html")
    # 2026-Q2 ladder: priced tier cards link to /checkout.html?tier={sprint|retainer}.
    for tier_key in ("sprint", "retainer"):
        pattern = f"/checkout.html?tier={tier_key}"
        assert pattern in html, f"pricing.html missing CTA for tier={tier_key}"


def test_pricing_no_longer_routes_priced_tiers_to_launchpad():
    """Pre-Track-B2 the CTAs went to /launchpad.html (static). After Track B2
    they go to /checkout.html. The Free Diagnostic still routes to /diagnostic.html."""
    html = _read("pricing.html")
    # Find all .cta hrefs
    ctas = re.findall(r'class="cta"\s+href="([^"]+)"', html)
    # Allowed targets: /checkout.html?..., /diagnostic.html, mailto:
    for href in ctas:
        if href.startswith("mailto:"):
            continue
        assert (
            href.startswith("/checkout.html") or href == "/diagnostic.html"
        ), f"pricing.html CTA points to unexpected target: {href}"


# ─── robots.txt + llms.txt ────────────────────────────────────────────


def test_robots_txt_disallows_checkout_pages():
    robots = (LANDING / "robots.txt").read_text(encoding="utf-8")
    assert "Disallow: /checkout.html" in robots
    assert "Disallow: /checkout-success.html" in robots


def test_robots_txt_allows_ai_crawlers():
    robots = (LANDING / "robots.txt").read_text(encoding="utf-8")
    for bot in ("PerplexityBot", "ChatGPT-User", "GPTBot", "ClaudeBot"):
        assert f"User-agent: {bot}" in robots, f"robots.txt missing AI crawler {bot}"


def test_llms_txt_exists_and_lists_hard_gates():
    llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
    for gate in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_LINKEDIN_AUTOMATION",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
        "NO_UNAPPROVED_TESTIMONIAL",
    ):
        assert gate in llms, f"llms.txt missing hard gate {gate!r}"


def test_llms_txt_lists_pricing_tiers():
    llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
    assert "499 SAR" in llms
    assert "2,999 SAR" in llms or "2999 SAR" in llms
    assert "12,000 SAR" in llms or "12000 SAR" in llms


def test_llms_txt_includes_vision_2030_alignment():
    llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
    assert "Vision 2030" in llms
    assert "PDPL" in llms
