"""
Tests for Intelligence Engine data models (Pydantic v2).
Arabic-friendly encoding and field validation tests included.
"""

from __future__ import annotations

import pytest
from datetime import datetime

from app.intelligence.models import (
    Company,
    Contact,
    DiscoveryCriteria,
    EstablishmentType,
    FundingEvent,
    HiringSignal,
    Lead,
    LeadStatus,
    NewsEvent,
    Region,
    ScoreBreakdown,
    Sector,
    Signal,
    SignalType,
    SocialHandles,
    TenderWin,
)


# ─────────────────────────── Company Model ────────────────────────────────────


class TestCompanyModel:
    def test_minimal_company(self):
        """Company can be created with just a name."""
        c = Company(name="Test Company")
        assert c.name == "Test Company"
        assert c.sector == Sector.OTHER
        assert c.decision_makers == []
        assert c.tech_stack == []
        assert c.signals == []

    def test_arabic_fields(self):
        """Arabic strings are stored correctly (Unicode)."""
        c = Company(
            name="Salla",
            name_ar="سلة",
            city_ar="جدة",
        )
        assert c.name_ar == "سلة"
        assert c.city_ar == "جدة"

    def test_full_company(self):
        """Full company with all fields."""
        c = Company(
            name="Foodics",
            name_ar="فودكس",
            domain="foodics.com",
            sector=Sector.B2B_SAAS,
            region=Region.RIYADH,
            city="Riyadh",
            employee_count=400,
            revenue_estimate_sar=150_000_000,
            tech_stack=["React", "Ruby on Rails", "PostgreSQL"],
            social_handles=SocialHandles(linkedin="company/foodics"),
        )
        assert c.sector == Sector.B2B_SAAS
        assert c.region == Region.RIYADH
        assert len(c.tech_stack) == 3
        assert c.social_handles.linkedin == "company/foodics"

    def test_company_id_auto_generated(self):
        """ID is auto-generated as UUID."""
        c1 = Company(name="A")
        c2 = Company(name="B")
        assert c1.id != c2.id
        assert len(c1.id) == 36  # UUID format

    def test_enriched_flag(self):
        """Enriched flag starts False."""
        c = Company(name="Test")
        assert c.enriched is False

    def test_json_serialization_with_arabic(self):
        """Serialization preserves Arabic characters."""
        c = Company(name="Test", name_ar="اختبار")
        j = c.model_dump_json()
        assert "اختبار" in j


# ─────────────────────────── Contact Model ────────────────────────────────────


class TestContactModel:
    def test_phone_normalization_saudi(self):
        """Saudi mobile numbers starting with 05 are normalized to +966prefix."""
        contact = Contact(full_name="Ahmed", phone="0501234567")
        # 0501234567 → remove leading 0, prepend +966 → +966501234567
        assert contact.phone == "+966501234567"

    def test_phone_normalization_already_e164(self):
        """E.164 phones are passed through unchanged."""
        contact = Contact(full_name="Ahmed", phone="+966501234567")
        assert contact.phone == "+966501234567"

    def test_phone_none(self):
        """None phone is allowed."""
        contact = Contact(full_name="Ahmed", phone=None)
        assert contact.phone is None

    def test_decision_maker_flag(self):
        """Decision maker flag defaults to False."""
        contact = Contact(full_name="Manager")
        assert contact.is_decision_maker is False

    def test_arabic_name(self):
        """Arabic name stored correctly."""
        contact = Contact(
            full_name="Hosam Arab",
            full_name_ar="حسام عرب",
            title="CEO",
        )
        assert contact.full_name_ar == "حسام عرب"


# ─────────────────────────── Signal Model ─────────────────────────────────────


class TestSignalModel:
    def test_score_contribution_bounds(self):
        """Score contribution must be 0-100."""
        signal = Signal(
            signal_type=SignalType.FUNDING,
            title="Test",
            score_contribution=50.0,
        )
        assert signal.score_contribution == 50.0

    def test_score_contribution_too_high_rejected(self):
        """Score contribution > 100 is rejected."""
        with pytest.raises(Exception):
            Signal(
                signal_type=SignalType.FUNDING,
                title="Test",
                score_contribution=150.0,  # Invalid
            )

    def test_signal_id_auto_generated(self):
        """Signal ID is auto-generated."""
        s1 = Signal(signal_type=SignalType.HIRING, title="Job A")
        s2 = Signal(signal_type=SignalType.HIRING, title="Job B")
        assert s1.id != s2.id

    def test_all_signal_types(self):
        """All SignalType values are valid."""
        for stype in SignalType:
            s = Signal(signal_type=stype, title=f"Signal {stype.value}")
            assert s.signal_type == stype


