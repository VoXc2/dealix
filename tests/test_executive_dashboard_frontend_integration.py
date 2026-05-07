"""Phase 6 — Executive dashboard frontend integration tests."""
from __future__ import annotations

import re
from pathlib import Path

import pytest


HTML_PATH = Path("landing/executive-command-center.html")
JS_PATH = Path("landing/assets/js/executive-command-center.js")


def test_html_exists() -> None:
    assert HTML_PATH.exists()


def test_js_exists() -> None:
    assert JS_PATH.exists()


def test_html_has_required_section_ids() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    required_ids = [
        "state-pill", "state-pill-text", "company-name",
        "executive-summary", "full-ops-score", "readiness-label",
        "degraded-banner", "degraded-list", "dec-list",
        "revenue-num", "sales-num", "growth-num", "support-num",
        "delivery-num", "finance-num", "proof-num", "risk-num",
        "approval-num",
    ]
    for sid in required_ids:
        assert f'id="{sid}"' in html, f"missing id: {sid}"


def test_html_has_arabic_content() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    # Should have non-trivial Arabic
    assert "مركز القيادة" in html
    assert "قرارات" in html or "قرار" in html


def test_html_has_english_helper() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "Executive Command Center" in html


def test_html_links_to_customer_portal() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "/customer-portal.html" in html


def test_html_no_internal_terms() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    forbidden_in_text = ["v11 ", "v12 ", "v13 ", "v14 ", "stacktrace", "pytest", "growth_beast"]
    for term in forbidden_in_text:
        assert term not in html, f"HTML leaks internal term: {term}"


def test_html_no_forbidden_claims() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    patterns = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"\bblast\b", re.IGNORECASE),
        re.compile(r"نضمن"),
        re.compile(r"مضمون"),
        re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
    ]
    for p in patterns:
        assert not p.search(html), f"forbidden pattern in HTML: {p.pattern}"


def test_html_has_4_state_styles() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "state-pill--demo" in html
    assert "state-pill--org" in html
    assert "state-pill--live" in html
    assert "state-pill--degraded" in html


def test_html_has_demo_label() -> None:
    """DEMO state must be visually distinguishable."""
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "DEMO" in html


def test_js_handles_3_url_states() -> None:
    js = JS_PATH.read_text(encoding="utf-8")
    assert "param('org')" in js
    assert "param('access')" in js
    assert "setState('live'" in js
    assert "setState('org'" in js
    assert "setState('demo')" in js


def test_js_has_degraded_handling() -> None:
    js = JS_PATH.read_text(encoding="utf-8")
    assert "degraded" in js.lower()
    # Mode passed to setState comes from a ternary; just check both branches exist
    assert "'degraded'" in js
    assert "state-pill--degraded" in js
    assert "degraded-banner" in js


def test_js_no_internal_terms() -> None:
    js = JS_PATH.read_text(encoding="utf-8")
    for term in ["v11 ", "v12 ", "v13 ", "v14 ", "stacktrace", "growth_beast"]:
        assert term not in js, f"JS leaks internal term: {term}"


def test_js_no_forbidden_claims() -> None:
    js = JS_PATH.read_text(encoding="utf-8")
    for pat in [r"\bguaranteed?\b", r"\bblast\b", r"\bcold\s+whatsapp\b", "نضمن"]:
        assert not re.search(pat, js, re.IGNORECASE), f"forbidden in JS: {pat}"


def test_html_balanced_tags() -> None:
    """Quick balance check on common block tags."""
    from html.parser import HTMLParser

    class Counter(HTMLParser):
        def __init__(self):
            super().__init__()
            self.opened = {}
            self.closed = {}
        def handle_starttag(self, tag, attrs):
            if tag not in ('br', 'meta', 'link', 'img', 'input', 'hr', 'source'):
                self.opened[tag] = self.opened.get(tag, 0) + 1
        def handle_endtag(self, tag):
            self.closed[tag] = self.closed.get(tag, 0) + 1

    p = Counter()
    p.feed(HTML_PATH.read_text(encoding="utf-8"))
    for tag, n in p.opened.items():
        assert n == p.closed.get(tag, 0), f"unbalanced tag: <{tag}> opened={n} closed={p.closed.get(tag, 0)}"
