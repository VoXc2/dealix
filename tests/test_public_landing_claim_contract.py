"""Contract for evidence-safe copy on the canonical static landing page."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing" / "index.html"


class _VisibleTextParser(HTMLParser):
    """Collect browser-visible text without regex-parsing HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._suppressed = 0
        self.parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag.casefold() in {"script", "style"}:
            self._suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"script", "style"} and self._suppressed:
            self._suppressed -= 1

    def handle_data(self, data: str) -> None:
        if not self._suppressed:
            self.parts.append(data)


def _visible_text() -> str:
    parser = _VisibleTextParser()
    parser.feed(LANDING.read_text(encoding="utf-8"))
    parser.close()
    return " ".join(parser.parts)


def _html() -> str:
    return LANDING.read_text(encoding="utf-8")


def test_public_landing_does_not_publish_unverified_benchmark_claims() -> None:
    visible = _visible_text()
    forbidden = (
        "خصومات بلا توثيق تُسرّب 5–15% من الهامش",
        "تجديدات مفوّتة بقيمة مئات الآلاف",
        "المندوب يُعطي 20–35% خصماً",
        "كل proposal تستغرق 2–4 ساعات",
        "كل مراجعة SAMA = أسابيع",
        "15 فريق يُرسل موافقاتهم",
        "20+ شريك استراتيجي",
        "الموزع الجديد يحتاج 2–3 أشهر",
        "6–10 مستويات موافقة",
        "3–5 مطورين × 12 شهراً = 1.5–3M",
        "سنتواصل خلال ٤ ساعات عمل",
        "نتائج حقيقية من محرك ذكاء اصطناعي",
        "3 paid pilots",
        "SLA 99.9%",
        "Saudi data residency",
    )
    assert not [claim for claim in forbidden if claim in visible]


def test_public_landing_states_current_operating_boundaries() -> None:
    visible = _visible_text()
    required = (
        "Saudi-first",
        "Approval-first",
        "Proof-backed",
        "بدون customer-facing auto-send",
        "لا cold WhatsApp ولا scraping مخالف",
        "Synthetic/demo/internal evidence لا يصبح Customer proof",
        "لا 499",
        "الـPilot quote-only",
        "لا Retainer أو Company-wide transformation تلقائي",
    )
    missing = [boundary for boundary in required if boundary not in visible]
    assert not missing, f"missing public claim boundary: {missing}"


def test_public_landing_makes_free_diagnostic_the_primary_entry() -> None:
    html = _html()
    assert html.count('href="/diagnostic.html"') >= 4
    assert "ابدأ Free Mini Diagnostic" in html
    assert "بلا دفع" in html
    assert "بلا PII capture" in html
    assert "مراجعة بشرية قبل أي عرض مدفوع" in html


def test_public_landing_has_no_live_prospect_or_paid_shortcut() -> None:
    html = _html()
    forbidden = (
        'id="demoForm"',
        'id="prospector-form"',
        'href="/start.html"',
        'href="/checkout',
        '/api/v1/public/demo-request',
        'src="script.js"',
    )
    assert not [fragment for fragment in forbidden if fragment in html]


def test_public_landing_does_not_link_quarantined_legacy_offers() -> None:
    html = _html()
    forbidden_links = (
        'href="/roi.html"',
        'href="/agency-partner.html"',
        'href="/case-study.html"',
        'href="/investor.html"',
        'href="/ai-team.html"',
        'href="/command-center.html"',
        'href="/verticals.html"',
        'href="/academy.html"',
        'href="/status.html"',
    )
    assert not [fragment for fragment in forbidden_links if fragment in html]


def test_public_landing_json_ld_has_no_personal_contact_or_fake_free_offer() -> None:
    html = _html()
    assert "hello@dealix.me" in html
    assert "sami.assiri11@gmail.com" not in html
    assert '"@type": "Offer"' not in html
    assert '"price": "0"' not in html


def test_public_landing_preserves_tier1_navigation_and_anchor_contract() -> None:
    html = _html()
    for anchor in (
        "pillars",
        "for-who",
        "sectors",
        "how",
        "trust",
        "proof",
        "pricing",
        "faq",
        "pilot",
        "wadl",
    ):
        assert f'id="{anchor}"' in html, anchor
    assert 'class="ds-mega-menu"' in html
    for current_surface in (
        "/services.html",
        "/proof.html",
        "/trust-center.html",
        "/pricing.html",
        "/privacy.html",
        "/terms.html",
    ):
        assert current_surface in html, current_surface
