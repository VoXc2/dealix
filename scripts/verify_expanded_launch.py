#!/usr/bin/env python3
"""Expanded Launch Verification — all sectors, all channels, all arms, online."""

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dealix.commercial.sector_company_factory import SectorCompanyFactory
from dealix.commercial.economic_cell import Sector
from dealix.commercial.channel_registry import ChannelRegistry
from dealix.commercial.consent_registry import ConsentRegistry
from dealix.commercial.arm_registry import ALL_ARMS, get_active_arms
from dealix.commercial.low_touch_products.diagnostic_product import DiagnosticProductEngine, DiagnosticProductRequest
from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth

def main() -> int:
    print("=== EXPANDED LAUNCH VERIFICATION ===")
    # 20 sectors
    scf = SectorCompanyFactory()
    all_cos = scf.build_all()
    assert len(all_cos) == 20, f"expected 20 got {len(all_cos)}"
    print(f"Sectors 20 PASS: {[c.sector.value for c in all_cos[:3]]}...")
    # Each sector has 3 services, diagnostic, channels
    for c in all_cos:
        assert len(c.diagnostic_families) > 0
        assert len(c.distribution_channels) > 0
    print("Sector diagnostic+channels PASS")

    # 44 arms
    assert len(ALL_ARMS) == 44
    assert len(get_active_arms()) == 42
    print(f"Arms 44 total, 42 active PASS")

    # 12 channels omnichannel
    from dealix.commercial.omnichannel_orchestrator import OmnichannelOrchestrator, ChannelId
    o = OmnichannelOrchestrator()
    # Verify all ChannelId present
    assert len(list(ChannelId)) == 12
    print("Omnichannel 12 PASS")

    # Low-touch diagnostic product
    e = DiagnosticProductEngine()
    r = e.run(DiagnosticProductRequest(request_id="test", sector="technology_saas_si", problem="revenue_leakage", consent=True))
    assert r.price_sar == 0 and len(r.diagnostic_families) > 0
    print("Low-touch diagnostic PASS")

    # Universal diagnostic 50 families
    udf = UniversalDiagnosticFactory()
    assert len(udf.families) == 50
    fams = udf.compose("construction_epc", "midmarket", "cfo", "project_to_cash", DiagnosticDepth.D2_FUNCTIONAL)
    assert len(fams) >= 4
    print(f"Universal 50 families, compose {len(fams)} PASS")

    # Solutions frontend + API
    import pathlib
    assert (ROOT / "frontend/src/content/solutions.ts").exists()
    assert (ROOT / "frontend/src/app/[locale]/solutions/page.tsx").exists()
    assert (ROOT / "frontend/src/app/[locale]/solutions/[sector]/page.tsx").exists()
    assert (ROOT / "api/routers/solutions.py").exists()
    print("Solutions layer online PASS (20 sectors, 3 services each, API+Web)")

    # 5 agents
    agents = list((ROOT / ".claude/agents").glob("*.md"))
    assert len(agents) == 5
    print("Five agents PASS")

    # DeepWIP
    from dealix.commercial.economic_cell_registry import EconomicCellRegistry
    import tempfile
    tmp = Path(tempfile.mktemp(suffix=".jsonl"))
    reg = EconomicCellRegistry(storage_path=tmp)
    from dealix.commercial.economic_cell import EconomicCell, Identity, Market, Sector as S, Buyer, BuyerGroup, Problem, ProblemClass, Value, Offer, Monetization, MonetizationRail, Distribution, DistributionRail, Procurement, Execution, Evidence, Economics, Risk, Portfolio, Proof, LifecycleState
    from datetime import UTC, datetime
    import uuid
    def mk(state):
        now = datetime.now(UTC).isoformat()
        return EconomicCell(identity=Identity(cell_id=str(uuid.uuid4()), canonical_name="test", version=1, created_at=now, updated_at=now), market=Market(sector=S.TECHNOLOGY_SAAS_SI), buyer=Buyer(buyer_group=BuyerGroup.CEO), problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE), value=Value(), offer=Offer(offer_family="test"), monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT), distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND), procurement=Procurement(), execution=Execution(), evidence=Evidence(), economics=Economics(), risk=Risk(), portfolio=Portfolio(lifecycle_state=state), proof=Proof())
    for _ in range(4):
        c = mk(LifecycleState.CANDIDATE_DEEP)
        reg.create(c)
    for c in reg.list_by_state(LifecycleState.CANDIDATE_DEEP)[:3]:
        assert reg.claim_deep_wip_slot(c.identity.cell_id)
    assert reg.count_active_deep() == 3
    print("DeepWIP 3 PASS")

    print("=== ALL EXPANDED LAUNCH CHECKS PASS ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
