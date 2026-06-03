"""Smoke tests for roadmap MVP slices (no full app import where avoidable)."""

from __future__ import annotations

from auto_client_acquisition.commercial_engagements.campaign_intelligence_sprint import (
    run_campaign_intelligence_sprint,
)
from auto_client_acquisition.commercial_engagements.delivery_catalog import (
    delivery_catalog_snapshot,
)
from auto_client_acquisition.commercial_engagements.schemas import (
    CampaignIntelligenceSprintInput,
)
from auto_client_acquisition.company_brain_mvp.memory import (
    ingest_chunk,
    query_workspace,
    reset_workspace,
)
from auto_client_acquisition.governance_os.policy_registry import forbidden_actions
from auto_client_acquisition.llm_gateway_v10 import (
    RoutingPolicy,
    assert_agent_plan_includes_compliance_guard,
    route_with_text_audit,
)
from auto_client_acquisition.revenue_data_intake.csv_preview import parse_account_csv


def test_csv_preview_parses_header() -> None:
    csv_text = "company_name,sector,city\nAcme,tech,Riyadh\n"
    out = parse_account_csv(csv_text)
    assert out["parsed_row_count"] == 1
    assert out["data_quality"]["row_count"] == 1


def test_delivery_catalog_contains_engagement_paths() -> None:
    snap = delivery_catalog_snapshot()
    assert any("lead-intelligence-sprint" in str(x) for x in snap["service_lines"])


def test_campaign_intel_audits() -> None:
    rep = run_campaign_intelligence_sprint(
        CampaignIntelligenceSprintInput(offer_title="Test", sector="SaaS", locale="en")
    )
    assert rep.angles
    assert isinstance(rep.risk_flags, list)


def test_company_brain_no_source_no_answer() -> None:
    reset_workspace("ws1")
    out = query_workspace(workspace_id="ws1", question="what is pricing?")
    assert out["answer_mode"] == "insufficient_evidence"
    ingest_chunk(workspace_id="ws1", text="Pricing is 999 SAR for pilot.", source_id="doc_pricing")
    out2 = query_workspace(workspace_id="ws1", question="pricing pilot")
    assert out2["answer_mode"] == "evidence_backed"
    assert out2["citations"][0]["source_id"] == "doc_pricing"


def test_policy_registry_loads() -> None:
    fa = forbidden_actions()
    assert "cold_whatsapp_auto_send" in fa


def test_llm_gateway_governance_shim() -> None:
    pol = RoutingPolicy(
        task_purpose="classification for support reply",
        language="ar",
        max_tokens=256,
    )
    dec, issues = route_with_text_audit(pol, draft_text_to_scan="safe text")
    assert dec.tier
    assert issues == []
    assert assert_agent_plan_includes_compliance_guard(
        ["StrategyAgent", "ComplianceGuardAgent"]
    ) == ["StrategyAgent", "ComplianceGuardAgent"]
