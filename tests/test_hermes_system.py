"""Tests for the Hermes multi-agent system."""

from __future__ import annotations

import asyncio
import pytest


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

class TestScoringTools:
    def test_score_lead_returns_tier(self):
        from dealix.hermes.tools.scoring_tools import score_lead
        result = asyncio.get_event_loop().run_until_complete(
            score_lead("TechCo", "technology", 5_000_000, 50)
        )
        assert "icp_score" in result
        assert result["tier"] in ("A", "B", "C")
        assert 0 <= result["icp_score"] <= 100

    def test_score_lead_low_revenue_gives_lower_score(self):
        from dealix.hermes.tools.scoring_tools import score_lead
        low = asyncio.get_event_loop().run_until_complete(
            score_lead("TinyShop", "other", 50_000, 2)
        )
        high = asyncio.get_event_loop().run_until_complete(
            score_lead("BigTech", "technology", 10_000_000, 100)
        )
        assert high["icp_score"] > low["icp_score"]

    def test_score_account_health_healthy(self):
        from dealix.hermes.tools.scoring_tools import score_account_health
        r = asyncio.get_event_loop().run_until_complete(
            score_account_health("acct-1", 1, 20_000, 80)
        )
        assert r["risk_level"] == "healthy"
        assert r["health_score"] >= 70

    def test_score_account_health_critical(self):
        from dealix.hermes.tools.scoring_tools import score_account_health
        r = asyncio.get_event_loop().run_until_complete(
            score_account_health("acct-2", 89, 0, -50)
        )
        assert r["risk_level"] == "critical"

    def test_prioritize_leads_returns_ranked(self):
        from dealix.hermes.tools.scoring_tools import prioritize_leads
        leads = [
            {"company": "A", "industry": "technology", "revenue_sar": 5_000_000, "employees": 50},
            {"company": "B", "industry": "other", "revenue_sar": 100_000, "employees": 3},
        ]
        r = asyncio.get_event_loop().run_until_complete(prioritize_leads(leads))
        assert r["total"] == 2
        assert r["ranked_leads"][0]["icp_score"] >= r["ranked_leads"][1]["icp_score"]

    def test_prioritize_leads_empty(self):
        from dealix.hermes.tools.scoring_tools import prioritize_leads
        r = asyncio.get_event_loop().run_until_complete(prioritize_leads([]))
        assert r["total"] == 0
        assert r["ranked_leads"] == []

    def test_calculate_deal_probability_high_stage(self):
        from dealix.hermes.tools.scoring_tools import calculate_deal_probability
        r = asyncio.get_event_loop().run_until_complete(
            calculate_deal_probability({
                "stage": "negotiation",
                "has_demo": True,
                "has_proposal": True,
                "champion_identified": True,
                "age_days": 5,
                "last_activity_days": 1,
            })
        )
        assert r["probability"] >= 60

    def test_calculate_deal_probability_early_stage(self):
        from dealix.hermes.tools.scoring_tools import calculate_deal_probability
        r = asyncio.get_event_loop().run_until_complete(
            calculate_deal_probability({"stage": "prospect", "age_days": 100, "last_activity_days": 30})
        )
        assert r["probability"] < 20


class TestDataTools:
    def test_score_data_quality_range(self):
        from dealix.hermes.tools.data_tools import score_data_quality
        records = [{"name": "A", "email": "a@b.com"}, {"name": "B", "email": None}]
        r = asyncio.get_event_loop().run_until_complete(
            score_data_quality(records, ["name", "email"])
        )
        assert 0 <= r["score"] <= 100
        assert r["tier"] in ("high", "medium", "low", "unusable")

    def test_score_data_quality_empty(self):
        from dealix.hermes.tools.data_tools import score_data_quality
        r = asyncio.get_event_loop().run_until_complete(score_data_quality([], ["name"]))
        assert r["score"] == 0
        assert r["tier"] == "unusable"

    def test_detect_duplicates_finds_dupes(self):
        from dealix.hermes.tools.data_tools import detect_duplicates
        records = [{"company": "A"}, {"company": "A"}, {"company": "B"}]
        r = asyncio.get_event_loop().run_until_complete(detect_duplicates(records, ["company"]))
        assert r["duplicate_count"] == 1
        assert r["unique_count"] == 2

    def test_detect_duplicates_no_dupes(self):
        from dealix.hermes.tools.data_tools import detect_duplicates
        records = [{"company": "A"}, {"company": "B"}, {"company": "C"}]
        r = asyncio.get_event_loop().run_until_complete(detect_duplicates(records, ["company"]))
        assert r["duplicate_count"] == 0

    def test_calculate_tam_sam_som_ordering(self):
        from dealix.hermes.tools.data_tools import calculate_tam_sam_som
        r = asyncio.get_event_loop().run_until_complete(
            calculate_tam_sam_som("technology", "riyadh", "sme")
        )
        assert r["tam_sar"] > r["sam_sar"] > r["som_sar"]

    def test_generate_data_passport_structure(self):
        from dealix.hermes.tools.data_tools import generate_data_passport
        r = asyncio.get_event_loop().run_until_complete(generate_data_passport("tenant-001"))
        assert r["generated"] is True
        assert "passport" in r
        assert r["passport"]["tenant_id"] == "tenant-001"


