"""HTML/JS integration tests for the Service Activation Console.

Verifies that:
  - landing/status.html mounts the data-driven console (no hardcoded rows)
  - landing/assets/js/service-console.js exposes the renderer surface
  - The fetched JSON path matches what the renderer requests
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
STATUS_HTML = REPO / "landing" / "status.html"
CONSOLE_JS = REPO / "landing" / "assets" / "js" / "service-console.js"
DATA_JSON = REPO / "landing" / "assets" / "data" / "service-readiness.json"


def test_status_html_mounts_console():
    html = STATUS_HTML.read_text(encoding="utf-8")
    assert 'id="services-mount"' in html
    assert 'id="services-counts-mount"' in html
    assert 'id="services-filter-mount"' in html
    assert "assets/js/service-console.js" in html


def test_status_html_no_hardcoded_service_rows():
    html = STATUS_HTML.read_text(encoding="utf-8")
    # The old page had .status-row blocks per service. The data-driven
    # console must own that surface entirely.
    assert "status-row__name" not in html, (
        "status.html must not contain hardcoded service rows; "
        "the renderer is responsible"
    )


def test_status_html_bilingual_titles():
    html = STATUS_HTML.read_text(encoding="utf-8")
    assert "حالة خدمات Dealix" in html
    assert "Dealix Service Readiness" in html


def test_console_js_exists_and_exports_renderer():
    js = CONSOLE_JS.read_text(encoding="utf-8")
    # Public surface for tests / inspection
    assert "DealixServiceConsole" in js
    assert "renderGrid" in js
    assert "applyFilters" in js
    # Fetches the JSON the exporter writes
    assert "service-readiness.json" in js


def test_console_status_ctas_use_arabic_labels():
    js = CONSOLE_JS.read_text(encoding="utf-8")
    assert "جرّب الآن" in js              # Live CTA
    assert "اختبر مع مؤسس Dealix" in js   # Pilot CTA
    assert "شاهد خطة التفعيل" in js       # Partial CTA
    assert "في خارطة الطريق" in js        # Target CTA
    assert "محظور حتى يزول السبب" in js   # Blocked CTA


def test_data_json_is_committed():
    assert DATA_JSON.exists(), (
        "landing/assets/data/service-readiness.json must be committed; "
        "regenerate via scripts/export_service_readiness_json.py"
    )


def test_homepage_trust_bar_fetches_live_counts():
    """P5 — landing/script.js must fetch the readiness JSON so the
    homepage trust-bar (stat-live / stat-partial / stat-target) stays
    auto-honest as the YAML evolves. Falls back to a static dict if
    fetch fails."""
    js_path = REPO / "landing" / "script.js"
    assert js_path.exists()
    js = js_path.read_text(encoding="utf-8")
    # The script must reference the readiness JSON path
    assert "/assets/data/service-readiness.json" in js
    # And the three stat IDs the homepage uses
    assert "stat-live" in js
    assert "stat-partial" in js
    assert "stat-target" in js
    # Plus a fallback dict so the bar never shows blank
    assert "FALLBACK_STATS" in js or "fallback" in js.lower()
