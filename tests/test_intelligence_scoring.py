"""Comprehensive tests for intelligence scoring, sprint orchestrator,
ZATCA invoice, KPI dashboard, and weekly report generator.

Covers:
- AI lead scorer (HOT/WARM/COOL/COLD bands, PDPL gate, sector weights)
- Sprint orchestrator (7 days, per-day structured output)
- ZATCA invoice (Phase 2, QR code, VAT calculation, hash chain)
- KPI dashboard endpoints (summary/commercial/cohort/nps/health-score)
- Weekly report generator (revenue/leads/content/risks/actions)
"""

from __future__ import annotations

import pytest


# ===========================================================================
# AI Lead Scorer tests
# ===========================================================================


class TestAILeadScorer:
    """Tests for dealix.intelligence.ai_lead_scorer."""

    def _make_lead(self, **kwargs):
        from dealix.intelligence.ai_lead_scorer import (
            AILeadInput,
            BANTSignals,
            BehaviouralSignals,
            PDPLConsent,
        )
        from dealix.intelligence.lead_scorer import LeadFeatures

        bant = BANTSignals(
            budget_sar=kwargs.get("budget_sar", 0),
            has_decision_maker=kwargs.get("has_decision_maker", False),
            pain_score=kwargs.get("pain_score", 0.0),
            timeline_days=kwargs.get("timeline_days", 0),
        )
        behav = BehaviouralSignals(
            pages_visited=kwargs.get("pages_visited", 0),
            email_opens=kwargs.get("email_opens", 0),
            whatsapp_replies=kwargs.get("whatsapp_replies", 0),
            referral_source=kwargs.get("referral_source", False),
            attended_event=kwargs.get("attended_event", False),
        )
        pdpl = PDPLConsent(
            consent_obtained=kwargs.get("consent_obtained", True),
            consent_ref=kwargs.get("consent_ref", "ref_001"),
            lawful_basis=kwargs.get("lawful_basis", "consent"),
        )
        # Provide base features so the sector_adjusted component is non-zero.
        base = kwargs.get(
            "base_features",
            LeadFeatures(
                company_size=kwargs.get("company_size", 50),
                budget_usd=kwargs.get("budget_usd", float(kwargs.get("budget_sar", 0)) / 3.75),
                urgency_score=kwargs.get("pain_score", 0.0),
                has_company_email=kwargs.get("has_company_email", True),
                pain_points_count=kwargs.get("pain_points_count", 2),
                sector_fit=kwargs.get("sector_fit", 0.6),
            ),
        )
        return AILeadInput(
            customer_id=kwargs.get("customer_id", "test_cust"),
            sector=kwargs.get("sector", "b2b_saas"),
            bant=bant,
            behavioural=behav,
            pdpl_consent=pdpl,
            base_features=base,
        )

    def test_hot_band(self):
        """Lead with strong budget, DM, urgency, and engagement scores HOT."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=60_000,
            has_decision_maker=True,
            pain_score=0.9,
            timeline_days=14,
            attended_event=True,
            whatsapp_replies=3,
            referral_source=True,
        )
        result = score_lead(lead)
        assert result.tier == "HOT", f"Expected HOT, got {result.tier} (score={result.score})"
        assert result.score >= 80

    def test_warm_band(self):
        """Lead with moderate signals scores WARM."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=20_000,
            has_decision_maker=True,
            pain_score=0.5,
            timeline_days=60,
            email_opens=2,
        )
        result = score_lead(lead)
        assert result.tier in ("HOT", "WARM"), f"Expected HOT or WARM, got {result.tier}"
        assert result.score >= 60

    def test_cool_band(self):
        """Lead with low signals scores COOL or COLD."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=2_000,
            has_decision_maker=False,
            pain_score=0.2,
            timeline_days=200,
        )
        result = score_lead(lead)
        assert result.tier in ("COOL", "COLD"), f"Expected COOL or COLD, got {result.tier}"

    def test_cold_band(self):
        """Lead with zero signals scores COLD."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=0,
            has_decision_maker=False,
            pain_score=0.0,
            timeline_days=0,
            consent_obtained=False,
        )
        result = score_lead(lead)
        assert result.tier == "COLD", f"Expected COLD, got {result.tier} (score={result.score})"
        assert result.score <= 30  # PDPL cap at 30

    def test_pdpl_gate_caps_score(self):
        """Without PDPL consent, score is capped at 30 and governance is REQUIRE_APPROVAL."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=100_000,
            has_decision_maker=True,
            pain_score=1.0,
            timeline_days=7,
            consent_obtained=False,
            consent_ref="",
        )
        result = score_lead(lead)
        assert result.score <= 30
        assert result.governance_decision == "REQUIRE_APPROVAL"
        assert not result.pdpl_cleared

    def test_pdpl_compliant_lead_not_capped(self):
        """PDPL-compliant lead is not capped."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=40_000,
            has_decision_maker=True,
            pain_score=0.8,
            consent_obtained=True,
            consent_ref="ref_001",
        )
        result = score_lead(lead)
        assert result.pdpl_cleared
        assert result.score > 30

    def test_saudi_sector_weight_b2b_saas(self):
        """b2b_saas sector gets a higher multiplier than an unknown sector."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        common_kwargs = dict(
            budget_sar=15_000,
            has_decision_maker=True,
            pain_score=0.6,
        )
        lead_saas = self._make_lead(sector="b2b_saas", **common_kwargs)
        lead_unknown = self._make_lead(sector="unknown_sector_xyz", **common_kwargs)

        result_saas = score_lead(lead_saas)
        result_unknown = score_lead(lead_unknown)
        assert result_saas.score >= result_unknown.score

    def test_bilingual_output(self):
        """Score result includes non-empty Arabic and English reasons."""
        from dealix.intelligence.ai_lead_scorer import score_lead

        lead = self._make_lead(
            budget_sar=25_000,
            has_decision_maker=True,
            pain_score=0.7,
            referral_source=True,
        )
        result = score_lead(lead)
        assert result.tier_ar  # non-empty Arabic tier label
        assert result.recommended_action_en
        assert result.recommended_action_ar

    def test_batch_score(self):
        """batch_score returns one result per input lead."""
        from dealix.intelligence.ai_lead_scorer import batch_score

        leads = [self._make_lead(budget_sar=i * 10_000) for i in range(5)]
        results = batch_score(leads)
        assert len(results) == 5


# ===========================================================================
# Sprint Orchestrator tests
# ===========================================================================


class TestSprintOrchestrator:
    """Tests for dealix.commercial.sprint_orchestrator."""

    def _make_context(self, **kwargs):
        from dealix.commercial.sprint_orchestrator import SprintContext

        return SprintContext(
            engagement_id=kwargs.get("engagement_id", "eng_test_001"),
            customer_id=kwargs.get("customer_id", "cust_test"),
            customer_name=kwargs.get("customer_name", "Test Co"),
            customer_name_ar=kwargs.get("customer_name_ar", "شركة اختبار"),
            sector=kwargs.get("sector", "b2b_saas"),
            city=kwargs.get("city", "Riyadh"),
            sources=kwargs.get(
                "sources",
                [
                    {
                        "source_id": "src_crm_001",
                        "source_type": "crm",
                        "owner": "cust_test",
                        "allowed_use": ["internal_analysis"],
                        "contains_pii": False,
                        "sensitivity": "medium",
                        "retention_policy": "project_duration",
                        "ai_access_allowed": True,
                        "external_use_allowed": False,
                    }
                ],
            ),
            rows=kwargs.get(
                "rows",
                [
                    {
                        "company_name": "Acme SA",
                        "sector": "fintech",
                        "city": "Riyadh",
                        "source": "crm",
                        "b2b_service_fit": 75,
                        "data_maturity": 60,
                        "governance_posture": 70,
                        "budget_signal": 80,
                        "decision_velocity": 65,
                    },
                    {
                        "company_name": "Beta Tech",
                        "sector": "healthcare",
                        "city": "Jeddah",
                        "source": "crm",
                        "b2b_service_fit": 55,
                        "data_maturity": 50,
                        "governance_posture": 60,
                        "budget_signal": 40,
                        "decision_velocity": 55,
                    },
                ],
            ),
            pain_summary=kwargs.get("pain_summary", "revenue growth challenges"),
            pain_summary_ar=kwargs.get("pain_summary_ar", "تحديات نمو الإيراد"),
            founder_approved=kwargs.get("founder_approved", True),
            proof_evidence=kwargs.get(
                "proof_evidence",
                {
                    "executive_summary": "Sprint delivered key insights.",
                    "problem": "Revenue funnel gaps identified.",
                    "inputs": "CRM export 200 rows.",
                    "work_completed": "DQ score + account scoring completed.",
                    "outputs": "Top 10 accounts ranked.",
                },
            ),
            workflow_owner_present=kwargs.get("workflow_owner_present", True),
            adoption_score_override=kwargs.get("adoption_score_override", 75.0),
            proof_score_override=kwargs.get("proof_score_override", 82.0),
        )

    def test_invalid_day_raises(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        with pytest.raises(ValueError):
            orc.run_day(0, ctx)
        with pytest.raises(ValueError):
            orc.run_day(8, ctx)

    def test_day_1_source_passport_audit(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        result = orc.run_day(1, ctx)
        assert result.day == 1
        assert result.status in ("complete", "pending")
        assert "sources_audited" in result.output
        assert result.output["sources_audited"] >= 1
        assert result.governance_decision in ("ALLOW", "REQUIRE_APPROVAL")

    def test_day_2_data_quality_score(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        result = orc.run_day(2, ctx)
        assert result.day == 2
        assert result.status == "complete"
        assert "overall_dq" in result.output
        assert 0 <= result.output["overall_dq"] <= 100

    def test_day_3_account_scoring(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        result = orc.run_day(3, ctx)
        assert result.day == 3
        assert result.status == "complete"
        top_10 = result.output.get("top_10", [])
        assert len(top_10) <= 10
        # Results should be sorted descending by icp_score.
        if len(top_10) > 1:
            assert top_10[0]["icp_score"] >= top_10[-1]["icp_score"]

    def test_day_4_draft_pack(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        result = orc.run_day(4, ctx)
        assert result.day == 4
        drafts = result.output.get("whatsapp_drafts", [])
        assert len(drafts) == 3
        for d in drafts:
            assert d["status"] == "draft_only"
        assert "email_sequence" in result.output
        assert "proposal_preview_md" in result.output

    def test_day_5_blocked_without_approval(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context(founder_approved=False)
        result = orc.run_day(5, ctx)
        assert result.day == 5
        assert result.status == "blocked"
        assert "REQUIRE_APPROVAL" in result.governance_decision

    def test_day_5_passes_with_approval(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context(founder_approved=True)
        result = orc.run_day(5, ctx)
        assert result.day == 5
        assert result.status == "complete"
        assert result.output.get("approved") is True

    def test_day_6_proof_pack(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        result = orc.run_day(6, ctx)
        assert result.day == 6
        assert result.status == "complete"
        assert "proof_pack" in result.output
        assert 0 <= result.output["completeness_score"] <= 100

    def test_day_7_capital_and_retainer(self, tmp_path, monkeypatch):
        monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))

        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context(
            adoption_score_override=75.0,
            proof_score_override=85.0,
            workflow_owner_present=True,
        )
        result = orc.run_day(7, ctx)
        assert result.day == 7
        assert result.status == "complete"
        assert "capital_asset_id" in result.output
        assert "retainer_eligible" in result.output

    def test_day_7_retainer_not_eligible_when_gaps(self, tmp_path, monkeypatch):
        monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))

        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context(
            adoption_score_override=30.0,  # below 70 threshold
            proof_score_override=40.0,     # below 80 threshold
            workflow_owner_present=False,
        )
        result = orc.run_day(7, ctx)
        assert result.output.get("retainer_eligible") is False
        assert len(result.output.get("retainer_gaps", [])) > 0

    def test_run_all_returns_7_results(self, tmp_path, monkeypatch):
        monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))

        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        results = orc.run_all(ctx)
        assert len(results) == 7
        for i, r in enumerate(results, start=1):
            assert r.day == i

    def test_day_result_to_dict(self):
        from dealix.commercial.sprint_orchestrator import SprintOrchestrator

        orc = SprintOrchestrator()
        ctx = self._make_context()
        result = orc.run_day(1, ctx)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["day"] == 1
        assert "governance_decision" in d
        assert "output" in d


# ===========================================================================
# ZATCA Invoice tests
# ===========================================================================


class TestZATCAInvoice:
    """Tests for dealix.commercial.zatca_invoice."""

    def test_compute_vat_standard(self):
        """15% KSA VAT calculation from inclusive amount."""
        from dealix.commercial.zatca_invoice import compute_vat

        result = compute_vat(1150.0)
        assert result["vat"] == pytest.approx(150.0, abs=0.02)
        assert result["net"] == pytest.approx(1000.0, abs=0.02)
        assert result["total"] == pytest.approx(1150.0, abs=0.01)

    def test_compute_vat_sprint_price(self):
        """Sprint price 499 SAR inclusive."""
        from dealix.commercial.zatca_invoice import compute_vat

        result = compute_vat(499.0)
        assert result["vat"] > 0
        assert result["net"] + result["vat"] == pytest.approx(result["total"], abs=0.02)

    def test_compute_vat_zero_amount(self):
        from dealix.commercial.zatca_invoice import compute_vat

        result = compute_vat(0.0)
        assert result["vat"] == 0.0
        assert result["net"] == 0.0

    def test_generate_phase2_invoice_local(self):
        """generate_phase2_invoice returns valid Phase2InvoiceResult."""
        from dealix.commercial.zatca_invoice import Phase2InvoiceResult, generate_phase2_invoice

        result = generate_phase2_invoice(
            invoice_number="INV-TEST-001",
            buyer_name="Test Buyer",
            buyer_name_ar="مشتري اختبار",
            amount_sar=1150.0,
            description="Revenue Intelligence Sprint",
            is_b2b=True,
        )
        assert isinstance(result, Phase2InvoiceResult)
        assert result.invoice_number == "INV-TEST-001"
        assert result.invoice_type == "standard"
        assert result.is_b2b is True
        assert result.xml_b64  # non-empty
        assert result.qr_code_b64  # non-empty
        assert result.hash_chain_ref  # non-empty

    def test_generate_phase2_invoice_simplified(self):
        """B2C simplified invoice (amount <= 1000 SAR)."""
        from dealix.commercial.zatca_invoice import generate_phase2_invoice

        result = generate_phase2_invoice(
            invoice_number="INV-TEST-002",
            buyer_name="Consumer",
            amount_sar=499.0,
            is_b2b=False,
        )
        assert result.invoice_type == "simplified"
        assert result.is_b2b is False

    def test_generate_phase2_vat_amounts(self):
        """VAT amounts in result match 15% calculation."""
        from decimal import Decimal

        from dealix.commercial.zatca_invoice import generate_phase2_invoice

        result = generate_phase2_invoice(
            invoice_number="INV-TEST-003",
            buyer_name="Buyer",
            amount_sar=1150.0,
        )
        grand = float(result.grand_total_sar)
        vat = float(result.vat_total_sar)
        # 15% of net = 15/115 of total
        expected_vat = round(grand * 15 / 115, 2)
        assert vat == pytest.approx(expected_vat, abs=0.05)

    def test_hash_chain_populated(self):
        """Two invoices with different hash_chain_refs (used as PIH chain)."""
        from dealix.commercial.zatca_invoice import generate_phase2_invoice

        r1 = generate_phase2_invoice(
            invoice_number="INV-A-001",
            buyer_name="Buyer A",
            amount_sar=575.0,
        )
        r2 = generate_phase2_invoice(
            invoice_number="INV-A-002",
            buyer_name="Buyer B",
            amount_sar=690.0,
            previous_invoice_hash=r1.hash_chain_ref,
        )
        assert r1.hash_chain_ref
        assert r2.hash_chain_ref
        assert r1.hash_chain_ref != r2.hash_chain_ref

    def test_arabic_buyer_name_in_xml(self):
        """Arabic buyer name appears in generated XML."""
        from dealix.commercial.zatca_invoice import generate_phase2_invoice

        result = generate_phase2_invoice(
            invoice_number="INV-AR-001",
            buyer_name="شركة المستقبل للتقنية",
            amount_sar=1150.0,
        )
        assert "شركة المستقبل للتقنية" in result.xml_string

    def test_phase2_result_to_dict(self):
        """to_dict returns JSON-serialisable dict."""
        import json

        from dealix.commercial.zatca_invoice import generate_phase2_invoice

        result = generate_phase2_invoice(
            invoice_number="INV-DICT-001",
            buyer_name="Dict Buyer",
            amount_sar=460.0,
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        # Should be JSON-serialisable.
        serialised = json.dumps(d)
        assert "INV-DICT-001" in serialised

    def test_tlv_qr_is_base64(self):
        """QR code is valid Base64."""
        import base64

        from dealix.commercial.zatca_invoice import generate_phase2_invoice

        result = generate_phase2_invoice(
            invoice_number="INV-QR-001",
            buyer_name="QR Buyer",
            amount_sar=500.0,
        )
        # Should not raise.
        decoded = base64.b64decode(result.qr_code_b64)
        assert len(decoded) > 0


# ===========================================================================
# KPI Dashboard pure-function tests
# (Full endpoint tests require the full app stack which depends on a working
# cryptography C extension — not available in this environment. These tests
# verify the router's pure helper functions directly.)
# ===========================================================================


class TestKPIDashboardPureFunctions:
    """Unit tests for the pure functions in api/routers/kpi_dashboard.py.

    We import only the pure helpers to avoid the jose/cryptography C-extension
    crash that occurs when importing the full api.security stack.
    """

    def _load_module(self):
        """Lazy-import without triggering api.security."""
        import importlib.util
        import sys

        # Patch api.security.api_key so the router import doesn't hit jose.
        if "api.security.api_key" not in sys.modules:
            from unittest.mock import MagicMock
            mock_mod = MagicMock()
            mock_mod.require_admin_key = lambda: None
            sys.modules["api.security.api_key"] = mock_mod
            sys.modules["api.security"] = MagicMock()

        import importlib
        return importlib.import_module("api.routers.kpi_dashboard")

    def test_mock_mrr_history_length(self):
        mod = self._load_module()
        history = mod._mock_mrr_history(6)
        assert len(history) == 6

    def test_mock_mrr_history_fields(self):
        mod = self._load_module()
        history = mod._mock_mrr_history(3)
        for entry in history:
            assert "month" in entry
            assert "mrr_sar" in entry
            assert "arr_sar" in entry
            assert entry["arr_sar"] == entry["mrr_sar"] * 12

    def test_mock_cohort_structure(self):
        mod = self._load_module()
        cohort = mod._mock_cohort("2026-01")
        assert cohort["cohort_month"] == "2026-01"
        assert "retention_by_month" in cohort
        assert len(cohort["retention_by_month"]) > 0
        assert cohort["retention_by_month"][0]["pct"] == 100

    def test_mock_nps_trend_length(self):
        mod = self._load_module()
        trend = mod._mock_nps_trend(6)
        assert len(trend) == 6

    def test_mock_nps_trend_fields(self):
        mod = self._load_module()
        trend = mod._mock_nps_trend(3)
        for entry in trend:
            assert "period" in entry
            assert "nps" in entry
            assert "promoters_pct" in entry

    def test_compute_health_score_range(self):
        mod = self._load_module()
        result = mod._compute_health_score(
            mrr_growth_pct=15.0,
            churn_rate=0.03,
            nps=52,
            pipeline_coverage=4.5,
            proof_score=72.0,
        )
        assert 0 <= result["score"] <= 100
        assert result["tier"] in ("healthy", "moderate", "at_risk", "critical")
        assert "components" in result

    def test_compute_health_score_healthy(self):
        mod = self._load_module()
        result = mod._compute_health_score(
            mrr_growth_pct=50.0,
            churn_rate=0.01,
            nps=70,
            pipeline_coverage=8.0,
            proof_score=90.0,
        )
        assert result["tier"] == "healthy"
        assert result["score"] >= 75

    def test_compute_health_score_at_risk(self):
        mod = self._load_module()
        result = mod._compute_health_score(
            mrr_growth_pct=0.0,
            churn_rate=0.15,
            nps=-10,
            pipeline_coverage=0.5,
            proof_score=20.0,
        )
        assert result["tier"] in ("at_risk", "critical")

    def test_label_helper_bilingual(self):
        mod = self._load_module()
        label = mod._label("mrr")
        assert "ar" in label
        assert "en" in label
        assert label["ar"]
        assert label["en"]

    def test_governance_decision_constant(self):
        mod = self._load_module()
        assert mod._GOV == "ALLOW_WITH_REVIEW"

    def test_kpi_summary_async_function_exists(self):
        """Verify the summary endpoint coroutine is present."""
        import asyncio

        mod = self._load_module()
        result = asyncio.run(mod.kpi_summary())
        assert "governance_decision" in result
        assert "metrics" in result
        assert "mrr" in result["metrics"]

    def test_kpi_commercial_async_function_exists(self):
        import asyncio

        mod = self._load_module()
        result = asyncio.run(mod.kpi_commercial())
        assert "governance_decision" in result
        assert "metrics" in result

    def test_kpi_nps_async_function(self):
        import asyncio

        mod = self._load_module()
        result = asyncio.run(mod.kpi_nps(periods=4))
        assert "trend" in result
        assert len(result["trend"]) == 4

    def test_kpi_health_score_async_function(self):
        import asyncio

        mod = self._load_module()
        result = asyncio.run(mod.kpi_health_score())
        assert 0 <= result["health_score"] <= 100
        assert result["tier"] in ("healthy", "moderate", "at_risk", "critical")

    def test_kpi_cohort_async_function(self):
        import asyncio

        mod = self._load_module()
        result = asyncio.run(mod.kpi_cohort(cohort_month="2026-03"))
        assert result["cohort"]["cohort_month"] == "2026-03"


# ===========================================================================
# Weekly Report Generator tests
# ===========================================================================


class TestWeeklyReportGenerator:
    """Tests for dealix.commercial_ops.weekly_report_generator."""

    def _week_data(self, **kwargs) -> dict:
        base = {
            "week_label": "W22 2026",
            "mrr_sar": 22_000,
            "mrr_prev_sar": 20_000,
            "new_deals": 3,
            "pipeline_value_sar": 90_000,
            "total_leads": 12,
            "hot": 3,
            "warm": 4,
            "cool": 3,
            "cold": 2,
            "avg_score": 61.5,
            "pdpl_compliant_pct": 95.0,
            "posts_published": 5,
            "total_impressions": 8_400,
            "avg_engagement_rate_pct": 4.2,
            "leads_from_content": 4,
        }
        base.update(kwargs)
        return base

    def test_generate_returns_weekly_report(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReport, WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data())
        assert isinstance(report, WeeklyReport)

    def test_week_label_preserved(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data(week_label="W10 2026"))
        assert report.week_label == "W10 2026"

    def test_revenue_summary_populated(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data())
        rev = report.revenue_summary
        assert rev["mrr_sar"] == 22_000
        assert rev["new_deals"] == 3
        assert rev["mrr_growth_pct"] == pytest.approx(10.0, abs=0.1)

    def test_mrr_growth_positive(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data(mrr_sar=22_000, mrr_prev_sar=20_000))
        assert report.revenue_summary["mrr_growth_pct"] > 0

    def test_mrr_decline_triggers_risk_flag(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data(mrr_sar=18_000, mrr_prev_sar=22_000))
        risk_levels = [f["level"] for f in report.risk_flags]
        assert "high" in risk_levels

    def test_low_pdpl_triggers_risk_flag(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data(pdpl_compliant_pct=70.0))
        risks = [f.get("risk_en", "") for f in report.risk_flags]
        assert any("PDPL" in r for r in risks)

    def test_hot_leads_trigger_action(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data(hot=5))
        actions = [a.get("action_en", "") for a in report.action_items]
        assert any("HOT" in a or "hot" in a.lower() for a in actions)

    def test_action_items_include_priority(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data())
        for item in report.action_items:
            assert "priority" in item

    def test_governance_decision_allow_when_healthy(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(
            self._week_data(
                mrr_sar=25_000,
                mrr_prev_sar=22_000,
                pdpl_compliant_pct=98.0,
                pipeline_value_sar=200_000,
            )
        )
        assert report.governance_decision in ("ALLOW", "ALLOW_WITH_REVIEW")

    def test_governance_allow_with_review_when_risky(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(
            self._week_data(
                mrr_sar=15_000,
                mrr_prev_sar=22_000,
                pdpl_compliant_pct=70.0,
            )
        )
        assert report.governance_decision == "ALLOW_WITH_REVIEW"

    def test_to_dict_is_json_serialisable(self):
        import json

        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data())
        d = report.to_dict()
        serialised = json.dumps(d)
        assert "W22 2026" in serialised

    def test_as_markdown_bilingual(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate(self._week_data())
        md = report.as_markdown()
        # Should contain both English and Arabic content markers.
        assert "Revenue Summary" in md
        assert "ملخص الإيراد" in md
        assert "Lead Quality" in md or "جودة العملاء" in md

    def test_empty_week_data_does_not_raise(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        report = gen.generate({})
        assert report is not None
        assert report.revenue_summary["mrr_sar"] == 0

    def test_custom_action_items_included(self):
        from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

        gen = WeeklyReportGenerator()
        custom = [
            {
                "action_en": "Call top prospect.",
                "action_ar": "الاتصال بأفضل عميل محتمل.",
                "priority": "high",
            }
        ]
        report = gen.generate(self._week_data(action_items=custom))
        actions_en = [a.get("action_en", "") for a in report.action_items]
        assert any("Call top prospect" in a for a in actions_en)
