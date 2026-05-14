"""Tier-1 Revenue Command Center frontend assertions.

These tests guard the May-2026 Tier-1 redesign: homepage repositioning,
WhatsApp Decision Layer (WADL), simplified nav, anchor pricing, L1-L5
proof ladder, 8 hard gates as features, agency-partner page, and
customer-portal Today's Decision hero.

Each assertion is intentionally narrow so we can pinpoint regressions
without flaky text-matching.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

LANDING = Path(__file__).resolve().parents[1] / "landing"


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


# ─── Homepage positioning ─────────────────────────────────────────────


def test_index_has_revenue_command_center_h1():
    """Hero H1 must reflect the Revenue Command Center positioning."""
    html = _read("index.html")
    h1_match = re.search(r'<h1[^>]*class="hero__title"[^>]*>([^<]+)</h1>', html)
    assert h1_match, "hero H1 with class 'hero__title' not found"
    h1_text = h1_match.group(1).strip()
    assert "غرفة قيادة" in h1_text or "Revenue Command Center" in h1_text, (
        f"hero H1 must contain Revenue Command Center positioning; got: {h1_text!r}"
    )


def test_index_hero_h1_word_count_within_tier1_bound():
    """Tier-1 H1s should be <= 8 words (research benchmark)."""
    html = _read("index.html")
    h1_match = re.search(r'<h1[^>]*class="hero__title"[^>]*>([^<]+)</h1>', html)
    assert h1_match
    word_count = len(h1_match.group(1).strip().split())
    assert word_count <= 8, f"hero H1 has {word_count} words; Tier-1 target <= 8"


def test_index_primary_cta_points_to_diagnostic():
    """Hero primary CTA should funnel into Mini Diagnostic (Free)."""
    html = _read("index.html")
    cta_section = re.search(
        r'<div class="hero__ctas">(.*?)</div>', html, flags=re.DOTALL
    )
    assert cta_section, "hero CTA block not found"
    body = cta_section.group(1)
    # Find the <a> tag whose class includes 'btn--primary' (attribute order
    # may vary).
    for anchor in re.finditer(r'<a\s+([^>]+)>', body):
        attrs = anchor.group(1)
        if "btn--primary" in attrs:
            href = re.search(r'href="([^"]+)"', attrs)
            assert href, "primary CTA missing href"
            assert "/diagnostic.html" in href.group(1), (
                f"primary CTA should target /diagnostic.html; got {href.group(1)!r}"
            )
            return
    pytest.fail("hero primary CTA <a class containing 'btn--primary'> not found")


# ─── Nav simplification ───────────────────────────────────────────────


def test_index_nav_has_at_most_nine_primary_links():
    """Primary nav must shrink from 35+ to <= 9 visible links.

    Originally Tier-1 target was 6-7. Wave 19+ Operational Closure
    intentionally added /verify.html (CISO-facing live verify page) and
    /dealix-os.html (open framework positioning) as primary surfaces
    between Promise and Customer Portal — these are reviewer-facing and
    must be one click from the home page.
    """
    html = _read("index.html")
    nav_block = re.search(
        r'<nav class="nav__links"[^>]*>(.*?)</nav>', html, flags=re.DOTALL
    )
    assert nav_block, "<nav class='nav__links'> not found"
    # Count direct <a> children (not those inside the mega-menu panel)
    body = nav_block.group(1)
    # Strip out the mega-menu panel (its links don't count as primary)
    body_no_panel = re.sub(
        r'<div class="ds-mega-menu__panel".*?</div>\s*</div>',
        "",
        body,
        flags=re.DOTALL,
    )
    primary_links = re.findall(r'<a\s+[^>]*href=', body_no_panel)
    assert len(primary_links) <= 9, (
        f"primary nav has {len(primary_links)} links; Tier-1 target <= 9 "
        "(7 baseline + 2 Wave 19+ reviewer surfaces: verify.html + dealix-os.html)"
    )


def test_index_nav_has_mega_menu():
    """The mega-menu must be present so removed pages remain reachable."""
    html = _read("index.html")
    assert "ds-mega-menu" in html, "ds-mega-menu component missing from nav"
    assert "ds-mega-menu__panel" in html, "ds-mega-menu__panel missing"


# ─── WhatsApp Decision Layer (killer differentiator) ──────────────────


def test_index_has_wadl_section():
    """WADL section must exist with id='wadl'."""
    html = _read("index.html")
    assert 'id="wadl"' in html, "#wadl section missing from homepage"


def test_index_wadl_has_demo_label():
    """WADL phone mock must carry a DEMO label (NO_FAKE_PROOF gate)."""
    html = _read("index.html")
    wadl_block = re.search(r'id="wadl"(.*?)</section>', html, flags=re.DOTALL)
    assert wadl_block, "#wadl block not found"
    body = wadl_block.group(1)
    assert "DEMO" in body, "WADL section must include a DEMO label"


def test_index_wadl_uses_ds_wadl_components():
    """WADL must use the new ds-wadl-* CSS components from design-system.css."""
    html = _read("index.html")
    css = (LANDING / "assets/css/design-system.css").read_text(encoding="utf-8")
    for cls in ("ds-wadl", "ds-wadl__phone", "ds-wadl__msg", "ds-wadl__chip"):
        assert cls in html, f"homepage missing class {cls!r} in WADL section"
        assert cls in css, f"design-system.css missing class {cls!r}"


# ─── Homepage anchor preservation ─────────────────────────────────────


def test_index_anchor_ids_preserved():
    """Existing anchor IDs (referenced externally) must not be removed."""
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
    ):
        assert f'id="{anchor}"' in html, f"anchor #{anchor} removed from homepage"


def test_index_has_problem_and_portal_preview_sections():
    html = _read("index.html")
    assert 'id="problem"' in html, "#problem section missing"
    assert 'id="portal-preview"' in html, "#portal-preview section missing"
    assert 'id="proof-strip"' in html, "#proof-strip section missing"


# ─── Customer portal Today's Decision hero ────────────────────────────


def test_customer_portal_today_decision_above_ops():
    """The Today's Decision hero must precede the dense ops grid."""
    html = _read("customer-portal.html")
    today_idx = html.find('id="today-decision"')
    ops_idx = html.find('id="ops-grid"')
    assert today_idx > 0, "#today-decision hero not added"
    assert ops_idx > 0, "#ops-grid still expected to exist"
    assert today_idx < ops_idx, (
        "Tier-1 redesign requires #today-decision to render BEFORE #ops-grid"
    )


