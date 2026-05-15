"""Institutional Dependency Index — Layer 46 scoring + registry honesty tests."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.dealix_master_layers import MASTER_LAYERS
from auto_client_acquisition.institutional_dependency_os import (
    InstitutionalDependencyDimensions,
    dependency_band,
    dependency_blockers,
    institutional_dependency_index,
)

_FIELDS: tuple[str, ...] = (
    "control_plane_coverage",
    "agent_society_governed",
    "assurance_contract_coverage",
    "memory_fabric_traceability",
    "org_reasoning_depth",
    "resilience_recovery",
    "meta_governance_improvement",
    "value_measurability",
    "learning_loop_active",
    "operating_core_reliance",
)


def _dims(value: int = 0, **overrides: int) -> InstitutionalDependencyDimensions:
    values = dict.fromkeys(_FIELDS, value)
    values.update(overrides)
    return InstitutionalDependencyDimensions(**values)


def test_score_bounded_and_clamps_out_of_range() -> None:
    assert institutional_dependency_index(_dims(0)) == 0
    assert institutional_dependency_index(_dims(100)) == 100
    # Out-of-range inputs are clamped, not silently mis-scored.
    assert institutional_dependency_index(_dims(-50)) == 0
    assert institutional_dependency_index(_dims(500)) == 100


def test_all_full_is_operating_core_with_no_blockers() -> None:
    dims = _dims(100)
    score = institutional_dependency_index(dims)
    assert score == 100
    assert dependency_band(score) == "institutional_operating_core"
    assert dependency_blockers(dims) == ()


def test_one_thin_dimension_blocks_the_operating_core_claim() -> None:
    # A high index alone is not enough: a single thin system fires a named
    # blocker, so the operating-core claim is gated independently of the band.
    dims = _dims(100, assurance_contract_coverage=10)
    blockers = dependency_blockers(dims)
    assert "assurance_contract_coverage_thin" in blockers
    assert institutional_dependency_index(dims) >= 85  # weighted avg stays high
    assert blockers != ()  # but the claim is blocked


def test_several_thin_dimensions_relegate_the_band() -> None:
    dims = _dims(100, resilience_recovery=20, meta_governance_improvement=20)
    score = institutional_dependency_index(dims)
    assert score < 85
    assert dependency_band(score) != "institutional_operating_core"
    assert "resilience_recovery_thin" in dependency_blockers(dims)
    assert "meta_governance_not_self_improving" in dependency_blockers(dims)


def test_bands_cover_the_full_ladder() -> None:
    assert dependency_band(0) == "tool"
    assert dependency_band(55) == "platform"
    assert dependency_band(72) == "infrastructure"
    assert dependency_band(90) == "institutional_operating_core"


def test_institutional_layers_37_to_46_map_to_real_packages() -> None:
    repo = Path(__file__).resolve().parents[1]
    pkg_root = repo / "auto_client_acquisition"
    institutional = [
        layer for layer in MASTER_LAYERS if layer.folder[:2] in {str(n) for n in range(37, 47)}
    ]
    assert len(institutional) == 10
    for layer in institutional:
        assert layer.primary_packages, f"{layer.folder} has no package"
        for pkg in layer.primary_packages:
            assert (pkg_root / pkg).is_dir(), f"{layer.folder} -> missing package {pkg}"
