"""Governed Value OS HTTP surface — North Star, state machine, gates."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_state_machine_reference() -> None:
    resp = client.get("/api/v1/governed-value/state-machine")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "prepared_not_sent" in body["states"]
    assert body["level_labels"]["used_in_meeting"] == "L5"
    assert body["level_labels"]["invoice_paid"] == "L7_confirmed"
    assert body["transitions"]["prepared_not_sent"] == ["sent"]


def test_transition_blocked_without_founder_confirmation() -> None:
    resp = client.post(
        "/api/v1/governed-value/transition",
        json={"current": "prepared_not_sent", "target": "sent"},
    )
    assert resp.status_code == 403, resp.text
    detail = resp.json()["detail"]
    assert detail["code"] == "sent_requires_founder_confirmation"
    assert detail["reason_ar"] and detail["reason_en"]


def test_transition_allowed_with_founder_confirmation() -> None:
    resp = client.post(
        "/api/v1/governed-value/transition",
        json={
            "current": "prepared_not_sent",
            "target": "sent",
            "founder_confirmed": True,
        },
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["allowed"] is True


def test_transition_invoice_paid_requires_payment_ref() -> None:
    resp = client.post(
        "/api/v1/governed-value/transition",
        json={"current": "invoice_sent", "target": "invoice_paid"},
    )
    assert resp.status_code == 403
    assert resp.json()["detail"]["code"] == "l7_confirmed_requires_payment"


def test_gates_endpoint() -> None:
    resp = client.get(
        "/api/v1/governed-value/gates",
        params={"messages_sent": 5, "classified_replies": 1},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["total"] == 7
    assert body["gates"][0]["passed"] is True


def test_north_star_and_record_decision(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv(
        "DEALIX_GOVERNED_DECISIONS_PATH", str(tmp_path / "decisions.jsonl")
    )
    assert client.get("/api/v1/governed-value/north-star").json()["count"] == 0

    ok = client.post(
        "/api/v1/governed-value/decisions",
        json={
            "summary": "Convert diagnostic to sprint",
            "decision_kind": "offer_progression",
            "source_ref": "diagnostic_report_001",
            "approval_ref": "approval_center:appr_009",
            "evidence_refs": ["evt_l4_022"],
            "value_estimate_sar": 25000.0,
        },
    )
    assert ok.status_code == 200, ok.text
    assert ok.json()["decision"]["decision_id"].startswith("gvd_")
    assert client.get("/api/v1/governed-value/north-star").json()["count"] == 1


def test_record_decision_rejected_without_evidence(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv(
        "DEALIX_GOVERNED_DECISIONS_PATH", str(tmp_path / "decisions.jsonl")
    )
    resp = client.post(
        "/api/v1/governed-value/decisions",
        json={
            "summary": "Send invoice",
            "decision_kind": "billing",
            "source_ref": "crm_export",
            "approval_ref": "approval_center:appr_010",
            "evidence_refs": [],
        },
    )
    # Empty evidence_refs fails Pydantic min_length=1 → 422.
    assert resp.status_code == 422


def test_governed_service_catalog_endpoint() -> None:
    resp = client.get("/api/v1/services/governed")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["count"] == 7
    assert len(body["headline_services"]) == 3
