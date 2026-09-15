from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web" / "app"


def _read(relative: str) -> str:
    return (WEB / relative).read_text(encoding="utf-8")


def test_root_layout_does_not_force_home_canonical_on_every_route() -> None:
    layout = _read("layout.tsx")
    assert 'canonical: "/"' not in layout


def test_home_owns_the_root_canonical() -> None:
    home = _read("page.tsx")
    assert 'alternates: { canonical: "/" }' in home


def test_static_public_routes_own_route_specific_canonicals() -> None:
    routes = {
        "services/page.tsx": "/services",
        "sectors/page.tsx": "/sectors",
        "products/page.tsx": "/products",
        "pricing/page.tsx": "/pricing",
        "cases/page.tsx": "/cases",
        "saudi-opportunity-radar/page.tsx": "/saudi-opportunity-radar",
        "safety/page.tsx": "/safety",
        "proof-vault/page.tsx": "/proof-vault",
    }
    for file_name, canonical in routes.items():
        source = _read(file_name)
        assert f'canonical: "{canonical}"' in source, file_name


def test_client_or_metadata_free_routes_get_route_layout_canonicals() -> None:
    routes = {
        "book/layout.tsx": "/book",
        "company/layout.tsx": "/company",
        "dealix-os/layout.tsx": "/dealix-os",
    }
    for file_name, canonical in routes.items():
        source = _read(file_name)
        assert f'canonical: "{canonical}"' in source, file_name


def test_sector_detail_canonical_tracks_slug() -> None:
    source = _read("sectors/[slug]/page.tsx")
    assert 'canonical: `/sectors/${slug}`' in source


def test_legacy_public_commercial_routes_remain_redirected() -> None:
    config = (ROOT / "apps" / "web" / "next.config.js").read_text(encoding="utf-8")
    for source in ("/ar", "/ar/pricing", "/ar/p1", "/ar/demo", "/ar/trust", "/company-brain-os", "/delivery-os"):
        assert f'{{ source: "{source}"' in config


def test_every_reviewed_legacy_fixed_offer_surface_is_quarantined_by_redirect() -> None:
    config = (ROOT / "apps" / "web" / "next.config.js").read_text(encoding="utf-8")
    retired = (
        "/revenue-os",
        "/ar/p1",
        "/ar/p2",
        "/ar/p3",
        "/ar/pricing",
        "/ar/demo",
        "/ar/trust",
        "/ar/transformation",
        "/company-brain-os",
        "/delivery-os",
    )
    for source in retired:
        assert f'{{ source: "{source}"' in config, source