def test_customer_portal_ops_wrapped_in_collapsible_details():
    """Heavy ops console must live inside <details class='ds-portal-deep'>."""
    html = _read("customer-portal.html")
    assert 'class="ds-portal-deep"' in html, "ds-portal-deep wrapper missing"


def test_customer_portal_keeps_demo_label():
    """DEMO src-pill must remain visible (polish rule)."""
    html = _read("customer-portal.html")
    assert "src-pill" in html, "src-pill DEMO marker removed"
    assert "DEMO" in html, "DEMO label removed"


# ─── Proof page L1-L5 evidence ladder ─────────────────────────────────


def test_proof_has_l1_to_l5_ladder():
    html = _read("proof.html")
    for level in ("L1", "L2", "L3", "L4", "L5"):
        assert level in html, f"proof.html missing evidence level {level!r}"
    assert "ds-evidence-ladder" in html, "ds-evidence-ladder component not used"


def test_proof_evidence_ladder_uses_correct_modifiers():
    html = _read("proof.html")
    for mod in ("ds-evidence-level--l1", "ds-evidence-level--l5"):
        assert mod in html, f"proof.html missing class {mod!r}"


# ─── Pricing page anchor structure ────────────────────────────────────


def test_pricing_has_three_offer_ladder():
    """2026-Q2 reframe: pricing.html shows exactly the 3-offer ladder."""
    html = _read("pricing.html")
    plans = re.findall(r'<div class="plan(?:\s[^"]*)?"', html)
    assert len(plans) == 3, f"pricing.html should have exactly 3 .plan cards; found {len(plans)}"


def test_pricing_flagship_sprint_is_first_anchor():
    """Anchor pricing pattern: the 25,000 SAR Sprint leads the grid."""
    html = _read("pricing.html")
    plans_block = re.search(r'<div class="plans">(.*)', html, flags=re.DOTALL)
    assert plans_block, "Could not isolate pricing .plans grid"
    first_plan = plans_block.group(1).split("</div>", 1)[0]
    assert "25,000" in first_plan or "Revenue Intelligence Sprint" in first_plan, (
        "Top-tier anchor must lead the pricing grid (25,000 SAR Revenue Intelligence Sprint)"
    )


