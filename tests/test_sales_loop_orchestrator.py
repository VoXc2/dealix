"""Unit tests for the Sales Loop Orchestrator — stage transitions."""
from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.sales_os import sales_loop_orchestrator as slo

_PAYLOAD = {
    "company": "Acme Retail",
    "email": "ops@acme-retail.sa",
    "sector": "retail",
    "region": "riyadh",
    "message": "we need help converting leads",
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
    """Resolve any open gate, then advance to ``target``."""
    if rec.pending_approval_id:
        orch.resolve_approval(
            loop_id=rec.loop_id,
            approval_id=rec.pending_approval_id,
            decision="approve",
            who="founder",
        )
    return await orch.advance(
        loop_id=rec.loop_id, target_stage=target, actor="founder", **kwargs,
    )


def test_start_loop_creates_record_at_message_drafted():
    rec = _orch().start_loop(
        raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co",
    )
    assert rec.loop_id.startswith("loop_")
    assert rec.stage == "message_drafted"
    assert rec.leadops_id
    assert rec.revenue_lead_id
    assert rec.pending_approval_id  # front-half draft gate is open


def test_start_loop_requires_customer_handle():
    with pytest.raises(ValueError, match="customer_handle"):
        _orch().start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="")


async def test_full_loop_reaches_closed_won():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    for target, kw in [
        ("founder_sent_manually", {}),
        ("replied", {}),
        ("diagnostic_requested", {}),
        ("diagnostic_delivered", {}),
        ("pilot_offered", {}),
        ("commitment_received", {"commitment_evidence": "email_signed_intent.png"}),
        ("payment_received", {"payment_evidence": "bank_ref_88421", "actual_amount_sar": 499}),
        ("delivery_started", {}),
        ("delivered", {}),
        ("proof_pack_delivered", {}),
        ("closed_won", {}),
    ]:
        rec = await _walk(orch, rec, target, **kw)
        assert rec.stage == target
    assert rec.stage == "closed_won"
    assert rec.payment_id
    assert rec.engagement_id


async def test_invalid_transition_raises_value_error():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    orch.resolve_approval(
        loop_id=rec.loop_id, approval_id=rec.pending_approval_id,
        decision="approve", who="founder",
    )
    with pytest.raises(ValueError, match="invalid transition"):
        await orch.advance(
            loop_id=rec.loop_id, target_stage="delivered", actor="founder",
        )


async def test_commitment_requires_evidence():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    for target in ("founder_sent_manually", "replied", "diagnostic_requested",
                   "diagnostic_delivered", "pilot_offered"):
        rec = await _walk(orch, rec, target)
    orch.resolve_approval(
        loop_id=rec.loop_id, approval_id=rec.pending_approval_id,
        decision="approve", who="founder",
    )
    with pytest.raises(ValueError, match="commitment_evidence"):
        await orch.advance(
            loop_id=rec.loop_id, target_stage="commitment_received", actor="founder",
        )


async def test_payment_requires_evidence_and_amount():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    for target, kw in [
        ("founder_sent_manually", {}), ("replied", {}),
        ("diagnostic_requested", {}), ("diagnostic_delivered", {}),
        ("pilot_offered", {}),
        ("commitment_received", {"commitment_evidence": "email_signed_intent.png"}),
    ]:
        rec = await _walk(orch, rec, target, **kw)
    orch.resolve_approval(
        loop_id=rec.loop_id, approval_id=rec.pending_approval_id,
        decision="approve", who="founder",
    )
    with pytest.raises(ValueError, match="payment_evidence"):
        await orch.advance(
            loop_id=rec.loop_id, target_stage="payment_received", actor="founder",
            actual_amount_sar=499,
        )


async def test_meeting_recorded_as_evidence_not_a_stage():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    rec = await _walk(orch, rec, "founder_sent_manually")
    rec = await _walk(orch, rec, "replied")
    rec = await _walk(orch, rec, "diagnostic_requested")
    # The meeting is captured as metadata + evidence; the stage is canonical.
    assert rec.stage == "diagnostic_requested"
    assert rec.booking_id
    assert rec.booking_meta is not None
    assert rec.booking_meta.get("provider") in ("manual", "calendly", "google")


async def test_advance_unknown_loop_id():
    with pytest.raises(KeyError):
        await _orch().advance(
            loop_id="loop_does_not_exist", target_stage="replied", actor="founder",
        )


async def test_next_actions_lists_valid_transitions():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    actions = orch.next_actions(rec.loop_id)
    assert actions["current_stage"] == "message_drafted"
    assert "founder_sent_manually" in actions["valid_transitions"]
    assert actions["gate_open"] is True


async def test_closed_lost_path_records_reason():
    orch = _orch()
    rec = orch.start_loop(raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co")
    orch.resolve_approval(
        loop_id=rec.loop_id, approval_id=rec.pending_approval_id,
        decision="approve", who="founder",
    )
    rec = await orch.advance(
        loop_id=rec.loop_id, target_stage="closed_lost", actor="founder",
        reason="budget_frozen",
    )
    assert rec.stage == "closed_lost"
    summaries = " ".join(e["summary"] for e in orch.audit_trail(rec.loop_id))
    assert "budget_frozen" in summaries
