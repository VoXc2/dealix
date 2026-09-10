"""Tier-1 public product assertions for the current Dealix launch.

The original May-2026 redesign tested a six-tier price ladder, Agency Partner
funnel, PDPL-ready badge and self-serve checkout. Those are no longer launch
authority. The current Tier-1 contract is one product and one governed path:

Free Mini Diagnostic -> qualified discovery -> quote-only 30-day Revenue
Command Pilot -> verified Proof -> evidence-based expansion.

Keep the useful UX invariants (short H1, primary diagnostic CTA, simple nav,
DEMO label, stable anchors, customer-portal hierarchy, L1-L5 evidence ladder,
and eight hard gates) while rejecting the retired commercial funnel.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from defusedxml import ElementTree

LANDING = Path(__file__).resolve().parents[1] / "landing"


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


# ─── Homepage positioning ─────────────────────────────────────────────


def test_index_h1_positions_dealix_as_operating_system() -> None:
    html = _read("index.html")
    h1_match = re.search(r'<h1[^>]*class="hero__title"[^>]*>([^<]+)</h1>', html)
    assert h1_match, "hero H1 with class 'hero__title' not found"
    h1_text = h1_match.group(1).strip()
    assert "نظام تشغيل" in h1_text or "Business Operating System" in h1_text


def test_index_hero_h1_word_count_within_tier1_bound() -> None:
    html = _read("index.html")
    h1_match = re.search(r'<h1[^>]*class="hero__title"[^>]*>([^<]+)</h1>', html)
    assert h1_match
    word_count = len(h1_match.group(1).strip().split())
    assert word_count <= 8, f"hero H1 has {word_count} words; target <= 8"


def test_index_primary_cta_points_to_diagnostic() -> None:
    html = _read("index.html")
    cta_section = re.search(
        r'<div class="hero__ctas">(.*?)</div>', html, flags=re.DOTALL
    )
    assert cta_section, "hero CTA block not found"
    body = cta_section.group(1)
    for anchor in re.finditer(r'<a\s+([^>]+)>', body):
        attrs = anchor.group(1)
        if "btn--primary" in attrs:
            href = re.search(r'href="([^"]+)"', attrs)
            assert href
            assert href.group(1) == "/diagnostic.html"
            return
    pytest.fail("hero primary CTA <a class containing 'btn--primary'> not found")


def test_index_states_one_product_and_current_wedge() -> None:
    html = _read("index.html")
    assert "One product" in html
    assert "Revenue + Proof + Command" in html
    assert "Company Operating Layer" in html
    assert "Saudi-first" in html
    assert "Approval-first" in html
    assert "Proof-backed" in html


# ─── Nav simplification ───────────────────────────────────────────────


def test_index_nav_has_at_most_seven_primary_links() -> None:
    html = _read("index.html")
    nav_block = re.search(
        r'<nav class="nav__links"[^>]*>(.*?)</nav>', html, flags=re.DOTALL
    )
    assert nav_block, "<nav class='nav__links'> not found"
    body = nav_block.group(1)
    body_no_panel = re.sub(
        r'<div class="ds-mega-menu__panel".*?</div>\s*</div>',
        "",
        body,
        flags=re.DOTALL,
    )
    primary_links = re.findall(r'<a\s+[^>]*href=', body_no_panel)
    assert len(primary_links) <= 7


def test_index_nav_has_current_surface_mega_menu() -> None:
    html = _read("index.html")
    assert "ds-mega-menu" in html
    assert "ds-mega-menu__panel" in html
    for surface in (
        "/diagnostic.html",
        "/pricing.html",
        "/proof.html",
        "/trust-center.html",
        "/privacy.html",
        "/terms.html",
    ):
        assert surface in html
    for retired in (
        "/roi.html",
        "/agency-partner.html",
        "/ai-team.html",
        "/checkout.html?tier=",
    ):
        assert retired not in html


# ─── Daily operating layer demo ──────────────────────────────────────


def test_index_has_wadl_section() -> None:
    html = _read("index.html")
    assert 'id="wadl"' in html


def test_index_wadl_is_explicitly_demo_not_customer_proof() -> None:
    html = _read("index.html")
    wadl_block = re.search(r'id="wadl"(.*?)</section>', html, flags=re.DOTALL)
    assert wadl_block
    body = wadl_block.group(1)
    assert "DEMO" in body
    assert "ليس Claim لنتيجة عميل" in body
    for phase in ("See reality", "Decide", "Prepare", "Prove"):
        assert phase in body


# ─── Homepage anchor preservation ─────────────────────────────────────


def test_index_anchor_ids_preserved() -> None:
    html = _read("index.html")
    for anchor in (
        "pillars",
        "for-who",
        "sectors",
        "how",
        "trust",
        "proof",
        "pricing",
        "faq",
        "pilot",
        "wadl",
    ):
        assert f'id="{anchor}"' in html, f"anchor #{anchor} removed from homepage"


# ─── Current first-launch path ────────────────────────────────────────


def test_index_exposes_quote_only_pilot_not_fixed_price_ladder() -> None:
    html = _read("index.html")
    assert "Free Mini Diagnostic" in html
    assert "30-day Revenue Command Pilot" in html
    assert "الـPilot quote-only" in html
    assert "لا 499" in html
    assert "لا tiers عامة" in html
    assert "لا self-serve checkout" in html
    assert "/checkout.html?tier=" not in html


def test_pricing_is_quote_only_not_six_tiers() -> None:
    html = _read("pricing.html")
    assert "Free Mini Diagnostic" in html
    assert "Revenue Command Pilot — 30 يومًا" in html
    assert "Quote-only" in html
    assert "Weekly Proof Pack" in html
    assert "Final Proof Pack" in html
    assert not re.search(r'<div class="plan(?:\s[^"]*)?"', html)
    assert "499" not in html
    assert "/checkout.html?tier=" not in html


def test_checkout_is_fail_closed() -> None:
    html = _read("checkout.html")
    for code in (
        "NO_LIVE_CHARGE",
        "QUOTE_ONLY",
        "NO_PUBLIC_FIXED_PRICE",
        "NO_SELF_SERVE_CHECKOUT",
    ):
        assert code in html
    assert "/api/v1/payment-ops/invoice-intent" not in html
    assert "<form" not in html


# ─── Public Diagnostic ────────────────────────────────────────────────


def test_diagnostic_matches_canonical_free_entry() -> None:
    html = _read("diagnostic.html")
    for output in (
        "Credible leak hypothesis",
        "Written diagnosis",
        "Missing-evidence report",
        "Pilot hypothesis",
    ):
        assert output in html
    assert "NO_PII_CAPTURE" in html
    assert "NO_LEAD_PERSISTENCE" in html
    assert "/api/v1/public/demo-request" not in html
    for pii_field in ('name="contact_name"', 'name="phone"', 'name="email"'):
        assert pii_field not in html


# ─── Customer portal Today's Decision hero ────────────────────────────


def test_customer_portal_is_retired_to_current_proof_surface() -> None:
    html = _read("customer-portal.html")
    compact = html.replace(" ", "").lower()
    assert "DEALIX_RETIRED_PUBLIC_SURFACE" in html
    assert "noindex,nofollow" in compact
    assert "url=/proof.html" in html
    assert "synthetic" in html
    assert "دليل عميل" in html
    assert 'id="today-decision"' not in html
    assert 'id="ops-grid"' not in html


# ─── Proof page L1-L5 evidence ladder ─────────────────────────────────


def test_proof_has_l1_to_l5_ladder() -> None:
    html = _read("proof.html")
    for level in ("L1", "L2", "L3", "L4", "L5"):
        assert level in html
    assert "ds-evidence-ladder" in html


def test_proof_evidence_ladder_uses_correct_modifiers() -> None:
    html = _read("proof.html")
    for mod in ("ds-evidence-level--l1", "ds-evidence-level--l5"):
        assert mod in html


# ─── Trust Center ─────────────────────────────────────────────────────


def test_trust_center_lists_eight_hard_gates() -> None:
    html = _read("trust-center.html")
    for code in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_LINKEDIN_AUTOMATION",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
        "NO_UNAPPROVED_TESTIMONIAL",
    ):
        assert code in html


def test_trust_center_does_not_promote_compliance_as_certification() -> None:
    html = _read("trust-center.html")
    assert "لا يدّعي PDPL certification" in html
    assert "SOC 2" in html
    assert "Saudi data residency" in html
    assert "ما يزال مفتوحًا" in html
    assert "PDPL-ready" not in html


# ─── Services / one-product capability map ────────────────────────────


def test_services_is_one_product_capability_map() -> None:
    html = _read("services.html")
    assert "Dealix منتج واحد" in html
    assert "Revenue + Proof + Command" in html
    assert "Company Brain + Business Graph" in html
    assert "Governed Execution" in html
    assert "Saudi Market & Partnership Intelligence" in html
    for retired_offer in (
        "Revenue Proof Sprint",
        "Saudi Opportunity Snapshot",
        "AI Company OS Setup",
        "Partner & Distributor Desk",
    ):
        assert retired_offer not in html


# ─── SEO/indexing boundary ────────────────────────────────────────────


def test_current_sitemaps_use_dealix_me_only() -> None:
    for name in ("sitemap.xml", "sitemap_dealix.xml"):
        root = ElementTree.fromstring(_read(name))
        raw_urls = [
            element.text.strip()
            for element in root.findall(".//{*}loc")
            if element.text and element.text.strip()
        ]
        assert raw_urls, f"{name} contains no sitemap URLs"
        parsed_urls = [urlsplit(url) for url in raw_urls]
        assert all(parsed.scheme == "https" for parsed in parsed_urls)
        assert all(parsed.hostname == "dealix.me" for parsed in parsed_urls)
        assert all(parsed.port is None for parsed in parsed_urls)
        paths = {parsed.path for parsed in parsed_urls}
        assert "/" in paths
        for current in (
            "/diagnostic.html",
            "/pricing.html",
            "/services.html",
            "/proof.html",
            "/trust-center.html",
        ):
            assert current in paths
        retired_paths = {"/agency-partner.html", "/roi.html"}
        assert paths.isdisjoint(retired_paths)


def test_robots_quarantines_retired_funnels() -> None:
    robots = _read("robots.txt")
    for path in (
        "/checkout.html",
        "/annual-pricing.html",
        "/roi.html",
        "/agency-partner.html",
        "/partners.html",
        "/start.html",
    ):
        assert f"Disallow: {path}" in robots


# ─── Current trust identity on reviewed public pages ──────────────────


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
        "trust-center.html",
    ],
)
def test_current_tier1_pages_carry_evidence_bound_trust_identity(page: str) -> None:
    html = _read(page)
    assert "Saudi-first" in html
    assert "Approval-first" in html
    assert "Proof-backed" in html
