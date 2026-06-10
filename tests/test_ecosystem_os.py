"""Tests for ecosystem_os."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os import (
    ACADEMY_PORTAL_SIGNALS,
    BENCHMARK_PORTAL_SIGNALS,
    CERTIFICATION_LEVELS,
    ECOSYSTEM_LAUNCH_STEPS,
    ECOSYSTEM_METRICS_SIGNALS,
    PARTNER_GATE_CRITERIA,
    PARTNER_PORTAL_SIGNALS,
    PartnerQualityDimensions,
    VentureGateInput,
    academy_portal_coverage_score,
    benchmark_methodology_ok,
    benchmark_portal_coverage_score,
    certification_level_valid,
    certification_slug_for_level,
    ecosystem_launch_step_index,
    ecosystem_metrics_coverage_score,
    partner_gate_passes,
    partner_portal_coverage_score,
    partner_quality_band,
    partner_quality_score,
    venture_gate_passes,
)


def test_partner_quality() -> None:
    d = PartnerQualityDimensions(85, 85, 85, 85, 80, 80)
    s = partner_quality_score(d)
    assert s == 84
    assert partner_quality_band(s) == "implementation"


def test_partner_gate() -> None:
    full = frozenset(PARTNER_GATE_CRITERIA)
    assert partner_gate_passes(full) == (True, ())
    ok, miss = partner_gate_passes(frozenset())
    assert not ok and miss


def test_certification() -> None:
    assert certification_level_valid(3)
    assert certification_slug_for_level(4) == "dealix_certified_partner"
    assert len(CERTIFICATION_LEVELS) == 5


def test_benchmark() -> None:
    assert benchmark_methodology_ok(
        no_client_identifiers=True,
        no_pii=True,
        methodology_disclosed=True,
        limitations_stated=True,
    ) == (True, ())
    assert benchmark_portal_coverage_score(frozenset(BENCHMARK_PORTAL_SIGNALS)) == 100


def test_ecosystem_metrics() -> None:
    assert ecosystem_metrics_coverage_score(frozenset(ECOSYSTEM_METRICS_SIGNALS)) == 100
    assert ecosystem_launch_step_index("partner_referral_program") == 3


def test_portals() -> None:
    assert partner_portal_coverage_score(frozenset(PARTNER_PORTAL_SIGNALS)) == 100
    assert academy_portal_coverage_score(frozenset(ACADEMY_PORTAL_SIGNALS)) == 100


def test_venture_gate_delegates() -> None:
    v = VentureGateInput(
        paid_clients=5,
        retainers=2,
        proof_packs_count=10,
        avg_proof_score=82.0,
        repeatable_delivery=True,
        product_module_used=True,
        playbook_maturity=85.0,
        owner_exists=True,
        healthy_margin=True,
        core_os_dependency_documented=True,
    )
    assert venture_gate_passes(v)[0]
