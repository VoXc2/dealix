"""End-to-end walk of the Sales Loop — lead all the way to closed_won."""
from __future__ import annotations

import pytest

from auto_client_acquisition.auditability_os.audit_event import list_events
from auto_client_acquisition.capital_os.capital_ledger import list_assets
from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.sales_os import sales_loop_orchestrator as slo
from auto_client_acquisition.value_os.value_ledger import summarize

_PAYLOAD = {
    "company": "Acme Retail",
    "email": "ops@acme-retail.sa",
    "sector": "retail",
    "region": "riyadh",
    "message": "manual lead follow-up is too slow",
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


async def test_lead_to_paid_full_loop():
    """Drive every transition, auto-approving each gate the loop opens."""
    orch = slo.get_default_sales_loop_orchestrator()
    rec = orch.start_loop(
        raw_payload=_PAYLOAD, source="manual", customer_handle="acme-co",
    )

    steps = [
        ("founder_sent_manually", {}),
        ("replied", {}),
        ("diagnostic_requested", {}),
        ("diagnostic_delivered", {}),
        ("pilot_offered", {}),
        ("commitment_received", {"commitment_evidence": "email_2026-05-17_signed_intent.png"}),
        ("payment_received", {"payment_evidence": "bank_statement_ref_8842", "actual_amount_sar": 499}),
        ("delivery_started", {}),
        ("delivered", {}),
        ("proof_pack_delivered", {}),
        ("closed_won", {}),
    ]

    for target, kwargs in steps:
        if rec.pending_approval_id:
            orch.resolve_approval(
                loop_id=rec.loop_id,
                approval_id=rec.pending_approval_id,
                decision="approve",
                who="founder",
            )
        rec = await orch.advance(
            loop_id=rec.loop_id, target_stage=target, actor="founder", **kwargs,
        )
        assert rec.stage == target

    # ── final state assertions ──────────────────────────────────
    assert rec.stage == "closed_won"
    assert rec.pending_approval_id is None
    assert rec.payment_id and rec.payment_id.startswith("pay_")
    assert rec.engagement_id
    assert rec.proposal_markdown and "Revenue Intelligence Sprint" in rec.proposal_markdown

    # Proof Pack (#10) + Capital Asset (#11) both produced.
    events = list_events(customer_id="acme-co", limit=500)
    assert any(e.kind == "proof_pack_assembled" for e in events)
    assert list_assets(customer_id="acme-co", engagement_id=rec.engagement_id)

    # Verified revenue landed in the value ledger.
    assert summarize(customer_id="acme-co")["verified"] == 499.0

    # The revenue-pipeline mirror reflects real revenue truth.
    assert get_default_pipeline().summary()["total_revenue_sar"] == 499
