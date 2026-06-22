from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    blocked = "blocked"


class ConsentState(str, Enum):
    unknown = "unknown"
    required = "required"
    granted = "granted"
    revoked = "revoked"
    inbound_only = "inbound_only"


class PriorityBucket(str, Enum):
    p0_now = "P0_NOW"
    p1_this_week = "P1_THIS_WEEK"
    p2_nurture = "P2_NURTURE"
    p3_low_priority = "P3_LOW_PRIORITY"
    blocked = "BLOCKED"


class WarmRouteType(str, Enum):
    founder_intro = "founder_intro"
    partner_intro = "partner_intro"
    customer_referral = "customer_referral"
    inbound_reply = "inbound_reply"
    email_draft = "email_draft"
    linkedin_manual = "linkedin_manual"
    phone_script = "phone_script"
    whatsapp_inbound_only = "whatsapp_inbound_only"


class SourceDefinition(BaseModel):
    source_name: str
    allowed_use: str
    consent_requirement: str
    risk_level: RiskLevel
    retention_policy: str
    can_auto_ingest: bool
    can_contact: bool
    provenance_required: bool


class ProvenanceRecord(BaseModel):
    source_name: str
    source_type: str
    collected_at: datetime
    allowed_use: str
    consent_state: ConsentState
    confidence: float = Field(ge=0, le=1)
    refresh_needed: bool = False
    risk_level: RiskLevel


class LeadCompany(BaseModel):
    company_name: str
    domain: str | None = None
    website_url: str | None = None
    city: str | None = None
    country: str = "SA"
    google_place_id: str | None = None
    crm_external_id: str | None = None
    phone: str | None = None
    email: str | None = None
    sector: str | None = None
    employee_band: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EnrichmentResult(BaseModel):
    provider: str
    configured: bool
    confidence: float = Field(ge=0, le=1)
    fields: dict[str, Any] = Field(default_factory=dict)
    status: str = "ok"
    reason: str | None = None


class DedupeResult(BaseModel):
    duplicate_of: str | None = None
    confidence: float = Field(ge=0, le=1)
    merge_recommendation: str
    safe_merge: bool
    matched_keys: list[str] = Field(default_factory=list)


class SignalRecord(BaseModel):
    signal_name: str
    detected: bool
    weight: int = 0
    evidence: str | None = None


class ScoreBreakdown(BaseModel):
    fit: int = Field(ge=0, le=100)
    intent: int = Field(ge=0, le=100)
    urgency: int = Field(ge=0, le=100)
    revenue_potential: int = Field(ge=0, le=100)
    engagement: int = Field(ge=0, le=100)
    data_quality: int = Field(ge=0, le=100)
    compliance_risk: int = Field(ge=0, le=100)
    deliverability_risk: int = Field(ge=0, le=100)
    final_priority: PriorityBucket
    penalties: list[str] = Field(default_factory=list)


class WarmRouteDecision(BaseModel):
    route: WarmRouteType
    allowed: bool
    reason: str
    action_mode: str = "approval_required"


class ComplianceDecision(BaseModel):
    allowed: bool
    status: str
    reasons: list[str] = Field(default_factory=list)


class LeadMachineRunRequest(BaseModel):
    lead: LeadCompany
    provenance: ProvenanceRecord
    existing_records: list[LeadCompany] = Field(default_factory=list)
    inbound_whatsapp: bool = False
    consented_whatsapp: bool = False


class LeadMachineRunResponse(BaseModel):
    source: SourceDefinition
    enrichment: list[EnrichmentResult]
    dedupe: DedupeResult
    signals: list[SignalRecord]
    score: ScoreBreakdown
    compliance: ComplianceDecision
    warm_route: WarmRouteDecision