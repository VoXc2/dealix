"""landing/verify.html — Wave 19+ Operational Closure.

CISO-facing public verify page. Lives at https://dealix.me/verify.html.
Live-fetches the 4 public read-only endpoints and renders them.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VERIFY_HTML = REPO / "landing" / "verify.html"


def test_verify_page_exists():
    assert VERIFY_HTML.exists()


def test_verify_page_has_all_four_public_endpoint_sections():
    text = VERIFY_HTML.read_text(encoding="utf-8")
    # Each of the 4 sections must be present
    assert 'data-section="promise"' in text
    assert 'data-section="doctrine"' in text
    assert 'data-section="assets"' in text
    assert 'data-section="markets"' in text
    # And each section must list its endpoint
    for endpoint in (
        "/api/v1/dealix-promise",
        "/api/v1/doctrine",
        "/api/v1/capital-assets/public",
        "/api/v1/gcc-markets",
    ):
        assert endpoint in text, f"verify.html missing endpoint reference: {endpoint}"


def test_verify_page_is_bilingual_and_carries_disclaimer():
    text = VERIFY_HTML.read_text(encoding="utf-8")
    # Bilingual title + Arabic disclaimer
    assert "Verify Dealix" in text
    assert "تحقّق من Dealix" in text
    assert "النتائج التقديرية ليست نتائج مضمونة" in text
    assert "Estimated outcomes are not guaranteed outcomes" in text


def test_verify_page_does_not_reference_admin_key_or_internal_paths():
    """The verify page is PUBLIC. It must not prompt for an admin key,
    must not reference any data/* internal file, must not reference any
    /api/v1/founder/command-center admin endpoint."""
    text = VERIFY_HTML.read_text(encoding="utf-8")
    forbidden = (
        "X-Admin-API-Key",
        "X-ADMIN-API-KEY",
        "anchor_partner_pipeline",
        "first_invoice_log",
        "partner_outreach_log",
        "ADMIN_API_KEYS",
    )
    for tok in forbidden:
        assert tok not in text, f"verify.html (public) leaks {tok!r}"


def test_verify_page_uses_only_public_endpoints():
    """Every fetch() call in verify.html must hit a public surface,
    never an admin-gated one."""
    text = VERIFY_HTML.read_text(encoding="utf-8")
    # Crude but effective: collect fetchJson('...') call paths
    import re
    paths = re.findall(r"fetchJson\(['\"]([^'\"]+)['\"]\)", text)
    assert paths, "verify.html has no fetchJson() calls — broken page"
    public_allowlist = {
        "/api/v1/dealix-promise",
        "/api/v1/doctrine",
        "/api/v1/capital-assets/public",
        "/api/v1/gcc-markets",
    }
    for p in paths:
        assert p in public_allowlist, (
            f"verify.html fetches non-public endpoint {p!r}"
        )