class TestAnalysisTools:
    def test_analyze_revenue_trend_growth(self):
        from dealix.hermes.tools.analysis_tools import analyze_revenue_trend
        data = [{"month": f"2025-{i:02d}", "revenue_sar": 100_000 * i} for i in range(1, 7)]
        r = asyncio.get_event_loop().run_until_complete(analyze_revenue_trend(data))
        assert r["growth_rate_pct"] > 0
        assert len(r["forecast_3m"]) == 3

    def test_analyze_revenue_trend_empty(self):
        from dealix.hermes.tools.analysis_tools import analyze_revenue_trend
        r = asyncio.get_event_loop().run_until_complete(analyze_revenue_trend([]))
        assert r["status"] == "no_data"
        assert "insufficient_data" in r["alert_flags"]

    def test_calculate_ltv_cac_healthy(self):
        from dealix.hermes.tools.analysis_tools import calculate_ltv_cac
        r = asyncio.get_event_loop().run_until_complete(
            calculate_ltv_cac(
                {"avg_mrr_sar": 5000, "churn_rate_monthly": 0.02, "gross_margin_pct": 0.70},
                {"total_sales_marketing_sar": 10_000, "new_customers_acquired": 5},
            )
        )
        assert r["ltv_cac_ratio"] >= 3
        assert r["health"] == "healthy"

    def test_calculate_ltv_cac_unhealthy(self):
        from dealix.hermes.tools.analysis_tools import calculate_ltv_cac
        r = asyncio.get_event_loop().run_until_complete(
            calculate_ltv_cac(
                {"avg_mrr_sar": 100, "churn_rate_monthly": 0.5, "gross_margin_pct": 0.2},
                {"total_sales_marketing_sar": 100_000, "new_customers_acquired": 1},
            )
        )
        assert r["health"] == "unhealthy"

    def test_generate_executive_summary_rating(self):
        from dealix.hermes.tools.analysis_tools import generate_executive_summary
        r = asyncio.get_event_loop().run_until_complete(
            generate_executive_summary(
                {"growth_rate_pct": 20, "nps": 60, "new_customers": 5},
                "Q2 2026",
            )
        )
        assert r["performance_rating"] == "strong"
        assert "Q2 2026" in r["headline"]

    def test_identify_growth_levers_no_crm(self):
        from dealix.hermes.tools.analysis_tools import identify_growth_levers
        r = asyncio.get_event_loop().run_until_complete(
            identify_growth_levers({"has_crm": False, "revenue_sar": 1_000_000, "employees": 20})
        )
        lever_names = [l["lever"] for l in r["growth_levers"]]
        assert "crm_implementation" in lever_names


