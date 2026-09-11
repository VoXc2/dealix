"""Launch Readiness — expanded, all sectors, all arms, all channels, SaaS comprehensive, market control."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from dealix.commercial.sector_company_factory import SectorCompanyFactory
from dealix.commercial.arm_registry import ALL_ARMS, get_active_arms
from dealix.commercial.saas_foundation import SaaSControlPlane
from dealix.commercial.saas_onboarding import SaaSOnboardingEngine
from dealix.commercial.economic_cell_registry import EconomicCellRegistry
from dealix.commercial.company_invariants import INVARIANTS
from dealix.commercial.scheduler_inventory import inventory_timers, classify_timers
from pathlib import Path

class LaunchReadiness(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sectors_ready: bool
    arms_active: int
    arms_total: int
    saas_tenants: int
    saas_onboarding: bool
    five_agents: bool
    deep_wip: bool
    five_hundred_cells: bool
    solutions_online: bool
    channels_governed: bool
    diagnostics_50: bool
    invariants_7: bool
    overall: bool
    generated_at: str = ""

def check() -> LaunchReadiness:
    scf_ok = len(SectorCompanyFactory().build_all()) == 20
    arms_ok = len(get_active_arms()) >= 42
    # SaaS
    cp = SaaSControlPlane()
    cp.create_tenant("LaunchCo", "technology_saas_si")
    saas_ok = cp.market_control_score() >= 0
    # Onboarding
    so = SaaSOnboardingEngine(cp)
    sess = so.start("LaunchCo2", "government_b2g")
    onboarding_ok = sess.data_isolation_verified
    # Agents
    agents_ok = len(list((Path(__file__).resolve().parents[2] / ".claude/agents").glob("*.md"))) >= 5
    # DeepWIP
    import tempfile
    from dealix.commercial.economic_cell import EconomicCell, Identity, Market, Sector, Buyer, BuyerGroup, Problem, ProblemClass, Value, Offer, Monetization, MonetizationRail, Distribution, DistributionRail, Procurement, Execution, Evidence, Economics, Risk, Portfolio, Proof, LifecycleState
    import uuid
    tmp = Path(tempfile.mktemp(suffix=".jsonl"))
    reg = EconomicCellRegistry(storage_path=tmp)
    def mk(state):
        now = datetime.now(UTC).isoformat()
        return EconomicCell(identity=Identity(cell_id=str(uuid.uuid4()), canonical_name="test", version=1, created_at=now, updated_at=now), market=Market(sector=Sector.TECHNOLOGY_SAAS_SI), buyer=Buyer(buyer_group=BuyerGroup.CEO), problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE), value=Value(), offer=Offer(offer_family="test"), monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT), distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND), procurement=Procurement(), execution=Execution(), evidence=Evidence(), economics=Economics(), risk=Risk(), portfolio=Portfolio(lifecycle_state=state), proof=Proof())
    for _ in range(4):
        c = mk(LifecycleState.CANDIDATE_DEEP)
        reg.create(c)
    for c in reg.list_by_state(LifecycleState.CANDIDATE_DEEP)[:3]:
        reg.claim_deep_wip_slot(c.identity.cell_id)
    deep_ok = reg.count_active_deep() == 3
    # 500 cells
    reg2 = EconomicCellRegistry(storage_path=Path(tempfile.mktemp(suffix=".jsonl")))
    cells500 = reg2.generate_addressable_universe(max_cells=500)
    cells_ok = len(cells500) == 500
    # Solutions online
    solutions_ok = (Path(__file__).resolve().parents[2] / "frontend/src/content/solutions.ts").exists() and (Path(__file__).resolve().parents[2] / "api/routers/solutions.py").exists()
    # Channels governed
    from dealix.commercial.omnichannel_orchestrator import OmnichannelOrchestrator, ChannelId
    o = OmnichannelOrchestrator()
    msg = o.prepare_draft(ChannelId.WHATSAPP_OPT_IN, "p1", "hi", "hi", "test")
    channels_ok = msg.handoff == "blocked_no_consent"
    # Diagnostics 50
    from dealix.commercial.universal_diagnostic_factory import FAMILIES
    diag_ok = len(FAMILIES) == 50
    # Invariants 7
    inv_ok = len(INVARIANTS) == 7
    overall = all([scf_ok, arms_ok, saas_ok, onboarding_ok, agents_ok, deep_ok, cells_ok, solutions_ok, channels_ok, diag_ok, inv_ok])
    return LaunchReadiness(
        sectors_ready=scf_ok,
        arms_active=len(get_active_arms()),
        arms_total=len(ALL_ARMS),
        saas_tenants=len(cp.tenants),
        saas_onboarding=onboarding_ok,
        five_agents=agents_ok,
        deep_wip=deep_ok,
        five_hundred_cells=cells_ok,
        solutions_online=solutions_ok,
        channels_governed=channels_ok,
        diagnostics_50=diag_ok,
        invariants_7=inv_ok,
        overall=overall,
        generated_at=datetime.now(UTC).isoformat(),
    )

__all__ = ["LaunchReadiness", "check"]
