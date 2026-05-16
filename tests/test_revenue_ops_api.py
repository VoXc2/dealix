from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from api.routers.invoices import _reset_invoices_alias
from api.routers.revenue_ops import _reset_revenue_ops_state
from auto_client_acquisition.approval_center import get_default_approval_store

client = TestClient(app)


def setup_function() -> None:
    _reset_revenue_ops_state()
    _reset_invoices_alias()
    get_default_approval_store().clear()


def test_revenue_ops_diagnostic_to_follow_up_flow() -> None:
    create_resp = client.post(
        "/api/v1/revenue-ops/diagnostics",
        json={
            "client_name": "Acme Consulting",
            "sector": "consulting",
            "crm_source_ref": "crm_export:q2",
            "requested_by": "sami",
            "pain_points": ["weak follow-up", "forecast unclear"],
        },
    )
    assert create_resp.status_code == 200, create_resp.text
    diagnostic_id = create_resp.json()["diagnostic_id"]

    upload_resp = client.post(
        "/api/v1/revenue-ops/upload",
        json={
            "diagnostic_id": diagnostic_id,
            "source_ref": "crm:file:acme_q2.csv",
            "filename": "acme_q2.csv",
            "row_count": 320,
            "quality_score": 0.71,
            "uploaded_by": "analyst_1",
        },
    )
    assert upload_resp.status_code == 200, upload_resp.text

    score_resp = client.post(
        "/api/v1/revenue-ops/score",
        json={
            "diagnostic_id": diagnostic_id,
            "opportunities": [
                {
                    "account_name": "Riyadh Tech Group",
                    "pipeline_stage": "proposal",
                    "estimated_value_sar": 150000,
                    "risk_signals": ["no_recent_touch"],
                    "source_ref": "crm:deal:1001",
                },
                {
                    "account_name": "GCC FinOps",
                    "pipeline_stage": "discovery",
                    "estimated_value_sar": 90000,
                    "risk_signals": ["budget_unclear", "timeline_unknown"],
                    "source_ref": "crm:deal:1002",
                },
            ],
        },
    )
    assert score_resp.status_code == 200, score_resp.text
    ranked = score_resp.json()["opportunities_ranked"]
    assert len(ranked) == 2
    assert ranked[0]["priority_score"] >= ranked[1]["priority_score"]

    draft_resp = client.post(
        f"/api/v1/revenue-ops/{diagnostic_id}/follow-up-drafts",
        json={"owner": "sami", "tone": "executive", "max_drafts": 2},
    )
    assert draft_resp.status_code == 200, draft_resp.text
    body = draft_resp.json()
    assert len(body["drafts"]) == 2
    assert body["approval"]["status"] == "pending"

    passport_resp = client.get(f"/api/v1/revenue-ops/{diagnostic_id}/decision-passport")
    assert passport_resp.status_code == 200, passport_resp.text
    passport = passport_resp.json()
    assert passport["decision_passport"]["approval"]["approval_id"] is not None
    assert passport["hard_gates"]["decision_passport_required"] is True


def test_evidence_events_and_invoice_aliases() -> None:
    create_resp = client.post(
        "/api/v1/revenue-ops/diagnostics",
        json={
            "client_name": "B2B Labs",
            "sector": "saas",
            "crm_source_ref": "crm_export:q3",
            "requested_by": "sami",
        },
    )
    diagnostic_id = create_resp.json()["diagnostic_id"]

    transitions = [
        "approved",
        "sent",
        "used_in_meeting",
        "scope_requested",
    ]
    for target_state in transitions:
        evidence_resp = client.post(
            "/api/v1/evidence/events",
            json={
                "diagnostic_id": diagnostic_id,
                "event_type": "workflow_progress",
                "summary_ar": "تقدم في الحالة التشغيلية",
                "summary_en": "Workflow state progressed",
                "source_ref": f"ops:{target_state}",
                "evidence_ref": f"proof:{target_state}",
                "target_state": target_state,
            },
        )
        assert evidence_resp.status_code == 200, evidence_resp.text

    invoice_resp = client.post(
        "/api/v1/invoices",
        json={
            "diagnostic_id": diagnostic_id,
            "customer_handle": "b2b_labs",
            "amount_sar": 25000,
            "description": "Revenue Intelligence Sprint",
            "mode": "manual_only",
            "mark_as_sent": True,
        },
    )
    assert invoice_resp.status_code == 200, invoice_resp.text
    invoice_body = invoice_resp.json()
    assert invoice_body["invoice"]["status"] == "sent"
    assert invoice_body["diagnostic_state"] == "invoice_sent"


def test_post_approvals_alias_creates_pending_request() -> None:
    response = client.post(
        "/api/v1/approvals",
        json={
            "object_type": "revenue_ops_follow_up_batch",
            "object_id": "rops_test",
            "action_type": "draft_email",
            "action_mode": "approval_required",
            "summary_ar": "مسودات متابعة جاهزة للمراجعة",
            "summary_en": "Follow-up drafts ready for review",
            "proof_impact": "decision_passport:rops_test",
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["approval"]["approval_id"].startswith("apr_")
    assert body["approval"]["status"] == "pending"