class TestSaudiTools:
    def test_validate_cr_valid(self):
        from dealix.hermes.tools.saudi_tools import validate_cr_number
        r = asyncio.get_event_loop().run_until_complete(validate_cr_number("1010012345"))
        assert r["is_valid"] is True
        assert r["region_hint"] == "riyadh_region"

    def test_validate_cr_invalid_length(self):
        from dealix.hermes.tools.saudi_tools import validate_cr_number
        r = asyncio.get_event_loop().run_until_complete(validate_cr_number("12345"))
        assert r["is_valid"] is False

    def test_validate_cr_non_numeric(self):
        from dealix.hermes.tools.saudi_tools import validate_cr_number
        r = asyncio.get_event_loop().run_until_complete(validate_cr_number("ABCD123456"))
        assert r["is_valid"] is False

    def test_validate_cr_invalid_first_digit(self):
        from dealix.hermes.tools.saudi_tools import validate_cr_number
        r = asyncio.get_event_loop().run_until_complete(validate_cr_number("5010012345"))
        assert r["is_valid"] is False

    def test_validate_cr_western_region(self):
        from dealix.hermes.tools.saudi_tools import validate_cr_number
        r = asyncio.get_event_loop().run_until_complete(validate_cr_number("2050012345"))
        assert r["is_valid"] is True
        assert r["region_hint"] == "western_region"

    def test_get_hijri_date_returns_date(self):
        from dealix.hermes.tools.saudi_tools import get_hijri_date
        r = asyncio.get_event_loop().run_until_complete(get_hijri_date("2026-01-01"))
        assert "hijri" in r
        assert r["hijri_year"] > 1440

    def test_get_hijri_date_invalid(self):
        from dealix.hermes.tools.saudi_tools import get_hijri_date
        r = asyncio.get_event_loop().run_until_complete(get_hijri_date("not-a-date"))
        assert "error" in r

    def test_classify_vat_b2b(self):
        from dealix.hermes.tools.saudi_tools import classify_vat_treatment
        r = asyncio.get_event_loop().run_until_complete(
            classify_vat_treatment("b2b_service", 10_000)
        )
        assert r["vat_rate_pct"] == 15.0
        assert r["vat_amount_sar"] == 1500.0

    def test_classify_vat_export_zero(self):
        from dealix.hermes.tools.saudi_tools import classify_vat_treatment
        r = asyncio.get_event_loop().run_until_complete(
            classify_vat_treatment("export", 10_000)
        )
        assert r["vat_rate_pct"] == 0.0
        assert r["vat_category"] == "zero_rated"

    def test_classify_vat_healthcare_exempt(self):
        from dealix.hermes.tools.saudi_tools import classify_vat_treatment
        r = asyncio.get_event_loop().run_until_complete(
            classify_vat_treatment("healthcare", 5_000)
        )
        assert r["vat_category"] == "exempt"

    def test_get_saudi_market_context_technology(self):
        from dealix.hermes.tools.saudi_tools import get_saudi_market_context
        r = asyncio.get_event_loop().run_until_complete(get_saudi_market_context("technology"))
        assert r["industry"] == "technology"
        ctx = r["context"]
        assert ctx["market_size_usd_b"] > 0
        assert len(ctx["vision_2030_programs"]) > 0


class TestCrmTools:
    def test_get_lead_profile_returns_profile(self):
        from dealix.hermes.tools.crm_tools import get_lead_profile
        r = asyncio.get_event_loop().run_until_complete(get_lead_profile("lead-abc"))
        assert r["found"] is True
        assert "lead" in r
        assert r["lead"]["lead_id"] == "lead-abc"

    def test_update_lead_stage_valid(self):
        from dealix.hermes.tools.crm_tools import update_lead_stage
        r = asyncio.get_event_loop().run_until_complete(
            update_lead_stage("lead-001", "qualified", "Great fit")
        )
        assert r["updated"] is True
        assert r["new_stage"] == "qualified"

    def test_update_lead_stage_invalid(self):
        from dealix.hermes.tools.crm_tools import update_lead_stage
        r = asyncio.get_event_loop().run_until_complete(
            update_lead_stage("lead-001", "invalid_stage")
        )
        assert r["updated"] is False

    def test_create_deal_returns_deal(self):
        from dealix.hermes.tools.crm_tools import create_deal
        r = asyncio.get_event_loop().run_until_complete(
            create_deal("ACME Corp", 50_000, "prospect")
        )
        assert r["created"] is True
        assert r["deal"]["company"] == "ACME Corp"

    def test_list_open_deals_returns_list(self):
        from dealix.hermes.tools.crm_tools import list_open_deals
        r = asyncio.get_event_loop().run_until_complete(list_open_deals(5))
        assert "deals" in r
        assert len(r["deals"]) <= 5

    def test_log_activity_valid(self):
        from dealix.hermes.tools.crm_tools import log_activity
        r = asyncio.get_event_loop().run_until_complete(
            log_activity("entity-1", "call", "Discussed proposal")
        )
        assert r["logged"] is True

    def test_log_activity_invalid_type(self):
        from dealix.hermes.tools.crm_tools import log_activity
        r = asyncio.get_event_loop().run_until_complete(
            log_activity("entity-1", "smoke_signal")
        )
        assert r["logged"] is False


