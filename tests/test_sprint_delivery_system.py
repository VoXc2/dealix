"""Comprehensive tests for the Dealix Revenue Intelligence Sprint delivery system.

Covers:
- Source Passport DQ scoring (Task 1)
- Account Scoring Matrix (Task 2)
- Retainer Eligibility Engine (Task 3)
- Proof Pack Ledger operations (Task 4)
- Capital Asset Registry (Task 5)
- Sprint Runner API endpoints (Task 6)
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Build a minimal app that mounts only the sprint router — avoids the broken
# jose/cryptography import chain in api.main that fails in this environment.
_app = FastAPI()
from api.routers.sprint_runner import router as _sprint_router  # noqa: E402
_app.include_router(_sprint_router)

client = TestClient(_app)

_ADMIN_HEADER = {"X-Admin-API-Key": "test-admin-key"}


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture()
def _isolated(tmp_path, monkeypatch):
    """Redirect all file-backed stores to tmp_path so tests never touch data/."""
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "val.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    yield tmp_path


@pytest.fixture()
def tmp_ledger_path(tmp_path):
    return tmp_path / "ledger.json"


@pytest.fixture()
def tmp_registry_path(tmp_path):
    return tmp_path / "registry.json"


# ===========================================================================
# Task 1 — Source Passport DQ scoring
# ===========================================================================


class TestSourcePassport:
    def test_empty_sources_returns_zero_dq(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport = SourcePassportBuilder().build([])
        assert passport.overall_dq_score == 0.0
        assert "no_sources_provided" in passport.red_flags

    def test_referral_source_scores_higher_than_cold(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        referral_passport = SourcePassportBuilder().build([
            {
                "name": "Partner Referrals",
                "type": "referral",
                "count": 50,
                "qualified_count": 30,
                "avg_deal_value": 5000.0,
            }
        ])
        cold_passport = SourcePassportBuilder().build([
            {
                "name": "Cold Calls",
                "type": "cold",
                "count": 50,
                "qualified_count": 5,
                "avg_deal_value": 0.0,
            }
        ])
        assert referral_passport.overall_dq_score > cold_passport.overall_dq_score

    def test_low_conversion_triggers_red_flag(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport = SourcePassportBuilder().build([
            {
                "name": "Bad Channel",
                "type": "crm",
                "count": 100,
                "qualified_count": 5,  # 5% < 20% threshold
                "avg_deal_value": 0.0,
            }
        ])
        assert any("low_conversion" in flag for flag in passport.red_flags)

    def test_good_conversion_boosts_score(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport_low = SourcePassportBuilder().build([
            {
                "name": "Channel A",
                "type": "crm",
                "count": 100,
                "qualified_count": 10,  # 10%
                "avg_deal_value": 5000.0,
            }
        ])
        passport_high = SourcePassportBuilder().build([
            {
                "name": "Channel A",
                "type": "crm",
                "count": 100,
                "qualified_count": 50,  # 50% >= 40% threshold
                "avg_deal_value": 5000.0,
            }
        ])
        assert passport_high.overall_dq_score > passport_low.overall_dq_score

    def test_conversion_rate_auto_computed_when_absent(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport = SourcePassportBuilder().build([
            {
                "name": "Inbound Web",
                "type": "inbound",
                "count": 40,
                "qualified_count": 20,
                # no conversion_rate key — builder must compute it
                "avg_deal_value": 3000.0,
            }
        ])
        src = passport.sources[0]
        assert abs(src.conversion_rate - 0.5) < 0.001

    def test_multi_source_totals(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport = SourcePassportBuilder().build([
            {
                "name": "CRM",
                "type": "crm",
                "count": 60,
                "qualified_count": 24,
                "avg_deal_value": 2000.0,
            },
            {
                "name": "WhatsApp",
                "type": "whatsapp",
                "count": 40,
                "qualified_count": 10,
                "avg_deal_value": 0.0,
            },
        ])
        assert passport.total_leads == 100
        assert passport.total_qualified == 34

    def test_cold_source_red_flagged(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport = SourcePassportBuilder().build([
            {
                "name": "Bought List",
                "type": "cold",
                "count": 200,
                "qualified_count": 40,
                "avg_deal_value": 0.0,
            }
        ])
        assert any("cold_source" in flag for flag in passport.red_flags)

    def test_bilingual_recommendations_present(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        passport = SourcePassportBuilder().build([
            {
                "name": "Referrals",
                "type": "referral",
                "count": 30,
                "qualified_count": 20,
                "avg_deal_value": 4000.0,
            }
        ])
        assert len(passport.recommendations_ar) > 0
        assert len(passport.recommendations_en) > 0

    def test_dq_score_bounded_0_to_100(self):
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        for _ in range(3):
            passport = SourcePassportBuilder().build([
                {
                    "name": "X",
                    "type": "referral",
                    "count": 10,
                    "qualified_count": 10,
                    "avg_deal_value": 10000.0,
                }
            ])
            assert 0.0 <= passport.overall_dq_score <= 100.0

    def test_diversity_bonus_applied(self):
        """Multiple trustworthy channel types get a diversity bonus."""
        from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

        single = SourcePassportBuilder().build([
            {
                "name": "CRM Only",
                "type": "crm",
                "count": 50,
                "qualified_count": 25,
                "avg_deal_value": 3000.0,
            }
        ])
        diverse = SourcePassportBuilder().build([
            {
                "name": "CRM",
                "type": "crm",
                "count": 30,
                "qualified_count": 15,
                "avg_deal_value": 3000.0,
            },
            {
                "name": "Inbound",
                "type": "inbound",
                "count": 20,
                "qualified_count": 12,
                "avg_deal_value": 3500.0,
            },
        ])
        assert diverse.overall_dq_score >= single.overall_dq_score


# ===========================================================================
# Task 2 — Account Scoring Matrix
# ===========================================================================


class TestAccountScoringMatrix:
    def _profile(self, **kwargs):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountProfile

        defaults = {
            "company_name": "Acme Corp",
            "sector": "logistics",
            "current_revenue_sar": 500_000.0,
            "growth_signals": [],
            "pain_score": 5.0,
            "engagement_score": 5.0,
            "deal_readiness": "MEDIUM",
        }
        defaults.update(kwargs)
        return AccountProfile(**defaults)

    def test_empty_list_returns_empty(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        assert AccountScoringMatrix().score_accounts([]) == []

    def test_scores_bounded_0_to_100(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        accounts = [self._profile(pain_score=i, engagement_score=i) for i in range(11)]
        results = AccountScoringMatrix().score_accounts(accounts)
        for r in results:
            assert 0.0 <= r.composite_score <= 100.0

    def test_priority_rank_starts_at_1_and_is_unique(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        accounts = [self._profile(company_name=f"Co{i}", pain_score=float(i)) for i in range(5)]
        results = AccountScoringMatrix().score_accounts(accounts)
        ranks = [r.priority_rank for r in results]
        assert ranks == list(range(1, 6))

    def test_high_deal_readiness_beats_low(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        high = self._profile(company_name="High", deal_readiness="HIGH")
        low = self._profile(company_name="Low", deal_readiness="LOW")
        results = AccountScoringMatrix().score_accounts([low, high])
        rank_high = next(r.priority_rank for r in results if r.account.company_name == "High")
        rank_low = next(r.priority_rank for r in results if r.account.company_name == "Low")
        assert rank_high < rank_low  # lower rank number = better

    def test_high_fit_sector_better_than_unknown(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        high = self._profile(company_name="Logistics Co", sector="logistics")
        unknown = self._profile(company_name="Mystery Co", sector="astrology")
        results = AccountScoringMatrix().score_accounts([unknown, high])
        rank_high = next(r.priority_rank for r in results if r.account.company_name == "Logistics Co")
        rank_unk = next(r.priority_rank for r in results if r.account.company_name == "Mystery Co")
        assert rank_high < rank_unk

    def test_growth_signals_add_bonus(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        no_signals = self._profile(company_name="NoGrowth", growth_signals=[])
        with_signals = self._profile(
            company_name="Growing",
            growth_signals=["new_funding", "hiring_fast"],
        )
        results = AccountScoringMatrix().score_accounts([no_signals, with_signals])
        score_growing = next(r.composite_score for r in results if r.account.company_name == "Growing")
        score_none = next(r.composite_score for r in results if r.account.company_name == "NoGrowth")
        assert score_growing >= score_none

    def test_bilingual_recommended_actions(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        results = AccountScoringMatrix().score_accounts([self._profile()])
        assert results[0].recommended_action_ar
        assert results[0].recommended_action_en

    def test_top_priority_recommendation_for_high_score(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        top = self._profile(
            company_name="TopCo",
            pain_score=10.0,
            engagement_score=10.0,
            deal_readiness="HIGH",
            sector="fintech",
            growth_signals=["new_funding", "hiring_fast", "product_launch"],
        )
        results = AccountScoringMatrix().score_accounts([top])
        # High score should trigger priority messaging
        assert results[0].composite_score >= 80.0

    def test_returns_sorted_descending(self):
        from dealix.revenue_ops_autopilot.account_scoring_matrix import AccountScoringMatrix

        accounts = [
            self._profile(company_name=f"Co{i}", pain_score=float(i), engagement_score=float(i))
            for i in range(5)
        ]
        results = AccountScoringMatrix().score_accounts(accounts)
        scores = [r.composite_score for r in results]
        assert scores == sorted(scores, reverse=True)


# ===========================================================================
# Task 3 — Retainer Eligibility Engine
# ===========================================================================


class TestRetainerEligibilityEngine:
    def _result(self, **kwargs):
        defaults = {
            "sprint_id": "sprint-001",
            "account_id": "account-001",
            "proof_level": "L2",
            "satisfaction_score": 8.0,
            "measurable_result_achieved": True,
        }
        defaults.update(kwargs)
        return defaults

    def test_eligible_when_all_gates_pass(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result())
        assert check.is_eligible is True
        assert check.recommended_tier is not None
        assert check.ineligibility_reasons == []

    def test_ineligible_when_proof_level_too_low(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result(proof_level="L0"))
        assert check.is_eligible is False
        assert any("proof_level_too_low" in r for r in check.ineligibility_reasons)

    def test_ineligible_when_satisfaction_below_threshold(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result(satisfaction_score=5.0))
        assert check.is_eligible is False
        assert any("satisfaction_below_threshold" in r for r in check.ineligibility_reasons)

    def test_ineligible_when_no_measurable_result(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result(measurable_result_achieved=False))
        assert check.is_eligible is False
        assert "no_measurable_result_achieved" in check.ineligibility_reasons

    def test_multiple_ineligibility_reasons_captured(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(
            self._result(
                proof_level="L0",
                satisfaction_score=3.0,
                measurable_result_achieved=False,
            )
        )
        assert len(check.ineligibility_reasons) == 3

    def test_scale_tier_for_high_proof_and_satisfaction(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(
            self._result(proof_level="L4", satisfaction_score=9.5)
        )
        assert check.recommended_tier == "scale_4999"

    def test_growth_tier_for_l2_and_good_satisfaction(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(
            self._result(proof_level="L2", satisfaction_score=8.5)
        )
        assert check.recommended_tier == "growth_3999"

    def test_starter_tier_for_l1_eligible(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(
            self._result(proof_level="L1", satisfaction_score=7.0)
        )
        assert check.is_eligible is True
        assert check.recommended_tier == "starter_2999"

    def test_upsell_pitch_present_when_eligible(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result())
        assert check.upsell_pitch_ar
        assert check.upsell_pitch_en

    def test_no_upsell_pitch_when_ineligible(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result(proof_level="L0"))
        assert check.upsell_pitch_ar == ""
        assert check.upsell_pitch_en == ""

    def test_unknown_proof_level_normalised_to_l0(self):
        from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerEligibilityEngine

        check = RetainerEligibilityEngine().check(self._result(proof_level="L99"))
        assert check.proof_level == "L0"
        assert check.is_eligible is False


# ===========================================================================
# Task 4 — Proof Pack Ledger
# ===========================================================================


class TestProofPackLedger:
    def test_append_and_get_all(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import (
            ProofPackEntry,
            ProofPackLedger,
        )

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        entry = ProofPackEntry(
            pack_id="pack-001",
            account_id="acct-001",
            proof_level="L2",
            evidence_items=["17 duplicates removed", "DQ score 84"],
            approved_by_founder=True,
            customer_consented=True,
        )
        ledger.append(entry)
        all_entries = ledger.get_all()
        assert len(all_entries) == 1
        assert all_entries[0].pack_id == "pack-001"

    def test_get_by_account_filters_correctly(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import (
            ProofPackEntry,
            ProofPackLedger,
        )

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        for i in range(3):
            ledger.append(ProofPackEntry(
                pack_id=f"pack-00{i}",
                account_id="acct-A" if i < 2 else "acct-B",
                proof_level="L1",
                evidence_items=[],
            ))
        assert len(ledger.get_by_account("acct-A")) == 2
        assert len(ledger.get_by_account("acct-B")) == 1

    def test_get_publishable_requires_l2_approved_consented(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import (
            ProofPackEntry,
            ProofPackLedger,
        )

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        # Should NOT be publishable (L1)
        ledger.append(ProofPackEntry(
            pack_id="low",
            account_id="acct-X",
            proof_level="L1",
            approved_by_founder=True,
            customer_consented=True,
        ))
        # Should NOT be publishable (missing consent)
        ledger.append(ProofPackEntry(
            pack_id="no-consent",
            account_id="acct-X",
            proof_level="L2",
            approved_by_founder=True,
            customer_consented=False,
        ))
        # Should BE publishable
        ledger.append(ProofPackEntry(
            pack_id="good",
            account_id="acct-X",
            proof_level="L2",
            approved_by_founder=True,
            customer_consented=True,
        ))
        publishable = ledger.get_publishable()
        assert len(publishable) == 1
        assert publishable[0].pack_id == "good"

    def test_get_publishable_with_l3_and_l4(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import (
            ProofPackEntry,
            ProofPackLedger,
        )

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        for level in ("L3", "L4"):
            ledger.append(ProofPackEntry(
                pack_id=f"pack-{level}",
                account_id="acct-Y",
                proof_level=level,  # type: ignore[arg-type]
                approved_by_founder=True,
                customer_consented=True,
            ))
        assert len(ledger.get_publishable()) == 2

    def test_empty_ledger_returns_empty_lists(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import ProofPackLedger

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        assert ledger.get_all() == []
        assert ledger.get_publishable() == []
        assert ledger.get_by_account("nobody") == []

    def test_export_markdown_no_entries(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import ProofPackLedger

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        md = ledger.export_markdown()
        assert "No entries found" in md

    def test_export_markdown_contains_pack_details(self, tmp_ledger_path):
        from dealix.revenue_ops_autopilot.proof_pack_ledger import (
            ProofPackEntry,
            ProofPackLedger,
        )

        ledger = ProofPackLedger(ledger_path=tmp_ledger_path)
        ledger.append(ProofPackEntry(
            pack_id="pack-md",
            account_id="acct-md",
            proof_level="L3",
            evidence_items=["Revenue increase 15%"],
            approved_by_founder=True,
            customer_consented=True,
        ))
        md = ledger.export_markdown()
        assert "pack-md" in md
        assert "L3" in md
        assert "Revenue increase 15%" in md

    def test_ledger_persists_across_instances(self, tmp_ledger_path):
        """A new ledger instance reading same path sees previously saved entries."""
        from dealix.revenue_ops_autopilot.proof_pack_ledger import (
            ProofPackEntry,
            ProofPackLedger,
        )

        l1 = ProofPackLedger(ledger_path=tmp_ledger_path)
        l1.append(ProofPackEntry(
            pack_id="persist-test",
            account_id="acct-persist",
            proof_level="L2",
        ))
        l2 = ProofPackLedger(ledger_path=tmp_ledger_path)
        entries = l2.get_all()
        assert len(entries) == 1
        assert entries[0].pack_id == "persist-test"


# ===========================================================================
# Task 5 — Capital Asset Registry
# ===========================================================================


class TestCapitalAssetRegistry:
    def _asset(self, account_id: str = "acct-001", **kwargs):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAsset

        defaults = {
            "account_id": account_id,
            "asset_type": "template",
            "title_ar": "قالب التواصل",
            "title_en": "Outreach Template",
            "value_estimate_sar": 500.0,
        }
        defaults.update(kwargs)
        return CapitalAsset(**defaults)

    def test_register_and_get_by_account(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        asset = self._asset()
        registry.register(asset)
        results = registry.get_by_account("acct-001")
        assert len(results) == 1
        assert results[0].title_en == "Outreach Template"

    def test_get_total_value_by_account(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        registry.register(self._asset(value_estimate_sar=1000.0))
        registry.register(self._asset(value_estimate_sar=2000.0))
        assert registry.get_total_value_by_account("acct-001") == 3000.0

    def test_archived_assets_excluded_from_total(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import (
            CapitalAsset,
            CapitalAssetRegistry,
        )

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        registry.register(self._asset(value_estimate_sar=1000.0, status="active"))
        registry.register(CapitalAsset(
            account_id="acct-001",
            asset_type="workflow",
            title_ar="سير عمل مؤرشف",
            title_en="Archived Workflow",
            value_estimate_sar=5000.0,
            status="archived",
        ))
        assert registry.get_total_value_by_account("acct-001") == 1000.0

    def test_asset_id_auto_generated(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import (
            CapitalAsset,
            CapitalAssetRegistry,
        )

        CapitalAssetRegistry(registry_path=tmp_registry_path)  # verify instantiation
        asset = self._asset()
        assert asset.asset_id  # non-empty UUID

    def test_get_by_account_filters_other_accounts(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        registry.register(self._asset(account_id="acct-A"))
        registry.register(self._asset(account_id="acct-B"))
        registry.register(self._asset(account_id="acct-A"))
        assert len(registry.get_by_account("acct-A")) == 2
        assert len(registry.get_by_account("acct-B")) == 1

    def test_get_all_returns_every_asset(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        for i in range(4):
            registry.register(self._asset(account_id=f"acct-{i}"))
        assert len(registry.get_all()) == 4

    def test_empty_registry_zero_value(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        assert registry.get_total_value_by_account("nobody") == 0.0

    def test_persists_across_instances(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

        r1 = CapitalAssetRegistry(registry_path=tmp_registry_path)
        r1.register(self._asset(account_id="persist-acct"))
        r2 = CapitalAssetRegistry(registry_path=tmp_registry_path)
        assert len(r2.get_all()) == 1

    def test_asset_types(self, tmp_registry_path):
        from dealix.revenue_ops_autopilot.capital_asset_registry import (
            CapitalAsset,
            CapitalAssetRegistry,
        )

        registry = CapitalAssetRegistry(registry_path=tmp_registry_path)
        for atype in ("automation", "knowledge", "template", "workflow"):
            asset = CapitalAsset(
                account_id="type-test",
                asset_type=atype,  # type: ignore[arg-type]
                title_ar="اختبار",
                title_en="Test Asset",
            )
            registry.register(asset)
        assets = registry.get_by_account("type-test")
        types = {a.asset_type for a in assets}
        assert types == {"automation", "knowledge", "template", "workflow"}


# ===========================================================================
# Task 6 — Sprint Runner API Endpoints
# ===========================================================================


class TestSprintRunnerAPI:
    """Tests for the four new sprint delivery endpoints."""

    # ---- /source-passport ------------------------------------------------

    def test_source_passport_requires_admin_key(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-001/source-passport",
            json={"sources": []},
        )
        assert resp.status_code == 401

    def test_source_passport_returns_passport(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-001/source-passport",
            headers=_ADMIN_HEADER,
            json={
                "sources": [
                    {
                        "name": "CRM",
                        "type": "crm",
                        "count": 50,
                        "qualified_count": 25,
                        "avg_deal_value": 3000.0,
                    }
                ]
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "overall_dq_score" in data
        assert data["sprint_id"] == "spr-001"
        assert isinstance(data["sources"], list)

    def test_source_passport_empty_sources_returns_zero_dq(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-002/source-passport",
            headers=_ADMIN_HEADER,
            json={"sources": []},
        )
        assert resp.status_code == 200
        assert resp.json()["overall_dq_score"] == 0.0

    # ---- /account-scoring ------------------------------------------------

    def test_account_scoring_requires_admin_key(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-001/account-scoring",
            json={"accounts": []},
        )
        assert resp.status_code == 401

    def test_account_scoring_returns_ranked_accounts(self, _isolated):
        accounts = [
            {
                "company_name": f"Company {i}",
                "sector": "logistics",
                "pain_score": float(i),
                "engagement_score": float(i),
                "deal_readiness": "MEDIUM",
            }
            for i in range(1, 6)
        ]
        resp = client.post(
            "/api/v1/sprint/spr-003/account-scoring",
            headers=_ADMIN_HEADER,
            json={"accounts": accounts},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["sprint_id"] == "spr-003"
        assert data["total_accounts_scored"] == 5
        assert len(data["top_accounts"]) == 5

    def test_account_scoring_caps_at_top_10(self, _isolated):
        accounts = [
            {
                "company_name": f"Co{i}",
                "sector": "retail",
                "pain_score": 5.0,
                "engagement_score": 5.0,
                "deal_readiness": "LOW",
            }
            for i in range(15)
        ]
        resp = client.post(
            "/api/v1/sprint/spr-004/account-scoring",
            headers=_ADMIN_HEADER,
            json={"accounts": accounts},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_accounts_scored"] == 15
        assert len(data["top_accounts"]) == 10

    def test_account_scoring_invalid_payload_returns_422(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-005/account-scoring",
            headers=_ADMIN_HEADER,
            json={
                "accounts": [{"company_name": "Bad", "pain_score": 999.0}]  # pain > 10
            },
        )
        assert resp.status_code == 422

    # ---- /retainer-check -------------------------------------------------

    def test_retainer_check_requires_admin_key(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-001/retainer-check",
            json={
                "account_id": "acc-1",
                "proof_level": "L2",
                "satisfaction_score": 8.0,
                "measurable_result_achieved": True,
            },
        )
        assert resp.status_code == 401

    def test_retainer_check_eligible_response(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-006/retainer-check",
            headers=_ADMIN_HEADER,
            json={
                "account_id": "acc-eligible",
                "proof_level": "L2",
                "satisfaction_score": 8.0,
                "measurable_result_achieved": True,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_eligible"] is True
        assert data["recommended_tier"] is not None
        assert data["sprint_id"] == "spr-006"

    def test_retainer_check_ineligible_response(self, _isolated):
        resp = client.post(
            "/api/v1/sprint/spr-007/retainer-check",
            headers=_ADMIN_HEADER,
            json={
                "account_id": "acc-ineligible",
                "proof_level": "L0",
                "satisfaction_score": 4.0,
                "measurable_result_achieved": False,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_eligible"] is False
        assert len(data["ineligibility_reasons"]) == 3

    # ---- /capital-assets -------------------------------------------------

    def test_capital_assets_requires_admin_key(self, _isolated):
        resp = client.get(
            "/api/v1/sprint/spr-001/capital-assets?account_id=acct-001"
        )
        assert resp.status_code == 401

    def test_capital_assets_empty_registry(self, _isolated):
        resp = client.get(
            "/api/v1/sprint/spr-008/capital-assets?account_id=acct-empty",
            headers=_ADMIN_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["sprint_id"] == "spr-008"
        assert data["total_assets"] == 0
        assert data["total_value_sar"] == 0.0
        assert data["assets"] == []

    def test_capital_assets_missing_account_id_returns_422(self, _isolated):
        resp = client.get(
            "/api/v1/sprint/spr-009/capital-assets",
            headers=_ADMIN_HEADER,
        )
        assert resp.status_code == 422
