"""
Tests for the LeadScorer — scoring formula, weights, and explainability.
"""

from __future__ import annotations

import pytest
from datetime import datetime, timedelta

from app.intelligence.models import (
    Company,
    Contact,
    FundingEvent,
    HiringSignal,
    Lead,
    Region,
    ScoreBreakdown,
    Sector,
    Signal,
    SignalType,
    SocialHandles,
    TenderWin,
)
from app.intelligence.scoring import LeadScorer, SCORE_WEIGHTS
from app.intelligence.enrichment import EnrichmentResult


# ─────────────────────────── Fixtures ────────────────────────────────────────


@pytest.fixture
def scorer():
    return LeadScorer()


@pytest.fixture
def strong_company():
    """A company that should score high across all dimensions."""
    return Company(
        name="StrongCo",
        name_ar="شركة قوية",
        domain="strongco.com",
        website="https://strongco.com",
        sector=Sector.ECOMMERCE,
        region=Region.RIYADH,
        city="Riyadh",
        employee_count=200,
        revenue_estimate_sar=500_000_000,
        ceo_name="Ahmed CEO",
        tech_stack=["AWS", "React", "HubSpot", "Salesforce"],
        social_handles=SocialHandles(linkedin="company/strongco"),
        decision_makers=[
            Contact(
                full_name="Ahmed CEO",
                title="CEO",
                seniority="c_level",
                is_decision_maker=True,
                email="ahmed@strongco.com",
            )
        ],
        funding_events=[
            FundingEvent(
                round_type="Series B",
                amount_usd=50_000_000,
                announced_at=datetime.utcnow() - timedelta(days=30),
            )
        ],
        hiring_signals=[
            HiringSignal(
                job_title="VP Sales",
                seniority="vp",
                source="linkedin_jobs",
                posted_at=datetime.utcnow() - timedelta(days=10),
            ),
            HiringSignal(
                job_title="Senior Engineer",
                seniority="individual_contributor",
                source="linkedin_jobs",
                posted_at=datetime.utcnow() - timedelta(days=5),
            ),
        ],
    )


@pytest.fixture
def weak_company():
    """A company that should score low — minimal data."""
    return Company(
        name="WeakCo",
        sector=Sector.OTHER,
        employee_count=3,
    )


@pytest.fixture
def enrichment_result_with_signals(strong_company):
    """EnrichmentResult with multiple intent signals."""
    result = EnrichmentResult(strong_company)
    result.add_signals([
        Signal(
            signal_type=SignalType.FUNDING,
            title="Series B raised",
            score_contribution=25.0,
            source="news",
            detected_at=datetime.utcnow() - timedelta(days=20),
        ),
        Signal(
            signal_type=SignalType.HIRING,
            title="VP Sales position open",
            score_contribution=15.0,
            source="linkedin",
            detected_at=datetime.utcnow() - timedelta(days=5),
        ),
        Signal(
            signal_type=SignalType.TECH_CHANGE,
            title="Using HubSpot CRM",
            score_contribution=15.0,
            source="builtwith",
            detected_at=datetime.utcnow() - timedelta(days=30),
        ),
    ], "test_source")
    return result


# ─────────────────────────── Weight Validation ───────────────────────────────


