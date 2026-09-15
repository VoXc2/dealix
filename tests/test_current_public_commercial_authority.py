from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PUBLIC = [
    ROOT / "apps/web/app/ar/page.tsx",
    ROOT / "apps/web/app/ar/pricing/page.tsx",
    ROOT / "apps/web/app/ar/p1/page.tsx",
    ROOT / "apps/web/app/ar/p2/page.tsx",
    ROOT / "apps/web/app/ar/p3/page.tsx",
    ROOT / "apps/web/app/ar/demo/page.tsx",
    ROOT / "apps/web/app/ar/trust/page.tsx",
    ROOT / "apps/web/app/ar/transformation/page.tsx",
    ROOT / "apps/web/app/revenue-os/page.tsx",
    ROOT / "apps/web/app/company-brain-os/page.tsx",
    ROOT / "apps/web/app/products/client-delivery-os/page.tsx",
    ROOT / "apps/web/app/delivery-os/page.tsx",
    ROOT / "apps/web/app/ar/zatca-readiness/page.tsx",
]

FORBIDDEN = (
    "تشخيص مدفوع",
    "paid diagnostic",
    "pdpl-native",
    "3,500",
    "7,500 ريال",
    "8,000",
    "12,000",
    "15,000",
    "20,000",
    "30,000",
    "35,000",
    "40,000",
    "45,000",
    "60,000",
    "75,000",
    "100,000",
    "180,000",
    "sar 2,500",
    "sar 7,500",
    "sar 15,000",
)


def test_active_public_surfaces_have_no_fixed_price_or_paid_diagnostic_authority() -> None:
    for path in PUBLIC:
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN:
            assert token.lower() not in text, f"{path}: forbidden authority {token}"


def test_current_runtime_duration_is_customer_specific() -> None:
    text = (ROOT / "api/routers/commercial_runtime_truth.py").read_text(encoding="utf-8")
    assert '"duration_days": None' in text
    assert '"duration_model": "customer_specific_after_qualified_discovery"' in text
    assert "Revenue Command Pilot — 30 Days" not in text
    assert "Pilot لمدة 30 يوم" not in text


def test_legacy_adapter_cannot_emit_price_duration_or_checkout_authority() -> None:
    text = (ROOT / "api/routers/commercial_map.py").read_text(encoding="utf-8")
    assert '"price_sar": None' in text
    assert '"duration_days": None' in text
    assert 'safe_wiring["checkout_url"] = None' in text
    assert 'safe_wiring["checkout_endpoint"] = None' in text


def test_public_delivery_surfaces_do_not_publish_fixed_contract_duration() -> None:
    merged = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC)
    for token in ("5–7 أيام", "3–7 أيام", "خلال أسبوع", "أسبوع واحد", "30 يوم للتشغيل", "in 30 days", "ابدأ بـ7 أيام"):
        assert token.casefold() not in merged.casefold(), token


def test_shared_delivery_pipeline_uses_phases_not_fixed_contract_days() -> None:
    text = (ROOT / "apps/web/lib/company-os/company-os.ts").read_text(encoding="utf-8")
    for token in ("Day 0–1", "Day 2–4", "Day 5–8", "Day 9–14", "Day 15 → ongoing", "Day 30+"):
        assert token not in text
