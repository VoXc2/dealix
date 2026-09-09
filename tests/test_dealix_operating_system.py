"""Tests for Dealix Operating System.

- Send gate never allows auto-sends.
- Commercial strategy never invents price authority.
- Bilingual outputs support en/ar/both.
- Research works without API keys.
- Communication hub is approval-first.
"""

from __future__ import annotations

from datetime import UTC

import pytest

from intelligence import (
    CommunicationHub,
    CustomerSuccessOperatingSystem,
    DeepResearchEngine,
    GrowthOperatingSystem,
    KnowledgeAccumulator,
    NegotiationEngine,
    SalesOperatingSystem,
    SendGate,
    SendGateViolation,
    list_packages,
    validate_sku,
)


def test_send_gate_blocked():
    assert SendGate.OUTBOUND_SEND_DISABLED is True


def test_send_gate_raises_on_send_attempt():
    with pytest.raises(SendGateViolation):
        SendGate.assert_blocked("send")


def test_legacy_packages_remain_compatibility_metadata():
    packages = list_packages()
    assert "Revenue Diagnostic" in packages
    assert "Lead Sprint" in packages


def test_invalid_sku_rejected_by_legacy_catalog_validator():
    assert validate_sku("Fake Package") is False
    assert validate_sku("Revenue Diagnostic") is True


def test_list_objections_bilingual():
    engine = NegotiationEngine()
    result = engine.list_objections(lang="both")
    assert "objections" in result
    assert result["governance_note"]["ar_available"] is True


def test_deal_strategy_does_not_infer_catalog_price():
    engine = NegotiationEngine()
    result = engine.generate_deal_strategy(
        company_name="Najm Tech",
        sector="software",
        city="Riyadh",
        package_sku="Revenue Diagnostic",
        employees=50,
        lang="both",
    )
    anchor = result["deal_strategy"]["pricing_anchor"]
    assert anchor["requested_package_context"] == "Revenue Diagnostic"
    assert anchor["commercial_mode"] == "quote_only_after_qualified_discovery"
    assert anchor["base_price_sar"] is None
    assert anchor["adjusted_price_sar"] is None
    assert anchor["roi_estimate_percent"] is None
    assert anchor["approval_required"] is True
    assert anchor["execution_allowed"] is False


def test_unknown_package_label_is_context_not_commercial_authority():
    engine = NegotiationEngine()
    result = engine.generate_deal_strategy(
        "X",
        "software",
        "Riyadh",
        "No Such Package",
    )
    anchor = result["deal_strategy"]["pricing_anchor"]
    assert anchor["requested_package_context"] == "No Such Package"
    assert anchor["adjusted_price_sar"] is None
    assert result["authority"]["public_fixed_pilot_price_allowed"] is False
    assert result["authority"]["execution_allowed"] is False


def test_research_without_api_keys(tmp_path):
    engine = DeepResearchEngine(
        knowledge=KnowledgeAccumulator(store_path=tmp_path / "research.json")
    )
    result = engine.research("Saudi fintech market", sector="fintech", lang="both")
    assert result.findings
    assert result.confidence > 0


def test_company_dossier_returns_data(tmp_path):
    engine = DeepResearchEngine(
        knowledge=KnowledgeAccumulator(store_path=tmp_path / "dossier.json")
    )
    dossier = engine.company_dossier("Acme Saudi", lang="both")
    assert dossier["company_name"] == "Acme Saudi"
    assert "icp_score" in dossier


def test_available_sources_safe(tmp_path):
    engine = DeepResearchEngine(
        knowledge=KnowledgeAccumulator(store_path=tmp_path / "sources.json")
    )
    sources = engine.available_sources()
    assert len(sources) > 0
    assert all("configured" in s for s in sources)


def test_knowledge_ingest_and_search(tmp_path):
    acc = KnowledgeAccumulator(store_path=tmp_path / "knowledge.json")
    from datetime import datetime

    from intelligence.bilingual import BilingualRenderer
    from intelligence.knowledge_accumulator import KnowledgeEntry

    entry = KnowledgeEntry(
        entry_id="k1",
        category="market_signal",
        title=BilingualRenderer.bt("Fintech grows", "الفينتك ينمو"),
        content=BilingualRenderer.bt("Market data", "بيانات السوق"),
        source="test",
        sector="fintech",
        company=None,
        tags=["test"],
        confidence=0.9,
        created_at=datetime.now(UTC).isoformat(),
        expires_at=None,
    )
    acc.ingest(entry)
    results = acc.search("Fintech")
    assert len(results) == 1


