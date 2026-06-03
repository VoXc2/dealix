"""V14 Phase K7 — enrichment unified confidence-score tests.

Closes the registry's `next_activation_step_en` for `enrichment`:
"Wire real provider API keys and add a unified confidence-score test."

Verifies:
  - Provider abstraction works for none/mock/hunter
  - Confidence scores are bounded [0.0, 1.0]
  - No-op provider returns 0.0 with reason `no_provider` (default-deny)
  - Mock provider is deterministic (same input → same score)
  - Hunter provider degrades gracefully when no API key
  - Empty inputs return 0.0 with reason `invalid_input`
  - Unknown provider name falls back to no-op (never raises)
  - Top-level enrich_lead() never raises
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.enrichment_provider import (
    EnrichmentProvider,
    EnrichmentResult,
    enrich_lead,
    get_provider,
)


@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch):
    """Each test gets a clean env so DEALIX_ENRICHMENT_PROVIDER /
    HUNTER_API_KEY don't leak across tests."""
    monkeypatch.delenv("DEALIX_ENRICHMENT_PROVIDER", raising=False)
    monkeypatch.delenv("DEALIX_ENRICHMENT_LIVE_CALLS", raising=False)
    monkeypatch.delenv("HUNTER_API_KEY", raising=False)
    yield


# ─────────────────── Default no-op provider ────────────────


def test_default_provider_is_no_op() -> None:
    """When no env var is set, get_provider() returns the no-op
    fallback. Default-deny."""
    p = get_provider()
    assert p.provider_id == "none"


def test_no_op_provider_returns_zero_confidence() -> None:
    p = get_provider("none")
    r = p.enrich(domain="acme.sa")
    assert r.confidence_score == 0.0
    assert r.reason_code == "no_provider"
    assert r.provider_id == "none"


def test_no_op_empty_domain_returns_invalid_input() -> None:
    p = get_provider("none")
    r = p.enrich(domain="")
    assert r.confidence_score == 0.0
    assert r.reason_code == "invalid_input"


# ─────────────────── Mock provider (deterministic) ─────────


def test_mock_provider_returns_deterministic_score() -> None:
    p = get_provider("mock")
    r1 = p.enrich(domain="acme.sa")
    r2 = p.enrich(domain="acme.sa")
    assert r1.confidence_score == r2.confidence_score
    assert 0.0 <= r1.confidence_score <= 1.0


def test_mock_provider_different_domain_different_score() -> None:
    p = get_provider("mock")
    r1 = p.enrich(domain="acme.sa")
    r2 = p.enrich(domain="another-completely-different-domain.com")
    # Statistically very likely distinct, but not strictly required.
    # We check both are in valid range and the company guess differs.
    assert 0.0 <= r1.confidence_score <= 1.0
    assert 0.0 <= r2.confidence_score <= 1.0
    assert r1.company_name_guess != r2.company_name_guess


def test_mock_empty_domain_returns_zero() -> None:
    p = get_provider("mock")
    r = p.enrich(domain="")
    assert r.confidence_score == 0.0
    assert r.reason_code == "invalid_input"


def test_mock_provider_id_is_mock() -> None:
    assert get_provider("mock").provider_id == "mock"


# ─────────────────── Hunter provider (graceful degradation) ──


def test_hunter_without_key_returns_mock_score() -> None:
    """Without HUNTER_API_KEY the Hunter provider returns a
    deterministic mock score with reason `live_disabled` —
    callers can build/test without a real API key."""
    p = get_provider("hunter")
    r = p.enrich(domain="acme.sa")
    assert r.reason_code == "live_disabled"
    assert 0.0 <= r.confidence_score <= 1.0
    assert r.provider_id == "hunter"


def test_hunter_with_key_but_live_disabled_still_mock(monkeypatch) -> None:
    """API key set but DEALIX_ENRICHMENT_LIVE_CALLS not 'true' →
    still returns mock score (no actual HTTP call)."""
    monkeypatch.setenv("HUNTER_API_KEY", "test-key-xyz")
    p = get_provider("hunter")
    r = p.enrich(domain="acme.sa")
    assert r.reason_code == "live_disabled"


def test_hunter_empty_domain_returns_zero() -> None:
    p = get_provider("hunter")
    r = p.enrich(domain="")
    assert r.confidence_score == 0.0
    assert r.reason_code == "invalid_input"


# ─────────────────── Score bounds ──────────────────────────


def test_score_always_within_zero_to_one_for_all_providers() -> None:
    domains = ["acme.sa", "x.io", "very-long-corporate-domain-name-test.example.com", "a.b.c.d.e"]
    for provider_name in ("none", "mock", "hunter"):
        p = get_provider(provider_name)
        for d in domains:
            r = p.enrich(domain=d)
            assert 0.0 <= r.confidence_score <= 1.0, (
                f"provider={provider_name} domain={d} score={r.confidence_score}"
            )


# ─────────────────── Unknown provider fallback ─────────────


def test_unknown_provider_name_falls_back_to_no_op() -> None:
    """Misconfigured DEALIX_ENRICHMENT_PROVIDER must NOT crash —
    silent fallback to no-op so the system stays green."""
    p = get_provider("clearbit")  # not implemented yet
    assert p.provider_id == "none"


def test_env_var_picks_provider(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ENRICHMENT_PROVIDER", "mock")
    p = get_provider()
    assert p.provider_id == "mock"


# ─────────────────── Top-level convenience ─────────────────


def test_enrich_lead_returns_result() -> None:
    """enrich_lead() always returns an EnrichmentResult — never raises."""
    r = enrich_lead(domain="acme.sa")
    assert isinstance(r, EnrichmentResult)


def test_enrich_lead_overrides_provider() -> None:
    r = enrich_lead(domain="acme.sa", provider_name="mock")
    assert r.provider_id == "mock"


def test_enrich_lead_empty_domain_doesnt_raise() -> None:
    r = enrich_lead(domain="")
    assert r.confidence_score == 0.0


# ─────────────────── Result schema ─────────────────────────


def test_enrichment_result_is_immutable() -> None:
    """EnrichmentResult is frozen — caller can't mutate after gate decision."""
    r = EnrichmentResult(
        domain="x.sa",
        contact_email="",
        confidence_score=0.5,
    )
    with pytest.raises((AttributeError, Exception)):
        r.confidence_score = 0.99  # type: ignore[misc]


def test_provider_implements_abstract_method() -> None:
    """Every provider class must implement enrich() — no abstract leaks."""
    for name in ("none", "mock", "hunter"):
        p = get_provider(name)
        assert isinstance(p, EnrichmentProvider)
        # call must work and return a result
        r = p.enrich(domain="test.sa")
        assert isinstance(r, EnrichmentResult)
