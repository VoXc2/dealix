"""
Tests for IntelligenceOrchestrator — discover, enrich, run_pipeline.
"""

from __future__ import annotations

import pytest

from app.intelligence import (
    IntelligenceOrchestrator,
    DiscoveryCriteria,
    Sector,
    Region,
    Company,
    Lead,
    LeadStatus,
    SocialHandles,
)


# ─────────────────────────── Fixtures ────────────────────────────────────────


@pytest.fixture
def orchestrator():
    """Orchestrator with no API keys — uses seed data."""
    return IntelligenceOrchestrator()


@pytest.fixture
def sample_company():
    """A sample company for direct enrichment tests."""
    return Company(
        name="Salla",
        name_ar="سلة",
        domain="salla.com",
        sector=Sector.B2B_SAAS,
        region=Region.MAKKAH,
        city="Jeddah",
        employee_count=350,
        revenue_estimate_sar=120_000_000,
        tech_stack=["Laravel", "Vue.js", "AWS"],
        social_handles=SocialHandles(linkedin="company/sallaksa"),
    )


# ─────────────────────────── Initialization ──────────────────────────────────


class TestOrchestratorInit:
    def test_default_init(self, orchestrator):
        """Orchestrator initializes with seed data."""
        assert orchestrator.seed_company_count > 0

    def test_seed_count_matches_known_count(self, orchestrator):
        """Seed should have exactly 30 companies as documented."""
        assert orchestrator.seed_company_count == 30

    def test_from_env_returns_orchestrator(self):
        """from_env() returns an IntelligenceOrchestrator instance."""
        orch = IntelligenceOrchestrator.from_env()
        assert isinstance(orch, IntelligenceOrchestrator)

    def test_get_all_seed_companies(self, orchestrator):
        """get_all_seed_companies returns the full seed list."""
        companies = orchestrator.get_all_seed_companies()
        assert len(companies) == 30
        assert all(isinstance(c, Company) for c in companies)


# ─────────────────────────── Discovery ───────────────────────────────────────


class TestDiscover:
    @pytest.mark.asyncio
    async def test_discover_all(self, orchestrator):
        """Discover without filters returns all seed companies."""
        criteria = DiscoveryCriteria(limit=100)
        companies = await orchestrator.discover(criteria)
        assert len(companies) > 0
        assert all(isinstance(c, Company) for c in companies)

    @pytest.mark.asyncio
    async def test_discover_by_sector(self, orchestrator):
        """Discover filters by sector correctly."""
        criteria = DiscoveryCriteria(sectors=[Sector.B2B_SAAS], limit=50)
        companies = await orchestrator.discover(criteria)
        assert len(companies) > 0
        assert all(c.sector == Sector.B2B_SAAS for c in companies)

    @pytest.mark.asyncio
    async def test_discover_by_region(self, orchestrator):
        """Discover filters by region correctly."""
        criteria = DiscoveryCriteria(regions=[Region.RIYADH], limit=50)
        companies = await orchestrator.discover(criteria)
        assert len(companies) > 0
        assert all(c.region == Region.RIYADH for c in companies)

    @pytest.mark.asyncio
    async def test_discover_by_employee_count(self, orchestrator):
        """Discover filters by min_employees correctly."""
        criteria = DiscoveryCriteria(min_employees=1000, limit=50)
        companies = await orchestrator.discover(criteria)
        assert all(
            c.employee_count is not None and c.employee_count >= 1000
            for c in companies
        )

    @pytest.mark.asyncio
    async def test_discover_limit_respected(self, orchestrator):
        """Discover respects the limit parameter."""
        criteria = DiscoveryCriteria(limit=3)
        companies = await orchestrator.discover(criteria)
        assert len(companies) <= 3

    @pytest.mark.asyncio
    async def test_discover_empty_result(self, orchestrator):
        """Discover with impossible criteria returns empty list."""
        criteria = DiscoveryCriteria(
            sectors=[Sector.ECOMMERCE],
            min_employees=999999,  # No company has this many
            limit=10,
        )
        companies = await orchestrator.discover(criteria)
        assert companies == []

    @pytest.mark.asyncio
    async def test_discover_by_keyword(self, orchestrator):
        """Discover filters by keyword in company name."""
        criteria = DiscoveryCriteria(keywords=["Salla"], limit=10)
        companies = await orchestrator.discover(criteria)
        assert len(companies) >= 1
        assert any("Salla" in c.name for c in companies)


# ─────────────────────────── Enrich ──────────────────────────────────────────


