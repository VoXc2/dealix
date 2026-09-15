from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEXT_CONFIG = ROOT / "apps" / "web" / "next.config.js"
DELIVERY_PAGE = ROOT / "apps" / "web" / "app" / "delivery-os" / "page.tsx"
PIPELINE_PAGE = ROOT / "apps" / "web" / "app" / "pipeline" / "page.tsx"


def test_legacy_public_operator_routes_are_redirected_to_current_authority() -> None:
    config = NEXT_CONFIG.read_text(encoding="utf-8")
    assert '{ source: "/delivery-os", destination: "/services", permanent: true }' in config
    assert '{ source: "/pipeline", destination: "/dealix-os", permanent: true }' in config


def test_redirected_legacy_sources_do_not_restore_stale_commercial_authority() -> None:
    delivery = DELIVERY_PAGE.read_text(encoding="utf-8")
    pipeline = PIPELINE_PAGE.read_text(encoding="utf-8")
    lowered = delivery.casefold()
    assert "30 days" not in lowered
    assert "30-day" not in lowered
    assert "30 day" not in lowered
    assert "Pipeline — Dealix" in pipeline