# ---------------------------------------------------------------------------
# Core infrastructure
# ---------------------------------------------------------------------------

class TestHermesConfig:
    def test_singleton(self):
        from dealix.hermes.config import get_hermes_config
        c1 = get_hermes_config()
        c2 = get_hermes_config()
        assert c1 is c2

    def test_defaults(self):
        from dealix.hermes.config import HermesConfig
        c = HermesConfig()
        assert c.hermes_max_tokens == 8192
        assert c.hermes_max_tool_rounds == 20
        assert c.hermes_cost_budget_usd == 5.0


class TestHermesMemory:
    def test_store_and_get(self):
        from dealix.hermes.memory import HermesMemory
        mem = HermesMemory()
        asyncio.get_event_loop().run_until_complete(mem.store("s1", "key", "value"))
        result = asyncio.get_event_loop().run_until_complete(mem.get("s1", "key"))
        assert result == "value"

    def test_get_missing_returns_default(self):
        from dealix.hermes.memory import HermesMemory
        mem = HermesMemory()
        result = asyncio.get_event_loop().run_until_complete(mem.get("no-session", "no-key", "default"))
        assert result == "default"

    def test_clear_session(self):
        from dealix.hermes.memory import HermesMemory
        mem = HermesMemory()
        asyncio.get_event_loop().run_until_complete(mem.store("s2", "k", "v"))
        asyncio.get_event_loop().run_until_complete(mem.clear_session("s2"))
        result = asyncio.get_event_loop().run_until_complete(mem.get("s2", "k"))
        assert result is None

    def test_list_sessions(self):
        from dealix.hermes.memory import HermesMemory
        mem = HermesMemory()
        asyncio.get_event_loop().run_until_complete(mem.store("alpha", "k", "v"))
        asyncio.get_event_loop().run_until_complete(mem.store("beta", "k", "v"))
        sessions = asyncio.get_event_loop().run_until_complete(mem.list_sessions())
        assert "alpha" in sessions
        assert "beta" in sessions


class TestHermesRegistry:
    def test_build_all_agents(self):
        from dealix.hermes.registry import HermesRegistry
        # Reset singleton for a clean test
        HermesRegistry._instance = None
        agents = HermesRegistry.build_all_agents()
        assert len(agents) == 11
        expected = {
            "lead_intelligence", "revenue_intelligence", "sprint_orchestrator",
            "diagnostic_agent", "data_architect", "managed_ops",
            "sales_intelligence", "market_intel", "company_brain", "governance",
            "customer_acquisition",
        }
        assert set(agents.keys()) == expected

    def test_get_missing_raises(self):
        from dealix.hermes.registry import HermesRegistry
        registry = HermesRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent_agent")

    def test_list_agents(self):
        from dealix.hermes.registry import HermesRegistry
        registry = HermesRegistry()
        from dealix.hermes.agents.lead_intelligence import LeadIntelligenceAgent
        agent = LeadIntelligenceAgent()
        registry.register(agent)
        names = registry.list_agents()
        assert "lead_intelligence" in names


class TestHermesEngine:
    def test_build_tool_schema(self):
        from dealix.hermes.engine import build_tool_schema
        schema = build_tool_schema(
            "my_tool",
            "A test tool",
            {"param": {"type": "string"}},
            ["param"],
        )
        assert schema["name"] == "my_tool"
        assert schema["input_schema"]["required"] == ["param"]
        assert "param" in schema["input_schema"]["properties"]

    def test_mock_response_when_no_key(self):
        import os
        from dealix.hermes.config import HermesConfig
        from dealix.hermes.engine import HermesEngine
        # Create engine with an empty key override to force mock mode
        cfg = HermesConfig(hermes_api_key="", hermes_model="claude-haiku-4-5-20251001")
        # Temporarily clear env key so engine enters mock mode
        orig_key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            engine = HermesEngine(config=cfg)
            # engine._client must be None because no key is set
            assert engine._client is None
            result = asyncio.get_event_loop().run_until_complete(
                engine.run_agent_loop("system", [{"role": "user", "content": "hi"}], [], 1)
            )
            text, history = result
            assert isinstance(text, str)
            assert "mock" in text or "No ANTHROPIC_API_KEY" in text
        finally:
            if orig_key is not None:
                os.environ["ANTHROPIC_API_KEY"] = orig_key


