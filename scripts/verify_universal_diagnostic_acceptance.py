#!/usr/bin/env python3
"""Synthetic acceptance for Universal Diagnostic Factory — 8 scenarios A-H."""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth, FAMILIES
from dealix.commercial.economic_cell_registry import EconomicCellRegistry
from dealix.commercial.financial_os import FinancialOS

def scenario(name, sector, size, buyer, problem, depth):
    f = UniversalDiagnosticFactory()
    families = f.compose(sector, size, buyer, problem, depth)
    questions = f.generate_questions(families[0]) if families else []
    leakage = f.economic_leakage([{"finding": f"manual {problem} delays", "evidence": "interview", "confidence": "WEAK_EVIDENCE"}])
    proposal = f.to_proposal(families, leakage)
    # Check offer matching
    offer_match = "NO_FIT" if not families else families[0].family_id
    # Evidence states
    evidence_ok = all(q.get("evidence_needed") for q in questions)
    # Next action
    next_action = proposal["next_step"]
    # L5 gating
    l5 = "tender_submission" in problem.lower()
    return {
        "scenario": name,
        "sector": sector,
        "buyer": buyer,
        "problem": problem,
        "families": [x.family_id for x in families][:5],
        "questions": len(questions),
        "leakage": len(leakage),
        "offer": offer_match,
        "evidence_ok": evidence_ok,
        "next_action": next_action,
        "l5": l5,
    }

def main() -> int:
    scenarios = [
        ("A", "construction_epc", "midmarket", "cfo", "project_to_cash", DiagnosticDepth.D2_FUNCTIONAL),
        ("B", "logistics_supply_chain", "midmarket", "coo", "shipment_exception", DiagnosticDepth.D2_FUNCTIONAL),
        ("C", "professional_services", "sme", "sales_director", "lead_to_proposal", DiagnosticDepth.D1_RAPID),
        ("D", "retail_commerce_ecommerce", "sme", "customer_service", "support_backlog", DiagnosticDepth.D1_RAPID),
        ("E", "industrial_manufacturing", "midmarket", "operations_director", "quality_failure", DiagnosticDepth.D2_FUNCTIONAL),
        ("F", "technology_saas_si", "enterprise", "ciso", "ai_governance_risk", DiagnosticDepth.D2_FUNCTIONAL),
        ("G", "government_b2g", "sme", "procurement_director", "supplier_readiness", DiagnosticDepth.D1_RAPID),
        ("H", "finance_fintech_insurance", "sme", "cfo", "fatoora", DiagnosticDepth.D2_FUNCTIONAL),
    ]
    ok = 0
    for s in scenarios:
        r = scenario(*s)
        print(f"{r['scenario']}: {r['sector']}/{r['buyer']}/{r['problem']} -> {r['families']} Q:{r['questions']} L:{r['leakage']} offer:{r['offer']} L5:{r['l5']}")
        if r["families"] and r["questions"] and r["evidence_ok"]:
            ok += 1
        else:
            print(f"  FAIL {r}")
    print(f"PASS {ok}/8 scenarios")
    # Test other invariants
    # Economic cell registry
    reg = EconomicCellRegistry(storage_path=Path(tempfile.mktemp(suffix=".jsonl")))
    cells = reg.generate_addressable_universe(max_cells=10)
    print(f"Registry 10 cells: {len(cells)}")
    # Financial truth
    fos = FinancialOS()
    from dealix.commercial.financial_os import FinancialRecord, FinancialState
    from datetime import UTC, datetime
    fos.add_record(FinancialRecord(record_id="q1", state=FinancialState.QUOTE_VALUE, amount_sar=10000, probability=0.5))
    assert fos.verified_cash() == 0, "quote should not be cash"
    fos.add_record(FinancialRecord(record_id="p1", state=FinancialState.PAYMENT_VERIFIED, amount_sar=5000, probability=1.0, verified_at=datetime.now(UTC).isoformat(), evidence_ref="ev_universal_diag"))
    assert fos.verified_cash() == 5000
    print("Financial truth PASS")
    # DeepWIP
    from dealix.commercial.deep_wip_enforcer import DeepWipEnforcer
    from dealix.commercial.economic_cell_registry import EconomicCellRegistry as ECR
    from dealix.commercial.economic_cell import EconomicCell, Identity, Market, Sector, Buyer, BuyerGroup, Problem, ProblemClass, Value, Offer, Monetization, MonetizationRail, Distribution, DistributionRail, Procurement, Execution, Evidence, Economics, Risk, Portfolio, Proof, LifecycleState
    from datetime import UTC, datetime
    import uuid
    tmp2 = Path(tempfile.mktemp(suffix=".jsonl"))
    reg2 = ECR(storage_path=tmp2)
    def mk(state):
        now = datetime.now(UTC).isoformat()
        return EconomicCell(identity=Identity(cell_id=str(uuid.uuid4()), canonical_name="test", version=1, created_at=now, updated_at=now), market=Market(sector=Sector.TECHNOLOGY_SAAS_SI), buyer=Buyer(buyer_group=BuyerGroup.CEO), problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE), value=Value(), offer=Offer(offer_family="test"), monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT), distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND), procurement=Procurement(), execution=Execution(), evidence=Evidence(), economics=Economics(), risk=Risk(), portfolio=Portfolio(lifecycle_state=state), proof=Proof())
    for _ in range(4):
        c = mk(LifecycleState.CANDIDATE_DEEP)
        reg2.create(c)
    for c in reg2.list_by_state(LifecycleState.CANDIDATE_DEEP)[:3]:
        assert reg2.claim_deep_wip_slot(c.identity.cell_id)
    assert reg2.count_active_deep() == 3
    c4 = reg2.list_by_state(LifecycleState.CANDIDATE_DEEP)[0]
    assert not reg2.claim_deep_wip_slot(c4.identity.cell_id)
    print("DeepWIP PASS")
    # Five agents
    import pathlib
    agents = list(pathlib.Path(" .claude/agents".replace(" ", "")).glob("*.md"))
    # Actually check workspace
    agents = list(Path(" .claude/agents".replace(" ", "")).glob("*.md")) if False else list(Path("/opt/dealix/workspace/dealix/.claude/agents").glob("*.md"))
    print(f"Agents {len(agents)}: {[a.name for a in agents]}")
    assert len(agents) >= 5, f"expected at least 5 got {len(agents)}"
    # Core 5 must exist, expanded staff (13) allowed per EXPANDED_STAFF_REGISTRY
    assert {"dealix-pm.md","dealix-sales.md","dealix-delivery.md","dealix-engineer.md","dealix-content.md"}.issubset({a.name for a in agents})
    print("Five agents PASS")
    # OpenCode
    import json
    data = json.loads(Path("/opt/dealix/workspace/dealix/opencode.json").read_text())
    assert "permission" in data and "permissions" not in data
    assert "bash" in data["permission"] and "shell" not in data["permission"]
    print("OpenCode V1 PASS")
    return 0 if ok == 8 else 1

if __name__ == "__main__":
    sys.exit(main())