class TestEnrich:
    @pytest.mark.asyncio
    async def test_enrich_returns_lead(self, orchestrator, sample_company):
        """enrich() returns a Lead object."""
        lead = await orchestrator.enrich(sample_company)
        assert isinstance(lead, Lead)

    @pytest.mark.asyncio
    async def test_enrich_scores_company(self, orchestrator, sample_company):
        """enrich() produces a non-zero score."""
        lead = await orchestrator.enrich(sample_company)
        assert lead.dealix_score > 0

    @pytest.mark.asyncio
    async def test_enrich_sets_priority_tier(self, orchestrator, sample_company):
        """enrich() sets priority_tier."""
        lead = await orchestrator.enrich(sample_company)
        assert lead.priority_tier in ["hot", "warm", "cool", "cold"]

    @pytest.mark.asyncio
    async def test_enrich_marks_company_enriched(self, orchestrator, sample_company):
        """enrich() marks the company as enriched."""
        lead = await orchestrator.enrich(sample_company)
        assert lead.company.enriched is True

    @pytest.mark.asyncio
    async def test_enrich_company_without_tech(self, orchestrator):
        """Enrich works even with minimal company data."""
        c = Company(name="Minimal Co", sector=Sector.OTHER)
        lead = await orchestrator.enrich(c)
        assert isinstance(lead, Lead)
        assert 0 <= lead.dealix_score <= 100


# ─────────────────────────── run_pipeline ────────────────────────────────────


class TestRunPipeline:
    @pytest.mark.asyncio
    async def test_pipeline_returns_leads(self, orchestrator):
        """run_pipeline() returns a non-empty list of leads."""
        criteria = DiscoveryCriteria(limit=5)
        leads = await orchestrator.run_pipeline(criteria)
        assert len(leads) > 0
        assert all(isinstance(l, Lead) for l in leads)

    @pytest.mark.asyncio
    async def test_pipeline_sorted_by_score(self, orchestrator):
        """run_pipeline() returns leads sorted by score descending."""
        criteria = DiscoveryCriteria(limit=10)
        leads = await orchestrator.run_pipeline(criteria, sort_by_score=True)
        scores = [l.dealix_score for l in leads]
        assert scores == sorted(scores, reverse=True)

    @pytest.mark.asyncio
    async def test_pipeline_min_score_filter(self, orchestrator):
        """run_pipeline() respects min_score filter."""
        criteria = DiscoveryCriteria(limit=20)
        leads = await orchestrator.run_pipeline(criteria, min_score=50.0)
        for lead in leads:
            assert lead.dealix_score >= 50.0

    @pytest.mark.asyncio
    async def test_pipeline_all_have_priority_tier(self, orchestrator):
        """All pipeline leads have a priority_tier set."""
        criteria = DiscoveryCriteria(limit=5)
        leads = await orchestrator.run_pipeline(criteria)
        for lead in leads:
            assert lead.priority_tier is not None

    @pytest.mark.asyncio
    async def test_pipeline_saas_focus(self, orchestrator):
        """Pipeline with SaaS sector focus only returns SaaS companies."""
        criteria = DiscoveryCriteria(sectors=[Sector.B2B_SAAS], limit=10)
        leads = await orchestrator.run_pipeline(criteria)
        for lead in leads:
            assert lead.company.sector == Sector.B2B_SAAS


# ─────────────────────────── enrich_companies ────────────────────────────────


class TestEnrichCompanies:
    @pytest.mark.asyncio
    async def test_enrich_multiple_companies(self, orchestrator):
        """enrich_companies() handles a batch correctly."""
        companies = [
            Company(name="Co A", sector=Sector.ECOMMERCE, employee_count=100),
            Company(name="Co B", sector=Sector.B2B_SAAS, employee_count=200),
            Company(name="Co C", sector=Sector.REAL_ESTATE, employee_count=500),
        ]
        leads = await orchestrator.enrich_companies(companies)
        assert len(leads) == 3
        assert all(isinstance(l, Lead) for l in leads)

    @pytest.mark.asyncio
    async def test_enrich_companies_sorted(self, orchestrator):
        """enrich_companies() returns results sorted by score."""
        companies = [
            Company(name="Tiny Co", sector=Sector.OTHER, employee_count=2),
            Company(
                name="Strong Co",
                sector=Sector.ECOMMERCE,
                employee_count=200,
                revenue_estimate_sar=500_000_000,
                tech_stack=["AWS", "Salesforce"],
                social_handles=SocialHandles(linkedin="company/strong"),
            ),
        ]
        leads = await orchestrator.enrich_companies(companies)
        scores = [l.dealix_score for l in leads]
        assert scores == sorted(scores, reverse=True)


# ─────────────────────────── Stats & Utils ───────────────────────────────────


class TestStats:
    @pytest.mark.asyncio
    async def test_stats_updated_after_pipeline(self, orchestrator):
        """Stats counter pipeline_runs increments after each run."""
        before = orchestrator.get_stats()["pipeline_runs"]
        criteria = DiscoveryCriteria(limit=3)
        await orchestrator.run_pipeline(criteria)
        after = orchestrator.get_stats()["pipeline_runs"]
        assert after == before + 1

    def test_explain_lead(self, orchestrator):
        """explain_lead() returns a non-empty string."""
        from app.intelligence.models import ScoreBreakdown
        c = Company(name="Test", sector=Sector.B2B_SAAS)
        sb = ScoreBreakdown(total_score=72.5, icp_score=80.0, intent_score=70.0)
        lead = Lead(company=c, score=sb)
        lead.set_priority_tier()

        explanation = orchestrator.explain_lead(lead)
        assert len(explanation) > 0
        assert "Dealix Score" in explanation