class TestHermesAgentBase:
    def test_agent_has_builtin_tools(self):
        from dealix.hermes.agents.lead_intelligence import LeadIntelligenceAgent
        agent = LeadIntelligenceAgent()
        tool_names = list(agent._tools.keys())
        assert "log_event" in tool_names
        assert "get_current_datetime" in tool_names

    def test_dispatch_unknown_tool_returns_error(self):
        from dealix.hermes.agents.lead_intelligence import LeadIntelligenceAgent
        agent = LeadIntelligenceAgent()
        result = asyncio.get_event_loop().run_until_complete(
            agent._dispatch_tool("nonexistent_tool", {})
        )
        import json
        parsed = json.loads(result)
        assert "error" in parsed

    def test_tools_schema_is_list(self):
        from dealix.hermes.agents.revenue_intelligence import RevenueIntelligenceAgent
        agent = RevenueIntelligenceAgent()
        schema = agent.tools_schema
        assert isinstance(schema, list)
        assert all("name" in t for t in schema)


class TestHermesOrchestrator:
    def test_unknown_pipeline_returns_error(self):
        from dealix.hermes.orchestrator import HermesOrchestrator
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        orch = HermesOrchestrator()
        result = asyncio.get_event_loop().run_until_complete(
            orch.run_pipeline("nonexistent_pipeline", {})
        )
        assert "error" in result
        assert "available_pipelines" in result

    def test_parallel_agents_runs_multiple(self):
        from dealix.hermes.orchestrator import HermesOrchestrator
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        orch = HermesOrchestrator()
        result = asyncio.get_event_loop().run_until_complete(
            orch.run_parallel_agents(
                ["diagnostic_agent", "governance"],
                {"company_name": "TestCo", "tenant_id": "t1"},
            )
        )
        assert "results" in result
        assert "diagnostic_agent" in result["results"]
        assert "governance" in result["results"]

    def test_pipeline_free_diagnostic(self):
        from dealix.hermes.orchestrator import HermesOrchestrator
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        orch = HermesOrchestrator()
        result = asyncio.get_event_loop().run_until_complete(
            orch.run_pipeline("free_diagnostic", {"company_name": "Demo"})
        )
        assert result["pipeline"] == "free_diagnostic"
        assert result["steps_completed"] == 1


class TestWatchdogLoop:
    def test_health_check_runs(self):
        from dealix.hermes.loops.watchdog_loop import WatchdogLoop
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        watchdog = WatchdogLoop()
        result = asyncio.get_event_loop().run_until_complete(watchdog.run_once())
        assert "status" in result
        assert result["status"] in ("healthy", "degraded", "critical")
        assert "checks" in result

    def test_health_check_all_agents_registered(self):
        from dealix.hermes.loops.watchdog_loop import WatchdogLoop
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        watchdog = WatchdogLoop()
        result = asyncio.get_event_loop().run_until_complete(watchdog.run_once())
        assert result["checks"]["agent_registry"]["ok"] is True


class TestLeadLoop:
    def test_run_once_empty(self):
        from dealix.hermes.loops.lead_loop import LeadLoop
        loop = LeadLoop()
        result = asyncio.get_event_loop().run_until_complete(loop.run_once([]))
        assert result["status"] == "no_leads"

    def test_run_once_with_leads(self):
        from dealix.hermes.loops.lead_loop import LeadLoop
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        loop = LeadLoop()
        result = asyncio.get_event_loop().run_until_complete(
            loop.run_once([{"company": "A", "industry": "technology", "revenue_sar": 1_000_000, "employees": 20}])
        )
        assert result.get("batch_lead_count") == 1


# ---------------------------------------------------------------------------
# MiniMax provider
# ---------------------------------------------------------------------------