def test_knowledge_daily_digest(tmp_path):
    acc = KnowledgeAccumulator(store_path=tmp_path / "knowledge.json")
    digest = acc.daily_digest(lang="both")
    assert "date" in digest
    assert "recent_24h_count" in digest


def test_draft_creation_blocked(tmp_path):
    hub = CommunicationHub()
    with pytest.raises(SendGateViolation):
        hub.create_draft(
            contact_id="c1",
            company_name="Najm Tech",
            contact_name="Ahmed",
            channel="email",
            subject_en="Hello",
            subject_ar="مرحبا",
            body_en="This is a draft.",
            body_ar="هذه مسودة.",
        )


def test_no_send_endpoint_exists():
    assert not hasattr(CommunicationHub, "send")


def test_sales_playbook_bilingual():
    os = SalesOperatingSystem()
    result = os.get_pipeline_playbook(lang="both")
    assert "playbook" in result
    assert len(result["playbook"]) > 0


def test_deal_review_returns_insights():
    os = SalesOperatingSystem()
    deal = {
        "deal_id": "d1",
        "company_name": "Najm Tech",
        "stage": "proposal_sent",
        "value_sar": 60000,
        "days_in_stage": 20,
        "activities_count": 1,
    }
    result = os.review_deal(deal, lang="both")
    assert result["deal_review"]["health_score"] > 0
    assert result["deal_review"]["risk_flags"]


def test_weekly_brief():
    os = SalesOperatingSystem()
    result = os.weekly_sales_brief([], lang="both")
    assert "pipeline_health" in result


def test_growth_campaign_is_draft():
    os = GrowthOperatingSystem()
    with pytest.raises(SendGateViolation):
        os.plan_campaign("Summer", "software", "Riyadh", "diagnostics", lang="both")


def test_content_brief_bilingual():
    os = GrowthOperatingSystem()
    result = os.generate_content_brief(
        "AI revenue ops", "عمليات إيرادات AI", "fintech", "thought_leadership", lang="both"
    )
    assert result["content_brief"]["topic"]["ar_available"] is True


def test_plg_diagnostic():
    os = GrowthOperatingSystem()
    result = os.run_plg_diagnostic("Najm Tech", "software", "Riyadh", 50, lang="both")
    assert result["plg_recommendation"]["company_name"] == "Najm Tech"


def test_success_plan_creation():
    cs = CustomerSuccessOperatingSystem()
    result = cs.create_success_plan(
        customer_id="c1",
        customer_name="Najm Tech",
        goals_en=["Increase qualified pipeline"],
        goals_ar=["زيادة خط الأنابيب المؤهل"],
        package_sku="Revenue Diagnostic",
        lang="both",
    )
    assert "success_plan" in result
    assert len(result["success_plan"]["milestones"]) == 4


def test_customer_health_dashboard():
    cs = CustomerSuccessOperatingSystem()
    customers = [
        {
            "customer_id": "c1",
            "customer_name": "Najm Tech",
            "last_activity_days": 5,
            "deliverables_completed": 3,
            "deliverables_total": 4,
            "payments_on_time": 4,
            "payments_total": 4,
            "support_tickets_open": 1,
            "nps_score": 60,
        }
    ]
    result = cs.health_dashboard(customers, lang="both")
    assert result["count"] == 1


def test_renewal_forecast():
    cs = CustomerSuccessOperatingSystem()
    customers = [
        {
            "customer_id": "c1",
            "customer_name": "Najm Tech",
            "renewal_date": "2026-12-31",
            "health_score": 80,
            "open_tickets": 0,
        }
    ]
    result = cs.forecast_renewals(customers, lang="both")
    assert len(result["renewal_forecasts"]) == 1
    assert result["renewal_forecasts"][0]["likelihood_percent"] > 0