def test_pricing_includes_strategic_diagnostic_and_retainer():
    html = _read("pricing.html")
    assert "Strategic Diagnostic" in html, "Strategic Diagnostic tier missing from pricing"
    assert "Governed Ops Retainer" in html, "Governed Ops Retainer tier missing from pricing"
    assert "4,999" in html, "4,999 SAR retainer floor missing from pricing"
    assert "25,000" in html, "25,000 SAR flagship Sprint missing from pricing"


def test_pricing_uses_iltizamat_not_damanat():
    """Brand voice: التزامات (commitments) replaces ضمانات (guarantees)."""
    html = _read("pricing.html")
    assert "التزامات Dealix" in html, "Pricing trust strip should say التزامات Dealix"


# ─── Trust Center: 8 hard gates as features ───────────────────────────


def test_trust_center_lists_eight_hard_gates():
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
        assert code in html, f"trust-center.html missing hard gate {code!r}"


def test_trust_center_pdpl_ready_phrasing():
    """Be honest: 'PDPL-ready' not 'PDPL certified'."""
    html = _read("trust-center.html")
    assert "PDPL-ready" in html, "trust-center should call workflows 'PDPL-ready'"


# ─── Agency Partner page ──────────────────────────────────────────────


def test_agency_partner_page_exists():
    assert (LANDING / "agency-partner.html").exists(), (
        "agency-partner.html must exist for the new Tier-1 funnel"
    )


def test_partners_redirects_to_agency_partner():
    html = _read("partners.html")
    assert 'http-equiv="refresh"' in html, "partners.html should be a thin redirect"
    assert "/agency-partner.html" in html, "redirect target must be /agency-partner.html"


def test_sitemap_lists_agency_partner():
    sitemap = (LANDING / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_dealix = (LANDING / "sitemap_dealix.xml").read_text(encoding="utf-8")
    assert "/agency-partner.html" in sitemap, "sitemap.xml missing agency-partner entry"
    assert "/agency-partner.html" in sitemap_dealix, (
        "sitemap_dealix.xml missing agency-partner entry"
    )


# ─── Footer trust badges (polish rule reinforcement) ──────────────────


@pytest.mark.parametrize(
    "page",
    [
        "agency-partner.html",
        "trust-center.html",
    ],
)
def test_tier1_pages_carry_footer_trust_badges(page):
    """Saudi-PDPL · Approval-first · Proof-backed must appear in footer."""
    html = _read(page)
    assert "Saudi-PDPL" in html, f"{page} missing Saudi-PDPL badge"
    assert "Approval-first" in html, f"{page} missing Approval-first badge"
    assert "Proof-backed" in html, f"{page} missing Proof-backed badge"


# ─── Diagnostic page polish ───────────────────────────────────────────


def test_diagnostic_promises_24h_outputs():
    html = _read("diagnostic.html")
    # New output-promise card lists the 5 deliverables. Numerals may be
    # Western (3) or Arabic-Indic (٣); accept either form.
    for token in ("فرص", "رسالة عربيّة", "أفضل قناة", "مخاطرة", "قرار التالي"):
        assert token in html, f"diagnostic.html output promise missing {token!r}"


# ─── Deep pages footer trust badges (Track D1) ─────────────────────────


@pytest.mark.parametrize(
    "page",
    [
        "ai-team.html",
        "launchpad.html",
        "compare.html",
        "roi.html",
    ],
)
def test_deep_pages_have_footer_trust_badges(page):
    """Track D1 polish: 4 highest-impact deep pages must carry the
    Saudi-PDPL · Approval-first · Proof-backed footer."""
    html = _read(page)
    for badge in ("Saudi-PDPL", "Approval-first", "Proof-backed"):
        assert badge in html, f"{page} missing footer badge {badge!r}"


@pytest.mark.parametrize(
    "page",
    [
        "launchpad.html",
        "compare.html",
        "roi.html",
    ],
)
def test_deep_pages_link_to_trust_center(page):
    """Deep pages should funnel high-intent buyers toward /trust-center.html
    where the 8 hard gates are explained as features."""
    html = _read(page)
    assert "/trust-center.html" in html, f"{page} should link to /trust-center.html"


@pytest.mark.parametrize(
    "page",
    [
        "launchpad.html",
        "compare.html",
    ],
)
def test_deep_pages_link_to_checkout(page):
    """Sprint-eligible deep pages route to the new /checkout.html?tier= flow
    (replacing the static /launchpad.html funnel)."""
    html = _read(page)
    assert "/checkout.html?tier=" in html, (
        f"{page} should funnel to /checkout.html?tier=X"
    )