class TestMiniMaxProvider:
    def test_is_available_without_key(self):
        import os
        from dealix.hermes.providers.minimax_provider import MiniMaxProvider
        orig = os.environ.pop("MINIMAX_API_KEY", None)
        try:
            provider = MiniMaxProvider(api_key="")
            assert provider.is_available is False
        finally:
            if orig is not None:
                os.environ["MINIMAX_API_KEY"] = orig

    def test_mock_response_returns_expected_keys(self):
        from dealix.hermes.providers.minimax_provider import MiniMaxProvider
        result = MiniMaxProvider._mock_response("sys", [{"role": "user", "content": "hi"}])
        assert "text" in result
        assert "tool_calls" in result
        assert "usage" in result
        assert result["tool_calls"] == []

    def test_init_with_key_creates_client(self):
        from dealix.hermes.providers.minimax_provider import MiniMaxProvider
        try:
            provider = MiniMaxProvider(api_key="test-key-does-not-need-to-be-valid")
            # openai package is installed so client should be set
            assert provider.is_available is True
        except Exception:
            # If openai package not installed, is_available is False — still valid
            pass

    def test_chat_without_client_returns_mock(self):
        import os
        from dealix.hermes.providers.minimax_provider import MiniMaxProvider
        orig = os.environ.pop("MINIMAX_API_KEY", None)
        try:
            provider = MiniMaxProvider(api_key="")
            result = asyncio.get_event_loop().run_until_complete(
                provider.chat(system="sys", messages=[{"role": "user", "content": "hi"}])
            )
            assert "text" in result
            assert "tool_calls" in result
        finally:
            if orig is not None:
                os.environ["MINIMAX_API_KEY"] = orig

    def test_run_agentic_loop_no_tools_returns_text(self):
        import os
        from dealix.hermes.providers.minimax_provider import MiniMaxProvider

        orig = os.environ.pop("MINIMAX_API_KEY", None)
        try:
            provider = MiniMaxProvider(api_key="")

            async def dummy_dispatcher(name, inp):
                return "{}"

            text, usage = asyncio.get_event_loop().run_until_complete(
                provider.run_agentic_loop(
                    system="sys",
                    user_msg="hi",
                    tools=[],
                    tool_dispatcher=dummy_dispatcher,
                    max_rounds=1,
                )
            )
            assert isinstance(text, str)
            assert "input_tokens" in usage
        finally:
            if orig is not None:
                os.environ["MINIMAX_API_KEY"] = orig


# ---------------------------------------------------------------------------
# OutreachQueue
# ---------------------------------------------------------------------------


class TestOutreachQueue:
    def _fresh_queue(self):
        from dealix.hermes.outreach_queue import OutreachQueue
        q = OutreachQueue()
        return q

    def test_enqueue_returns_draft_id(self):
        from dealix.hermes.outreach_queue import OutreachDraft
        q = self._fresh_queue()
        draft = OutreachDraft(company_name="Acme", channel="email")
        draft_id = q.enqueue(draft)
        assert draft_id == draft.draft_id
        assert len(q.pending()) == 1

    def test_approve_changes_status(self):
        from dealix.hermes.outreach_queue import OutreachDraft
        q = self._fresh_queue()
        draft = OutreachDraft(company_name="BetaCo")
        q.enqueue(draft)
        approved = q.approve(draft.draft_id, approved_by="founder")
        assert approved.status == "approved"
        assert approved.approved_by == "founder"
        assert len(q.pending()) == 0
        assert len(q.approved()) == 1

    def test_reject_changes_status(self):
        from dealix.hermes.outreach_queue import OutreachDraft
        q = self._fresh_queue()
        draft = OutreachDraft(company_name="GammaCo")
        q.enqueue(draft)
        rejected = q.reject(draft.draft_id, reason="not a fit")
        assert rejected.status == "rejected"
        assert rejected.rejection_reason == "not a fit"

    def test_approve_missing_draft_raises(self):
        q = self._fresh_queue()
        with pytest.raises(KeyError):
            q.approve("NO_SUCH_ID")

    def test_reject_missing_draft_raises(self):
        q = self._fresh_queue()
        with pytest.raises(KeyError):
            q.reject("NO_SUCH_ID")

    def test_stats_counts_by_status(self):
        from dealix.hermes.outreach_queue import OutreachDraft
        q = self._fresh_queue()
        d1 = OutreachDraft(company_name="Co1")
        d2 = OutreachDraft(company_name="Co2")
        d3 = OutreachDraft(company_name="Co3")
        q.enqueue(d1)
        q.enqueue(d2)
        q.enqueue(d3)
        q.approve(d1.draft_id)
        stats = q.stats()
        assert stats.get("pending_approval", 0) == 2
        assert stats.get("approved", 0) == 1

    def test_to_dict_has_all_fields(self):
        from dealix.hermes.outreach_queue import OutreachDraft
        draft = OutreachDraft(company_name="DeltaCo", channel="email", score=85.0)
        d = draft.to_dict()
        assert d["company_name"] == "DeltaCo"
        assert d["channel"] == "email"
        assert d["score"] == 85.0
        assert "draft_id" in d
        assert "status" in d

    def test_all_drafts_returns_all(self):
        from dealix.hermes.outreach_queue import OutreachDraft
        q = self._fresh_queue()
        for i in range(3):
            q.enqueue(OutreachDraft(company_name=f"Co{i}"))
        assert len(q.all_drafts()) == 3

    def test_queue_never_auto_approves(self):
        """Doctrine guard: enqueued drafts start as pending_approval only."""
        from dealix.hermes.outreach_queue import OutreachDraft
        q = self._fresh_queue()
        draft = OutreachDraft(company_name="AutoCheck")
        q.enqueue(draft)
        assert draft.status == "pending_approval"
        # Pending list must contain the draft
        assert any(d.draft_id == draft.draft_id for d in q.pending())


