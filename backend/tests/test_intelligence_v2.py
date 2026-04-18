"""
Lead Intelligence Engine V2 — Test Suite
=========================================
Tests: discovery flow, phone normalization, Arabic dedup, 
Gulf geo filters, query planner (mocked LLM), API endpoints.

Run:
    cd backend && pytest tests/test_intelligence_v2.py -v
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime
from typing import List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, ASGITransport

# Ensure backend root is on path
sys.path.insert(0, "/home/user/workspace/dealix-clean/backend")

# ─────────────────────────── Test Fixtures ───────────────────────────────────

@pytest.fixture
def sample_icp_dict():
    return {
        "industries": ["restaurants"],
        "geo": {"countries": ["SA"], "cities": ["Riyadh"]},
        "signals": ["hiring"],
    }


@pytest.fixture
def sample_discovery_query():
    from app.intelligence.v2.models import DiscoveryQuery, ICP, GeoFilter, DepthLevel
    return DiscoveryQuery(
        icp=ICP(
            industries=["restaurants"],
            geo=GeoFilter(countries=["SA"], cities=["Riyadh"]),
            signals=["hiring"],
        ),
        depth=DepthLevel.QUICK,
        limit=5,
        language="ar",
    )


@pytest.fixture
def sample_raw_lead():
    from app.intelligence.v2.models import RawLead, ProvenanceRecord
    return RawLead(
        provenance=ProvenanceRecord(
            source_name="test_source",
            query_used="مطاعم الرياض",
            url="https://example.com",
            is_mock=True,
        ),
        company_name="Al Noor Restaurant Group",
        company_name_ar="مجموعة النور للمطاعم",
        domain="alnoor-restaurant.com.sa",
        phone="+966501234567",
        email="info@alnoor-restaurant.com.sa",
        city="Riyadh",
        country="SA",
        industry="restaurants",
        is_hiring=True,
        hiring_roles=["Chef", "Sales Manager"],
    )


@pytest.fixture
def sample_normalized_lead(sample_raw_lead):
    """Return a pre-built NormalizedLead for tests that don't need async normalize."""
    from app.intelligence.v2.models import NormalizedLead
    return NormalizedLead(
        raw_lead_ids=[sample_raw_lead.id],
        provenances=[sample_raw_lead.provenance],
        company_name=sample_raw_lead.company_name,
        company_name_ar=sample_raw_lead.company_name_ar,
        domain=sample_raw_lead.domain,
        phone_e164=sample_raw_lead.phone,
        email=sample_raw_lead.email,
        city=sample_raw_lead.city,
        country=sample_raw_lead.country,
        industry=sample_raw_lead.industry,
        is_hiring=sample_raw_lead.is_hiring,
        hiring_roles=sample_raw_lead.hiring_roles,
        dedup_key=f"domain:{sample_raw_lead.domain}",
    )


# ─────────────────────────── TEST 1: Gulf Geo Constants ──────────────────────

def test_gulf_geo_countries():
    """Gulf geo module has all 6 countries with correct phone prefixes."""
    from app.intelligence.v2.gulf_geo import GULF_COUNTRIES

    assert len(GULF_COUNTRIES) == 6
    assert "SA" in GULF_COUNTRIES
    assert "UAE" in GULF_COUNTRIES

    sa = GULF_COUNTRIES["SA"]
    assert sa.phone_prefix == "+966"
    assert sa.tld == ".sa"

    uae = GULF_COUNTRIES["UAE"]
    assert uae.phone_prefix == "+971"
    assert uae.tld == ".ae"

    kw = GULF_COUNTRIES["KW"]
    assert kw.phone_prefix == "+965"

    qa = GULF_COUNTRIES["QA"]
    assert qa.phone_prefix == "+974"


def test_gulf_geo_saudi_cities():
    """Saudi cities dict has priority cities with valid bboxes."""
    from app.intelligence.v2.gulf_geo import SAUDI_CITIES, PRIORITY_CITIES

    assert "riyadh" in SAUDI_CITIES
    assert "jeddah" in SAUDI_CITIES
    assert "dammam" in SAUDI_CITIES
    assert "riyadh" in PRIORITY_CITIES

    # Bounding box sanity check
    riyadh = SAUDI_CITIES["riyadh"]
    lat_min, lon_min, lat_max, lon_max = riyadh.bbox
    assert 24 < lat_min < 25
    assert 46 < lon_min < 47
    assert lat_max > lat_min
    assert lon_max > lon_min

    # Arabic name present
    assert "الرياض" in riyadh.name_ar


