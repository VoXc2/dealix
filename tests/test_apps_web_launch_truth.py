from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"


def _read(relative: str) -> str:
    return (WEB / relative).read_text(encoding="utf-8")


def test_homepage_uses_current_interactive_market_truth_without_price_or_proof_drift() -> None:
    page = _read("app/page.tsx")
    home = _read("components/landing/InteractiveHome.tsx")

    assert "InteractiveHome" in page
    assert "AI Business Operating System" in page
    assert "Saudi Arabia" in page

    assert "Signal" in home
    assert "Decision" in home
    assert "Action" in home
    assert "Proof" in home
    assert "Execution Diagnostic" in home
    assert "Qualified Discovery" in home
    assert "Customer-Specific Outcome Sprint" in home
    assert "Proof Review" in home
    assert "Dealix Runtime" in home
    assert "Free Execution Diagnostic" in home
    assert "عرض خاص بالعميل" in home

    for retired in (
        "PREMIUM_OFFERS",
        "شاهد كل العروض السبعة",
        "ابدأ بـ7 أيام",
        "100 شركة تُبحث يوميًا",
        "ROI مضمون خلال",
    ):
        assert retired not in home

    # Explicit negation is allowed and required; a positive guarantee is not.
    assert "لا نضمن ROI" in home


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


def test_book_page_is_inbound_execution_diagnostic_with_evidence_first_truth() -> None:
    text = _read("app/book/page.tsx")

    assert "Free Execution Diagnostic" in text
    assert "/api/v1/public/execution-diagnostic" in text
    assert "workflow" in text
    assert "decision_owner" in text
    assert "tools_data" in text
    assert "business_impact" in text
    assert "proof_metric" in text
    assert "baseline" in text
    assert "target_outcome" in text
    assert "followup_requested" in text

    assert "لا نعتبر الفرضية مشكلة مثبتة قبل وجود baseline ودليل" in text
    assert "لا يتم اعتبار المشكلة أو العائد أو Proof مثبتًا من مجرد التسجيل" in text
    assert "هذه الصفحة قناة inbound" in text
    assert "لا تعتبر رقمًا أو بريدًا عامًا موافقة على مراسلات تسويقية" in text
    assert "شبكة Dealix الوكيلة المحكومة" in text
    assert "Dealix الخمسة" not in text

    for forbidden in ("سعر ثابت", "نضمن ROI", "public checkout", "auto-send"):
        assert forbidden not in text


def test_next_redirects_retire_legacy_public_and_self_serve_surfaces() -> None:
    text = _read("next.config.js")

    required_redirects = {
        '{ source: "/pricing.html", destination: "/pricing", permanent: true }',
        '{ source: "/academy.html", destination: "/", permanent: true }',
        '{ source: "/customer-portal.html", destination: "/", permanent: true }',
        '{ source: "/proof.html", destination: "/", permanent: true }',
        '{ source: "/workflow.html", destination: "/pricing", permanent: true }',
        '{ source: "/trust.html", destination: "/safety", permanent: true }',
        '{ source: "/services.html", destination: "/services", permanent: true }',
        '{ source: "/ai-team.html", destination: "/agents", permanent: true }',
        '{ source: "/checkout.html", destination: "/pricing", permanent: true }',
        '{ source: "/signup", destination: "/book", permanent: true }',
        '{ source: "/offers", destination: "/pricing", permanent: true }',
        '{ source: "/revenue-os", destination: "/dealix-os", permanent: true }',
        '{ source: "/enterprise-readiness", destination: "/services", permanent: true }',
    }
    for redirect in required_redirects:
        assert redirect in text

    assert '{ source: "/customer-portal.html", destination: "/proof-vault"' not in text
    assert '{ source: "/proof.html", destination: "/proof-vault"' not in text
    assert "Self-serve /signup is intentionally active" not in text
