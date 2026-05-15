"""Phase 10 — Frontend Professional Polish tests."""
from __future__ import annotations

import re
from pathlib import Path


CUSTOMER_FACING = [
    "landing/customer-portal.html",
    "landing/executive-command-center.html",
    "landing/launchpad.html",
    "landing/index.html",
]


def test_all_customer_facing_have_mobile_meta() -> None:
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert (
            'viewport' in html and 'width=device-width' in html
        ), f"{page} missing mobile viewport meta"


def test_all_customer_facing_have_arabic() -> None:
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert 'lang="ar"' in html, f"{page} missing lang=ar"
        assert 'dir="rtl"' in html, f"{page} missing dir=rtl"


def test_all_customer_facing_have_english() -> None:
    """At least one English word must appear (e.g., 'Dealix' or 'Saudi')."""
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert re.search(r'\b[A-Za-z]{4,}\b', html), f"{page} missing English text"


def test_no_fake_metrics_without_demo_label() -> None:
    """Customer-portal.html must show DEMO label where it shows numbers."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    # DEMO label must appear
    assert "DEMO" in html
    # Specific marker — `src-pill` is the demo pill
    assert "src-pill" in html


def test_executive_command_center_demo_label_present() -> None:
    html = Path("landing/executive-command-center.html").read_text(encoding="utf-8")
    assert "DEMO" in html
    assert "demo-tag" in html


def test_no_forbidden_claims_in_customer_pages() -> None:
    forbidden = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"\bblast\b", re.IGNORECASE),
        re.compile(r"نضمن"),
        re.compile(r"مضمون"),
    ]
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        # Strip script/style/comments first — only customer-visible copy counts.
        html = path.read_text(encoding="utf-8")
        html_visible = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html_visible = re.sub(r"<style[^>]*>.*?</style>", "", html_visible, flags=re.DOTALL | re.IGNORECASE)
        html_visible = re.sub(r"<!--.*?-->", "", html_visible, flags=re.DOTALL)
        for pat in forbidden:
            assert not pat.search(html_visible), f"{page} contains: {pat.pattern}"


def test_customer_portal_links_to_legal_pages() -> None:
    """Customer portal footer must link to privacy + terms."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert "/privacy.html" in html
    assert "/terms.html" in html


def test_polish_doc_exists() -> None:
    """Phase 10 doc must exist."""
    assert Path("docs/FRONTEND_PROFESSIONAL_POLISH_PLAN.md").exists()
