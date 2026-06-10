"""Wave 7.5 §24.2 Fix 3 — enrichment honestly says when it's in demo mode."""
from __future__ import annotations

import os
from unittest.mock import patch

from auto_client_acquisition.enrichment_provider import (
    EnrichmentResult,
    _HunterProvider,
    _stable_score_for,
)


def test_no_provider_is_demo_mode_true() -> None:
    r = EnrichmentResult(
        domain="example.sa",
        contact_email="x@example.sa",
        confidence_score=0.0,
        reason_code="no_provider",
    )
    assert r.is_demo_mode is True
    assert r.to_public_dict()["data_source"] == "deterministic_demo_fallback"


def test_live_disabled_is_demo_mode_true_with_message() -> None:
    r = EnrichmentResult(
        domain="example.sa",
        contact_email="x@example.sa",
        confidence_score=0.42,
        reason_code="live_disabled",
        provider_id="hunter",
    )
    pub = r.to_public_dict()
    assert r.is_demo_mode is True
    assert pub["is_demo_mode"] is True
    assert pub["data_source"] == "deterministic_demo_fallback"
    assert "HUNTER_API_KEY" in pub["demo_reason"]


def test_ok_is_not_demo_mode() -> None:
    r = EnrichmentResult(
        domain="example.sa",
        contact_email="x@example.sa",
        confidence_score=0.85,
        company_name_guess="Example",
        industry_guess="real-estate",
        reason_code="ok",
        provider_id="hunter",
    )
    pub = r.to_public_dict()
    assert r.is_demo_mode is False
    assert pub["data_source"] == "live_provider"
    assert pub["demo_reason"] is None


def test_hunter_without_api_key_returns_demo_mode_flag() -> None:
    # Ensure HUNTER_API_KEY absent + DEALIX_ENRICHMENT_LIVE_CALLS unset
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("HUNTER_API_KEY", None)
        os.environ.pop("DEALIX_ENRICHMENT_LIVE_CALLS", None)
        provider = _HunterProvider()
        r = provider.enrich(domain="acme-real-estate.sa", contact_email="info@acme-real-estate.sa")
        assert r.reason_code == "live_disabled"
        assert r.is_demo_mode is True
        assert r.to_public_dict()["is_demo_mode"] is True
        # confidence score is deterministic from domain hash
        assert 0.0 <= r.confidence_score <= 1.0
        assert r.confidence_score == _stable_score_for("acme-real-estate.sa")
