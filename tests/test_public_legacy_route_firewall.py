from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEXT_CONFIG = ROOT / "apps" / "web" / "next.config.js"
DELIVERY_PAGE = ROOT / "apps" / "web" / "app" / "delivery-os" / "page.tsx"
PIPELINE_PAGE = ROOT / "apps" / "web" / "app" / "pipeline" / "page.tsx"


def test_legacy_public_operator_routes_are_redirected_to_current_authority() -> None:
    config = NEXT_CONFIG.read_text(encoding="utf-8")
    assert '{ source: "/delivery-os", destination: "/services", permanent: true }' in config
    assert '{ source: "/pipeline", destination: "/dealix-os", permanent: true }' in config


def test_redirects_cover_known_stale_public_copy_sources() -> None:
    delivery = DELIVERY_PAGE.read_text(encoding="utf-8")
    pipeline = PIPELINE_PAGE.read_text(encoding="utf-8")
    assert "30 days" in delivery
    assert "Pipeline — Dealix" in pipeline
