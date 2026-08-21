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


def test_trust_center_distinguishes_enforced_gates_from_open_work() -> None:
    trust = _read("trust-center.html")
    for gate in (
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_LINKEDIN_AUTOMATION",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
        "NO_UNAPPROVED_TESTIMONIAL",
    ):
        assert gate in trust, gate
    for required in (
        "ما هو مثبت وممنوع، وما يزال مفتوحًا",
        "Production frontend ownership",
        "Real customer-sensitive data",
        "Live payment / invoicing",
        "Compliance / certification claims",
        "Missing evidence → Draft / Block / Unknown",
    ):
        assert required in trust, required
    assert "لا يدّعي PDPL certification" in trust
    assert "SOC 2" in trust  # only inside an explicit non-claim sentence
    assert "Saudi data residency" in trust  # only inside an explicit non-claim sentence
    assert "لا تُفتح أبداً" not in trust
    assert "كل بوّابة هي قاعدة برمجيّة محظورة" not in trust
    assert "فاتورة Moyasar" not in trust
    assert "فاتورة ZATCA" not in trust


def test_current_public_notices_share_one_product_start_path() -> None:
    combined = "\n".join(_read(name) for name in ("terms.html", "privacy.html", "trust-center.html"))
    assert "Free Mini Diagnostic" in combined
    assert "Revenue Command Pilot" in combined
    assert "30 يومًا" in combined
