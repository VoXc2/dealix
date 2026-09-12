from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"


def _read(relative: str) -> str:
    return (WEB / relative).read_text(encoding="utf-8")


def test_zatca_readiness_wedge_is_free_source_backed_and_truth_bounded() -> None:
    text = _read("app/zatca-fatoora-readiness/page.tsx")
    assert "187,500" in text
    assert "1 فبراير 2027" in text
    assert "Wave25-E-invoicing.aspx" in text
    assert 'href="/book"' in text
    assert "التشخيص المجاني" in text
    assert "لا تصدر حكمًا ضريبيًا" in text
    assert "شهادة امتثال" in text


def test_ai_governance_readiness_wedge_is_free_source_backed_and_truth_bounded() -> None:
    text = _read("app/ai-governance-readiness/page.tsx")
    assert "تعيين مسؤول للذكاء الاصطناعي" in text
    assert "الاستبيان" in text
    assert "aiserviceprovideraccreditation" in text
    assert 'href="/book"' in text
    assert "التشخيص المجاني" in text
    assert "Readiness ≠ Accreditation" in text
    assert "لا تمنح اعتماد SDAIA" in text


def test_services_and_sitemap_expose_both_money_now_wedges() -> None:
    services = _read("app/services/page.tsx")
    sitemap = _read("app/sitemap.ts")
    for path in ("/zatca-fatoora-readiness", "/ai-governance-readiness"):
        assert path in services
        assert path in sitemap
    assert "SAUDI MONEY-NOW WEDGES" in services


def test_money_now_registry_preserves_research_truth_boundary() -> None:
    payload = json.loads((ROOT / "config/growth/saudi_money_now_wedges_2026-09-12.json").read_text(encoding="utf-8"))
    assert payload["schema"] == "dealix.saudi_money_now_wedges.v1"
    assert "not relationship" in payload["truth_law"]
    assert "not certification" in payload["truth_law"]
    assert "not pipeline" in payload["truth_law"]
    assert "not revenue" in payload["truth_law"]
    ids = {item["id"] for item in payload["wedges"]}
    assert {"zatca_fatoora_wave25", "sdaia_ai_provider_accreditation"} <= ids
