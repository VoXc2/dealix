from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"


def _read(relative: str) -> str:
    return (WEB / relative).read_text(encoding="utf-8")


def test_homepage_uses_single_canonical_launch_path() -> None:
    text = _read("app/page.tsx")

    assert "Free Mini Diagnostic" in text
    assert "Customer-Specific Quote" in text
    assert "30-Day Revenue Command Pilot" in text
    assert "Proof → Stop / Expand / Redesign" in text
    assert "PREMIUM_OFFERS" not in text
    assert "شاهد كل العروض السبعة" not in text
    assert "ابدأ بـ7 أيام" not in text
    assert "100 شركة تُبحث يوميًا" not in text


def test_pricing_page_is_quote_only_and_has_no_subscription_or_refund_promise() -> None:
    text = _read("app/pricing/page.tsx")

    assert "مسار شراء واحد" in text
    assert "Free Mini Diagnostic" in text
    assert "Customer-Specific Quote" in text
    assert "Revenue Command Pilot — 30 Days" in text
    assert "لا سعر عام" in text
    assert "لا Checkout عام" in text
    assert "PREMIUM_OFFERS" not in text
    assert "سبع أنظمة استراتيجية" not in text
    assert "قابل للاسترداد خلال 14 يوم" not in text
    assert "الاشتراك الشهري قابل للإلغاء" not in text


def test_book_page_is_free_mini_diagnostic_not_seven_day_or_self_serve() -> None:
    text = _read("app/book/page.tsx")

    assert "Free Mini Diagnostic" in text
    assert "لا بطاقة" in text
    assert "Customer-Specific Quote" in text
    assert "30 يومًا" in text
    assert "mass outreach" in text
    assert "cold WhatsApp" in text


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
