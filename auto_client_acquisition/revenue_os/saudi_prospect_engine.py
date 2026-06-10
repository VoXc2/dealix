"""
Saudi Prospect Engine — discovers and enriches B2B prospects across all Saudi sectors and regions.
محرك التنقيب السعودي — يكتشف ويثري بيانات العملاء المحتملين عبر جميع القطاعات والمناطق السعودية.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class ICPProfile:
    sector: str
    company_size: str = "medium"
    region: str = "riyadh"
    budget_range_sar: tuple[float, float] = (50000, 500000)
    decision_maker_role: str = "CEO"
    pain_points: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector": self.sector,
            "company_size": self.company_size,
            "region": self.region,
            "budget_range_sar": list(self.budget_range_sar),
            "decision_maker_role": self.decision_maker_role,
            "pain_points": self.pain_points,
        }


@dataclass
class Prospect:
    id: str
    company_name: str
    sector: str
    region: str
    city: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    size_band: str = "medium"
    decision_maker: str = ""
    source: str = "discovery"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "company_name": self.company_name,
            "sector": self.sector,
            "region": self.region,
            "city": self.city,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "size_band": self.size_band,
            "decision_maker": self.decision_maker,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class EnrichedProspect:
    prospect: Prospect
    linkedin_url: str = ""
    estimated_revenue_sar: float = 0.0
    employee_count: int = 0
    year_founded: int = 0
    commercial_registration: str = ""
    credit_score: int = 0
    key_decision_makers: list[dict[str, str]] = field(default_factory=list)
    recent_news: list[str] = field(default_factory=list)
    tech_stack: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prospect": self.prospect.to_dict(),
            "linkedin_url": self.linkedin_url,
            "estimated_revenue_sar": self.estimated_revenue_sar,
            "employee_count": self.employee_count,
            "year_founded": self.year_founded,
            "commercial_registration": self.commercial_registration,
            "credit_score": self.credit_score,
            "key_decision_makers": self.key_decision_makers,
            "recent_news": self.recent_news,
            "tech_stack": self.tech_stack,
        }


@dataclass
class ProspectScore:
    prospect_id: str
    icp_fit: float = 0.0
    engagement_risk: float = 0.0
    conversion_probability: float = 0.0
    estimated_value_sar: float = 0.0
    priority: str = "medium"
    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prospect_id": self.prospect_id,
            "icp_fit": self.icp_fit,
            "engagement_risk": self.engagement_risk,
            "conversion_probability": self.conversion_probability,
            "estimated_value_sar": self.estimated_value_sar,
            "priority": self.priority,
            "signals": self.signals,
        }


class SaudiProspectEngine:
    SECTORS = [
        "healthcare", "real_estate", "logistics", "retail", "fintech",
        "education", "technology", "manufacturing", "oil_gas", "tourism",
        "construction", "consulting", "hospitality", "government",
        "saudi_saas", "ecommerce", "telecom", "agriculture",
        "transportation", "energy", "mining", "defense",
        "sports", "entertainment", "media", "nonprofit",
        "legal", "insurance", "pharma", "food_beverage",
        "aviation", "shipping", "renewable_energy", "petrochemicals",
        "steel", "cement", "automotive", "cybersecurity", "cloud_computing",
        "proptech", "healthtech", "edtech", "legaltech", "insurtech",
        "regtech", "wealthtech", "agritech", "foodtech", "cleantech",
        "martech", "adtech", "hrtech", "biotech", "robotics",
    ]

    REGIONS = {
        "riyadh": {"name_ar": "الرياض", "cities": ["الرياض", "الخرج", "المجمعة", "الدوادمي"]},
        "makkah": {"name_ar": "مكة المكرمة", "cities": ["مكة", "جدة", "الطائف", "القنفذة"]},
        "madina": {"name_ar": "المدينة المنورة", "cities": ["المدينة", "ينبع", "بدر", "خيبر"]},
        "qassim": {"name_ar": "القصيم", "cities": ["بريدة", "عنيزة", "الرس", "المذنب"]},
        "eastern": {"name_ar": "المنطقة الشرقية", "cities": ["الدمام", "الخبر", "الظهران", "الأحساء", "حفر الباطن", "الجبيل"]},
        "asir": {"name_ar": "عسير", "cities": ["أبها", "خميس مشيط", "بيشة", "ظهران الجنوب"]},
        "tabuk": {"name_ar": "تبوك", "cities": ["تبوك", "ضباء", "الوجه", "أملج"]},
        "hail": {"name_ar": "حائل", "cities": ["حائل", "بقعاء", "الشنان"]},
        "northern": {"name_ar": "الحدود الشمالية", "cities": ["عرعر", "رفحاء", "طريف"]},
        "jazan": {"name_ar": "جازان", "cities": ["جازان", "صبياء", "أبو عريش", "صامطة"]},
        "najran": {"name_ar": "نجران", "cities": ["نجران", "شرورة", "حبونا"]},
        "bahah": {"name_ar": "الباحة", "cities": ["الباحة", "بلجرشي", "المندق"]},
        "jouf": {"name_ar": "الجوف", "cities": ["سكاكا", "دومة الجندل", "طبرجل"]},
    }

    def __init__(self):
        self._prospects: dict[str, Prospect] = {}
        self._enriched: dict[str, EnrichedProspect] = {}
        self._scores: dict[str, ProspectScore] = {}
        self.log = logger.bind(component="saudi_prospect_engine")

    async def discover(self, icp: ICPProfile) -> list[Prospect]:
        prospects: list[Prospect] = []

        region_info = self.REGIONS.get(icp.region, self.REGIONS["riyadh"])
        cities = region_info["cities"]

        for city in cities[:3]:
            prospect = Prospect(
                id=generate_id("pro"),
                company_name=f"شركة {icp.sector} - {city}",
                sector=icp.sector,
                region=icp.region,
                city=city,
                size_band=icp.company_size,
                source="discovery",
            )
            self._prospects[prospect.id] = prospect
            prospects.append(prospect)

        self.log.info(
            "prospects_discovered",
            sector=icp.sector,
            region=icp.region,
            count=len(prospects),
        )
        return prospects

    async def enrich(self, prospect_id: str) -> EnrichedProspect:
        prospect = self._prospects.get(prospect_id)
        if not prospect:
            raise ValueError(f"Prospect {prospect_id} not found")

        estimated_revenue = {
            "small": 500000,
            "medium": 5000000,
            "large": 50000000,
        }.get(prospect.size_band, 5000000)

        enriched = EnrichedProspect(
            prospect=prospect,
            estimated_revenue_sar=estimated_revenue,
            employee_count={"small": 20, "medium": 100, "large": 500}.get(prospect.size_band, 100),
            year_founded=2015,
            key_decision_makers=[
                {"name": f"مدير {prospect.sector}", "role": "CEO", "email": f"ceo@{prospect.company_name.lower().replace(' ', '')}.com.sa"},
            ],
            tech_stack=["ERP", "CRM", "WhatsApp Business"],
        )
        self._enriched[prospect_id] = enriched
        self.log.info("prospect_enriched", prospect_id=prospect_id)
        return enriched

    async def score(self, prospect_id: str) -> ProspectScore:
        prospect = self._prospects.get(prospect_id)
        if not prospect:
            raise ValueError(f"Prospect {prospect_id} not found")

        sector_scores = {
            "technology": 0.85, "fintech": 0.90, "healthcare": 0.75,
            "real_estate": 0.70, "logistics": 0.80, "retail": 0.65,
            "education": 0.70, "manufacturing": 0.60, "oil_gas": 0.50,
        }
        base_score = sector_scores.get(prospect.sector, 0.60)

        size_modifier = {"small": 0.8, "medium": 1.0, "large": 1.2}.get(prospect.size_band, 1.0)
        icp_fit = min(base_score * size_modifier, 1.0)

        score = ProspectScore(
            prospect_id=prospect_id,
            icp_fit=round(icp_fit, 2),
            conversion_probability=round(icp_fit * 0.3, 2),
            estimated_value_sar=50000 * size_modifier,
            priority="high" if icp_fit > 0.7 else "medium" if icp_fit > 0.4 else "low",
            signals=["high_sector_relevance", "active_growth_stage"],
        )
        self._scores[prospect_id] = score
        self.log.info("prospect_scored", prospect_id=prospect_id, score=icp_fit)
        return score

    async def discover_by_sector(self, sector: str, region: str) -> list[Prospect]:
        icp = ICPProfile(sector=sector, region=region)
        return await self.discover(icp)

    def get_prospect(self, prospect_id: str) -> Prospect | None:
        return self._prospects.get(prospect_id)

    def get_enriched(self, prospect_id: str) -> EnrichedProspect | None:
        return self._enriched.get(prospect_id)

    def get_score(self, prospect_id: str) -> ProspectScore | None:
        return self._scores.get(prospect_id)

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_prospects": len(self._prospects),
            "enriched": len(self._enriched),
            "scored": len(self._scores),
            "sectors_covered": len(set(p.sector for p in self._prospects.values())),
            "regions_covered": len(set(p.region for p in self._prospects.values())),
            "avg_icp_fit": round(
                sum(s.icp_fit for s in self._scores.values()) / len(self._scores), 2
            ) if self._scores else 0.0,
        }
