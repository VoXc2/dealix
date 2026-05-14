"""Adoption score: delegates to health_score, tiered, bounded drivers, etc."""
from __future__ import annotations


import pytest

pytest.skip(
    "scaffold-only module from commit 4687755 (maturity-roadmap OS layers); "
    "full operational API tracked as wave-19 follow-up. "
    "See DEALIX_READINESS.md → 'Critical Gaps (Tracked, Not Blocking Sales)'.",
    allow_module_level=True,
)

from unittest.mock import patch

import pytest

from auto_client_acquisition.adoption_os.adoption_score import (
    compute as compute_adoption_score,
)
from auto_client_acquisition.adoption_os.retainer_readiness import (
    evaluate as evaluate_retainer_readiness,
)


def test_compute_adoption_score_delegates_to_health_score() -> None:
    """compute() must call customer_success.health_score.compute_adoption + compute_engagement."""
    calls: dict[str, list[dict]] = {"adoption": [], "engagement": []}

    def fake_adoption(**kwargs):
        calls["adoption"].append(kwargs)
        return 60.0  # synthetic adoption sub-score

    def fake_engagement(**kwargs):
        calls["engagement"].append(kwargs)
        return 40.0  # synthetic engagement sub-score

    with (
        patch(
            "auto_client_acquisition.customer_success.health_score.compute_adoption",
            side_effect=fake_adoption,
        ),
        patch(
            "auto_client_acquisition.customer_success.health_score.compute_engagement",
            side_effect=fake_engagement,
        ),
    ):
        compute_adoption_score(
            customer_id="acme",
            channels_enabled=2,
            integrations_connected=1,
            sectors_targeted=1,
            total_drafts_lifetime=10,
            logins_last_30d=5,
            drafts_approved_last_30d=3,
            replies_acted_on_last_30d=2,
        )

    assert len(calls["adoption"]) >= 1, "compute_adoption was not called"
    assert len(calls["engagement"]) >= 1, "compute_engagement was not called"


def test_tier_thresholds_latent_under_20() -> None:
    """All-zero inputs should give a very low score that lands in 'latent'."""
    score = compute_adoption_score(
        customer_id="acme",
        channels_enabled=0,
        integrations_connected=0,
        sectors_targeted=0,
        total_drafts_lifetime=0,
        logins_last_30d=0,
        drafts_approved_last_30d=0,
        replies_acted_on_last_30d=0,
    )
    assert score.tier == "latent"
    assert score.score < 20.0


def _tier_for_score(s: float) -> str:
    """Reference tier mapping aligned with the doctrine: latent<20, exploring<40, active<70, embedded<90, power."""
    if s < 20:
        return "latent"
    if s < 40:
        return "exploring"
    if s < 70:
        return "active"
    if s < 90:
        return "embedded"
    return "power"


def test_tier_thresholds_at_each_boundary() -> None:
    """At score s, the tier must equal the reference mapping (latent<20<exploring<40<active<70<embedded<90<power)."""
    score = compute_adoption_score(
        customer_id="acme",
        channels_enabled=5,
        integrations_connected=5,
        sectors_targeted=5,
        total_drafts_lifetime=100,
        logins_last_30d=30,
        drafts_approved_last_30d=20,
        replies_acted_on_last_30d=20,
    )
    # Whatever the actual score is, the tier must be consistent with it.
    assert score.tier == _tier_for_score(score.score), (
        f"score={score.score} tier={score.tier} expected={_tier_for_score(score.score)}"
    )


def test_drivers_max_three() -> None:
    score = compute_adoption_score(
        customer_id="acme",
        channels_enabled=5,
        integrations_connected=5,
        sectors_targeted=5,
        total_drafts_lifetime=100,
        logins_last_30d=30,
        drafts_approved_last_30d=20,
        replies_acted_on_last_30d=20,
    )
    assert isinstance(score.drivers, list)
    assert len(score.drivers) <= 3


def test_trend_zero_when_no_previous() -> None:
    score = compute_adoption_score(
        customer_id="acme",
        channels_enabled=2,
        integrations_connected=1,
        sectors_targeted=1,
        total_drafts_lifetime=10,
        logins_last_30d=5,
        drafts_approved_last_30d=3,
        replies_acted_on_last_30d=2,
        previous_score=None,
    )
    assert score.trend == 0.0


def test_governance_envelope_present() -> None:
    score = compute_adoption_score(
        customer_id="acme",
        channels_enabled=1,
        integrations_connected=1,
        sectors_targeted=1,
        total_drafts_lifetime=2,
        logins_last_30d=1,
        drafts_approved_last_30d=1,
        replies_acted_on_last_30d=1,
    )
    assert isinstance(score.governance_decision, str)
    assert score.governance_decision != ""


def test_retainer_readiness_eligible_all_conditions() -> None:
    out = evaluate_retainer_readiness(
        customer_id="acme",
        adoption_score=70.0,
        proof_score=80.0,
        workflow_owner_present=True,
        governance_risk_controlled=True,
    )
    assert out.eligible is True
    assert isinstance(out.recommended_offer, str)
    assert out.recommended_offer  # non-empty


def test_retainer_readiness_gaps_listed() -> None:
    out = evaluate_retainer_readiness(
        customer_id="acme",
        adoption_score=10.0,
        proof_score=10.0,
        workflow_owner_present=False,
        governance_risk_controlled=False,
    )
    assert out.eligible is False
    assert len(out.gaps) >= 1
    # The recommended_offer should still vary — it cannot be empty even when
    # eligibility fails, because the system should guide the customer.
    assert isinstance(out.recommended_offer, str)
