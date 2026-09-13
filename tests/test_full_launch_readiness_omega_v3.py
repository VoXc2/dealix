from __future__ import annotations

import importlib.util
from pathlib import Path

from dealix.agentic_holding.runtime import ResourceGovernor, ResourceSnapshot, build_current_registry
from dealix.commercial.arm_registry import get_active_arms
from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_factory import SectorCompanyFactory


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "verify_full_launch_readiness.py"


def test_verifier_does_not_reassert_historical_fixed_runtime_counts() -> None:
    text = VERIFIER.read_text(encoding="utf-8").lower()
    assert "deepwip 3 pass" not in text
    assert "5 core agents + 8 expanded" not in text
    assert "assert len(all_arms) == 44" not in text
    assert "assert len(all_cos) == 20" not in text
    assert "frontend/src" not in text


def test_every_canonical_sector_builds_with_execution_inputs() -> None:
    companies = SectorCompanyFactory().build_all()
    assert {company.sector for company in companies} == set(Sector)
    for company in companies:
        assert company.buyer_focus
        assert company.top_problems
        assert company.top_workflows
        assert company.relevant_offers
        assert company.diagnostic_families


def test_all_active_arms_map_into_agentic_holding_without_orphans() -> None:
    registry = build_current_registry()
    receipt = registry.receipt()
    assert registry.validate() == []
    assert receipt["distinct_arms"] == len(get_active_arms())
    assert receipt["unmapped_arms"] == []
    assert receipt["orphan_failures"] == []


def test_resource_governor_scales_and_throttles_instead_of_fixed_three() -> None:
    governor = ResourceGovernor(max_workers=12, max_repo_writers=2)
    roomy = governor.budget(
        ResourceSnapshot(
            cpu_load=0.1,
            available_ram_mb=16384,
            swap_pressure=0.0,
            disk_io_pressure=0.1,
            provider_quota_fraction=0.5,
            model_quota_fraction=0.5,
            worktree_slots=4,
            cpu_count=8,
        )
    )
    pressure = governor.budget(
        ResourceSnapshot(
            cpu_load=0.95,
            available_ram_mb=900,
            swap_pressure=0.85,
            disk_io_pressure=0.95,
            provider_quota_fraction=None,
            model_quota_fraction=None,
            worktree_slots=4,
            cpu_count=8,
            incident_state="degraded",
        )
    )
    assert roomy.worker_slots > 3
    assert pressure.worker_slots == 1
    assert not roomy.paid_model_allowed
    assert not pressure.paid_model_allowed