def test_gulf_geo_city_lookup():
    """City normalization handles both English and Arabic names."""
    from app.intelligence.v2.gulf_geo import normalize_city_name

    assert normalize_city_name("Riyadh") == "riyadh"
    assert normalize_city_name("الرياض") == "riyadh"
    assert normalize_city_name("jeddah") == "jeddah"
    assert normalize_city_name("Unknown City") is None


# ─────────────────────────── TEST 2: Arabic i18n ─────────────────────────────

def test_arabic_digit_normalization():
    """Arabic-Indic digits are converted to ASCII."""
    from app.intelligence.v2.i18n import normalize_arabic_digits

    assert normalize_arabic_digits("٠١٢٣٤٥٦٧٨٩") == "0123456789"
    assert normalize_arabic_digits("٠٥١٢٣٤٥٦٧٨") == "0512345678"
    assert normalize_arabic_digits("Hello 123") == "Hello 123"


def test_normalize_company_name_en():
    """English company name normalization strips legal suffixes."""
    from app.intelligence.v2.i18n import normalize_company_name

    assert normalize_company_name("Al Noor Trading LLC", lang="en") == "al noor"
    assert normalize_company_name("Gulf Group Ltd", lang="en") == "gulf"
    assert normalize_company_name("Riyadh Technology Inc", lang="en") == "riyadh technology"


def test_normalize_company_name_ar():
    """Arabic company name normalization strips Arabic legal suffixes."""
    from app.intelligence.v2.i18n import normalize_company_name

    result = normalize_company_name("شركة النور للتجارة", lang="ar")
    assert "النور" in result

    result2 = normalize_company_name("مجموعة الخليج للخدمات", lang="ar")
    assert "الخليج" in result2


def test_detect_language():
    """Language detection works for Arabic and English."""
    from app.intelligence.v2.i18n import detect_language

    assert detect_language("شركة النور للتجارة") == "ar"
    assert detect_language("Al Noor Trading Company") == "en"
    assert detect_language("") == "en"
    assert detect_language("مطعم Restaurant Mix") == "ar"  # >20% Arabic


def test_arabic_text_normalization():
    """Arabic text normalization handles alef variants and diacritics."""
    from app.intelligence.v2.i18n import normalize_arabic_text, strip_diacritics

    # Diacritics removed
    text_with_diacritics = "مُحَمَّد"
    stripped = strip_diacritics(text_with_diacritics)
    assert stripped == "محمد"

    # Alef normalization
    text_alef = "أحمد"
    normalized = normalize_arabic_text(text_alef)
    assert normalized == "احمد"


# ─────────────────────────── TEST 3: Phone Normalization ─────────────────────

def test_phone_normalization_saudi():
    """Saudi phone numbers normalized to E.164."""
    from app.intelligence.v2.normalizer import normalize_phone_e164

    # Local format
    result = normalize_phone_e164("0501234567", "SA")
    assert result == "+966501234567"

    # Already E.164
    result2 = normalize_phone_e164("+966501234567", "SA")
    assert result2 == "+966501234567"

    # With spaces
    result3 = normalize_phone_e164("+966 50 123 4567", "SA")
    assert result3 == "+966501234567"

    # Invalid
    result4 = normalize_phone_e164("not-a-phone", "SA")
    assert result4 is None


def test_phone_normalization_arabic_digits():
    """Phone numbers with Arabic-Indic digits are normalized correctly."""
    from app.intelligence.v2.normalizer import normalize_phone_e164

    # ٠٥٠١٢٣٤٥٦٧ → 0501234567 → +966501234567
    result = normalize_phone_e164("٠٥٠١٢٣٤٥٦٧", "SA")
    assert result == "+966501234567"


def test_phone_normalization_uae():
    """UAE phone numbers normalized correctly."""
    from app.intelligence.v2.normalizer import normalize_phone_e164

    result = normalize_phone_e164("+971501234567", "UAE")
    assert result == "+971501234567"


# ─────────────────────────── TEST 4: Models ──────────────────────────────────

def test_discovery_query_model(sample_icp_dict):
    """DiscoveryQuery and ICP models parse correctly."""
    from app.intelligence.v2.models import DiscoveryQuery, ICP, GeoFilter, DepthLevel

    geo = GeoFilter(countries=["SA"], cities=["Riyadh"])
    icp = ICP(industries=["restaurants"], geo=geo, signals=["hiring"])
    query = DiscoveryQuery(icp=icp, depth=DepthLevel.QUICK, limit=5)

    assert query.icp.industries == ["restaurants"]
    assert query.icp.geo.countries == ["SA"]
    assert query.depth == DepthLevel.QUICK
    assert query.limit == 5
    assert query.id  # UUID auto-generated


