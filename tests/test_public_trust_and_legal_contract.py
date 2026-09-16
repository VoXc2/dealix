"""Public trust/legal notices must stay conservative and evidence-bound."""

from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


def test_terms_is_notice_not_stale_fixed_contract() -> None:
    terms = _read("terms.html")
    for required in (
        "ليست Service Agreement نهائيًا",
        "Revenue Command Pilot لمدة 30 يومًا",
        "quote-only",
        "لا توجد في الإطلاق الحالي باقة عامة ثابتة السعر",
        "لا Refund أو Discount أو SLA أو Tax treatment يُفترض",
        "ليس عقد خدمة نهائيًا ولا DPA ولا رأيًا قانونيًا",
    ):
        assert required in terms, required
    for retired in (
        "Growth Starter Pilot 499",
        "Executive Growth OS",
        "Moyasar",
        "صفحة ROI",
        "SLA المحدّد",
        "7 أيّام",
        "أوّل ٣ paid pilots",
    ):
        assert retired not in terms, retired


def test_privacy_notice_does_not_claim_closed_pdpl_or_residency_posture() -> None:
    privacy = _read("privacy.html")
    for required in (
        "ليس DPA ولا شهادة امتثال",
        "لا ندّعي حاليًا أن كل بيانات Dealix أو بيانات العملاء مقيمة داخل السعودية",
        "NO_INFERRED_CONSENT",
        "NO_LIVE_SEND",
        "Data-flow register",
        "لا تعيّن هذه الصفحة DPO",
    ):
        assert required in privacy, required
    for stale_claim in (
        "متوافقة مع PDPL السعودي",
        "أوّل ٣ paid pilots",
        "نلتزم بالردّ خلال 30 يوماً",
        "سجلّات التدقيق: 7 سنوات",
        "أكثر من 24 شهراً",
        "TLS 1.2+",
        "الاسم: Sami Assiri",
    ):
        assert stale_claim not in privacy, stale_claim


def test_retired_static_trust_surface_defers_to_canonical_safety_page() -> None:
    trust = _read("trust-center.html")
    for required in (
        "DEALIX_RETIRED_PUBLIC_SURFACE",
        'name="robots" content="noindex,nofollow"',
        'rel="canonical" href="https://dealix.me/safety"',
        'http-equiv="refresh" content="0; url=/safety"',
        'href="/safety"',
    ):
        assert required in trust, required
    for stale_authority in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "Production frontend ownership",
        "Saudi data residency",
    ):
        assert stale_authority not in trust, stale_authority


def test_current_public_notices_share_one_product_start_path() -> None:
    combined = "\n".join(_read(name) for name in ("terms.html", "privacy.html", "trust-center.html"))
    assert "Free Mini Diagnostic" in combined
    assert "Revenue Command Pilot" in combined
    assert "30 يومًا" in combined
