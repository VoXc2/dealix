"""Moyasar payment side-effects — HubSpot + evidence."""

from __future__ import annotations

from dealix.commercial_ops.moyasar_payment_sync import (
    append_payment_evidence,
    sync_paid_payment_to_hubspot,
)


def test_sync_skips_unpaid() -> None:
    out = sync_paid_payment_to_hubspot(payment={"status": "pending"}, event_type="payment_created")
    assert out.get("skipped") is True


def test_evidence_skips_without_company(tmp_path, monkeypatch) -> None:
    import dealix.commercial_ops.evidence_append as ea

    csv_path = tmp_path / "evidence.csv"
    csv_path.write_text(
        "event_id,event_date,event_type,company,contact,motion,offer_id,owner,source_channel,notes,next_action,next_action_date,war_room_status\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ea, "EVIDENCE_TRACKER_CSV", csv_path)
    out = append_payment_evidence(
        payment={"status": "paid", "amount": 49900, "metadata": {}},
        event_type="payment_paid",
    )
    assert out.get("skipped") is True


def test_evidence_appends_on_paid(tmp_path, monkeypatch) -> None:
    import dealix.commercial_ops.evidence_append as ea

    csv_path = tmp_path / "evidence.csv"
    csv_path.write_text(
        "event_id,event_date,event_type,company,contact,motion,offer_id,owner,source_channel,notes,next_action,next_action_date,war_room_status\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ea, "EVIDENCE_TRACKER_CSV", csv_path)
    out = append_payment_evidence(
        payment={
            "status": "paid",
            "amount": 49900,
            "metadata": {"email": "client@agency.sa", "company": "Agency Co", "plan": "sprint_499"},
        },
        event_type="payment_paid",
    )
    assert out.get("evidence", {}).get("event_type") == "payment_received"
    text = csv_path.read_text(encoding="utf-8")
    assert "Agency Co" in text
    assert "payment_received" in text