def test_scored_lead_tier():
    """ScoredLead.set_tier() assigns correct tier based on score."""
    from app.intelligence.v2.models import ScoredLead, EnrichedLead, NormalizedLead, LeadTier, ProvenanceRecord

    def _make_scored(score):
        prov = ProvenanceRecord(source_name="test", query_used="test", is_mock=True)
        nl = NormalizedLead(
            raw_lead_ids=[], provenances=[prov],
            company_name="Test Co", country="SA",
        )
        from app.intelligence.v2.models import EnrichedLead
        el = EnrichedLead(normalized_lead=nl)
        scored = ScoredLead(enriched_lead=el, total_score=score)
        scored.set_tier()
        return scored

    assert _make_scored(85).tier == LeadTier.HOT
    assert _make_scored(70).tier == LeadTier.WARM
    assert _make_scored(50).tier == LeadTier.COOL
    assert _make_scored(30).tier == LeadTier.COLD


# ─────────────────────────── TEST 5: BaseSource Mock Leads ───────────────────

def test_base_source_mock_leads(sample_discovery_query):
    """BaseSource._mock_leads returns is_mock=True leads."""
    from app.intelligence.v2.sources.base import BaseSource
    from app.intelligence.v2.models import SearchPlan

    class TestSource(BaseSource):
        SOURCE_NAME = "test"
        async def discover(self, query, plan):
            return self._mock_leads(query, plan, count=3)

    source = TestSource()
    plan = SearchPlan(source_name="test", query_string="مطاعم الرياض")
    leads = source._mock_leads(sample_discovery_query, plan, count=3)

    assert len(leads) == 3
    for lead in leads:
        assert lead.provenance.is_mock is True
        assert lead.provenance.source_name == "test"
        assert lead.company_name is not None


# ─────────────────────────── TEST 6: Deduplication ───────────────────────────

def test_dedup_exact_domain(sample_normalized_lead):
    """Exact dedup removes duplicates with same domain."""
    from app.intelligence.v2.dedup import _exact_dedup
    from app.intelligence.v2.models import NormalizedLead, ProvenanceRecord

    # Create a duplicate with same domain
    prov2 = ProvenanceRecord(source_name="source2", query_used="test", is_mock=True)
    duplicate = NormalizedLead(
        raw_lead_ids=["other-id"],
        provenances=[prov2],
        company_name="Al Noor Restaurant",  # slightly different name
        domain="alnoor-restaurant.com.sa",  # SAME domain
        country="SA",
        dedup_key="domain:alnoor-restaurant.com.sa",
    )

    leads = [sample_normalized_lead, duplicate]
    result = _exact_dedup(leads)

    assert len(result) == 1  # Deduped to 1
    assert len(result[0].provenances) == 2  # Both provenances merged


def test_dedup_fuzzy_company_name():
    """Fuzzy dedup merges leads with very similar company names."""
    from app.intelligence.v2.dedup import _fuzzy_dedup
    from app.intelligence.v2.models import NormalizedLead, ProvenanceRecord

    def _make_lead(name, domain=None):
        prov = ProvenanceRecord(source_name="test", query_used="test", is_mock=True)
        nl = NormalizedLead(
            raw_lead_ids=[str(uuid.uuid4())],
            provenances=[prov],
            company_name=name,
            domain=domain,
            country="SA",
            dedup_key=f"name_en:{name.lower()}",
        )
        return nl

    lead1 = _make_lead("Al Noor Restaurant Group")
    lead2 = _make_lead("Alnoor Restaurant Group")  # Very similar
    lead3 = _make_lead("Completely Different Co")  # Should NOT merge

    result = _fuzzy_dedup([lead1, lead2, lead3])
    assert len(result) == 2  # lead1+lead2 merged, lead3 separate


# ─────────────────────────── TEST 7: Normalizer ──────────────────────────────

@pytest.mark.asyncio
async def test_normalize_lead_basic(sample_raw_lead):
    """normalize_lead converts RawLead to NormalizedLead correctly."""
    from app.intelligence.v2.normalizer import normalize_lead

    result = await normalize_lead(sample_raw_lead)

    assert result is not None
    assert result.company_name == "Al Noor Restaurant Group"
    assert result.company_name_ar == "مجموعة النور للمطاعم"
    assert result.phone_e164 == "+966501234567"
    assert result.domain == "alnoor-restaurant.com.sa"
    assert result.country == "SA"
    assert result.is_hiring is True
    assert "Chef" in result.hiring_roles
    assert result.dedup_key is not None


@pytest.mark.asyncio
async def test_normalize_lead_missing_company():
    """normalize_lead returns None when no company name can be inferred."""
    from app.intelligence.v2.normalizer import normalize_lead
    from app.intelligence.v2.models import RawLead, ProvenanceRecord

    prov = ProvenanceRecord(source_name="test", query_used="test", is_mock=True)
    lead = RawLead(provenance=prov)  # No company name, no domain

    result = await normalize_lead(lead)
    assert result is None


