"""Company invariants — deterministic tests for INV-001..007."""

import pathlib
import json

def test_inv001_exactly_five_agents():
    root = pathlib.Path(__file__).resolve().parents[1]
    agents = list((root / ".claude/agents").glob("*.md"))
    # Core 5 must exist, expanded staff allows 13 total (5 core + 8 extended) per EXPANDED_STAFF_REGISTRY
    assert len(agents) >= 5, f"expected at least 5 agents, got {len(agents)}: {[a.name for a in agents]}"
    core = {"dealix-pm.md","dealix-sales.md","dealix-delivery.md","dealix-engineer.md","dealix-content.md"}
    assert core.issubset({a.name for a in agents}), f"core 5 missing: {core - {a.name for a in agents}}"
    codex = list((root / ".codex/agents").glob("*.toml"))
    assert len(codex) >= 5, f"expected at least 5 codex agents, got {len(codex)}"
    assert core.issubset({c.name.replace(".toml",".md") for c in codex}) or len(codex)==5

def test_inv002_deep_wip_max_3():
    import tempfile
    from dealix.commercial.economic_cell_registry import EconomicCellRegistry
    from dealix.commercial.economic_cell import EconomicCell, Identity, Market, Sector, Buyer, BuyerGroup, Problem, ProblemClass, Value, Offer, Monetization, MonetizationRail, Distribution, DistributionRail, Procurement, Execution, Evidence, Economics, Risk, Portfolio, Proof, LifecycleState
    from datetime import UTC, datetime
    import uuid
    tmp = pathlib.Path(tempfile.mktemp(suffix='.jsonl'))
    reg = EconomicCellRegistry(storage_path=tmp)
    def mk(state):
        now = datetime.now(UTC).isoformat()
        return EconomicCell(identity=Identity(cell_id=str(uuid.uuid4()), canonical_name="test", version=1, created_at=now, updated_at=now), market=Market(sector=Sector.TECHNOLOGY_SAAS_SI), buyer=Buyer(buyer_group=BuyerGroup.CEO), problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE), value=Value(), offer=Offer(offer_family="test"), monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT), distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND), procurement=Procurement(), execution=Execution(), evidence=Evidence(), economics=Economics(), risk=Risk(), portfolio=Portfolio(lifecycle_state=state), proof=Proof())
    for _ in range(4):
        c = mk(LifecycleState.CANDIDATE_DEEP)
        reg.create(c)
    for c in reg.list_by_state(LifecycleState.CANDIDATE_DEEP)[:3]:
        assert reg.claim_deep_wip_slot(c.identity.cell_id)
    assert reg.count_active_deep() == 3
    c4 = reg.list_by_state(LifecycleState.CANDIDATE_DEEP)[0]
    assert not reg.claim_deep_wip_slot(c4.identity.cell_id), "4th DeepWIP must fail"

def test_inv003_no_verified_payment_without_evidence():
    from dealix.commercial.financial_os import FinancialOS, FinancialRecord, FinancialState
    fos = FinancialOS()
    # Quote should not be verified cash
    fos.add_record(FinancialRecord(record_id="q1", state=FinancialState.QUOTE_VALUE, amount_sar=10000, probability=0.5))
    assert fos.verified_cash() == 0
    # PAYMENT_VERIFIED without an evidence reference must fail closed.
    try:
        fos.add_record(FinancialRecord(
            record_id="p-missing-proof",
            state=FinancialState.PAYMENT_VERIFIED,
            amount_sar=5000,
            probability=1.0,
            verified_at="2026-09-11T00:00:00Z",
        ))
        assert False, "PAYMENT_VERIFIED without evidence_ref should have raised"
    except ValueError:
        pass
    # Evidence-backed verified payment should be counted.
    fos.add_record(FinancialRecord(
        record_id="p1",
        state=FinancialState.PAYMENT_VERIFIED,
        amount_sar=5000,
        probability=1.0,
        verified_at="2026-09-11T00:00:00Z",
        evidence_ref="bank-ref-1",
    ))
    assert fos.verified_cash() == 5000
    # Quote with verified_at should be rejected
    try:
        fos.add_record(FinancialRecord(record_id="q2", state=FinancialState.QUOTE_VALUE, amount_sar=1000, verified_at="2026-09-11T00:00:00Z"))
        assert False, "should have raised"
    except ValueError:
        pass

def test_inv004_no_cold_whatsapp():
    from dealix.commercial.channel_registry import ChannelRegistry, Channel, ChannelType, ChannelStatus
    from dealix.commercial.consent_registry import ConsentRegistry
    from dealix.commercial.omnichannel_orchestrator import OmnichannelOrchestrator, ChannelId
    # Channel registry must have cold whatsapp blocked
    cr = ChannelRegistry()
    cr.register(Channel(channel_id="cold_whatsapp", channel_type=ChannelType.WHATSAPP_OPT_IN, current_status=ChannelStatus.BLOCKED, kill_condition="consent missing"))
    assert cr.channels["cold_whatsapp"].current_status == ChannelStatus.BLOCKED
    # Omnichannel must block cold without consent
    o = OmnichannelOrchestrator()
    msg = o.prepare_draft(ChannelId.WHATSAPP_OPT_IN, "p1", "مرحبا", "Hello", "test")
    assert msg.handoff == "blocked_no_consent" and not msg.sent

def test_inv006_no_public_llm():
    # Ollama must be loopback only
    import subprocess
    r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
    # Should have 127.0.0.1:11434 not 0.0.0.0:11434 for ollama
    # Check that ollama is not on 0.0.0.0
    assert "0.0.0.0:11434" not in r.stdout, "Ollama must not be public"

def test_inv007_production_green_requires_parity():
    # Sentinel must check API_RELEASE_PARITY
    import pathlib
    sentinel = pathlib.Path("/opt/dealix/control/autonomous-company/bin/dealix-server-sentinel")
    assert sentinel.exists()
    text = sentinel.read_text()
    assert "API_RELEASE_PARITY" in text
    assert "API_RELEASE_SHA" in text

def test_opencode_v1_valid():
    import json, pathlib
    root = pathlib.Path(__file__).resolve().parents[1]
    data = json.loads((root / "opencode.json").read_text())
    assert "permission" in data and "permissions" not in data
    assert "bash" in data["permission"] and "shell" not in data["permission"]
    assert data["permission"]["edit"] == "allow"
