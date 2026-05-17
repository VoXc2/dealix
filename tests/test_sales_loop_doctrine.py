"""Doctrine guard tests for the Sales Loop Orchestrator.

Each test pins one of the 11 non-negotiables for this feature:
  #8  no external action without approval
  #9  no agent without identity
  #10 no project without a Proof Pack
  #11 no project without a Capital Asset
  #6  no PII in logs
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os.agent_registry import get_agent
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.capital_os.capital_ledger import list_assets
from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.sales_os import sales_loop_orchestrator as slo
from auto_client_acquisition.value_os.value_ledger import summarize

_PAYLOAD = {
    "company": "Acme Retail",
    "email": "secret-buyer@acme-retail.sa",
    "phone": "+966512345678",
    "sector": "retail",
    "region": "riyadh",
}


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_SALES_LOOP_LEDGER_PATH", str(tmp_path / "loop.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    monkeypatch.setenv("VALUE_LEDGER_BACKEND", "jsonl")
    slo.clear_for_test()
    get_default_pipeline().reset()
    yield


def _orch() -> slo.SalesLoopOrchestrator:
    return slo.get_default_sales_loop_orchestrator()


async def _walk(orch, rec, target, **kwargs):
    if rec.pending_approval_id:
        orch.resolve_approval(
            loop_id=rec.loop_id, approval_id=rec.pending_approval_id,
            decision="approve", who="founder",
        )
    return await orch.advance(
        loop_id=rec.loop_id, target_stage=target, actor="founder", **kwargs,
    )


async def _full_walk(orch, customer_handle="acme-co"):
    rec = orch.start_loop(
        raw_payload=_PAYLOAD, source="manual", customer_handle=customer_handle,
    )
    steps = [
        ("founder_sent_manually", {}), ("replied", {}),
        ("diagnostic_requested", {}), ("diagnostic_delivered", {}),
        ("pilot_offered", {}),
        ("commitment_received", {"commitment_evidence": "email_signed_intent.png"}),
        ("payment_received", {"payment_evidence": "bank_ref_88421", "actual_amount_sar": 499}),
        ("delivery_started", {}), ("delivered", {}),
        ("proof_pack_delivered", {}), ("closed_won", {}),
    ]
    for target, kw in steps:
        rec = await _walk(orch, rec, target, **kw)
    return rec


# ── #9 no agent without identity ─────────────────────────────────

def test_orchestrator_is_a_registered_agent():
    _orch().start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    card = get_agent(slo.AGENT_ID)
    assert card is not None
    assert card.owner == "founder"


def test_orchestrator_autonomy_is_recommend_or_lower():
    _orch().start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    card = get_agent(slo.AGENT_ID)
    # L3 RECOMMEND: never auto-sends, never auto-confirms payment.
    assert card.autonomy_level <= int(AutonomyLevel.L3_RECOMMEND)


# ── #8 no external action without approval ───────────────────────

async def test_external_transition_opens_a_gate():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    rec = await _walk(orch, rec, "founder_sent_manually")
    rec = await _walk(orch, rec, "replied")
    rec = await _walk(orch, rec, "diagnostic_requested")
    rec = await _walk(orch, rec, "diagnostic_delivered")
    # The diagnostic is a client deliverable — a gate must now be open.
    assert rec.pending_approval_id is not None


async def test_open_gate_blocks_the_next_advance():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    # The front-half draft gate is open from start — advancing must 409.
    with pytest.raises(slo.SalesLoopGateError):
        await orch.advance(
            loop_id=rec.loop_id, target_stage="founder_sent_manually", actor="founder",
        )


# ── #10 / #11 no project without Proof Pack + Capital Asset ──────

async def test_closed_won_unreachable_without_proof_pack_stage():
    """``stage_policy`` forbids skipping ``proof_pack_delivered``."""
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    for target, kw in [
        ("founder_sent_manually", {}), ("replied", {}),
        ("diagnostic_requested", {}), ("diagnostic_delivered", {}),
        ("pilot_offered", {}),
        ("commitment_received", {"commitment_evidence": "email_signed_intent.png"}),
        ("payment_received", {"payment_evidence": "bank_ref_88421", "actual_amount_sar": 499}),
        ("delivery_started", {}), ("delivered", {}),
    ]:
        rec = await _walk(orch, rec, target, **kw)
    # From ``delivered`` you cannot jump straight to ``closed_won``.
    with pytest.raises(ValueError, match="invalid transition"):
        await orch.advance(
            loop_id=rec.loop_id, target_stage="closed_won", actor="founder",
        )


async def test_closed_won_produces_proof_pack_and_capital_asset():
    orch = _orch()
    rec = await _full_walk(orch)
    assert rec.stage == "closed_won"
    kinds = {e["kind"] for e in orch.audit_trail(rec.loop_id)}
    assert "proof_pack_assembled" in kinds  # #10
    assets = list_assets(customer_id="acme-co", engagement_id=rec.engagement_id)
    assert len(assets) >= 1  # #11


# ── #6 no PII in logs ────────────────────────────────────────────

async def test_audit_summaries_carry_no_pii():
    orch = _orch()
    rec = await _full_walk(orch)
    blob = " ".join(e["summary"] for e in orch.audit_trail(rec.loop_id))
    assert "secret-buyer@acme-retail.sa" not in blob
    assert "+966512345678" not in blob


# ── revenue truth ────────────────────────────────────────────────

async def test_payment_records_verified_revenue():
    orch = _orch()
    rec = await _full_walk(orch)
    assert rec.stage == "closed_won"
    summary = summarize(customer_id="acme-co")
    assert summary["verified"] == 499.0
