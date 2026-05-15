"""Tests for category_os, holding_os, and new enterprise_os product constants."""

from __future__ import annotations

import pytest

from auto_client_acquisition.category_os import (
    CategoryOwnershipSignals,
    compute_category_ownership_score,
    content_pillar_coverage_score,
    language_adoption_index,
)
from auto_client_acquisition.category_os.content_signal import CONTENT_ENGINE_PILLAR_IDS
from auto_client_acquisition.enterprise_os import (
    CONTROL_PLANE_ENTERPRISE_MODULES,
    GOVERNANCE_RUNTIME_DECISIONS,
    GOVERNANCE_RUNTIME_PRODUCT_COMPONENTS,
    TRUST_PRODUCT_COMPONENTS,
)
from auto_client_acquisition.holding_os import (
    BusinessUnitCharter,
    PortfolioUnitInputs,
    UnitMonthlySnapshot,
    UnitPortfolioDecision,
    compute_portfolio_priority_score,
    evaluate_unit_decision,
)


def test_category_ownership_full_score() -> None:
    assert (
        compute_category_ownership_score(
            CategoryOwnershipSignals(
                clients_use_dealix_terms=True,
                partners_repeat_method=True,
                proof_pack_requested=True,
                capability_score_requested=True,
                inbound_revenue_intelligence=True,
                benchmark_requests=True,
                academy_interest=True,
                enterprise_governance_runtime_asks=True,
            ),
        )
        == 100
    )


def test_content_pillar_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown pillar"):
        content_pillar_coverage_score({"not_a_pillar"})


def test_content_pillar_all_ids_scores_100() -> None:
    assert content_pillar_coverage_score(set(CONTENT_ENGINE_PILLAR_IDS)) == 100


def test_language_adoption_counts() -> None:
    pref, avoided = language_adoption_index(
        "We deliver governed ai operations with a proof pack; no lead scraper.",
    )
    assert pref >= 2 and avoided >= 1


def test_unit_decision_spinout() -> None:
    d = evaluate_unit_decision(
        UnitMonthlySnapshot(
            revenue_growing=True,
            margin_ok=True,
            retainers_growing=True,
            proof_delivery_on_track=True,
            qa_score=90,
            governance_risk_acceptable=True,
            module_usage_growing=True,
            playbook_maturity_ok=True,
            client_health_ok=True,
            venture_signal_strong=True,
        ),
    )
    assert d == UnitPortfolioDecision.SPINOUT


def test_unit_decision_kill_bad_qa() -> None:
    d = evaluate_unit_decision(
        UnitMonthlySnapshot(
            client_health_ok=True,
            governance_risk_acceptable=True,
            qa_score=40,
            revenue_growing=False,
        ),
    )
    assert d == UnitPortfolioDecision.KILL


def test_unit_decision_hold_on_governance() -> None:
    d = evaluate_unit_decision(
        UnitMonthlySnapshot(
            governance_risk_acceptable=False,
        ),
    )
    assert d == UnitPortfolioDecision.HOLD


def test_portfolio_priority_score() -> None:
    s = compute_portfolio_priority_score(
        PortfolioUnitInputs(
            revenue_signal=80,
            repeatability=70,
            proof_signal=75,
            retainer_signal=60,
            product_signal=50,
        ),
    )
    assert s > 0.0


def test_business_unit_charter_fields() -> None:
    c = BusinessUnitCharter(
        name="Revenue OS",
        problem_statement="x",
        buyer_persona="y",
        primary_offer="Sprint",
        recurring_offer="Retainer",
        venture_readiness_score=42.0,
    )
    assert c.name == "Revenue OS"


def test_enterprise_product_constants_nonempty() -> None:
    assert len(TRUST_PRODUCT_COMPONENTS) >= 6
    assert len(GOVERNANCE_RUNTIME_PRODUCT_COMPONENTS) >= 8
    assert "BLOCK" in GOVERNANCE_RUNTIME_DECISIONS
    assert len(CONTROL_PLANE_ENTERPRISE_MODULES) >= 5
