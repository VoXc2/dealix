"""Commercial strategy snapshot — unified founder commercial hub."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from dealix.business_now.commercial_strategy import (
    build_commercial_strategy_snapshot,
    resolve_focus,
)

client = TestClient(app)


def test_commercial_strategy_has_seven_offers() -> None:
    snap = build_commercial_strategy_snapshot(
        commercial_kpi_pending=0,
        transformation_verdict="PASS",
        all_pilots_template_ready=False,
    )
    assert len(snap["offers_playbook"]) >= 7
    assert snap["focus"]["stage"]
    assert len(snap["guardrails_ar"]) >= 3
    assert len(snap["weekly_motions"]) >= 5


def test_focus_kpi_hygiene_when_pending() -> None:
    focus = resolve_focus(commercial_kpi_pending=6, transformation_verdict="PASS")
    assert focus["stage"] == "kpi_hygiene"
    assert focus["primary_offer_id"] is None


def test_focus_platform_repair() -> None:
    focus = resolve_focus(commercial_kpi_pending=0, transformation_verdict="FAIL")
    assert focus["stage"] == "platform_repair"


def test_no_invented_crm_revenue_fields() -> None:
    snap = build_commercial_strategy_snapshot(
        commercial_kpi_pending=0,
        transformation_verdict="PASS",
        all_pilots_template_ready=False,
    )
    blob = str(snap)
    assert "pipeline_sar" not in blob.lower() or "is_estimate" in blob
    ue = snap["unit_economics"]["gross_margin_demo"]
    assert ue.get("is_estimate") is True


def test_ops_client_pack_in_strategy() -> None:
    snap = build_commercial_strategy_snapshot(
        commercial_kpi_pending=0,
        transformation_verdict="PASS",
        all_pilots_template_ready=False,
    )
    pack = snap.get("ops_client_pack") or {}
    assert pack.get("runbook_doc")
    assert pack.get("sales_kit_deck")
    assert pack.get("demo_steps")


def test_api_commercial_strategy() -> None:
    res = client.get("/api/v1/business-now/commercial-strategy")
    assert res.status_code == 200
    body = res.json()
    assert "offers_playbook" in body
    assert "integration_truth_summary" in body
    assert body["integration_truth_summary"].get("overall_status")
    assert "upsell_matrix" in body["expansion"]
    assert "next_best_actions" in body
    assert body["quality_scores_demo"]["is_estimate"] is True
    upsell = body["expansion"]["upsell_matrix"]
    assert upsell and upsell[0].get("label_ar")


def test_snapshot_includes_commercial_strategy_summary() -> None:
    res = client.get("/api/v1/business-now/snapshot")
    assert res.status_code == 200
    body = res.json()
    assert "commercial_strategy_summary" in body
    assert "focus" in body["commercial_strategy_summary"]
