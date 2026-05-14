"""landing/dealix-os.html — Wave 19+ Operational Closure.

Public framework positioning page. Lives at https://dealix.me/dealix-os.html.
Positions Dealix as the commercial reference implementation for the open
Governed AI Operations Doctrine.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OS_HTML = REPO / "landing" / "dealix-os.html"


def test_dealix_os_page_exists():
    assert OS_HTML.exists()


def test_dealix_os_page_lists_license_posture_correctly():
    text = OS_HTML.read_text(encoding="utf-8")
    # Dual license + trademark reservation MUST be visible
    assert "CC BY 4.0" in text
    assert "MIT" in text
    # Trademark explicitly reserved
    assert "trademark" in text.lower()
    assert "Dealix" in text


def test_dealix_os_page_cross_links_to_public_surfaces():
    text = OS_HTML.read_text(encoding="utf-8")
    for endpoint in (
        "/api/v1/doctrine",
        "/api/v1/dealix-promise",
        "/api/v1/capital-assets/public",
        "/promise.html",
        "/verify.html",
    ):
        assert endpoint in text, f"dealix-os.html missing cross-link: {endpoint}"


def test_dealix_os_page_bilingual_and_disclaimer():
    text = OS_HTML.read_text(encoding="utf-8")
    assert "Governed AI Operations Doctrine" in text
    assert "دستور تشغيل AI المحوكم" in text
    assert "النتائج التقديرية ليست نتائج مضمونة" in text


def test_dealix_os_page_states_four_adoption_tiers():
    """The framework offers 4 adoption tiers: awareness / alignment /
    compliance / Dealix-certified. Only tier 4 is commercial."""
    text = OS_HTML.read_text(encoding="utf-8")
    lower = text.lower()
    for tier_marker in ("tier 1", "tier 2", "tier 3", "tier 4"):
        assert tier_marker in lower, f"dealix-os.html missing {tier_marker}"


def test_dealix_os_page_does_not_leak_commercial_secrets():
    """Public framework page must not reference commercial-sensitive tokens."""
    text = OS_HTML.read_text(encoding="utf-8")
    forbidden = (
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
        "ADMIN_API_KEYS",
        "first_invoice_log",
    )
    for tok in forbidden:
        assert tok not in text, f"dealix-os.html (public) leaks {tok!r}"
