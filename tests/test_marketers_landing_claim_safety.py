"""Regression contracts for public pilot-stage landing surfaces."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETERS_PAGE = ROOT / "landing" / "marketers.html"
SERVICES_PAGE = ROOT / "landing" / "services.html"
NO_OVERCLAIM_REGISTER = ROOT / "dealix" / "registers" / "no_overclaim.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_existing_no_overclaim_register_blocks_unapproved_public_pricing() -> None:
    register = _read(NO_OVERCLAIM_REGISTER)

    assert "first_launch_checkout_fail_closed" in register
    assert "Public pricing and checkout remain disabled" in register
    assert "The founder has not yet approved a public first-launch price" in register


def test_marketers_page_is_explicitly_pilot_stage_and_approval_first() -> None:
    html = _read(MARKETERS_PAGE)

    required_contracts = (
        "مرحلة بايلوت",
        "Draft-first",
        "Approval-first",
        "لا إرسال حيّ",
        "لا يوجد ضمان لنتيجة تجارية",
        "لا يصبح التزامًا إلا داخل اتفاق مكتوب ومعتمد",
        "ليست إعلانًا عن منصة مكتملة ذاتية الخدمة",
    )
    for contract in required_contracts:
        assert contract in html


def test_marketers_page_does_not_publish_unverified_prices_or_capability_claims() -> None:
    lowered = _read(MARKETERS_PAGE).lower()

    forbidden_claims = (
        "ابدأ بـ 1 ريال",
        "1 ر.س",
        "999 ر.س",
        "2,999 ر.س",
        "7,999 ر.س",
        "99.9% uptime",
        "34% تحسّن في roas",
        "18 ساعة/أسبوع",
        "60% وقت إعداد التقارير",
        "متوافق مرحلة 2",
        "4.8★",
        "دقة 88%+",
        "60% من عملائنا",
        "soc 2 compliance",
        "soc 2 (q3 2026)",
        "sla 1 ساعة",
        "sla 4 ساعات",
        "15 ساعة أسبوعياً",
        "تحسين تلقائي",
        "فواتير متوافقة مع zatca",
        "البيانات في aws me-south-1",
        "أسعارنا 40-60% أرخص",
        "توفّرلك 15 ساعة/أسبوع",
        "حملات غير محدودة",
        "عملاء غير محدودين",
    )
    for claim in forbidden_claims:
        assert claim.lower() not in lowered


def test_services_page_is_a_governed_offer_ladder_not_a_public_price_sheet() -> None:
    html = _read(SERVICES_PAGE)
    lowered = html.lower()

    required_contracts = (
        "منتج واحد. القدرات تتوسع بعد إثبات القيمة.",
        "مسار واحد للشراء",
        "quote-only 30-day Revenue Command Pilot",
        "هذه ليست باقات أو أسعارًا مستقلة",
        "Expand only if earned",
        "إذا لم تظهر قيمة قابلة للإثبات، نتوقف أو نعيد التصميم",
    )
    for contract in required_contracts:
        assert contract in html

    forbidden_commitments = (
        "499 ر.س",
        "٤٩٩ ر.س",
        "1500 sar/mo",
        "١٬٥٠٠ ر.س",
        "7500 sar/mo",
        "٧٬٥٠٠ ر.س",
        "5,000–25,000",
        "30% عمولة",
        "٣٠٪ عمولة",
        "استرداد كامل",
        "استرداد شهر",
        "أقل من ٣٠ دقيقة",
        "٤ أشهر التزام",
        "٨ صباحًا ksa",
        "refund:",
    )
    for claim in forbidden_commitments:
        assert claim.lower() not in lowered


def test_public_pilot_pages_do_not_capture_or_send_data_directly() -> None:
    for page in (MARKETERS_PAGE, SERVICES_PAGE):
        lowered = _read(page).lower()
        assert "<form" not in lowered
        assert "fetch(" not in lowered
        assert "xmlhttprequest" not in lowered
        assert "/trust-center.html" in lowered
        assert "/privacy.html" in lowered

    marketers = _read(MARKETERS_PAGE).lower()
    assert "mailto:" not in marketers
    assert marketers.count('href="/diagnostic.html"') >= 4

    # The broader services page still uses a draft-only mail client handoff.
    # Its eventual retirement is part of the wider public-authority alignment
    # scope; this focused PR owns only the marketers.html slice.
    services = _read(SERVICES_PAGE).lower()
    assert "mailto:" in services
