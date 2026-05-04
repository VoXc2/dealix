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
