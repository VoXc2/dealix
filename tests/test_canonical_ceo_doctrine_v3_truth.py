from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_platform_source_of_truth_uses_ceo_doctrine_v3_market_identity() -> None:
    text = _read("docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md")

    assert "Dealix — Governed AI Execution Platform for Saudi Business" in text
    assert "Turn company signals into governed execution and measurable proof." in text
    assert "Signal -> Decision -> Action -> Proof" in text
    assert "Execution Diagnostic" in text
    assert "Outcome Sprint" in text
    assert "Dealix Runtime" in text
    assert "Revenue + Proof + Command" in text
    assert "twelve Operating Systems" in text
    assert "customer-specific quote" in text.lower()
    assert "no public fixed-price" in text.lower()


def test_top_level_readmes_do_not_restore_v2_as_market_headline() -> None:
    readme = _read("README.md")
    readme_ar = _read("README.ar.md")

    assert "# Dealix — Governed AI Execution Platform for Saudi Business" in readme
    assert "Signal -> Decision -> Action -> Proof" in readme
    assert "# Dealix — منصة التنفيذ الذكي المحكوم للأعمال في السعودية" in readme_ar
    assert "Signal -> Decision -> Action -> Proof" in readme_ar

    assert "# Dealix — Saudi-first AI Business Operating System" not in readme
    assert "# 🏢 Dealix — نظام تشغيل أعمال بالذكاء الاصطناعي للشركات السعودية" not in readme_ar


def test_brand_positioning_matches_canonical_market_identity() -> None:
    text = _read("docs/brand/POSITIONING.md")

    assert "Dealix — Governed AI Execution Platform for Saudi Business" in text
    assert "Execution Diagnostic" in text
    assert "Outcome Sprint" in text
    assert "Dealix Runtime" in text
    assert "Revenue + Proof + Command" in text
    assert "current generic category headline" in text


def test_v3_market_labels_do_not_grant_new_runtime_pricing_authority() -> None:
    icp = _read("dealix/config/icp_primary.yaml")

    assert "market_identity: governed_ai_execution_platform" in icp
    assert "market_entry_label: execution_diagnostic" in icp
    assert "market_paid_offer_label: outcome_sprint" in icp
    assert "market_expansion_label: dealix_runtime" in icp
    assert "primary_offer_id: revenue_command_pilot_30d" in icp
    assert "pricing_authority: customer_specific_quote_only" in icp
    assert "public_fixed_price: false" in icp
    assert "public_checkout: false" in icp
