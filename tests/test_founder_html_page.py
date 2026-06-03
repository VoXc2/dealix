"""Tests for the bookmarkable founder dashboard HTML page.

The page is read-only, bilingual (Arabic primary, English secondary), and
fetches the founder dashboard JSON at runtime. We assert structural
guarantees only — no live HTTP, no JS execution.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = REPO_ROOT / "landing" / "founder-dashboard.html"
JS_PATH = REPO_ROOT / "landing" / "assets" / "js" / "founder-dashboard.js"

# Forbidden marketing claims. Mirrors the spirit of the broader landing
# guard: no overpromises, no aggressive outbound language.
FORBIDDEN_PATTERN = re.compile(r"(نضمن|guaranteed|blast|scrape)", re.IGNORECASE)


@pytest.fixture(scope="module")
def page_html() -> str:
    assert PAGE_PATH.exists(), f"Founder dashboard HTML missing at {PAGE_PATH}"
    return PAGE_PATH.read_text(encoding="utf-8")


def test_page_file_exists():
    assert PAGE_PATH.is_file(), f"expected file at {PAGE_PATH}"


def test_page_declares_arabic_rtl(page_html: str):
    assert '<html lang="ar"' in page_html
    assert 'dir="rtl"' in page_html


def test_page_references_dashboard_js(page_html: str):
    assert "founder-dashboard.js" in page_html
    assert JS_PATH.is_file(), f"expected JS asset at {JS_PATH}"


def test_page_references_dashboard_endpoint(page_html: str):
    # Endpoint can live in the HTML (data-attr) or the JS file.
    js_src = JS_PATH.read_text(encoding="utf-8") if JS_PATH.exists() else ""
    combined = page_html + "\n" + js_src
    assert "/api/v1/founder/dashboard" in combined


def test_page_has_no_forbidden_marketing_claims(page_html: str):
    matches = FORBIDDEN_PATTERN.findall(page_html)
    assert not matches, f"Forbidden marketing tokens found: {matches}"


def test_page_has_noindex_meta(page_html: str):
    # Founder dashboard must not be indexed by search engines.
    assert re.search(
        r'<meta\s+name="robots"\s+content="[^"]*noindex',
        page_html,
        re.IGNORECASE,
    ), "expected <meta name=\"robots\" content=\"noindex...\""


def test_js_uses_configurable_api_base(page_html: str):
    js_src = JS_PATH.read_text(encoding="utf-8")
    assert "data-api-base" in page_html
    assert "data-api-base" in js_src
    assert "https://api.dealix.me" in js_src  # documented default
