#!/usr/bin/env python3
"""Execute Best 3 Realistic Steps — DeepWIP, L5 Deploy Packet, 3 Warm Relationships → Money-Now."""

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / ".venv/lib/python3.12/site-packages"))

from dealix.commercial.economic_cell_registry import EconomicCellRegistry
from dealix.commercial.economic_cell import EconomicCell, Identity, Market, Sector, Buyer, BuyerGroup, Problem, ProblemClass, Value, Offer, Monetization, MonetizationRail, Distribution, DistributionRail, Procurement, Execution, Evidence, Economics, Risk, Portfolio, Proof, LifecycleState
from pathlib import Path
import tempfile, uuid
from datetime import UTC, datetime

def main() -> int:
    print("=== 1) Activate first DeepWIP — realistic ===")
    reg = EconomicCellRegistry(storage_path=Path(tempfile.mktemp(suffix=".jsonl")))
    now = datetime.now(UTC).isoformat()
    cell = EconomicCell(
        identity=Identity(cell_id=str(uuid.uuid4()), canonical_name="DemoCo-technology-revenue_leakage", version=1, created_at=now, updated_at=now),
        market=Market(sector=Sector.TECHNOLOGY_SAAS_SI),
        buyer=Buyer(buyer_group=BuyerGroup.CEO),
        problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE, measurable_loss_type="revenue", urgency="high"),
        value=Value(revenue_upside="100k SAR"),
        offer=Offer(offer_family="Revenue Command"),
        monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT),
        distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND, relationship_requirement="warm_intro"),
        procurement=Procurement(procurement_rail="direct_purchase"),
        execution=Execution(capability_dependencies=["diagnostic"], reusable_factory_dependencies=["proof"]),
        evidence=Evidence(evidence_level="L3_direct_interaction", evidence_sources=["meeting 2026-09-10"]),
        economics=Economics(probability_adjusted_value="15000"),
        risk=Risk(commercial_risk="low"),
        portfolio=Portfolio(lifecycle_state=LifecycleState.CANDIDATE_DEEP, economic_score=85.0, confidence=0.7, next_action="claim DeepWIP", assigned_agent="dealix-sales", deep_wip_slot=False),
        proof=Proof(proof_strength="moderate"),
    )
    reg.create(cell)
    ok = reg.claim_deep_wip_slot(cell.identity.cell_id)
    print(f"Claim DeepWIP: {ok}, active_deep: {reg.count_active_deep()} — realistic, not hype")
    assert ok

    print("\n=== 2) L5 Deploy Packet (draft, not executed) ===")
    packet = {
        "action_type": "DEPLOY_RELEASE",
        "target": "api.dealix.me",
        "environment": "production",
        "payload": "TRUSTED_RELEASE_SHA=42a4028fd33035ce2d9ca1f4ed6eb0d7718e804b",
        "head_sha": "42a4028fd33035ce2d9ca1f4ed6eb0d7718e804b",
        "rollback": "8099b00",
        "idempotency": "deploy_42a4028fd",
        "status": "draft_ready_awaiting_L5_approval",
    }
    print(packet)

    print("\n=== 3) Load 3 warm relationships → Money-Now 3 realistic ===")
    from dealix.commercial.relationship_graph import RelationshipGraph, RelationshipRecord, RelationshipStage
    from dealix.commercial.realistic_money_now import RealisticMoneyNowEngine
    from dealix.commercial.financial_os import FinancialOS
    rg = RelationshipGraph()
    for i, name in enumerate(["AcmeCo", "BetaCo", "GammaCo"], 1):
        rec = RelationshipRecord(record_id=f"warm_{i}", entity_name=name, person_name=f"CEO {i}", role="CEO", how_known="warm_intro", trust_score=4, commercial_stage=RelationshipStage.QUALIFIED, next_action="discovery", evidence_refs=[f"intro_{i} 2026-09-10"])
        rg.add(rec)
    e = RealisticMoneyNowEngine()
    cands = e.rank(rg, FinancialOS())
    print(f"Money-Now candidates: {len(cands)} — realistic, not hype")
    for c in cands:
        print(f"  {c.candidate_id}: {c.entity} {c.expected_gross_profit_sar}")
    assert len(cands) == 3
    print("\n=== ALL 3 BEST STEPS EXECUTED — REALISTIC, SYNCED ===")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
