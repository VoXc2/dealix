from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_SURFACES = {
    "offers": ROOT / "apps/web/app/ar/offers/page.tsx",
    "diagnostic": ROOT / "apps/web/app/ar/diagnostic-sprint/page.tsx",
    "intake": ROOT / "apps/web/app/ar/intake/page.tsx",
    "enterprise": ROOT / "apps/web/app/enterprise-readiness/page.tsx",
    "book": ROOT / "apps/web/app/book/page.tsx",
}

FORBIDDEN_PUBLIC_AUTHORITY = (
    "499 ريال",
    "1,500 ريال",
    "2,999",
    "4,999",
    "7,500",
    "12,500",
    "25,000",
    "100,000",
    "499 SAR",
    "paid diagnostic",
    "تشخيص تحولي مدفوع",
    "PDPL-native",
    "PDPL-compliant",
    "KSA-region by default",
)


def read(name: str) -> str:
    return PUBLIC_SURFACES[name].read_text(encoding="utf-8")


def test_legacy_arabic_commercial_routes_converge_on_book() -> None:
    for name in ("offers", "diagnostic", "intake"):
        source = read(name)
        assert 'redirect("/book")' in source


def test_active_public_surfaces_do_not_publish_stale_price_or_compliance_authority() -> None:
    for name, path in PUBLIC_SURFACES.items():
        source = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_PUBLIC_AUTHORITY:
            assert token.lower() not in source.lower(), f"{name} resurrected forbidden public authority: {token}"


def test_book_is_free_truth_safe_inbound_surface() -> None:
    source = read("book")
    assert "Free Execution Diagnostic" in source
    assert "/api/v1/public/execution-diagnostic" in source
    assert "followup_requested" in source
    assert "لا يتم اعتبار المشكلة أو العائد أو Proof مثبتًا" in source


def test_enterprise_terms_are_customer_specific_after_discovery() -> None:
    source = read("enterprise")
    assert "free execution diagnostic" in source.lower()
    assert "customer-specific" in source.lower()
    assert "after qualified discovery" in source.lower()


def test_retired_value_engine_cannot_publish_synthetic_roi() -> None:
    source = (ROOT / "apps/web/app/value-engine/page.tsx").read_text(encoding="utf-8")
    assert 'redirect("/cases")' in source
    assert "12000" not in source
    assert "15600" not in source
    assert "WorkflowROIReport" not in source
