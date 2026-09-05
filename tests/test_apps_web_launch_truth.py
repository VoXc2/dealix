from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"


def _read(relative: str) -> str:
    return (WEB / relative).read_text(encoding="utf-8")


def test_homepage_uses_v3_market_labels_without_public_price_or_proof_drift() -> None:
    text = _read("app/page.tsx")

    assert "منصة التنفيذ الذكي المحكوم للأعمال" in text
    assert "Signal → Decision → Action → Proof" in text
    assert "Execution Diagnostic" in text
    assert "Outcome Sprint" in text
    assert "Dealix Runtime" in text
    assert "Qualified Discovery + Quote" in text
    assert "Proof Review" in text

    assert "PREMIUM_OFFERS" not in text
    assert "شاهد كل العروض السبعة" not in text
    assert "ابدأ بـ7 أيام" not in text
    assert "100 شركة تُبحث يوميًا" not in text
    assert "ROI مضمون" not in text


def test_pricing_page_is_customer_specific_quote_only_and_not_self_serve() -> None:
    text = _read("app/pricing/page.tsx")

    assert "مسار تنفيذ واحد، بدون باقات عامة" in text
    assert "Execution Diagnostic" in text
    assert "Qualified Discovery + Customer-Specific Quote" in text
    assert "Outcome Sprint" in text
    assert "Dealix Runtime" in text
    assert "لا سعر عام" in text
    assert "لا Checkout عام" in text
    assert "Quote ليست Invoice" in text
    assert "Invoice ليست Payment" in text

    assert "PREMIUM_OFFERS" not in text
    assert "سبع أنظمة استراتيجية" not in text
    assert "قابل للاسترداد خلال 14 يوم" not in text
    assert "الاشتراك الشهري قابل للإلغاء" not in text


def test_book_page_is_execution_diagnostic_then_quote_only_governed_delivery() -> None:
    text = _read("app/book/page.tsx")

    assert "Execution Diagnostic" in text
    assert "Qualified Discovery" in text
    assert "Customer-Specific Quote" in text
    assert "Outcome Sprint" in text
    assert "Dealix Runtime" in text
    assert "لا Checkout" in text
    assert "mass outreach" in text
    assert "cold WhatsApp" in text

    # Market-facing names must not grant public pricing, checkout, or guaranteed results.
    assert "سعر ثابت" not in text
    assert "ROI مضمون" not in text


def test_next_redirects_retire_legacy_public_and_self_serve_surfaces() -> None:
    text = _read("next.config.js")

    required_redirects = {
        '{ source: "/pricing.html", destination: "/pricing", permanent: true }',
        '{ source: "/academy.html", destination: "/", permanent: true }',
        '{ source: "/customer-portal.html", destination: "/", permanent: true }',
        '{ source: "/proof.html", destination: "/", permanent: true }',
        '{ source: "/checkout.html", destination: "/pricing", permanent: true }',
        '{ source: "/signup", destination: "/book", permanent: true }',
        '{ source: "/offers", destination: "/pricing", permanent: true }',
    }
    for redirect in required_redirects:
        assert redirect in text

    # Public legacy URLs must never be routed into founder/RBAC-only surfaces.
    assert '{ source: "/customer-portal.html", destination: "/proof-vault"' not in text
    assert '{ source: "/proof.html", destination: "/proof-vault"' not in text
    assert "Self-serve /signup is intentionally active" not in text
