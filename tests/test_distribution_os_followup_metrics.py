"""Distribution OS — follow-up cadence, proof, renewal metadata, win/loss, metrics."""

from __future__ import annotations

import pytest

from auto_client_acquisition.distribution_os import (
    draft_factory,
    followup,
    metrics,
    payment_handoff,
    proof_pack,
    proposal,
    prospect,
    renewal,
    win_loss,
)


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    for var, name in (
        ("DEALIX_PROSPECTS_PATH", "prospects.jsonl"),
        ("DEALIX_DRAFTS_PATH", "drafts.jsonl"),
        ("DEALIX_FOLLOWUPS_PATH", "followups.jsonl"),
        ("DEALIX_PROPOSALS_PATH", "proposals.jsonl"),
        ("DEALIX_PROOF_PACKS_PATH", "proof.jsonl"),
        ("DEALIX_PAYMENT_HANDOFFS_PATH", "pay.jsonl"),
        ("DEALIX_DELIVERY_HANDOFFS_PATH", "deliv.jsonl"),
        ("DEALIX_WIN_LOSS_PATH", "wl.jsonl"),
        ("DEALIX_RENEWAL_SCHEDULE_PATH", "renewal.jsonl"),
    ):
        monkeypatch.setenv(var, str(tmp_path / name))


def test_cadence_schedules_four_touches_in_order() -> None:
    fus = followup.schedule_cadence(
        prospect_id="p1", channel="email", start_date="2026-01-01T00:00:00+00:00"
    )
    assert [f.draft_type for f in fus] == [
        "outreach_first",
        "outreach_followup_1",
        "outreach_followup_2",
        "breakup",
    ]


def test_due_followups_respects_due_date() -> None:
    followup.schedule_cadence(prospect_id="p1", start_date="2026-01-01T00:00:00+00:00")
    due_day0 = followup.due_followups(on_date="2026-01-01T12:00:00+00:00")
    assert len(due_day0) == 1
    due_day5 = followup.due_followups(on_date="2026-01-05T12:00:00+00:00")
    assert len(due_day5) == 3


def test_complete_followup_drops_it_from_due() -> None:
    fus = followup.schedule_cadence(prospect_id="p1", start_date="2026-01-01T00:00:00+00:00")
    followup.complete_followup(fus[0].id, message_ref="draft_x")
    due = followup.due_followups(on_date="2026-01-01T12:00:00+00:00")
    assert all(f.id != fus[0].id for f in due)


def test_proof_pack_validates_evidence_level() -> None:
    with pytest.raises(ValueError):
        proof_pack.build_proof_pack(customer_id="c", evidence_level=9)
    pack = proof_pack.build_proof_pack(customer_id="c", quick_win="auto-followup", evidence_level=3)
    assert pack.evidence_level == 3
    assert proof_pack.list_proof_packs(customer_id="c")[0].id == pack.id


def test_upsell_ladder_from_sprint_is_taxonomy_only() -> None:
    ids = [u["id"] for u in renewal.upsell_ladder("prod_sprint_v1")]
    assert ids == ["prod_data_pack_v1", "prod_managed_ops_v1", "prod_custom_ai_v1"]
    assert renewal.next_upsell("prod_sprint_v1")["id"] == "prod_data_pack_v1"
    assert renewal.next_upsell("prod_custom_ai_v1") is None


def test_renewal_scheduler_reused() -> None:
    sched = renewal.schedule_renewal(customer_id="c", plan="managed_ops", amount_sar=2999)
    assert sched.customer_id == "c"
    assert renewal.list_by_customer("c")


def test_win_loss_summary() -> None:
    win_loss.record(company="A", sector="marketing_agencies", outcome="won", channel="email")
    win_loss.record(
        company="B", sector="clinics", outcome="lost", objection="price", channel="phone"
    )
    win_loss.record(company="C", sector="marketing_agencies", outcome="won", channel="email")
    s = win_loss.summarize()
    assert s["total"] == 3
    assert s["win_rate"] == round(2 / 3, 3)
    assert s["best_sector"] == "marketing_agencies"
    assert s["top_objection"] == "price"


def test_win_loss_rejects_invalid_outcome() -> None:
    with pytest.raises(ValueError):
        win_loss.record(company="A", outcome="maybe")


def test_daily_kpis_reflect_quote_bound_store_state() -> None:
    p = prospect.add_prospect(
        company="Acme",
        sector="marketing_agencies",
        pain_hypothesis="leaks",
        offer_angle="prod_sprint_v1",
        preferred_channel="email",
        risk="low",
    )
    draft_factory.generate_draft(prospect=p, draft_type="outreach_first")
    prop = proposal.generate_proposal(
        prospect_id=p.id,
        product_id="prod_sprint_v1",
        out_of_scope=["x"],
        discovery_ref="discovery:acme-001",
        quote_id="quote_acme_001",
        customer_specific_quote_sar=12500,
    )
    proof_pack.build_proof_pack(customer_id="Acme", evidence_level=1)
    payment_handoff.prepare_handoff(
        proposal_id=prop.id,
        customer_id="Acme",
        product_id="prod_sprint_v1",
        discovery_ref="discovery:acme-001",
        quote_id="quote_acme_001",
        amount_sar=12500,
    )
    win_loss.record(company="Acme", outcome="won")

    kpis = metrics.daily_kpis()
    assert kpis["prospects_total"] == 1
    assert kpis["drafts_generated"] == 1
    assert kpis["drafts_pending_approval"] == 1
    assert kpis["proposals_generated"] == 1
    assert kpis["proof_packs_generated"] == 1
    assert kpis["payment_handoffs"] == 1
    assert kpis["won_deals"] == 1


def test_snapshot_has_daily_and_weekly() -> None:
    snap = metrics.snapshot()
    assert "daily" in snap and "weekly" in snap
    assert "approval_rate" in snap["weekly"]
