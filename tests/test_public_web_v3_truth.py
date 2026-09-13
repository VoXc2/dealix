from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"

CANONICAL_PUBLIC_FILES = [
    WEB / "components/landing/InteractiveHome.tsx",
    WEB / "app/services/page.tsx",
    WEB / "app/sectors/page.tsx",
    WEB / "app/sectors/[slug]/page.tsx",
    WEB / "app/products/page.tsx",
    WEB / "app/pricing/page.tsx",
    WEB / "app/book/page.tsx",
    WEB / "app/company/page.tsx",
    WEB / "app/dealix-os/page.tsx",
]

FORBIDDEN_CURRENT_MARKERS = (
    "تشخيص مدفوع",
    "خمسة أنظمة تشغيلية",
    "5 وكلاء ai",
    "٥ وكلاء ai",
    "3,500–15,000",
    "8,000–30,000",
    "20,000–60,000",
    "7 أيام للتشغيل",
    "5 أيام للتشغيل",
    "30 يوم للتشغيل",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def test_canonical_public_routes_do_not_reintroduce_legacy_commercial_authority() -> None:
    merged = "\n".join(_read(path).casefold() for path in CANONICAL_PUBLIC_FILES)
    for marker in FORBIDDEN_CURRENT_MARKERS:
        assert marker.casefold() not in merged, marker
    assert "free execution diagnostic" in merged
    assert "customer-specific" in merged


def test_sector_catalog_covers_every_canonical_sector_enum_value() -> None:
    source = _read(ROOT / "dealix/commercial/economic_cell.py")
    block = source.split("class Sector(StrEnum):", 1)[1].split("class Geography", 1)[0]
    enum_values = set(re.findall(r'=\s*"([a-z0-9_]+)"', block))

    catalog = _read(WEB / "lib/public-catalog.ts")
    catalog_values = set(re.findall(r'key:\s*"([a-z0-9_]+)"', catalog))

    assert enum_values
    assert catalog_values == enum_values


def test_legacy_public_offer_routes_redirect_to_current_authority() -> None:
    config = _read(WEB / "next.config.js")
    required = {
        "/ar/p1": "/pricing",
        "/ar/p2": "/pricing",
        "/ar/p3": "/pricing",
        "/ar/pricing": "/pricing",
        "/ar/demo": "/book",
        "/products/revenue-command-room-os": "/products",
        "/products/company-brain-os": "/products",
        "/products/whatsapp-inbox-followup-os": "/products",
        "/products/ai-trust-compliance-os": "/products",
        "/products/client-delivery-os": "/products",
    }
    for source, destination in required.items():
        marker = f'{{ source: "{source}", destination: "{destination}", permanent: true }}'
        assert marker in config, marker


def test_sectors_and_products_are_first_class_public_navigation_and_sitemap() -> None:
    nav = _read(WEB / "components/Nav.tsx")
    home = _read(WEB / "components/landing/InteractiveHome.tsx")
    sitemap = _read(WEB / "app/sitemap.ts")
    for route in ("/sectors", "/products"):
        assert route in nav
        assert route in home
        assert route in sitemap


def test_mobile_home_overrides_global_main_grid_and_keeps_touch_targets() -> None:
    home_css = _read(WEB / "app/interactive-home.css")
    global_css = _read(WEB / "app/globals.css")

    # globals.css intentionally makes generic <main> a grid; the interactive
    # home must opt out or its intrinsic mobile track expands beyond viewport.
    assert ".dx-main { width: min(1220px, calc(100% - 36px)); margin: 0 auto; padding: 30px 0 90px; display: block; }" in home_css
    assert "grid-template-columns: minmax(0, 1fr)" in home_css
    assert "width: min(1220px, calc(100% - 24px))" in home_css
    assert ".dx-home" in home_css and "overflow-x: clip" in home_css

    # Mobile and canonical public nav actions use at least a 44px tap target.
    assert "min-height: 44px" in home_css
    assert global_css.count("min-height: 44px") >= 3


def test_mobile_public_navigation_remains_reachable_and_accessible() -> None:
    nav = _read(WEB / "components/Nav.tsx")
    home = _read(WEB / "components/landing/InteractiveHome.tsx")
    global_css = _read(WEB / "app/globals.css")
    home_css = _read(WEB / "app/interactive-home.css")

    assert 'className="mobile-menu"' in nav
    assert 'className="dx-mobile-menu"' in home
    assert 'aria-label="فتح قائمة التنقل"' in nav
    assert 'aria-label="فتح قائمة التنقل"' in home
    assert "links.map" in nav
    assert "publicNavLinks.map" in home
    assert ".mobile-menu-panel" in global_css
    assert ".dx-mobile-menu-panel" in home_css
    assert "min-height: 48px" in global_css
    assert "min-height: 48px" in home_css
    for route in ("/services", "/sectors", "/products", "/dealix-os", "/proof-vault"):
        assert route in nav
        assert route in home
