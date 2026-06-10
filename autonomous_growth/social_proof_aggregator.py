"""
Social Proof Aggregator — collects social proof signals from multiple sources.
مجمّع الإثبات الاجتماعي — يجمع إشارات الإثبات الاجتماعي من مصادر متعددة.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class ProofEvent:
    proof_id: str
    event_type: str
    title: str
    description: str
    evidence_level: int
    customer_handle: str
    sector: str
    created_at: datetime = field(default_factory=utcnow)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proof_id": self.proof_id,
            "event_type": self.event_type,
            "title": self.title,
            "description": self.description,
            "evidence_level": self.evidence_level,
            "customer_handle": self.customer_handle,
            "sector": self.sector,
            "created_at": self.created_at.isoformat(),
            "metrics": self.metrics,
        }


@dataclass
class Testimonial:
    id: str
    customer_name: str
    customer_title: str
    company: str
    quote_ar: str
    quote_en: str
    sector: str
    rating: int = 5
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_title": self.customer_title,
            "company": self.company,
            "quote_ar": self.quote_ar,
            "quote_en": self.quote_en,
            "sector": self.sector,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SocialProofBundle:
    l3_plus_events: list[ProofEvent] = field(default_factory=list)
    testimonials: list[Testimonial] = field(default_factory=list)
    metrics: ProofMetrics | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "l3_plus_events": [e.to_dict() for e in self.l3_plus_events],
            "testimonials": [t.to_dict() for t in self.testimonials],
            "metrics": self.metrics.to_dict() if self.metrics else None,
        }


@dataclass
class ProofMetrics:
    total_events: int = 0
    total_l3_plus: int = 0
    total_testimonials: int = 0
    sectors_covered: list[str] = field(default_factory=list)
    avg_evidence_level: float = 0.0
    last_updated: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_events": self.total_events,
            "total_l3_plus": self.total_l3_plus,
            "total_testimonials": self.total_testimonials,
            "sectors_covered": self.sectors_covered,
            "avg_evidence_level": self.avg_evidence_level,
            "last_updated": self.last_updated.isoformat(),
        }


class SocialProofAggregator:
    def __init__(self):
        self._events: list[ProofEvent] = []
        self._testimonials: list[Testimonial] = []
        self._metrics: ProofMetrics | None = None
        self.log = logger.bind(component="social_proof_aggregator")

    async def aggregate(self) -> SocialProofBundle:
        bundle = SocialProofBundle(
            l3_plus_events=[e for e in self._events if e.evidence_level >= 3],
            testimonials=list(self._testimonials),
            metrics=await self.get_metrics(),
        )
        return bundle

    async def refresh(self) -> SocialProofBundle:
        self.log.info("social_proof_refresh_started")
        bundle = await self.aggregate()
        self._metrics = bundle.metrics
        self.log.info("social_proof_refresh_complete", metrics=bundle.metrics.to_dict() if bundle.metrics else None)
        return bundle

    async def get_metrics(self) -> ProofMetrics:
        sectors = set()
        for e in self._events:
            sectors.add(e.sector)
        for t in self._testimonials:
            sectors.add(t.sector)

        l3_count = sum(1 for e in self._events if e.evidence_level >= 3)
        avg_level = 0.0
        if self._events:
            avg_level = sum(e.evidence_level for e in self._events) / len(self._events)

        return ProofMetrics(
            total_events=len(self._events),
            total_l3_plus=l3_count,
            total_testimonials=len(self._testimonials),
            sectors_covered=sorted(sectors),
            avg_evidence_level=round(avg_level, 2),
        )

    def add_event(self, event: ProofEvent) -> None:
        self._events.append(event)
        self.log.info("proof_event_added", proof_id=event.proof_id, level=event.evidence_level)

    def add_testimonial(self, testimonial: Testimonial) -> None:
        self._testimonials.append(testimonial)
        self.log.info("testimonial_added", id=testimonial.id, company=testimonial.company)

    def get_events(self, min_level: int = 0) -> list[ProofEvent]:
        if min_level > 0:
            return [e for e in self._events if e.evidence_level >= min_level]
        return list(self._events)

    def get_testimonials(self, sector: str | None = None) -> list[Testimonial]:
        if sector:
            return [t for t in self._testimonials if t.sector == sector]
        return list(self._testimonials)