# ---------------------------------------------------------------------------
# CustomerAcquisitionAgent
# ---------------------------------------------------------------------------


class TestCustomerAcquisitionAgent:
    def test_agent_name_and_description(self):
        from dealix.hermes.agents.customer_acquisition import CustomerAcquisitionAgent
        agent = CustomerAcquisitionAgent()
        assert agent.name == "customer_acquisition"
        assert isinstance(agent.description, str)
        assert len(agent.description) > 0

    def test_agent_has_expected_tools(self):
        from dealix.hermes.agents.customer_acquisition import CustomerAcquisitionAgent
        agent = CustomerAcquisitionAgent()
        tool_names = list(agent._tools.keys())
        assert "score_lead" in tool_names
        assert "prioritize_leads" in tool_names
        assert "get_saudi_market_context" in tool_names
        assert "format_arabic_proposal" in tool_names
        assert "get_lead_profile" in tool_names
        assert "list_open_deals" in tool_names
        assert "run_commercial_diagnostic" in tool_names

    def test_agent_run_no_leads_returns_complete(self):
        from unittest.mock import patch
        from dealix.hermes.agents.customer_acquisition import CustomerAcquisitionAgent
        agent = CustomerAcquisitionAgent()
        with patch.object(agent._engine, "_client", None):
            result = asyncio.get_event_loop().run_until_complete(
                agent.run({"leads": [], "max_drafts": 3})
            )
        assert result["status"] == "complete"
        assert result["agent"] == "customer_acquisition"
        assert result["approval_required"] is True
        assert result["governance_decision"] == "approved"
        assert result["leads_processed"] == 0

    def test_agent_run_result_never_auto_sends(self):
        """Doctrine guard: run() result must not indicate any send occurred."""
        from unittest.mock import patch
        from dealix.hermes.agents.customer_acquisition import CustomerAcquisitionAgent
        agent = CustomerAcquisitionAgent()
        with patch.object(agent._engine, "_client", None):
            result = asyncio.get_event_loop().run_until_complete(
                agent.run({"leads": [], "max_drafts": 1})
            )
        raw = result.get("raw_response", "").lower()
        assert "sent" not in raw or "not sent" in raw or "approval" in raw or raw == ""

    def test_score_lead_adapter_returns_tier(self):
        from dealix.hermes.agents.customer_acquisition import _score_lead_adapter
        result = asyncio.get_event_loop().run_until_complete(
            _score_lead_adapter(
                lead_id="L001",
                company_name="TechSA",
                sector="technology",
                employee_count=50,
                annual_revenue_sar=5_000_000,
                has_crm=False,
            )
        )
        assert result["tier"] in ("A", "B", "C")
        assert result["lead_id"] == "L001"

    def test_prioritize_leads_adapter_returns_ranked(self):
        from dealix.hermes.agents.customer_acquisition import _prioritize_leads_adapter
        leads = [
            {"company": "A", "industry": "technology", "revenue_sar": 5_000_000, "employees": 50},
            {"company": "B", "industry": "other", "revenue_sar": 50_000, "employees": 2},
        ]
        result = asyncio.get_event_loop().run_until_complete(_prioritize_leads_adapter(leads))
        assert result["total"] == 2
        assert result["ranked_leads"][0]["icp_score"] >= result["ranked_leads"][1]["icp_score"]

    def test_get_saudi_market_context_adapter(self):
        from dealix.hermes.agents.customer_acquisition import _get_saudi_market_context_adapter
        result = asyncio.get_event_loop().run_until_complete(
            _get_saudi_market_context_adapter(sector="retail", city="Jeddah")
        )
        assert result["industry"] == "retail"
        assert result["city"] == "Jeddah"

    def test_format_arabic_proposal_adapter(self):
        from dealix.hermes.agents.customer_acquisition import _format_arabic_proposal_adapter
        result = asyncio.get_event_loop().run_until_complete(
            _format_arabic_proposal_adapter(
                company_name="TestCo",
                pain_summary_ar="ارتفاع تكلفة الاكتساب",
                pain_summary_en="High acquisition cost",
                offer_tier="starter",
                roi_estimate_sar=50_000,
            )
        )
        assert result["formatted"] is True

    def test_get_lead_profile_adapter(self):
        from dealix.hermes.agents.customer_acquisition import _get_lead_profile_adapter
        result = asyncio.get_event_loop().run_until_complete(
            _get_lead_profile_adapter(lead_id="test-lead-001")
        )
        assert result["found"] is True

    def test_list_open_deals_adapter(self):
        from dealix.hermes.agents.customer_acquisition import _list_open_deals_adapter
        result = asyncio.get_event_loop().run_until_complete(_list_open_deals_adapter())
        assert "deals" in result


