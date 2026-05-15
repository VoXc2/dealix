"""Agentic Enterprise OS — maturity index, coverage registry, service ladder."""

from __future__ import annotations

from auto_client_acquisition.agentic_enterprise_os.coverage_registry import (
    CORE_SYSTEMS,
    CoreSystemSpec,
    coverage_registry,
    coverage_summary,
    module_coverage,
)
from auto_client_acquisition.agentic_enterprise_os.enterprise_maturity import (
    EnterpriseCapabilityScores,
    compute_emi,
    enterprise_maturity_stage,
)
from auto_client_acquisition.agentic_enterprise_os.service_ladder import (
    emi_to_ladder_level,
    enterprise_offer_recommendation,
)


def _scores(value: float) -> EnterpriseCapabilityScores:
    return EnterpriseCapabilityScores(*([value] * 10))


def test_compute_emi_bounds_and_weight_sum() -> None:
    # A uniform input proves the 10 weights sum to exactly 1.0.
    assert compute_emi(_scores(0.0)) == 0.0
    assert compute_emi(_scores(50.0)) == 50.0
    assert compute_emi(_scores(100.0)) == 100.0


def test_compute_emi_clamps_out_of_range_inputs() -> None:
    assert compute_emi(_scores(150.0)) == 100.0
    assert compute_emi(_scores(-20.0)) == 0.0


def test_enterprise_maturity_stage_boundaries() -> None:
    assert enterprise_maturity_stage(34.9).key == "ad_hoc"
    assert enterprise_maturity_stage(35.0).key == "structured"
    assert enterprise_maturity_stage(54.9).key == "structured"
    assert enterprise_maturity_stage(55.0).key == "governed"
    assert enterprise_maturity_stage(74.9).key == "governed"
    assert enterprise_maturity_stage(75.0).key == "scaled"
    assert enterprise_maturity_stage(89.9).key == "scaled"
    assert enterprise_maturity_stage(90.0).key == "autonomous_enterprise"
    # Bilingual labels are always populated.
    stage = enterprise_maturity_stage(80.0)
    assert stage.label_ar and stage.label_en


def test_emi_to_ladder_level_boundaries() -> None:
    assert emi_to_ladder_level(34.0) == 0
    assert emi_to_ladder_level(35.0) == 1
    assert emi_to_ladder_level(47.9) == 1
    assert emi_to_ladder_level(48.0) == 2
    assert emi_to_ladder_level(58.0) == 3
    assert emi_to_ladder_level(68.0) == 4
    assert emi_to_ladder_level(78.0) == 5
    assert emi_to_ladder_level(86.0) == 6
    assert emi_to_ladder_level(93.0) == 7
    assert emi_to_ladder_level(100.0) == 7


def test_enterprise_offer_recommendation_uses_offer_matrix() -> None:
    rec = enterprise_offer_recommendation(20.0)
    assert rec["ladder_level"] == 0
    assert rec["recommended_offer"]  # drawn from client_maturity_os.offer_matrix
    assert isinstance(rec["blocked_offers"], list)
    assert rec["note_ar"] and rec["note_en"]


def test_coverage_registry_has_twelve_systems() -> None:
    coverage = coverage_registry()
    assert len(coverage) == 12
    assert len(CORE_SYSTEMS) == 12
    for entry in coverage:
        assert entry.status in {"EXISTS", "PARTIAL", "MISSING"}


def test_coverage_summary_counts_consistent() -> None:
    summary = coverage_summary()
    assert summary["systems_total"] == 12
    assert summary["exists"] + summary["partial"] + summary["missing"] == 12
    assert 0.0 <= summary["coverage_pct"] <= 100.0


def test_module_coverage_real_vs_fabricated_paths() -> None:
    real = "auto_client_acquisition.agentic_enterprise_os.enterprise_maturity"
    fake = "auto_client_acquisition.this_module_does_not_exist_xyz"

    all_real = module_coverage(CoreSystemSpec("t", "T", "ت", (real,)))
    assert all_real.status == "EXISTS"

    mixed = module_coverage(CoreSystemSpec("t", "T", "ت", (real, fake)))
    assert mixed.status == "PARTIAL"
    assert mixed.missing_paths == (fake,)

    all_fake = module_coverage(CoreSystemSpec("t", "T", "ت", (fake,)))
    assert all_fake.status == "MISSING"