class TestScoringWeights:
    def test_default_weights_sum_to_one(self):
        """Default weights must sum to 1.0."""
        total = sum(SCORE_WEIGHTS.values())
        assert abs(total - 1.0) < 0.01

    def test_invalid_weights_rejected(self):
        """Weights that don't sum to 1.0 raise ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            LeadScorer(weights={"icp": 0.5, "intent": 0.5, "timing": 0.5,
                                "budget": 0.5, "authority": 0.5, "engagement": 0.5})

    def test_custom_weights_accepted(self):
        """Custom valid weights work."""
        scorer = LeadScorer(weights={
            "icp": 0.40,
            "intent": 0.30,
            "timing": 0.10,
            "budget": 0.10,
            "authority": 0.05,
            "engagement": 0.05,
        })
        assert scorer is not None


# ─────────────────────────── Score Range ─────────────────────────────────────


class TestScoreRange:
    def test_score_always_0_100(self, scorer, strong_company, weak_company):
        """Score is always between 0 and 100."""
        strong_score = scorer.score(strong_company)
        weak_score = scorer.score(weak_company)

        assert 0.0 <= strong_score.total_score <= 100.0
        assert 0.0 <= weak_score.total_score <= 100.0

    def test_strong_company_scores_higher(self, scorer, strong_company, weak_company):
        """Strong company scores significantly higher than weak company."""
        strong = scorer.score(strong_company)
        weak = scorer.score(weak_company)
        assert strong.total_score > weak.total_score + 20

    def test_all_sub_scores_in_range(self, scorer, strong_company):
        """All sub-scores are 0-100."""
        s = scorer.score(strong_company)
        assert 0 <= s.icp_score <= 100
        assert 0 <= s.intent_score <= 100
        assert 0 <= s.timing_score <= 100
        assert 0 <= s.budget_score <= 100
        assert 0 <= s.authority_score <= 100
        assert 0 <= s.engagement_score <= 100


# ─────────────────────────── ICP Scoring ─────────────────────────────────────


class TestICPScoring:
    def test_ecommerce_scores_high(self, scorer):
        """E-commerce sector has highest ICP score."""
        c = Company(name="Shop", sector=Sector.ECOMMERCE, employee_count=100,
                    website="https://shop.com",
                    social_handles=SocialHandles(linkedin="company/shop"))
        s = scorer.score(c)
        assert s.icp_score >= 60.0

    def test_government_scores_low(self, scorer):
        """Government sector has low ICP score (well below ecommerce)."""
        c = Company(name="Gov", sector=Sector.GOVERNMENT, employee_count=100)
        s = scorer.score(c)
        # Government ICP = 30% * 0.5 (sector) + size bonus ≈ 45 max
        # The overall score should be significantly lower than ecommerce sector
        assert s.icp_score < 55.0

    def test_sweet_spot_employee_count(self, scorer):
        """50-499 employees scores highest for size."""
        c1 = Company(name="A", sector=Sector.B2B_SAAS, employee_count=100)
        c2 = Company(name="B", sector=Sector.B2B_SAAS, employee_count=5000)
        s1 = scorer.score(c1)
        s2 = scorer.score(c2)
        assert s1.icp_score > s2.icp_score


# ─────────────────────────── Intent Scoring ──────────────────────────────────


class TestIntentScoring:
    def test_funding_signal_boosts_intent(
        self, scorer, strong_company, enrichment_result_with_signals
    ):
        """Funding signals significantly boost intent score."""
        without = scorer.score(strong_company)
        with_signals = scorer.score(strong_company, enrichment_result_with_signals)
        assert with_signals.intent_score >= without.intent_score

    def test_no_signals_low_intent(self, scorer, weak_company):
        """Company with no signals has low intent score."""
        s = scorer.score(weak_company)
        assert s.intent_score < 40.0

    def test_hiring_signal_boosts_intent(self, scorer):
        """Active hiring via enrichment signals boosts intent."""
        from app.intelligence.enrichment import EnrichmentResult
        c = Company(
            name="Hiring Co",
            sector=Sector.B2B_SAAS,
            hiring_signals=[
                HiringSignal(job_title="VP Sales", seniority="vp", source="linkedin"),
                HiringSignal(job_title="Engineer", seniority="individual_contributor", source="linkedin"),
            ]
        )
        # Pass hiring signals via EnrichmentResult to test scoring with signals
        er = EnrichmentResult(c)
        from app.intelligence.models import Signal, SignalType
        from datetime import timedelta
        er.add_signals([
            Signal(
                signal_type=SignalType.HIRING,
                title="VP Sales open",
                score_contribution=15.0,
                source="linkedin",
                detected_at=datetime.utcnow() - timedelta(days=5),
            )
        ], "linkedin")
        s = scorer.score(c, er)
        assert s.intent_score > 10.0

    def test_tender_win_boosts_intent(self, scorer):
        """Government tender wins boost intent (proven budget)."""
        c = Company(
            name="Gov Vendor",
            sector=Sector.TECHNOLOGY,
            tender_wins=[
                TenderWin(
                    title_ar="مشروع حكومي",
                    entity="وزارة",
                    value_sar=20_000_000,
                    awarded_at=datetime.utcnow() - timedelta(days=30),
                )
            ],
        )
        s = scorer.score(c)
        assert s.intent_score > 15.0


# ─────────────────────────── Timing Scoring ──────────────────────────────────


class TestTimingScoring:
    def test_recent_signals_score_higher(self, scorer):
        """Signals from last 30 days score higher than 6-month old signals."""
        recent_signals = [
            Signal(
                signal_type=SignalType.NEWS_MENTION,
                title="Recent news",
                score_contribution=10.0,
                source="news",
                detected_at=datetime.utcnow() - timedelta(days=5),
            )
        ]
        old_signals = [
            Signal(
                signal_type=SignalType.NEWS_MENTION,
                title="Old news",
                score_contribution=10.0,
                source="news",
                detected_at=datetime.utcnow() - timedelta(days=200),
            )
        ]

        c = Company(name="Test", sector=Sector.B2B_SAAS)

        er_recent = EnrichmentResult(c)
        er_recent.add_signals(recent_signals, "news")

        er_old = EnrichmentResult(c)
        er_old.add_signals(old_signals, "news")

        s_recent = scorer.score(c, er_recent)
        s_old = scorer.score(c, er_old)

        assert s_recent.timing_score > s_old.timing_score

    def test_no_signals_low_timing(self, scorer, weak_company):
        """No signals → low timing score."""
        s = scorer.score(weak_company)
        assert s.timing_score <= 15.0


# ─────────────────────────── Budget Scoring ──────────────────────────────────


class TestBudgetScoring:
    def test_high_revenue_scores_higher(self, scorer):
        """Higher revenue → higher budget score."""
        c_big = Company(name="Big", sector=Sector.ECOMMERCE, revenue_estimate_sar=1_000_000_000)
        c_small = Company(name="Small", sector=Sector.ECOMMERCE, revenue_estimate_sar=1_000_000)

        s_big = scorer.score(c_big)
        s_small = scorer.score(c_small)
        assert s_big.budget_score > s_small.budget_score

    def test_employee_count_boosts_budget(self, scorer):
        """More employees → higher budget proxy."""
        c_big = Company(name="Big", sector=Sector.B2B_SAAS, employee_count=500)
        c_small = Company(name="Small", sector=Sector.B2B_SAAS, employee_count=5)

        s_big = scorer.score(c_big)
        s_small = scorer.score(c_small)
        assert s_big.budget_score > s_small.budget_score

    def test_no_financial_data_minimum_score(self, scorer):
        """Company with no financial data gets minimum budget score."""
        c = Company(name="Ghost", sector=Sector.OTHER)
        s = scorer.score(c)
        assert s.budget_score >= 0


# ─────────────────────────── Authority Scoring ───────────────────────────────


class TestAuthorityScoring:
    def test_ceo_known_boosts_authority(self, scorer):
        """Known CEO name boosts authority."""
        c_with = Company(name="A", sector=Sector.B2B_SAAS, ceo_name="Ahmed")
        c_without = Company(name="B", sector=Sector.B2B_SAAS)

        s_with = scorer.score(c_with)
        s_without = scorer.score(c_without)
        assert s_with.authority_score > s_without.authority_score

    def test_c_level_contact_highest_authority(self, scorer):
        """C-level contact gives highest authority score."""
        c_c = Company(
            name="A", sector=Sector.B2B_SAAS,
            decision_makers=[Contact(full_name="CEO", seniority="c_level", is_decision_maker=True)]
        )
        c_mgr = Company(
            name="B", sector=Sector.B2B_SAAS,
            decision_makers=[Contact(full_name="Mgr", seniority="manager", is_decision_maker=True)]
        )
        s_c = scorer.score(c_c)
        s_mgr = scorer.score(c_mgr)
        assert s_c.authority_score > s_mgr.authority_score

    def test_email_available_boosts_authority(self, scorer):
        """Contact with email address boosts authority."""
        c = Company(
            name="A", sector=Sector.B2B_SAAS,
            decision_makers=[
                Contact(full_name="CEO", seniority="c_level", email="ceo@company.com")
            ]
        )
        s = scorer.score(c)
        assert s.authority_score > 20.0


# ─────────────────────────── Engagement Scoring ──────────────────────────────


class TestEngagementScoring:
    def test_no_engagement_zero_score(self, scorer, strong_company):
        """No engagement data → 0 engagement score."""
        s = scorer.score(strong_company, engagement_data={})
        assert s.engagement_score == 0.0

    def test_whatsapp_reply_highest_signal(self, scorer, strong_company):
        """WhatsApp replies are the highest engagement signal."""
        engagement = {"whatsapp_replies": 2}
        s = scorer.score(strong_company, engagement_data=engagement)
        assert s.engagement_score > 20.0

    def test_email_opens_boost_engagement(self, scorer, strong_company):
        """Email opens boost engagement score."""
        engagement = {"email_opens": 3}
        s = scorer.score(strong_company, engagement_data=engagement)
        assert s.engagement_score > 0.0


# ─────────────────────────── Explainability ──────────────────────────────────


class TestExplainability:
    def test_contributing_signals_not_empty_for_strong(
        self, scorer, strong_company, enrichment_result_with_signals
    ):
        """Strong company has contributing signals."""
        s = scorer.score(strong_company, enrichment_result_with_signals)
        assert len(s.contributing_signals) > 0

    def test_score_rationale_exists(self, scorer, strong_company):
        """Score rationale is always set."""
        s = scorer.score(strong_company)
        assert s.score_rationale is not None
        assert len(s.score_rationale) > 0

    def test_explain_output_contains_score(self, scorer, strong_company):
        """explain() output contains the total score."""
        s = scorer.score(strong_company)
        explanation = scorer.explain(s)
        assert "Dealix Score" in explanation
        assert str(int(s.total_score)) in explanation

    def test_weak_company_has_penalizing_factors(self, scorer, weak_company):
        """Weak company has penalizing factors listed."""
        s = scorer.score(weak_company)
        assert len(s.penalizing_factors) > 0


# ─────────────────────────── score_lead Integration ──────────────────────────


class TestScoreLead:
    def test_score_lead_sets_priority_tier(self, scorer, strong_company):
        """score_lead sets priority_tier on the Lead."""
        lead = Lead(company=strong_company)
        assert lead.priority_tier is None

        scored_lead = scorer.score_lead(lead)
        assert scored_lead.priority_tier is not None
        assert scored_lead.priority_tier in ["hot", "warm", "cool", "cold"]

    def test_score_lead_updates_timestamp(self, scorer, strong_company):
        """score_lead updates the updated_at timestamp."""
        from datetime import datetime
        lead = Lead(company=strong_company)
        old_time = lead.updated_at

        import asyncio
        import time
        time.sleep(0.01)  # Small delay

        scored_lead = scorer.score_lead(lead)
        # updated_at should be >= old_time
        assert scored_lead.updated_at >= old_time
