"""Company OS — registry, maturity, roadmap, doctrine map."""

from __future__ import annotations

import pytest

from auto_client_acquisition.company_os import (
    NON_NEGOTIABLES,
    MaturityBand,
    RoadmapPhase,
    band_from_score,
    doctrine_coverage,
    gates_for_system,
    get_phase_gate,
    get_system,
    is_phase_active,
    list_systems,
    maturity_report,
    phase_gates,
    registry_digest,
    roadmap_digest,
    score_system,
    systems_for_gate,
    systems_for_phase,
)

_EXPECTED_SYSTEMS = {
    "delivery_system",
    "agent_factory",
    "governance_system",
    "knowledge_os",
    "executive_system",
    "evaluation_system",
    "transformation_system",
}


def test_seven_systems_registered() -> None:
    systems = list_systems()
    assert len(systems) == 7
    assert {s.system_id for s in systems} == _EXPECTED_SYSTEMS


def test_every_system_has_backing_modules_and_gates() -> None:
    for s in list_systems():
        assert s.backing_modules, f"{s.system_id} has no backing modules"
        assert s.doctrine_gates, f"{s.system_id} has no doctrine gates"
        assert s.name_ar and s.name_en


def test_get_system_unknown_raises() -> None:
    with pytest.raises(KeyError):
        get_system("does_not_exist")


def test_systems_for_phase() -> None:
    foundation = systems_for_phase(RoadmapPhase.FOUNDATION)
    assert foundation
    assert all(s.roadmap_phase == RoadmapPhase.FOUNDATION for s in foundation)


def test_registry_digest_shape() -> None:
    digest = registry_digest()
    assert digest["system_count"] == 7
    assert len(digest["systems"]) == 7


def test_band_from_score_boundaries() -> None:
    assert band_from_score(0) == MaturityBand.SEED
    assert band_from_score(39) == MaturityBand.SEED
    assert band_from_score(40) == MaturityBand.WORKING
    assert band_from_score(69) == MaturityBand.WORKING
    assert band_from_score(70) == MaturityBand.PROVEN
    assert band_from_score(89) == MaturityBand.PROVEN
    assert band_from_score(90) == MaturityBand.SCALED
    assert band_from_score(100) == MaturityBand.SCALED


def test_band_from_score_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        band_from_score(-1)
    with pytest.raises(ValueError):
        band_from_score(101)


def test_score_system_with_signals() -> None:
    sys = get_system("governance_system")
    base = score_system(sys)
    boosted = score_system(sys, signals={"has_api": True, "has_evals": True})
    assert boosted["score"] > base["score"]
    assert 0 <= boosted["score"] <= 100


def test_maturity_report_covers_all_systems() -> None:
    report = maturity_report()
    assert report["system_count"] == 7
    assert len(report["systems"]) == 7
    assert 0 <= report["average_score"] <= 100


def test_roadmap_has_four_phases() -> None:
    gates = phase_gates()
    assert len(gates) == 4
    assert {g.phase for g in gates} == set(RoadmapPhase)


def test_phase_three_and_four_are_deferred_gated() -> None:
    assert get_phase_gate(RoadmapPhase.AGENTIC_PLATFORM).deferred_gated is True
    assert get_phase_gate(RoadmapPhase.ENTERPRISE_READINESS).deferred_gated is True
    assert get_phase_gate(RoadmapPhase.FOUNDATION).deferred_gated is False


def test_deferred_phase_activates_only_at_three_pilots() -> None:
    assert is_phase_active(RoadmapPhase.FOUNDATION) is True
    assert is_phase_active(RoadmapPhase.AGENTIC_PLATFORM, paid_pilots=2) is False
    assert is_phase_active(RoadmapPhase.AGENTIC_PLATFORM, paid_pilots=3) is True
    assert is_phase_active(RoadmapPhase.ENTERPRISE_READINESS, paid_pilots=3) is True


def test_roadmap_digest_reflects_pilot_count() -> None:
    locked = roadmap_digest(paid_pilots=1)
    unlocked = roadmap_digest(paid_pilots=3)
    locked_phase3 = next(
        p for p in locked["phases"] if p["phase"] == RoadmapPhase.AGENTIC_PLATFORM.value
    )
    unlocked_phase3 = next(
        p for p in unlocked["phases"] if p["phase"] == RoadmapPhase.AGENTIC_PLATFORM.value
    )
    assert locked_phase3["active"] is False
    assert unlocked_phase3["active"] is True


def test_doctrine_coverage_is_complete() -> None:
    coverage = doctrine_coverage()
    assert coverage["non_negotiable_count"] == 11
    assert coverage["fully_covered"] is True
    assert coverage["unmapped"] == []


def test_every_non_negotiable_maps_to_a_system() -> None:
    coverage = doctrine_coverage()
    for gate in NON_NEGOTIABLES:
        assert coverage["mapping"][gate], f"{gate} has no enforcing system"


def test_systems_for_gate_and_gates_for_system() -> None:
    assert "agent_factory" in systems_for_gate("no_unbounded_agents")
    assert "no_unbounded_agents" in gates_for_system("agent_factory")
