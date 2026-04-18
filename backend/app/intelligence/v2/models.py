"""
Pydantic V2 Data Models — Dealix Lead Intelligence Engine V2
============================================================
Core models for the discovery pipeline:
  DiscoveryQuery → RawLead → NormalizedLead → EnrichedLead → ScoredLead

Every RawLead carries full ProvenanceRecord (source + query + timestamp + URL).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# ─────────────────────────── Enumerations ────────────────────────────────────

class DepthLevel(str, Enum):
    QUICK = "quick"      # Fast pass: 1-3 sources, ~1min
    STANDARD = "standard"  # Default: 5-8 sources, ~5min
    DEEP = "deep"        # All sources, unlimited time


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class LeadTier(str, Enum):
    HOT = "hot"      # 80-100
    WARM = "warm"    # 60-79
    COOL = "cool"    # 40-59
    COLD = "cold"    # < 40


# ─────────────────────────── Provenance ──────────────────────────────────────

class ProvenanceRecord(BaseModel):
    """Tracks exactly where each piece of data came from."""

    source_name: str = Field(..., description="Source adapter name, e.g. 'google_places'")
    query_used: str = Field(..., description="The actual query string sent to the source")
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    url: Optional[str] = Field(None, description="Source URL if applicable")
    is_mock: bool = Field(False, description="True when returning mock data (no API key)")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Source confidence (0-1)")
    raw_snippet: Optional[str] = Field(None, description="Raw text snippet from source")


# ─────────────────────────── Discovery Query ─────────────────────────────────

class GeoFilter(BaseModel):
    """Geographic constraints for a discovery query."""

    countries: List[str] = Field(default_factory=lambda: ["SA"], description="ISO country codes")
    cities: List[str] = Field(default_factory=list, description="City names or slugs")
    bbox: Optional[tuple[float, float, float, float]] = Field(
        None, description="Bounding box (lat_min, lon_min, lat_max, lon_max)"
    )


class ICP(BaseModel):
    """Ideal Customer Profile — defines who we're looking for."""

    industries: List[str] = Field(default_factory=list, description="Industry names or codes")
    geo: GeoFilter = Field(default_factory=GeoFilter)
    company_size: Optional[str] = Field(None, description="micro|small|medium|large")
    min_employees: Optional[int] = None
    max_employees: Optional[int] = None
    roles: List[str] = Field(default_factory=list, description="Decision maker roles to find")
    signals: List[str] = Field(
        default_factory=list,
        description="Buying signals: hiring|funding|expansion|tech_change"
    )
    keywords: List[str] = Field(default_factory=list, description="Additional search keywords")
    keywords_ar: List[str] = Field(default_factory=list, description="Arabic search keywords")
    exclude_keywords: List[str] = Field(default_factory=list)
    has_website: Optional[bool] = None
    has_ecommerce: Optional[bool] = None


class DiscoveryQuery(BaseModel):
    """
    Top-level input to the discovery engine.
    Passed through planner → orchestrator → sources.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    icp: ICP = Field(default_factory=ICP)
    depth: DepthLevel = Field(DepthLevel.STANDARD)
    limit: int = Field(50, ge=1, le=500)
    sources: Optional[List[str]] = Field(
        None, description="Specific sources to use; None = all applicable"
    )
    language: str = Field("ar", description="Primary language: ar|en|both")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


# ─────────────────────────── Search Plan ─────────────────────────────────────

class SearchPlan(BaseModel):
    """A single planned search operation from the LLM query planner."""

    source_name: str = Field(..., description="Target source adapter name")
    query_string: str = Field(..., description="Query to send to the source")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Source-specific filters")
    language: str = Field("en", description="Query language: ar|en")
    priority: int = Field(1, ge=1, le=10, description="Execution priority (1=highest)")
    rationale: Optional[str] = Field(None, description="LLM reasoning for this search")


# ─────────────────────────── Raw Lead ────────────────────────────────────────

class RawLead(BaseModel):
    """
    Unvalidated data returned by a source adapter.
    May contain duplicates, missing fields, and unvalidated formats.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provenance: ProvenanceRecord

    # Core fields (all optional at this stage)
    company_name: Optional[str] = None
    company_name_ar: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None           # Raw, unvalidated
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None

    # Contact
    contact_name: Optional[str] = None
    contact_name_ar: Optional[str] = None
    contact_title: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    # Social / Digital
    linkedin_url: Optional[str] = None
    instagram_handle: Optional[str] = None
    twitter_handle: Optional[str] = None

    # Signals
    is_hiring: bool = False
    hiring_roles: List[str] = Field(default_factory=list)
    is_new_business: bool = False

    # Metadata
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Full source response")
    place_id: Optional[str] = None        # Google Places ID
    rating: Optional[float] = None
    review_count: Optional[int] = None

    model_config = {"populate_by_name": True}


