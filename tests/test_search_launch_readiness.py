from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_sitemap_does_not_fake_lastmod_on_every_build() -> None:
    source = read("apps/web/app/sitemap.ts")
    assert "const now = new Date()" not in source
    assert "lastModified: now" not in source


def test_robots_quarantines_sensitive_internal_surfaces() -> None:
    source = read("apps/web/app/robots.ts")
    for path in ("/proof-vault", "/control-plane", "/founder", "/war-room", "/sales-machine", "/revenue-machine", "/hubspot-os", "/daily-draft"):
        assert f'"{path}"' in source
    for path in ("/services", "/sectors", "/products", "/book", "/saudi-opportunity-radar"):
        assert f'"{path}"' in source


def test_money_route_has_specific_search_metadata() -> None:
    source = read("apps/web/app/book/layout.tsx")
    assert "Free Execution Diagnostic" in source
    assert "description:" in source
    assert 'canonical: "/book"' in source
    assert "بدون بطاقة" in source


def test_company_and_dealix_os_have_intent_specific_descriptions() -> None:
    company = read("apps/web/app/company/layout.tsx")
    dealix_os = read("apps/web/app/dealix-os/layout.tsx")
    assert "Saudi B2B Strategy" in company and "description:" in company
    assert "AI Business Operating System" in dealix_os and "description:" in dealix_os


def test_saudi_radar_is_machine_readable_without_claiming_pipeline() -> None:
    source = read("apps/web/app/saudi-opportunity-radar/page.tsx")
    assert 'type="application/ld+json"' in source
    assert '"@type": "ItemList"' in source
    assert "Public signal ≠ buyer intent" in source
    assert "VERIFIED 15 SEP 2026" in source