# ─────────────────────────── ScoreBreakdown Model ─────────────────────────────


class TestScoreBreakdownModel:
    def test_default_scores_zero(self):
        """All scores default to 0."""
        sb = ScoreBreakdown()
        assert sb.total_score == 0.0
        assert sb.icp_score == 0.0
        assert sb.intent_score == 0.0

    def test_score_bounds(self):
        """Scores must be 0-100."""
        with pytest.raises(Exception):
            ScoreBreakdown(total_score=101.0)

    def test_full_breakdown(self):
        """Full breakdown with all fields."""
        sb = ScoreBreakdown(
            icp_score=80.0,
            intent_score=70.0,
            timing_score=60.0,
            budget_score=75.0,
            authority_score=85.0,
            engagement_score=20.0,
            total_score=72.5,
            contributing_signals=["Signal A", "Signal B"],
            penalizing_factors=["No engagement"],
            score_rationale="Strong ICP and Intent.",
        )
        assert sb.icp_score == 80.0
        assert len(sb.contributing_signals) == 2


# ─────────────────────────── Lead Model ──────────────────────────────────────


class TestLeadModel:
    def test_lead_defaults(self):
        """Lead defaults are correct."""
        c = Company(name="Test")
        lead = Lead(company=c)
        assert lead.status == LeadStatus.NEW
        assert lead.outreach_attempts == 0
        assert lead.priority_tier is None

    def test_set_priority_tier_hot(self):
        """Score >= 80 → hot."""
        c = Company(name="Test")
        sb = ScoreBreakdown(total_score=85.0)
        lead = Lead(company=c, score=sb)
        lead.set_priority_tier()
        assert lead.priority_tier == "hot"

    def test_set_priority_tier_warm(self):
        """Score 60-79 → warm."""
        c = Company(name="Test")
        sb = ScoreBreakdown(total_score=65.0)
        lead = Lead(company=c, score=sb)
        lead.set_priority_tier()
        assert lead.priority_tier == "warm"

    def test_set_priority_tier_cool(self):
        """Score 40-59 → cool."""
        c = Company(name="Test")
        sb = ScoreBreakdown(total_score=50.0)
        lead = Lead(company=c, score=sb)
        lead.set_priority_tier()
        assert lead.priority_tier == "cool"

    def test_set_priority_tier_cold(self):
        """Score < 40 → cold."""
        c = Company(name="Test")
        sb = ScoreBreakdown(total_score=25.0)
        lead = Lead(company=c, score=sb)
        lead.set_priority_tier()
        assert lead.priority_tier == "cold"

    def test_dealix_score_property(self):
        """dealix_score property returns total_score."""
        c = Company(name="Test")
        sb = ScoreBreakdown(total_score=72.3)
        lead = Lead(company=c, score=sb)
        assert lead.dealix_score == 72.3


# ─────────────────────────── DiscoveryCriteria ───────────────────────────────


class TestDiscoveryCriteria:
    def test_default_criteria(self):
        """Default criteria has no filters."""
        c = DiscoveryCriteria()
        assert c.sectors == []
        assert c.regions == []
        assert c.limit == 50

    def test_limit_bounds(self):
        """Limit must be 1-500."""
        with pytest.raises(Exception):
            DiscoveryCriteria(limit=0)

        with pytest.raises(Exception):
            DiscoveryCriteria(limit=501)

    def test_sector_filter(self):
        """Sectors list is stored."""
        c = DiscoveryCriteria(sectors=[Sector.ECOMMERCE, Sector.B2B_SAAS])
        assert Sector.ECOMMERCE in c.sectors
        assert len(c.sectors) == 2


# ─────────────────────────── FundingEvent ─────────────────────────────────────


class TestFundingEvent:
    def test_funding_event(self):
        """FundingEvent with all fields."""
        fe = FundingEvent(
            round_type="Series A",
            amount_usd=10_000_000,
            amount_sar=37_500_000,
            investors=["STV", "Sanabil"],
            announced_at=datetime(2024, 1, 1),
        )
        assert fe.round_type == "Series A"
        assert fe.amount_usd == 10_000_000
        assert len(fe.investors) == 2


# ─────────────────────────── TenderWin ────────────────────────────────────────


class TestTenderWin:
    def test_tender_win_arabic(self):
        """TenderWin with Arabic title."""
        tw = TenderWin(
            title_ar="تطوير بوابة الخدمات الحكومية",
            entity="وزارة الداخلية",
            value_sar=45_000_000,
        )
        assert tw.title_ar == "تطوير بوابة الخدمات الحكومية"
        assert tw.entity == "وزارة الداخلية"
        assert tw.value_sar == 45_000_000
