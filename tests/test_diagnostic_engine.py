"""Tests for auto_client_acquisition.diagnostic_engine.

Pure local generation. NO LLM, NO live sends. Bilingual output
must always carry approval_required + safety_notes; forbidden
marketing tokens must never appear.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.diagnostic_engine import (
    DiagnosticRequest,
    DiagnosticResult,
    generate_diagnostic,
    list_supported_sectors,
)


def test_module_exports_public_api():
    # Smoke: imports succeed and the public surface is what we expect.
    assert callable(generate_diagnostic)
    assert callable(list_supported_sectors)
    assert issubclass(DiagnosticRequest, object)
    assert issubclass(DiagnosticResult, object)


def test_list_supported_sectors_non_empty():
    sectors = list_supported_sectors()
    assert len(sectors) >= 5
    assert "b2b_services" in sectors
    assert "agency" in sectors


def test_generate_diagnostic_returns_full_result():
    req = DiagnosticRequest(
        company="ACME Saudi Co.",
        sector="b2b_services",
        region="riyadh",
        pipeline_state="WhatsApp incoming, founder responds at night",
    )
    result = generate_diagnostic(req)
    assert isinstance(result, DiagnosticResult)
    assert result.company == "ACME Saudi Co."
    assert result.recommended_bundle == "growth_starter"
    assert result.bundle_name_ar
    assert result.bundle_name_en
    assert result.services_in_bundle, "growth_starter must have ≥1 service"
    assert result.markdown_ar_en
    assert result.approval_status == "approval_required"
    assert result.safety_notes


def test_unknown_sector_falls_back_to_growth_starter():
    req = DiagnosticRequest(
        company="ACME",
        sector="totally_unknown_sector",
        region="ksa",
        pipeline_state="—",
    )
    result = generate_diagnostic(req)
    assert result.recommended_bundle == "growth_starter"


def test_agency_sector_recommends_partnership_growth():
    req = DiagnosticRequest(
        company="An Agency",
        sector="agency",
        region="ksa",
        pipeline_state="—",
    )
    result = generate_diagnostic(req)
    assert result.recommended_bundle == "partnership_growth"


def test_markdown_contains_both_arabic_and_english_sections():
    req = DiagnosticRequest(
        company="ACME",
        sector="b2b_services",
        region="riyadh",
        pipeline_state="—",
    )
    md = generate_diagnostic(req).markdown_ar_en
    # Arabic section
    assert "القراءة السريعة" in md
    assert "التشخيص الأوّليّ" in md
    # English section
    assert "Executive summary" in md
    # Pricing visible
    assert "499" in md


def test_markdown_never_contains_forbidden_marketing_tokens():
    """Hard rule: no نضمن, guaranteed, blast, scrape in any brief."""
    req = DiagnosticRequest(
        company="ACME",
        sector="b2b_services",
        region="riyadh",
        pipeline_state="—",
    )
    md = generate_diagnostic(req).markdown_ar_en.lower()
    forbidden = ["نضمن لكم", "guaranteed revenue", "guaranteed ranking", "blast"]
    for token in forbidden:
        assert token.lower() not in md, (
            f"diagnostic brief contains forbidden token {token!r}"
        )


def test_diagnostic_request_rejects_missing_company():
    """Pydantic validation must refuse empty/missing company."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        DiagnosticRequest(company="", sector="b2b_services")
    with pytest.raises(ValidationError):
        DiagnosticRequest(sector="b2b_services")  # type: ignore[call-arg]
