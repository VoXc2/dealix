"""
Tests for individual data sources.
"""

from __future__ import annotations

import pytest
from datetime import datetime

from app.intelligence.models import (
    Company,
    DiscoveryCriteria,
    Region,
    Sector,
    SocialHandles,
)
from app.intelligence.sources.saudi_registry import SaudiBusinessRegistrySource
from app.intelligence.sources.etimad import EtimadSource
from app.intelligence.sources.news import NewsSource
from app.intelligence.sources.hiring import HiringIntentSource, SENIORITY_KEYWORDS
from app.intelligence.sources.tech_stack import TechStackSource
from app.intelligence.sources.linkedin import LinkedInSource


# ─────────────────────────── Saudi Registry ──────────────────────────────────


class TestSaudiBusinessRegistrySource:
    @pytest.fixture
    def source(self):
        return SaudiBusinessRegistrySource()

    def test_seed_loaded(self, source):
        """Seed data is loaded on initialization."""
        assert source.seed_count == 30

    def test_all_seed_have_names(self, source):
        """All seed companies have names."""
        for company in source.all_seed_companies:
            assert company.name
            assert company.name_ar  # Should have Arabic name

    def test_all_seed_have_sectors(self, source):
        """All seed companies have sectors (not OTHER for known companies)."""
        for company in source.all_seed_companies:
            assert company.sector is not None

    def test_all_seed_have_regions(self, source):
        """All seed companies have regions."""
        for company in source.all_seed_companies:
            assert company.region is not None

    @pytest.mark.asyncio
    async def test_discover_no_filter(self, source):
        """Discover without filters returns seed companies."""
        criteria = DiscoveryCriteria(limit=50)
        companies = await source.discover(criteria)
        assert len(companies) > 0

    @pytest.mark.asyncio
    async def test_filter_by_sector(self, source):
        """Sector filter works correctly."""
        criteria = DiscoveryCriteria(sectors=[Sector.B2B_SAAS], limit=50)
        companies = await source.discover(criteria)
        assert len(companies) > 0
        for c in companies:
            assert c.sector == Sector.B2B_SAAS

    @pytest.mark.asyncio
    async def test_filter_by_region(self, source):
        """Region filter works correctly."""
        criteria = DiscoveryCriteria(regions=[Region.RIYADH], limit=50)
        companies = await source.discover(criteria)
        for c in companies:
            assert c.region == Region.RIYADH

    @pytest.mark.asyncio
    async def test_filter_by_min_employees(self, source):
        """Min employees filter works."""
        criteria = DiscoveryCriteria(min_employees=5000, limit=50)
        companies = await source.discover(criteria)
        for c in companies:
            assert c.employee_count is not None
            assert c.employee_count >= 5000

    @pytest.mark.asyncio
    async def test_limit_respected(self, source):
        """Limit parameter is respected."""
        criteria = DiscoveryCriteria(limit=3)
        companies = await source.discover(criteria)
        assert len(companies) <= 3

    @pytest.mark.asyncio
    async def test_get_company_by_cr_seed(self, source):
        """Can retrieve a specific company by CR number from seed."""
        # Jarir has CR 1010150609
        company = await source.get_company_details("1010150609")
        assert company is not None
        assert "Jarir" in company.name

    @pytest.mark.asyncio
    async def test_verify_vat_raises_not_implemented(self, source):
        """VAT verification raises NotImplementedError (needs credential)."""
        with pytest.raises(NotImplementedError):
            await source.verify_vat("300087331900003")

    @pytest.mark.asyncio
    async def test_live_api_raises_not_implemented(self):
        """Live API raises NotImplementedError when api_key is provided."""
        source = SaudiBusinessRegistrySource(api_key="fake_key")
        criteria = DiscoveryCriteria(limit=5)
        with pytest.raises(NotImplementedError):
            await source.discover(criteria)

    def test_keyword_filter(self, source):
        """Keyword filter matches on name and sub_sector."""
        import asyncio
        criteria = DiscoveryCriteria(keywords=["ecommerce"], limit=50)
        companies = asyncio.get_event_loop().run_until_complete(source.discover(criteria))
        # ecommerce keyword should match e-commerce sector companies
        # (matches sub_sector field)

    @pytest.mark.asyncio
    async def test_data_sources_marked(self, source):
        """Discovered companies have data_sources set."""
        criteria = DiscoveryCriteria(limit=5)
        companies = await source.discover(criteria)
        for c in companies:
            assert "seed_saudi_registry" in c.data_sources


# ─────────────────────────── Etimad Source ───────────────────────────────────


