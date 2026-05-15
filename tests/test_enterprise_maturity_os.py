"""Enterprise maturity OS — stages, readiness gates, verification, assessment."""

from __future__ import annotations

from auto_client_acquisition.enterprise_maturity_os.maturity_assessment import (
    assess_current_platform,
    assess_platform_maturity,
)
from auto_client_acquisition.enterprise_maturity_os.readiness_gates import (
    GATE_CRITERIA,
    GATE_IDS,
    readiness_band,
    score_gate,
)
from auto_client_acquisition.enterprise_maturity_os.stages import (
    MAX_LEVEL,
    STAGES,
    next_stage,
    stage_for_level,
)
from auto_client_acquisition.enterprise_maturity_os.verification_systems import (
    VERIFICATION_SYSTEM_IDS,
    VERIFICATION_SYSTEMS,
    verification_coverage,
)

# --- Stages -----------------------------------------------------------------


def test_five_stages_ordered_levels_one_to_five() -> None:
    assert len(STAGES) == 5
    assert [s.level for s in STAGES] == [1, 2, 3, 4, 5]
    assert MAX_LEVEL == 5


def test_stages_have_bilingual_fields_and_signals() -> None:
    for s in STAGES:
        assert s.stage_id.strip()
        assert s.name_en.strip() and s.name_ar.strip()
        assert s.description_ar.strip()
        assert len(s.entry_signals) >= 2


def test_stage_for_level_clamps_out_of_range() -> None:
    assert stage_for_level(0).level == 1
    assert stage_for_level(99).level == 5
    assert stage_for_level(3).stage_id == "enterprise_ai_platform"


def test_next_stage_tops_out() -> None:
    assert next_stage(1).level == 2
    assert next_stage(5) is None


# --- Readiness gates --------------------------------------------------------


def test_ten_gates_each_weight_sum_is_100() -> None:
    assert len(GATE_IDS) == 10
    for gate_id, criteria in GATE_CRITERIA.items():
        assert sum(criteria.values()) == 100, gate_id


def test_score_gate_bounds_and_breakdown() -> None:
    empty = score_gate("governance", {})
    assert empty.score == 0
    full = score_gate("governance", dict.fromkeys(GATE_CRITERIA["governance"], True))
    assert full.score == 100
    assert set(full.breakdown) == set(GATE_CRITERIA["governance"])


def test_readiness_band_boundaries() -> None:
    assert readiness_band(0) == "prototype"
    assert readiness_band(59) == "prototype"
    assert readiness_band(60) == "internal_beta"
    assert readiness_band(74) == "internal_beta"
    assert readiness_band(75) == "client_pilot"
    assert readiness_band(84) == "client_pilot"
    assert readiness_band(85) == "enterprise_ready"
    assert readiness_band(94) == "enterprise_ready"
    assert readiness_band(95) == "mission_critical"
    assert readiness_band(100) == "mission_critical"


# --- Verification systems ---------------------------------------------------


def test_five_verification_systems() -> None:
    assert len(VERIFICATION_SYSTEMS) == 5
    assert len(VERIFICATION_SYSTEM_IDS) == 5


def test_verification_coverage_bounds() -> None:
    for system_id in VERIFICATION_SYSTEM_IDS:
        assert verification_coverage(system_id, {}) == 0
    sys0 = VERIFICATION_SYSTEMS[0]
    all_met = dict.fromkeys(sys0.checks, True)
    assert verification_coverage(sys0.system_id, all_met) == 100


# --- Assessment engine ------------------------------------------------------


def test_all_zero_evidence_is_ai_tool_prototype() -> None:
    result = assess_platform_maturity()
    assert result.current_stage.stage_id == "ai_tool"
    assert result.current_band == "prototype"
    assert result.next_stage is not None


def test_all_perfect_evidence_reaches_top_stage() -> None:
    gate_evidence = {
        gate_id: dict.fromkeys(criteria, True)
        for gate_id, criteria in GATE_CRITERIA.items()
    }
    verification_evidence = {
        v.system_id: dict.fromkeys(v.checks, True) for v in VERIFICATION_SYSTEMS
    }
    result = assess_platform_maturity(
        gate_evidence=gate_evidence,
        verification_evidence=verification_evidence,
    )
    assert result.current_stage.stage_id == "agentic_enterprise_infrastructure"
    assert result.current_band == "mission_critical"
    assert result.next_stage is None
    assert result.blockers == ()


def test_high_gates_low_verification_cannot_reach_stage_four() -> None:
    """Strong gates but unproven verification must stall below Agentic Operating Platform."""
    gate_evidence = {
        gate_id: dict.fromkeys(criteria, True)
        for gate_id, criteria in GATE_CRITERIA.items()
    }
    result = assess_platform_maturity(
        gate_evidence=gate_evidence,
        verification_evidence={},
    )
    assert result.overall_gate_score == 100
    assert result.overall_verification_coverage == 0
    assert result.current_stage.level < 4
    assert any(b.startswith("verification:") for b in result.blockers)


def test_current_platform_assessment_is_deterministic() -> None:
    first = assess_current_platform()
    second = assess_current_platform()
    assert first.to_dict() == second.to_dict()
    # Honest baseline: governance/security are strong, executive proof is not.
    assert first.gate_scores["governance"] == 100
    assert first.verification_coverages["executive_proof"] == 0
    assert first.current_stage.level >= 3
