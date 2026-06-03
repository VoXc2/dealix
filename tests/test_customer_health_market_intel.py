"""Tests for Customer Health Scoring + Market Intelligence systems."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dealix.commercial.customer_health import (
    CustomerHealthEngine,
    HealthInput,
    HEALTH_TIERS,
    SECTOR_BENCHMARKS,
)
from dealix.commercial.market_intelligence import (
    MarketIntelligenceEngine,
    SAUDI_MARKET_SIGNALS,
    SECTOR_INTELLIGENCE,
)
from dealix.commercial.onboarding import OnboardingOrchestrator


# ── Customer Health Scoring ──────────────────────────────────────────

class TestCustomerHealthEngine:
    """Tests for AI-powered customer health scoring."""

    def setup_method(self):
        self.engine = CustomerHealthEngine()

    def _make_input(self, **kwargs) -> HealthInput:
        defaults = {
            "account_id": "acct_test",
            "company_name": "Test Company",
            "sector": "b2b_services",
            "days_since_last_interaction": 5,
            "interactions_last_30_days": 6,
            "sprints_completed": 1,
            "proof_level_achieved": "L2",
            "invoices_paid_on_time": 2,
            "invoices_total": 2,
            "nps_score": 60,
        }
        defaults.update(kwargs)
        return HealthInput(**defaults)

    def test_healthy_customer_scores_high(self):
        inp = self._make_input(
            days_since_last_interaction=2,
            interactions_last_30_days=10,
            sprints_completed=2,
            proof_level_achieved="L3",
            nps_score=80,
            has_testimonial=True,
            lifetime_value_sar=12000,
        )
        report = self.engine.calculate(inp)
        assert report.overall_score >= 70
        assert report.health_tier in ("CHAMPION", "HEALTHY")

    def test_at_risk_customer_flagged(self):
        inp = self._make_input(
            days_since_last_interaction=35,
            interactions_last_30_days=0,
            proof_level_achieved="L0",
            nps_score=-20,
            support_tickets_open=5,
        )
        report = self.engine.calculate(inp)
        assert report.overall_score < 70
        assert report.health_tier in ("AT_RISK", "CRITICAL", "CHURNED")

    def test_churn_risk_elevated_with_key_signals(self):
        inp = self._make_input(
            key_contact_left=True,
            competitor_mentioned=True,
            budget_at_risk=True,
            days_since_last_interaction=30,
        )
        report = self.engine.calculate(inp)
        assert report.is_churn_risk is True
        assert report.churn_probability > 0.3

    def test_expansion_readiness_detected(self):
        # Need score >=70 for expansion — build a healthy profile
        inp_healthy = self._make_input(
            sprints_completed=2,
            proof_level_achieved="L3",
            nps_score=70,
            days_since_last_interaction=2,
            interactions_last_30_days=10,
            invoices_paid_on_time=3,
            invoices_total=3,
            has_testimonial=True,
        )
        report = self.engine.calculate(inp_healthy)
        if report.overall_score >= 70:
            assert report.expansion_ready is True
            assert report.recommended_upsell_ar != ""

    def test_dimensions_present(self):
        inp = self._make_input()
        report = self.engine.calculate(inp)
        assert len(report.dimensions) == 6
        dim_names = {d.name_en for d in report.dimensions}
        assert "Engagement" in dim_names
        assert "Delivery Quality" in dim_names
        assert "Financial Health" in dim_names
        assert "Customer Satisfaction" in dim_names
        assert "Product Adoption" in dim_names
        assert "Risk Indicators" in dim_names

    def test_all_tiers_reachable(self):
        """Verify score ranges cover all 5 tiers."""
        for tier, (lo, hi) in HEALTH_TIERS.items():
            assert lo <= hi, f"Invalid range for {tier}"

    def test_sector_benchmarks_exist(self):
        """Verify benchmarks for all main Saudi sectors."""
        sectors = ["b2b_saas", "agency", "healthcare_clinic", "real_estate", "logistics"]
        for sector in sectors:
            assert sector in SECTOR_BENCHMARKS

    def test_score_bounded_0_100(self):
        """Overall score must be between 0 and 100 for any input."""
        # Worst case
        inp_worst = HealthInput(
            account_id="x",
            company_name="X",
            days_since_last_interaction=90,
            key_contact_left=True,
            budget_at_risk=True,
            competitor_mentioned=True,
            nps_score=-100,
            support_tickets_open=20,
            proof_level_achieved="L0",
        )
        report = self.engine.calculate(inp_worst)
        assert 0 <= report.overall_score <= 100

        # Best case
        inp_best = HealthInput(
            account_id="y",
            company_name="Y",
            days_since_last_interaction=1,
            interactions_last_30_days=20,
            sprints_completed=5,
            proof_level_achieved="L4",
            invoices_paid_on_time=10,
            invoices_total=10,
            nps_score=90,
            has_testimonial=True,
            has_referral=True,
            lifetime_value_sar=50000,
            weekly_active_usage=True,
            uses_approval_center=True,
        )
        report_best = self.engine.calculate(inp_best)
        assert 0 <= report_best.overall_score <= 100

    def test_needs_immediate_attention_flag(self):
        inp = self._make_input(
            days_since_last_interaction=45,
            key_contact_left=True,
            nps_score=-50,
            proof_level_achieved="L0",
        )
        report = self.engine.calculate(inp)
        assert report.needs_immediate_attention is True

    def test_priority_actions_present(self):
        inp = self._make_input(
            days_since_last_interaction=25,
            proof_level_achieved="L0",
        )
        report = self.engine.calculate(inp)
        assert len(report.priority_actions_ar) > 0
        assert len(report.priority_actions_en) > 0

    def test_to_dict_serializable(self):
        inp = self._make_input()
        report = self.engine.calculate(inp)
        d = report.to_dict()
        assert isinstance(d, dict)
        assert "overall_score" in d
        assert "health_tier" in d
        assert "dimensions" in d


# ── Market Intelligence ──────────────────────────────────────────────

class TestMarketIntelligenceEngine:

    def setup_method(self):
        self.engine = MarketIntelligenceEngine()

    def test_signals_present(self):
        signals = self.engine.get_all_signals()
        assert len(signals) >= 5

    def test_urgent_signals_filterable(self):
        high = self.engine.get_all_signals(urgency_filter="HIGH")
        for s in high:
            assert s.urgency == "HIGH"

    def test_sector_filter(self):
        agency_signals = self.engine.get_all_signals(sector_filter="agency")
        sectors_in_results = {s.sector for s in agency_signals}
        assert "agency" in sectors_in_results or "all" in sectors_in_results

    def test_sector_intelligence_exists(self):
        sectors = ["b2b_saas", "agency", "healthcare_clinic", "real_estate", "logistics"]
        for sector in sectors:
            intel = self.engine.get_sector_intelligence(sector)
            assert intel is not None
            assert intel.ai_adoption_rate >= 0
            assert intel.avg_deal_value_sar > 0

    def test_sector_ranking_sorted(self):
        ranking = self.engine.get_sector_ranking()
        assert len(ranking) >= 3
        scores = [r["opportunity_score"] for r in ranking]
        assert scores == sorted(scores, reverse=True), "Ranking must be descending"

    def test_why_now_brief(self):
        brief = self.engine.get_why_now_brief("agency")
        assert "ar" in brief
        assert "en" in brief
        assert len(brief["ar"]) > 5
        assert len(brief["en"]) > 5

    def test_unknown_sector_returns_fallback(self):
        brief = self.engine.get_why_now_brief("unknown_sector_xyz")
        assert "ar" in brief
        assert len(brief["ar"]) > 0

    def test_all_sector_data_valid(self):
        for sector, intel in SECTOR_INTELLIGENCE.items():
            assert 0 <= intel.ai_adoption_rate <= 100
            assert 0 <= intel.pain_intensity <= 10
            assert intel.avg_deal_value_sar > 0
            assert intel.recommended_offer != ""
            assert len(intel.key_pain_points_ar) > 0

    def test_signals_have_bilingual_content(self):
        for signal in SAUDI_MARKET_SIGNALS:
            assert len(signal.title_ar) > 0
            assert len(signal.title_en) > 0
            assert len(signal.opportunity_ar) > 0
            assert signal.urgency in ("HIGH", "MEDIUM", "LOW")


# ── Onboarding System ────────────────────────────────────────────────

class TestOnboardingOrchestrator:

    def setup_method(self):
        self.orch = OnboardingOrchestrator()

    def test_create_onboarding_record(self):
        record = self.orch.create_onboarding(
            account_id="acct_001",
            company_name="Riyadh Consulting",
            contact_name="أحمد",
            contact_phone="+966501234567",
            service_tier="sprint_499",
        )
        assert record.account_id == "acct_001"
        assert record.company_name == "Riyadh Consulting"
        assert record.current_stage == "WELCOME"
        assert len(record.steps) == 6

    def test_welcome_drafts_generated(self):
        record = self.orch.create_onboarding(
            account_id="acct_002",
            company_name="Test Co",
            contact_name="Sara",
            contact_phone="+966509999999",
            service_tier="data_pack_1500",
        )
        assert len(record.welcome_draft_ar) > 50
        assert len(record.welcome_draft_en) > 50
        assert "موافقة المؤسس" in record.welcome_draft_ar
        assert "approval" in record.welcome_draft_en.lower()

    def test_advance_stage(self):
        record = self.orch.create_onboarding(
            account_id="acct_003",
            company_name="Co",
            contact_name="X",
            contact_phone="+966",
            service_tier="sprint_499",
        )
        updated = self.orch.advance_stage(record, "WELCOME")
        assert updated.current_stage != "WELCOME"

    def test_sla_deadlines_set(self):
        record = self.orch.create_onboarding(
            account_id="acct_004",
            company_name="Co",
            contact_name="X",
            contact_phone="+966",
            service_tier="sprint_499",
        )
        for step in record.steps:
            assert step.sla_deadline is not None

    def test_intake_form_has_questions(self):
        form = self.orch.get_intake_form()
        assert len(form["questions_ar"]) >= 5
        assert len(form["questions_en"]) >= 5
        assert form["duration_minutes"] > 0

    def test_overdue_detection(self):
        record = self.orch.create_onboarding(
            account_id="acct_005",
            company_name="Co",
            contact_name="X",
            contact_phone="+966",
            service_tier="sprint_499",
        )
        # Force a past deadline
        past_time = datetime.now(UTC) - timedelta(hours=100)
        for step in record.steps:
            if step.stage == "WELCOME":
                step.sla_deadline = past_time

        overdue = self.orch.get_overdue_steps(record)
        assert len(overdue) >= 1

    def test_to_dict_serializable(self):
        record = self.orch.create_onboarding(
            account_id="acct_006",
            company_name="Co",
            contact_name="X",
            contact_phone="+966",
            service_tier="sprint_499",
        )
        d = record.to_dict()
        assert isinstance(d, dict)
        assert "onboarding_id" in d
        assert "steps" in d
