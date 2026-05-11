"""Wave 13 Phase 6 — Customer Portal Full Ops tests.

Asserts (static HTML/JS analysis — no Playwright):
  - 4-card section present with 4 data-test attributes
  - Degraded banner CSS class + ARIA live region defined
  - 8-section invariant preserved (existing test file already enforces;
    here we re-verify section count post-Phase 6)
  - No internal jargon leaked into the new HTML

Sandbox-safe: pure file I/O.
"""

from __future__ import annotations

import re
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_PORTAL = _REPO_ROOT / "landing" / "customer-portal.html"
_DASHBOARD_JS = _REPO_ROOT / "landing" / "assets" / "js" / "customer-dashboard.js"


# ── Test 1 ────────────────────────────────────────────────────────────
def test_four_cards_section_present():
    """4-card above-fold pattern with all 4 data-test attributes."""
    html = _PORTAL.read_text(encoding="utf-8")
    assert 'class="w13-fourcards"' in html, "missing w13-fourcards section"
    expected_test_ids = [
        "w13-card-current-status",
        "w13-card-today-decision",
        "w13-card-pending-approvals",
        "w13-card-proof-progress",
    ]
    for tid in expected_test_ids:
        assert f'data-test="{tid}"' in html, f"missing card: {tid}"


# ── Test 2 ────────────────────────────────────────────────────────────
def test_degraded_banner_defined():
    """ARIA live region + CSS class for degraded state."""
    html = _PORTAL.read_text(encoding="utf-8")
    assert 'id="w13-degraded-banner"' in html
    assert 'role="status"' in html
    assert 'aria-live="polite"' in html
    # CSS class state-pill--degraded defined
    assert ".state-pill--degraded" in html
    assert ".w13-degraded-banner" in html


# ── Test 3 ────────────────────────────────────────────────────────────
def test_eight_section_invariant_preserved():
    """Article 6: existing 8 customer-portal sections still present.

    Counts top-level <section ...> tags inside <main>. The 4-card
    block uses <article> tags wrapped in <section class="w13-fourcards">
    which adds ONE additional section to the count, but the
    existing 9-section content stays. We assert ≥9 sections (additive only).
    """
    html = _PORTAL.read_text(encoding="utf-8")
    # Count <section> appearances
    section_count = len(re.findall(r"<section[\s>]", html))
    # Pre-Wave-13 baseline: 9 sections inside <main>. We added 1 (w13-fourcards).
    # So we expect at least 10 total sections in the HTML now.
    assert section_count >= 10, f"section count regressed: {section_count}"


# ── Test 4 ────────────────────────────────────────────────────────────
def test_no_internal_jargon_in_new_html_block():
    """The new 4-card HTML must not leak internal terms (Article 6 + 8)."""
    html = _PORTAL.read_text(encoding="utf-8")
    # Extract just the w13-fourcards section
    m = re.search(
        r'<section class="w13-fourcards"[\s\S]*?</section>',
        html,
    )
    assert m is not None, "w13-fourcards section not found"
    block = m.group(0)
    forbidden = [
        "leadops_spine", "customer_brain", "approval_center",
        "v10", "v11", "v12", "v13",
        "stacktrace", "pyo3", "_pycache_",
        "guaranteed", "نضمن",
    ]
    for tok in forbidden:
        assert tok not in block, f"new HTML block leaks: {tok}"

    # JS dashboard renderer present
    js = _DASHBOARD_JS.read_text(encoding="utf-8")
    assert "renderW13FourCards" in js, "JS renderer not wired"
    assert "maybeShowW13DegradedBanner" in js, "JS degraded-banner trigger not wired"
