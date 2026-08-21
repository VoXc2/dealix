"""Lock the marketers reference page to the governed acquisition path."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "landing" / "marketers.html"


def _page() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_marketers_page_is_a_noncanonical_reference() -> None:
    html = _page()
    assert '<meta name="robots" content="noindex,follow"' in html
    assert '<link rel="canonical" href="https://dealix.me/diagnostic.html"' in html
    assert '<meta property="og:url" content="https://dealix.me/diagnostic.html"' in html


def test_marketers_page_routes_to_the_governed_diagnostic() -> None:
    html = _page()
    assert html.count('href="/diagnostic.html"') >= 4
    assert "mailto:" not in html.lower()
    assert "sami.assiri11@gmail.com" not in html.lower()


def test_marketers_page_has_no_legacy_public_commitments() -> None:
    html = _page().lower()
    forbidden = (
        "ابدأ بـ 1 ريال",
        "1 ر.س",
        "999 ر.س",
        "2,999 ر.س",
        "7,999 ر.س",
        "99.9% uptime",
        "34% تحسّن",
        "60% من عملائنا",
        "soc 2 compliance",
        "aws me-south-1",
        "متوافق مرحلة 2",
        "checkout",
    )
    present = [claim for claim in forbidden if claim.lower() in html]
    assert not present, f"legacy unsupported marketers claims returned: {present}"


def test_marketers_page_preserves_approval_first_boundaries() -> None:
    html = _page()
    for statement in (
        "Draft-first",
        "Approval-first",
        "لا إرسال حيّ",
        "لا يوجد ضمان لنتيجة تجارية",
        "هذه الصفحة ليست إعلانًا عن منصة مكتملة ذاتية الخدمة",
    ):
        assert statement in html
