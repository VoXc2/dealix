"""Omega V3 commercial source readiness.

This module reports source-level readiness from canonical registries and policy.
It deliberately does not claim runtime health, deployed release identity, customer
value, payment, or Production Green.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from dealix.agentic_holding.runtime import ResourceGovernor, ResourceSnapshot, build_current_registry
from dealix.commercial.arm_registry import ALL_ARMS, get_active_arms
from dealix.commercial.company_invariants import INVARIANTS
from dealix.commercial.economic_cell import Sector
from dealix.commercial.saas_foundation import SaaSControlPlane
from dealix.commercial.saas_onboarding import SaaSOnboardingEngine
from dealix.commercial.sector_company_factory import SectorCompanyFactory


class LaunchReadiness(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sectors_ready: bool
    sector_companies: int
    arms_active: int
    arms_total: int
    agentic_holding_valid: bool
    logical_agents: int
    arm_pods: int
    unmapped_arms: list[str]
    orphan_failures: list[str]
    resource_governor_dynamic: bool
    roomy_worker_slots: int
    pressure_worker_slots: int
    saas_tenants: int
    saas_onboarding: bool
    solutions_source_ready: bool
    channels_governed: bool
    diagnostic_family_count: int
    invariant_count: int
    overall: bool
    source_only: bool = True
    runtime_acceptance: str = "NOT_PROVEN"
    deployed_release_identity: str = "NOT_PROVEN"
    generated_at: str = ""


def _sector_source_ready() -> tuple[bool, list[object]]:
    companies = SectorCompanyFactory().build_all()
    expected = {sector.value for sector in Sector}
    actual = [company.sector.value for company in companies]
    unique_complete = len(actual) == len(set(actual)) and set(actual) == expected
    execution_inputs = all(
        company.buyer_focus
        and company.top_problems
        and company.top_workflows
        and company.relevant_offers
        and company.diagnostic_families
        for company in companies
    )
    return bool(unique_complete and execution_inputs), companies


def _resource_governor_source_ready() -> tuple[bool, int, int]:
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
            incident_state="degraded",
            cpu_count=8,
        )
    )
    ok = (
        roomy.worker_slots > 3
        and roomy.writer_slots <= 2
        and pressure.worker_slots == 1
        and pressure.writer_slots <= pressure.worker_slots
        and not roomy.paid_model_allowed
        and not pressure.paid_model_allowed
    )
    return ok, roomy.worker_slots, pressure.worker_slots


def check() -> LaunchReadiness:
    sectors_ok, companies = _sector_source_ready()

    active_arms = get_active_arms()
    arm_ids = [arm.arm_id for arm in ALL_ARMS]
    active_ids = [arm.arm_id for arm in active_arms]
    arm_inventory_ok = (
        bool(active_ids)
        and len(arm_ids) == len(set(arm_ids))
        and len(active_ids) == len(set(active_ids))
    )

    registry = build_current_registry()
    registry_failures = registry.validate()
    registry_receipt = registry.receipt()
    agentic_ok = (
        not registry_failures
        and registry_receipt["unmapped_arms"] == []
        and registry_receipt["orphan_failures"] == []
        and registry_receipt["sector_companies"] == len(companies)
        and registry_receipt["distinct_arms"] == len(active_arms)
        and registry_receipt["arm_pods"] > 0
    )

    resource_ok, roomy_workers, pressure_workers = _resource_governor_source_ready()

    cp = SaaSControlPlane()
    cp.create_tenant("LaunchCo", "technology_saas_si")
    saas_ok = cp.market_control_score() >= 0
    onboarding = SaaSOnboardingEngine(cp)
    session = onboarding.start("LaunchCo2", "government_b2g")
    onboarding_ok = bool(session.data_isolation_verified)

    root = Path(__file__).resolve().parents[2]
    solutions_ok = (
        (root / "apps" / "web" / "app" / "page.tsx").is_file()
        and (root / "api" / "routers" / "solutions.py").is_file()
    )

    from dealix.commercial.omnichannel_orchestrator import ChannelId, OmnichannelOrchestrator

    orchestrator = OmnichannelOrchestrator()
    message = orchestrator.prepare_draft(ChannelId.WHATSAPP_OPT_IN, "p1", "hi", "hi", "test")
    channels_ok = message.handoff == "blocked_no_consent"

    from dealix.commercial.universal_diagnostic_factory import FAMILIES

    diagnostic_count = len(FAMILIES)
    invariant_count = len(INVARIANTS)

    overall = all(
        [
            sectors_ok,
            arm_inventory_ok,
            agentic_ok,
            resource_ok,
            saas_ok,
            onboarding_ok,
            solutions_ok,
            channels_ok,
            diagnostic_count > 0,
            invariant_count > 0,
        ]
    )

    return LaunchReadiness(
        sectors_ready=sectors_ok,
        sector_companies=len(companies),
        arms_active=len(active_arms),
        arms_total=len(ALL_ARMS),
        agentic_holding_valid=agentic_ok,
        logical_agents=int(registry_receipt["logical_agents"]),
        arm_pods=int(registry_receipt["arm_pods"]),
        unmapped_arms=list(registry_receipt["unmapped_arms"]),
        orphan_failures=list(registry_receipt["orphan_failures"]),
        resource_governor_dynamic=resource_ok,
        roomy_worker_slots=roomy_workers,
        pressure_worker_slots=pressure_workers,
        saas_tenants=len(cp.tenants),
        saas_onboarding=onboarding_ok,
        solutions_source_ready=solutions_ok,
        channels_governed=channels_ok,
        diagnostic_family_count=diagnostic_count,
        invariant_count=invariant_count,
        overall=overall,
        generated_at=datetime.now(UTC).isoformat(),
    )


__all__ = ["LaunchReadiness", "check"]
