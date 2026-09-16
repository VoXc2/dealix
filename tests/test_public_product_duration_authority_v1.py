from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PUBLIC_PRODUCT_PAGES = (
    "apps/web/app/products/ai-trust-compliance-os/page.tsx",
    "apps/web/app/products/client-delivery-os/page.tsx",
    "apps/web/app/products/company-brain-os/page.tsx",
    "apps/web/app/products/revenue-command-room-os/page.tsx",
    "apps/web/app/products/whatsapp-inbox-followup-os/page.tsx",
)

FORBIDDEN_FIXED_DURATION = (
    "مدة التسليم", "ابدأ سباق 7 أيام", "7 أيام للتشغيل الأول",
    "5 أيام للتشغيل الأول", "7-day sprint", "30-day pilot",
)

def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")

def test_public_products_do_not_emit_fixed_delivery_duration_authority() -> None:
    for rel in PUBLIC_PRODUCT_PAGES:
        text = _read(rel)
        for marker in FORBIDDEN_FIXED_DURATION:
            assert marker not in text, (rel, marker)
        assert "نطاق ومدة التنفيذ" in text
        assert "Qualified Discovery" in text
        assert 'href="/book"' in text

def test_public_brain_surface_does_not_reintroduce_fixed_sprint_cta() -> None:
    text = _read("apps/web/app/brain/page.tsx")
    assert "ابدأ سباق 7 أيام" not in text
    assert 'href="/book"' in text

def test_customer_specific_terms_remain_explicit() -> None:
    for rel in PUBLIC_PRODUCT_PAGES:
        text = _read(rel)
        assert "النطاق" in text
        assert "المدة" in text
        assert "معايير القبول" in text
