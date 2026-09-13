from __future__ import annotations

from pathlib import Path

from dealix.commercial.launch_readiness import check
from dealix.commercial.next_expansion import NextExpansion


ROOT = Path(__file__).resolve().parents[1]


def test_launch_readiness_is_registry_and_resource_governed() -> None:
    readiness = check()
    assert readiness.sectors_ready
    assert readiness.sector_companies > 0
    assert readiness.arms_active > 0
    assert readiness.agentic_holding_valid
    assert readiness.unmapped_arms == []
    assert readiness.orphan_failures == []
    assert readiness.resource_governor_dynamic
    assert readiness.roomy_worker_slots > 3
    assert readiness.pressure_worker_slots == 1
    assert readiness.runtime_acceptance == "NOT_PROVEN"
    assert readiness.deployed_release_identity == "NOT_PROVEN"


def test_launch_readiness_source_has_no_legacy_fixed_architecture_fields() -> None:
    text = (ROOT / "dealix/commercial/launch_readiness.py").read_text(encoding="utf-8").lower()
    for stale in (
        "five_agents",
        "deep_wip:",
        "five_hundred_cells",
        "diagnostics_50",
        "invariants_7",
        "== 20",
        ">= 42",
        "frontend/src",
    ):
        assert stale not in text


def test_next_expansion_does_not_mint_arbitrary_double_targets() -> None:
    result = NextExpansion().execute()
    assert result["expansion_mode"] == "EVIDENCE_DRIVEN_REGISTRY_GROWTH"
    assert result["next_sectors_target"] == result["current_sectors"]
    assert result["next_arms_target"] == result["current_arms"]
    assert "40" not in result["next_action"]
    assert "88" not in result["next_action"]
    assert "DeepWIP 3" not in result["next_action"]


def test_comprehensive_launch_does_not_reassert_fixed_market_control_counts() -> None:
    text = (ROOT / "dealix/commercial/comprehensive_launch.py").read_text(encoding="utf-8")
    assert "20 sectors × 44 arms" not in text
    assert "DeepWIP 3" not in text
    assert "counts_are_architecture_authority" in text