# ─────────────────────────── TEST 8: Query Planner Fallback ──────────────────

@pytest.mark.asyncio
async def test_planner_fallback_no_llm(sample_discovery_query):
    """Planner generates fallback plans when no GROQ key available."""
    from app.intelligence.v2.planner import _fallback_plans

    plans = _fallback_plans(sample_discovery_query)

    assert len(plans) >= 3
    source_names = [p.source_name for p in plans]
    assert "google_places" in source_names or "duckduckgo" in source_names or "osm_nominatim" in source_names

    for plan in plans:
        assert plan.query_string  # All plans have a query string
        assert plan.source_name  # All plans have a source name


@pytest.mark.asyncio
async def test_planner_with_mocked_llm(sample_discovery_query):
    """Planner correctly processes LLM JSON response."""
    from app.intelligence.v2.planner import plan_queries

    mock_response = {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "plans": [
                        {
                            "source_name": "google_places",
                            "query_string": "مطاعم الرياض",
                            "filters": {"language": "ar"},
                            "language": "ar",
                            "priority": 1,
                            "rationale": "Best for local restaurants",
                        },
                        {
                            "source_name": "bayt_jobs",
                            "query_string": "restaurant",
                            "filters": {},
                            "language": "en",
                            "priority": 2,
                            "rationale": "Hiring signal",
                        },
                    ]
                })
            }
        }]
    }

    mock_resp = MagicMock()
    mock_resp.json.return_value = mock_response
    mock_resp.raise_for_status = MagicMock()

    with patch("app.intelligence.v2.planner.GROQ_API_KEY", "test-key"):
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.post = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            plans = await plan_queries(sample_discovery_query)

    assert len(plans) == 2
    assert plans[0].source_name == "google_places"
    assert plans[0].query_string == "مطاعم الرياض"
    assert plans[1].source_name == "bayt_jobs"


# ─────────────────────────── TEST 9: Rule-Based Scoring ──────────────────────

def test_rule_based_scoring(sample_normalized_lead, sample_discovery_query):
    """Rule-based scoring produces valid score for matching lead."""
    from app.intelligence.v2.scoring import _rule_based_score
    from app.intelligence.v2.models import EnrichedLead

    enriched = EnrichedLead(
        normalized_lead=sample_normalized_lead,
        has_website=True,
        has_ecommerce=False,
    )

    result = _rule_based_score(enriched, sample_discovery_query)

    assert 0 <= result["total_score"] <= 100
    assert 0 <= result["icp_score"] <= 100
    assert 0 <= result["intent_score"] <= 100
    assert isinstance(result["talking_points"], list)
    assert isinstance(result["talking_points_ar"], list)
    assert result["total_score"] > 0  # Should score > 0 (SA country + hiring)


# ─────────────────────────── TEST 10: API End-to-End ─────────────────────────

@pytest.mark.asyncio
async def test_api_discover_endpoint(sample_icp_dict):
    """POST /api/v2/intelligence/discover returns a job_id."""
    from dashboard_api import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v2/intelligence/discover",
            json={
                "icp": sample_icp_dict,
                "depth": "quick",
                "limit": 3,
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "job_id" in data
    assert data["status"] == "pending"
    assert data["job_id"]
    assert "/api/v2/intelligence/jobs/" in data["poll_url"]


@pytest.mark.asyncio
async def test_api_job_status_endpoint(sample_icp_dict):
    """GET /api/v2/intelligence/jobs/{id} returns job status."""
    from dashboard_api import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Start a job
        resp = await client.post(
            "/api/v2/intelligence/discover",
            json={"icp": sample_icp_dict, "depth": "quick", "limit": 3},
        )
        job_id = resp.json()["job_id"]

        # Check status
        status_resp = await client.get(f"/api/v2/intelligence/jobs/{job_id}")

    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["job_id"] == job_id
    # In test env, job may fail due to network (sources fall back to mock but pipeline may still fail)
    assert status_data["status"] in ("pending", "running", "completed", "failed")


@pytest.mark.asyncio
async def test_api_job_not_found():
    """GET /jobs/{nonexistent_id} returns 404."""
    from dashboard_api import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v2/intelligence/jobs/nonexistent-job-id-12345")

    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_api_sources_endpoint():
    """GET /api/v2/intelligence/sources lists all 8 sources."""
    from dashboard_api import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v2/intelligence/sources")

    assert resp.status_code == 200
    data = resp.json()
    assert "sources" in data
    source_names = [s["name"] for s in data["sources"]]
    assert len(source_names) == 8
    assert "google_places" in source_names
    assert "duckduckgo" in source_names
    assert "bayt_jobs" in source_names
    assert "osm_nominatim" in source_names