# ─────────────────────────── Normalized Lead ─────────────────────────────────

class NormalizedLead(BaseModel):
    """
    Cleaned + validated lead after normalization pipeline.
    Phones in E.164, emails validated, names deduplicated.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    raw_lead_ids: List[str] = Field(default_factory=list, description="Source RawLead IDs")
    provenances: List[ProvenanceRecord] = Field(default_factory=list)

    # Validated fields
    company_name: str
    company_name_ar: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    phone_e164: Optional[str] = Field(None, description="Phone in E.164 format e.g. +966501234567")
    email: Optional[str] = None
    email_mx_valid: bool = False
    address: Optional[str] = None
    city: Optional[str] = None
    city_slug: Optional[str] = None
    country: str = "SA"
    industry: Optional[str] = None

    # Contact
    contact_name: Optional[str] = None
    contact_name_ar: Optional[str] = None
    contact_title: Optional[str] = None

    # Social
    linkedin_url: Optional[str] = None

    # Dedup key (domain > phone > name)
    dedup_key: Optional[str] = None

    # Signals
    is_hiring: bool = False
    hiring_roles: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


# ─────────────────────────── Enriched Lead ───────────────────────────────────

class EnrichedLead(BaseModel):
    """Lead after enrichment: WHOIS, email patterns, LinkedIn detection, etc."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    normalized_lead: NormalizedLead

    # Enrichment outputs
    whois_registrar: Optional[str] = None
    whois_creation_date: Optional[datetime] = None
    whois_country: Optional[str] = None
    domain_age_days: Optional[int] = None
    has_website: bool = False
    website_tech: List[str] = Field(default_factory=list)

    # Discovered emails
    discovered_emails: List[str] = Field(default_factory=list)

    # LinkedIn
    linkedin_url: Optional[str] = None
    linkedin_found: bool = False

    # Additional signals
    tech_stack: List[str] = Field(default_factory=list)
    has_ecommerce: bool = False
    ecommerce_platform: Optional[str] = None

    enriched_at: datetime = Field(default_factory=datetime.utcnow)
    enrichment_sources: List[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


# ─────────────────────────── Scored Lead ─────────────────────────────────────

class ScoredLead(BaseModel):
    """Final output: enriched lead with ICP match score and talking points."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    enriched_lead: EnrichedLead

    # Scoring
    icp_score: float = Field(0.0, ge=0, le=100)
    intent_score: float = Field(0.0, ge=0, le=100)
    total_score: float = Field(0.0, ge=0, le=100)
    tier: Optional[LeadTier] = None
    score_rationale: Optional[str] = None
    score_rationale_ar: Optional[str] = None

    # Talking points (in Arabic for Arabic leads)
    talking_points: List[str] = Field(default_factory=list, description="Up to 3 talking points")
    talking_points_ar: List[str] = Field(default_factory=list)

    # LLM metadata
    scored_at: datetime = Field(default_factory=datetime.utcnow)
    scoring_model: Optional[str] = None

    @property
    def company_name(self) -> str:
        return self.enriched_lead.normalized_lead.company_name

    @property
    def phone(self) -> Optional[str]:
        return self.enriched_lead.normalized_lead.phone_e164

    @property
    def email(self) -> Optional[str]:
        return self.enriched_lead.normalized_lead.email

    def set_tier(self) -> None:
        s = self.total_score
        if s >= 80:
            self.tier = LeadTier.HOT
        elif s >= 60:
            self.tier = LeadTier.WARM
        elif s >= 40:
            self.tier = LeadTier.COOL
        else:
            self.tier = LeadTier.COLD

    model_config = {"populate_by_name": True}


# ─────────────────────────── Job Models ──────────────────────────────────────

class DiscoveryJob(BaseModel):
    """In-memory job tracking for a discovery run."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: DiscoveryQuery
    status: JobStatus = JobStatus.PENDING
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Completion percentage")
    leads_found: int = 0
    leads_scored: int = 0
    sources_completed: List[str] = Field(default_factory=list)
    sources_total: int = 0
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Results (stored in memory for now)
    scored_leads: List[ScoredLead] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