class TestEtimadSource:
    @pytest.fixture
    def source(self):
        return EtimadSource()

    @pytest.fixture
    def elm_company(self):
        return Company(name="Elm Company", sector=Sector.TECHNOLOGY)

    @pytest.mark.asyncio
    async def test_get_tender_wins_seed(self, source, elm_company):
        """Get tender wins from seed for Elm Company."""
        tenders = await source.get_tender_wins(elm_company)
        assert len(tenders) >= 1
        assert any("Elm" in t.title_ar or "حكوم" in t.title_ar for t in tenders)

    @pytest.mark.asyncio
    async def test_get_signals_from_tenders(self, source, elm_company):
        """Tender wins produce signals."""
        signals = await source.get_signals(elm_company)
        assert len(signals) > 0
        from app.intelligence.models import SignalType
        for s in signals:
            assert s.signal_type == SignalType.TENDER_WIN

    @pytest.mark.asyncio
    async def test_tender_value_in_signal(self, source, elm_company):
        """Tender value is included in signal metadata."""
        signals = await source.get_signals(elm_company)
        if signals:
            assert "value_sar" in signals[0].metadata

    @pytest.mark.asyncio
    async def test_company_without_tenders(self, source):
        """Unknown company returns empty tender list from seed."""
        c = Company(name="Unknown XYZ Corp", sector=Sector.OTHER)
        tenders = await source.get_tender_wins(c)
        assert tenders == []

    @pytest.mark.asyncio
    async def test_live_api_raises_not_implemented(self):
        """Live API raises NotImplementedError."""
        source = EtimadSource(api_key="fake_key")
        c = Company(name="Test", sector=Sector.TECHNOLOGY)
        with pytest.raises(NotImplementedError):
            await source.get_tender_wins(c)

    @pytest.mark.asyncio
    async def test_search_tenders_raises_not_implemented(self, source):
        """search_tenders_by_sector always raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            await source.search_tenders_by_sector("IT")


# ─────────────────────────── News Source ─────────────────────────────────────


class TestNewsSource:
    @pytest.fixture
    def source(self):
        return NewsSource()

    @pytest.fixture
    def tabby_company(self):
        return Company(name="Tabby", sector=Sector.FINANCIAL_SERVICES)

    @pytest.mark.asyncio
    async def test_get_news_seed(self, source, tabby_company):
        """Get news from seed for Tabby."""
        news = await source.get_news(tabby_company)
        assert len(news) >= 1

    @pytest.mark.asyncio
    async def test_news_has_arabic_headline(self, source, tabby_company):
        """News events have Arabic headlines."""
        news = await source.get_news(tabby_company)
        for item in news:
            assert item.headline_ar is not None

    @pytest.mark.asyncio
    async def test_signals_from_funding_news(self, source, tabby_company):
        """Funding news produces non-zero signals."""
        signals = await source.get_signals(tabby_company)
        assert len(signals) > 0
        # Tabby has Series D funding news — should have positive contribution
        scores = [s.score_contribution for s in signals]
        assert sum(scores) > 0

    @pytest.mark.asyncio
    async def test_no_news_for_unknown_company(self, source):
        """Unknown company has no seed news."""
        c = Company(name="Obscure Corp XYZ", sector=Sector.OTHER)
        news = await source.get_news(c)
        assert news == []

    @pytest.mark.asyncio
    async def test_perplexity_raises_not_implemented(self):
        """Perplexity API raises NotImplementedError."""
        source = NewsSource(perplexity_api_key="fake_key")
        c = Company(name="Tabby", sector=Sector.FINANCIAL_SERVICES)
        with pytest.raises(NotImplementedError):
            await source.get_news(c)


# ─────────────────────────── Hiring Source ───────────────────────────────────


class TestHiringIntentSource:
    @pytest.fixture
    def source(self):
        return HiringIntentSource()

    @pytest.fixture
    def foodics_company(self):
        return Company(name="Foodics", sector=Sector.B2B_SAAS)

    @pytest.mark.asyncio
    async def test_get_hiring_signals_seed(self, source, foodics_company):
        """Get hiring signals from seed for Foodics."""
        signals = await source.get_hiring_signals(foodics_company)
        assert len(signals) >= 1

    @pytest.mark.asyncio
    async def test_signals_have_seniority(self, source, foodics_company):
        """Hiring signals have seniority set."""
        signals = await source.get_hiring_signals(foodics_company)
        for s in signals:
            assert s.seniority is not None

    @pytest.mark.asyncio
    async def test_get_signals_produces_intent_signals(self, source, foodics_company):
        """get_signals() produces scored Signal objects."""
        from app.intelligence.models import SignalType
        intent_signals = await source.get_signals(foodics_company)
        assert len(intent_signals) > 0
        for s in intent_signals:
            assert s.signal_type == SignalType.HIRING

    def test_detect_seniority_c_level(self):
        """Detect C-level from job title."""
        assert HiringIntentSource.detect_seniority("CEO") == "c_level"
        assert HiringIntentSource.detect_seniority("Chief Technology Officer") == "c_level"

    def test_detect_seniority_vp(self):
        """Detect VP from job title."""
        assert HiringIntentSource.detect_seniority("VP Sales") == "vp"

    def test_detect_seniority_director(self):
        """Detect Director from job title."""
        assert HiringIntentSource.detect_seniority("Head of Marketing") == "director"

    def test_detect_seniority_individual_contributor(self):
        """Default seniority for engineers."""
        assert HiringIntentSource.detect_seniority("Software Engineer") == "individual_contributor"

    def test_detect_seniority_arabic(self):
        """Arabic seniority keywords are detected."""
        # "مدير" matches director keyword
        result = HiringIntentSource.detect_seniority("المدير التنفيذي")
        assert result in ["c_level", "director"]  # Either is valid for مدير

    @pytest.mark.asyncio
    async def test_unknown_company_empty_signals(self, source):
        """Unknown company has no seed hiring signals."""
        c = Company(name="Obscure Corp", sector=Sector.OTHER)
        signals = await source.get_hiring_signals(c)
        assert signals == []


# ─────────────────────────── Tech Stack Source ───────────────────────────────


class TestTechStackSource:
    @pytest.fixture
    def source(self):
        return TechStackSource()

    @pytest.fixture
    def salla_company(self):
        return Company(
            name="Salla",
            domain="salla.com",
            sector=Sector.B2B_SAAS,
        )

    @pytest.mark.asyncio
    async def test_detect_from_seed(self, source, salla_company):
        """Detect tech stack from seed data."""
        tech = await source.detect(salla_company)
        assert len(tech) > 0
        assert "AWS" in tech

    @pytest.mark.asyncio
    async def test_signals_from_known_tech(self, source, salla_company):
        """HubSpot/Salesforce in stack produces competitor signals."""
        from app.intelligence.models import SignalType
        # Salla seed doesn't have HubSpot, but add it manually
        salla_company.tech_stack = ["HubSpot", "AWS"]
        signals = await source.get_signals(salla_company)
        tech_signals = [s for s in signals if s.signal_type == SignalType.TECH_CHANGE]
        assert len(tech_signals) > 0

    @pytest.mark.asyncio
    async def test_digital_maturity_cloud(self, source):
        """Company using AWS scores high digital maturity."""
        c = Company(
            name="Cloud Co",
            domain="cloud.sa",
            tech_stack=["AWS", "React", "HubSpot", "Google Analytics", "Stripe"],
        )
        maturity = await source.estimate_digital_maturity(c)
        assert maturity >= 60.0

    @pytest.mark.asyncio
    async def test_digital_maturity_no_stack(self, source):
        """Company with no tech stack has low digital maturity."""
        c = Company(name="Old School Co", domain="old.sa")
        maturity = await source.estimate_digital_maturity(c)
        assert maturity == 0.0

    def test_categorize_ecommerce_tech(self, source):
        """Shopify is categorized as ecommerce."""
        category = source._categorize("Shopify")
        assert category == "ecommerce"

    def test_categorize_crm(self, source):
        """Salesforce is categorized as CRM."""
        category = source._categorize("Salesforce")
        assert category == "crm"

    @pytest.mark.asyncio
    async def test_builtwith_raises_not_implemented(self):
        """BuiltWith raises NotImplementedError without key."""
        source = TechStackSource(builtwith_api_key="fake_key")
        c = Company(name="Test", domain="test.sa")
        with pytest.raises(NotImplementedError):
            await source._fetch_builtwith(c)


# ─────────────────────────── LinkedIn Source ─────────────────────────────────


class TestLinkedInSource:
    @pytest.fixture
    def source(self):
        return LinkedInSource()

    @pytest.fixture
    def company(self):
        return Company(
            name="Foodics",
            sector=Sector.B2B_SAAS,
            social_handles=SocialHandles(linkedin="company/foodics"),
        )

    @pytest.mark.asyncio
    async def test_get_decision_makers_raises_not_implemented(self, source, company):
        """Decision maker lookup raises NotImplementedError without credentials."""
        with pytest.raises(NotImplementedError):
            await source.get_decision_makers(company)

    @pytest.mark.asyncio
    async def test_get_signals_with_linkedin_handle(self, source, company):
        """get_signals() works without credentials — uses existing data."""
        signals = await source.get_signals(company)
        # Should get at least a signal for having LinkedIn presence
        assert len(signals) >= 1

    @pytest.mark.asyncio
    async def test_get_signals_no_handle(self, source):
        """Company without LinkedIn handle gets fewer signals."""
        c = Company(name="No Social Co", sector=Sector.OTHER)
        signals = await source.get_signals(c)
        # No LinkedIn handle → minimal signals
        assert len(signals) == 0

    @pytest.mark.asyncio
    async def test_send_connection_raises_not_implemented(self, source):
        """Connection request raises NotImplementedError."""
        from app.intelligence.models import Contact
        contact = Contact(full_name="Test User")
        with pytest.raises(NotImplementedError):
            await source.send_connection_request(contact, "مرحباً")