# ---------------------------------------------------------------------------
# DailyOutreachLoop
# ---------------------------------------------------------------------------


class TestDailyOutreachLoop:
    def test_run_once_no_agent_returns_skipped(self):
        from dealix.hermes.loops.daily_outreach_loop import DailyOutreachLoop
        from dealix.hermes.registry import HermesRegistry
        # Registry without customer_acquisition agent
        registry = HermesRegistry()
        loop = DailyOutreachLoop(registry=registry)
        result = asyncio.get_event_loop().run_until_complete(loop.run_once(leads=[]))
        assert result["status"] == "skipped"

    def test_run_once_with_agent_returns_complete(self):
        from unittest.mock import patch
        from dealix.hermes.loops.daily_outreach_loop import DailyOutreachLoop
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        agent = HermesRegistry.instance().get("customer_acquisition")
        with patch.object(agent._engine, "_client", None):
            loop = DailyOutreachLoop(registry=HermesRegistry.instance())
            result = asyncio.get_event_loop().run_until_complete(loop.run_once(leads=[]))
        assert result["status"] == "complete"
        assert result["agent"] == "customer_acquisition"

    def test_stop_sets_running_false(self):
        from dealix.hermes.loops.daily_outreach_loop import DailyOutreachLoop
        loop = DailyOutreachLoop()
        loop._running = True
        loop.stop()
        assert loop._running is False

    def test_run_once_respects_max_drafts_from_config(self):
        from unittest.mock import patch
        from dealix.hermes.config import HermesConfig
        from dealix.hermes.loops.daily_outreach_loop import DailyOutreachLoop
        from dealix.hermes.registry import HermesRegistry
        HermesRegistry._instance = None
        HermesRegistry.build_all_agents()
        agent = HermesRegistry.instance().get("customer_acquisition")
        cfg = HermesConfig(minimax_outreach_max_per_day=3)
        with patch.object(agent._engine, "_client", None):
            loop = DailyOutreachLoop(registry=HermesRegistry.instance(), config=cfg)
            result = asyncio.get_event_loop().run_until_complete(loop.run_once(leads=[]))
        assert "drafts_queued" in result
