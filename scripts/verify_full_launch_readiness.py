#!/usr/bin/env python3
"""Dealix Omega V3 source-readiness verifier.

This verifier checks canonical registry/public-source invariants only. It never
claims deployed Production Green, runtime health, provider entitlement, or
customer/revenue truth.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dealix.agentic_holding.runtime import (  # noqa: E402
    ResourceGovernor,
    ResourceSnapshot,
    build_current_registry,
)
from dealix.commercial.arm_registry import ALL_ARMS, get_active_arms  # noqa: E402
from dealix.commercial.economic_cell import Sector  # noqa: E402
from dealix.commercial.sector_company_factory import SectorCompanyFactory  # noqa: E402


def _verify_sector_companies() -> tuple[list[str], list[object]]:
    companies = SectorCompanyFactory().build_all()
    sector_ids = [company.sector.value for company in companies]
    expected = {sector.value for sector in Sector}
    assert len(sector_ids) == len(set(sector_ids)), "duplicate sector company"
    assert set(sector_ids) == expected, (
        f"sector registry drift expected={sorted(expected)} actual={sorted(sector_ids)}"
    )
    for company in companies:
        assert company.buyer_focus, f"{company.sector.value}: buyer_focus missing"
        assert company.top_problems, f"{company.sector.value}: top_problems missing"
        assert company.top_workflows, f"{company.sector.value}: top_workflows missing"
        assert company.relevant_offers, f"{company.sector.value}: relevant_offers missing"
        assert company.diagnostic_families, f"{company.sector.value}: diagnostics missing"
    return sector_ids, companies


def _verify_arms_and_agentic_holding(sector_ids: list[str]) -> dict[str, object]:
    active_arms = get_active_arms()
    arm_ids = [arm.arm_id for arm in ALL_ARMS]
    active_ids = [arm.arm_id for arm in active_arms]
    assert arm_ids and len(arm_ids) == len(set(arm_ids)), "duplicate capability arm id"
    assert active_ids and len(active_ids) == len(set(active_ids)), "duplicate active arm id"

    registry = build_current_registry()
    failures = registry.validate()
    assert not failures, f"Agentic Holding registry failures: {failures}"
    receipt = registry.receipt()
    assert receipt["sector_companies"] == len(sector_ids)
    assert receipt["distinct_arms"] == len(active_arms)
    assert receipt["arm_pods"] > 0
    assert receipt["logical_agents"] > len(sector_ids)
    assert receipt["unmapped_arms"] == []
    assert receipt["orphan_failures"] == []
    return receipt


def _budget_dict(budget: object) -> dict[str, int | bool]:
    return {
        "worker_slots": int(getattr(budget, "worker_slots")),
        "writer_slots": int(getattr(budget, "writer_slots")),
        "paid_model_allowed": bool(getattr(budget, "paid_model_allowed")),
        "model_capacity_available": bool(getattr(budget, "model_capacity_available")),
        "host_cpu_cap": int(getattr(budget, "host_cpu_cap")),
    }


def _verify_resource_governor() -> tuple[dict[str, int | bool], dict[str, int | bool]]:
    governor = ResourceGovernor(max_workers=12, max_repo_writers=2)
    roomy = governor.budget(
        ResourceSnapshot(
            cpu_load=0.10,
            available_ram_mb=16_384,
            swap_pressure=0.0,
            disk_io_pressure=0.10,
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
    assert roomy.worker_slots > 3, "runtime capacity must not inherit historical DeepWIP=3 ceiling"
    assert roomy.writer_slots <= 2
    assert pressure.worker_slots == 1
    assert pressure.writer_slots <= pressure.worker_slots
    assert not roomy.paid_model_allowed
    assert not pressure.paid_model_allowed
    return _budget_dict(roomy), _budget_dict(pressure)


def _verify_public_source_truth() -> dict[str, object]:
    manifest_path = ROOT / "landing" / "public-surface-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rules = manifest["rules"]
    assert rules["public_fixed_agent_count_authority"] is False
    assert rules["public_fixed_pilot_price"] is False
    assert rules["public_fixed_pilot_duration_authority"] is False
    assert rules["public_live_checkout"] is False
    assert "Free Execution Diagnostic" in rules["canonical_commercial_truth"]
    assert "Sector Companies" in rules["canonical_agent_architecture"]
    assert (ROOT / "apps" / "web" / "app" / "page.tsx").is_file()
    assert (ROOT / "api" / "routers" / "solutions.py").is_file()
    return rules


def main() -> int:
    print("=== DEALIX OMEGA V3 SOURCE READINESS ===")
    sector_ids, _companies = _verify_sector_companies()
    print(f"SECTOR_COMPANIES=PASS count={len(sector_ids)} registry_derived=true")

    agentic = _verify_arms_and_agentic_holding(sector_ids)
    print(
        "AGENTIC_HOLDING=PASS "
        f"active_arms={agentic['distinct_arms']} logical_agents={agentic['logical_agents']} "
        f"arm_pods={agentic['arm_pods']} orphans=0"
    )

    roomy, pressure = _verify_resource_governor()
    print(
        "RESOURCE_GOVERNOR=PASS "
        f"roomy_workers={roomy['worker_slots']} pressure_workers={pressure['worker_slots']} "
        "historical_deepwip_ceiling=false paid_spill=false"
    )

    rules = _verify_public_source_truth()
    print(
        "PUBLIC_SOURCE_TRUTH=PASS "
        f"fixed_agent_count={rules['public_fixed_agent_count_authority']} "
        f"fixed_duration={rules['public_fixed_pilot_duration_authority']}"
    )

    print("SOURCE_READINESS=PASS")
    print("RUNTIME_ACCEPTANCE=NOT_PROVEN_BY_THIS_SCRIPT")
    print("DEPLOYED_RELEASE_IDENTITY=NOT_PROVEN_BY_THIS_SCRIPT")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
