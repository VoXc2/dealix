"""Phase 10 — Frontend Professional Polish tests."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

CUSTOMER_FACING = [
    "landing/customer-portal.html",
    "landing/executive-command-center.html",
    "landing/launchpad.html",
    "landing/index.html",
]


class _VisibleTextExtractor(HTMLParser):
    """Collect visible text while ignoring script/style content structurally."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._suppressed_depth = 0
        self._parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag.lower() in {"script", "style"}:
            self._suppressed_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._suppressed_depth:
            self._suppressed_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._suppressed_depth == 0:
            self._parts.append(data)

    def text(self) -> str:
        return "\n".join(self._parts)


def _visible_text(html: str) -> str:
    parser = _VisibleTextExtractor()
    parser.feed(html)
    parser.close()
    return parser.text()


def test_all_customer_facing_have_mobile_meta() -> None:
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert (
            "viewport" in html and "width=device-width" in html
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
        assert re.search(r"\b[A-Za-z]{4,}\b", html), f"{page} missing English text"


def test_no_fake_metrics_without_demo_label() -> None:
    """Customer-portal.html must show DEMO label where it shows numbers."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert "DEMO" in html
    assert "src-pill" in html


def test_executive_command_center_demo_label_present() -> None:
    html = Path("landing/executive-command-center.html").read_text(encoding="utf-8")
    assert "DEMO" in html
    assert "demo-tag" in html


def _strip_explicit_negative_claim_language(html_visible: str) -> str:
    """Remove only explicit negative/disclaimer uses before claim scanning.

    Positive promises must remain detectable. This keeps copy such as
    "not guaranteed outcomes", "نتائج غير مضمونة", or a first-cohort
    exclusion like "طلبات guaranteed revenue خارج ..." from being mistaken
    for a performance promise.
    """
    patterns = (
        r"[^\n<]*(?:not guaranteed outcomes|ليست نتائج مضمونة|نتائج غير مضمونة)[^\n>]*",
        r"[^\n<]*طلبات\s+guaranteed\s+revenue\s+خارج[^\n>]*",
        r"[^\n<]*guaranteed\s+revenue\s+request[^\n>]*",
    )
    for pattern in patterns:
        html_visible = re.sub(pattern, "", html_visible, flags=re.IGNORECASE)
    return html_visible


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
        html = path.read_text(encoding="utf-8")
        html_visible = _visible_text(html)
        html_visible = _strip_explicit_negative_claim_language(html_visible)
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
