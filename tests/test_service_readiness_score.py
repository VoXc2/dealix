"""Tests for service readiness score."""

from __future__ import annotations

from auto_client_acquisition.delivery_os.service_readiness import (
    compute_service_readiness_score,
    default_evidence_for,
)


def test_lead_intelligence_full_score() -> None:
    out = compute_service_readiness_score("lead_intelligence_sprint")
    assert out["score"] == 100
    assert out["sellable_officially"] is True


def test_support_desk_score_without_upsell() -> None:
    out = compute_service_readiness_score("support_desk_sprint")
    assert out["score"] == 90
    assert out["sellable_officially"] is True
    assert out["sellable_beta_only"] is False


def test_below_80_not_officially_sellable() -> None:
    from auto_client_acquisition.delivery_os.service_readiness import WEIGHTS

    overrides = dict.fromkeys(WEIGHTS, False)
    overrides["has_offer_page"] = True
    out = compute_service_readiness_score(
        "lead_intelligence_sprint",
        evidence_overrides=overrides,
    )
    assert out["score"] == 10
    assert out["sellable_officially"] is False
    assert out["sellable_beta_only"] is True


def test_override_flips_upsell() -> None:
    base = default_evidence_for("support_desk_sprint")
    assert base["has_upsell_path"] is False
    out = compute_service_readiness_score(
        "support_desk_sprint",
        evidence_overrides={"has_upsell_path": True},
    )
    assert out["score"] == 100


def test_unknown_service_zero_score() -> None:
    out = compute_service_readiness_score("unknown_service_xyz")
    assert out["score"] == 0
