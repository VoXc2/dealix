"""Ecosystem Metrics — typed snapshot across partner/academy/benchmark/platform/venture."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PartnerMetrics:
    partner_leads: int
    win_rate: float
    qa_score: float
    compliance_incidents: int
    partner_revenue: float


@dataclass(frozen=True)
class AcademyMetrics:
    registrations: int
    completion_rate: float
    assessment_pass_rate: float
    certified_partners: int
    course_to_lead_conversion: float


@dataclass(frozen=True)
class BenchmarkMetrics:
    downloads: int
    inbound_diagnostics: int
    media_mentions: int
    partner_usage: int
    enterprise_inquiries: int


@dataclass(frozen=True)
class PlatformMetrics:
    active_clients: int
    proof_timeline_views: int
    approval_completion: float
    monthly_active_stakeholders: int
    audit_export_requests: int


@dataclass(frozen=True)
class EcosystemMetricsSnapshot:
    period: str
    partner: PartnerMetrics
    academy: AcademyMetrics
    benchmark: BenchmarkMetrics
    platform: PlatformMetrics
