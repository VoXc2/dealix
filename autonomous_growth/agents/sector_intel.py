"""
Sector Intelligence Agent — researches and analyzes Saudi/Gulf sectors.
وكيل ذكاء القطاعات — يبحث ويحلل القطاعات السعودية والخليجية.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.agents.base import BaseAgent
from core.config.models import Task
from core.llm.base import Message
from core.prompts import get_prompt
from core.utils import generate_id, utcnow


@dataclass
class SectorProfile:
    sector_key: str
    name_ar: str
    name_en: str
    market_size_sar: float = 0.0
    growth_rate: float = 0.0
    digital_maturity: float = 0.0
    key_players: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    regulations: list[str] = field(default_factory=list)
    vision_2030_alignment: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector_key": self.sector_key,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "market_size_sar": self.market_size_sar,
            "growth_rate": self.growth_rate,
            "digital_maturity": self.digital_maturity,
            "key_players": self.key_players,
            "pain_points": self.pain_points,
            "regulations": self.regulations,
            "vision_2030_alignment": self.vision_2030_alignment,
        }


@dataclass
class Opportunity:
    sector: str
    title_ar: str
    title_en: str
    description_ar: str
    description_en: str
    potential_impact: str = "high"
    timeframe: str = "short_term"
    ai_readiness: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector": self.sector,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "potential_impact": self.potential_impact,
            "timeframe": self.timeframe,
            "ai_readiness": self.ai_readiness,
        }


@dataclass
class SectorReport:
    sector_key: str
    profile: SectorProfile
    opportunities: list[Opportunity] = field(default_factory=list)
    generated_at: datetime = field(default_factory=utcnow)
    report_id: str = ""

    def __post_init__(self):
        if not self.report_id:
            self.report_id = generate_id("sr")

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "sector_key": self.sector_key,
            "profile": self.profile.to_dict(),
            "opportunities": [o.to_dict() for o in self.opportunities],
            "generated_at": self.generated_at.isoformat(),
        }


class SectorIntelAgent(BaseAgent):
    ALL_SECTORS = [
        "healthcare", "real_estate", "logistics", "retail", "fintech",
        "education", "technology", "manufacturing", "oil_gas", "tourism",
        "construction", "consulting", "hospitality", "government",
        "saudi_saas", "ecommerce", "telecom", "agriculture",
        "transportation", "energy", "mining", "defense", "sports",
        "entertainment", "media", "nonprofit", "legal", "insurance",
        "pharma", "food_beverage", "aviation", "shipping", "railways",
        "water", "waste_management", "renewable_energy", "petrochemicals",
        "steel", "cement", "automotive", "furniture", "textile",
        "chemicals", "plastics", "packaging", "printing", "advertising",
        "market_research", "hr_consulting", "it_services", "cybersecurity",
        "cloud_computing", "blockchain", "iot", "robotics", "biotech",
        "nanotech", "aerospace", "satellite", "smart_cities",
        "proptech", "healthtech", "edtech", "legaltech", "insurtech",
        "regtech", "wealthtech", "agritech", "foodtech", "cleantech",
        "martech", "adtech", "hrtech", "remotecare", "telehealth",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._profiles: dict[str, SectorProfile] = {}

    async def get_sector_profile(self, sector: str) -> SectorProfile:
        sector_key = sector.lower().replace(" ", "_").replace("-", "_")

        if sector_key in self._profiles:
            return self._profiles[sector_key]

        base = self._get_base_profile(sector_key)
        if not base:
            try:
                prompt = get_prompt("sector_analysis", sector=sector_key)
                response = await self.router.run(
                    task=Task.RESEARCH,
                    messages=[Message(role="user", content=prompt)],
                    max_tokens=1000,
                    temperature=0.3,
                )
                extra = self.parse_json_response(response.content)
                base = SectorProfile(
                    sector_key=sector_key,
                    name_ar=extra.get("name_ar", sector_key),
                    name_en=extra.get("name_en", sector_key),
                    market_size_sar=float(extra.get("market_size_sar", 0)),
                    growth_rate=float(extra.get("growth_rate", 0.05)),
                    digital_maturity=float(extra.get("digital_maturity", 0.5)),
                    key_players=extra.get("key_players", []),
                    pain_points=extra.get("pain_points", []),
                    regulations=extra.get("regulations", []),
                    vision_2030_alignment=extra.get("vision_2030_alignment", ""),
                )
            except Exception:
                base = SectorProfile(
                    sector_key=sector_key,
                    name_ar=sector_key,
                    name_en=sector_key,
                )

        self._profiles[sector_key] = base
        self.log.info("sector_profile_loaded", sector=sector_key)
        return base

    async def identify_opportunities(self, sector: str) -> list[Opportunity]:
        profile = await self.get_sector_profile(sector)
        sector_key = sector.lower().replace(" ", "_")

        opportunities = [
            Opportunity(
                sector=sector_key,
                title_ar=f"أتمتة عمليات {profile.name_ar} بالذكاء الاصطناعي",
                title_en=f"AI-Powered {profile.name_en} Process Automation",
                description_ar=f"تحسين كفاءة عمليات {profile.name_ar} باستخدام حلول الذكاء الاصطناعي لتقليل التكاليف وزيادة الإنتاجية.",
                description_en=f"Improve {profile.name_en} operational efficiency using AI solutions to reduce costs and increase productivity.",
                ai_readiness=profile.digital_maturity,
            ),
            Opportunity(
                sector=sector_key,
                title_ar=f"تحليل بيانات {profile.name_ar} للتنبؤ",
                title_en=f"Predictive Data Analytics for {profile.name_en}",
                description_ar=f"استخدام تحليل البيانات والتنبؤ لاتخاذ قرارات أفضل في قطاع {profile.name_ar}.",
                description_en=f"Leverage data analytics and forecasting for better decision-making in {profile.name_en}.",
                ai_readiness=profile.digital_maturity * 0.9,
            ),
            Opportunity(
                sector=sector_key,
                title_ar=f"خدمة عملاء ذكية لـ {profile.name_ar}",
                title_en=f"AI Customer Service for {profile.name_en}",
                description_ar=f"تطبيق مساعد ذكي لخدمة العملاء باللغة العربية في قطاع {profile.name_ar}.",
                description_en=f"Deploy an intelligent Arabic customer service assistant in {profile.name_en}.",
                ai_readiness=profile.digital_maturity * 0.8,
            ),
        ]

        self.log.info("opportunities_identified", sector=sector_key, count=len(opportunities))
        return opportunities

    async def generate_report(self, sector: str) -> SectorReport:
        profile = await self.get_sector_profile(sector)
        opportunities = await self.identify_opportunities(sector)

        report = SectorReport(
            sector_key=profile.sector_key,
            profile=profile,
            opportunities=opportunities,
        )

        self.log.info("sector_report_generated", report_id=report.report_id, sector=sector)
        return report

    def _get_base_profile(self, sector_key: str) -> SectorProfile | None:
        base_profiles = {
            "healthcare": SectorProfile(
                sector_key="healthcare", name_ar="الرعاية الصحية", name_en="Healthcare",
                market_size_sar=180_000_000_000, growth_rate=0.10, digital_maturity=0.6,
                key_players=["MOH", "Dr. Sulaiman Al Habib", "Mouwasat", "Dallah"],
                pain_points=["جدولة المواعيد", "إدارة السجلات الطبية", "التواصل مع المرضى"],
                regulations=["MOH Licensing", "CCHI", "NPHI"],
                vision_2030_alignment="Health Sector Transformation Program",
            ),
            "real_estate": SectorProfile(
                sector_key="real_estate", name_ar="العقارات", name_en="Real Estate",
                market_size_sar=150_000_000_000, growth_rate=0.08, digital_maturity=0.5,
                key_players=["Dar Al Arkan", "ROSHN", "Emaar EC"],
                pain_points=["إدارة العقود", "التسويق العقاري", "تحليل السوق"],
                regulations=["REGA", "White Land Tax", "Sakani"],
                vision_2030_alignment="Housing Program — 70% ownership",
            ),
            "logistics": SectorProfile(
                sector_key="logistics", name_ar="اللوجستيات", name_en="Logistics",
                market_size_sar=30_000_000_000, growth_rate=0.15, digital_maturity=0.65,
                key_players=["SALIC", "Aramex", "SMSA", "Naqel"],
                pain_points=["تتبع الشحنات", "تحسين المسارات", "إدارة المخزون"],
                regulations=["TGA", "Zakat & Customs"],
                vision_2030_alignment="Logistics hub — top 25 globally",
            ),
            "fintech": SectorProfile(
                sector_key="fintech", name_ar="التقنية المالية", name_en="Fintech",
                market_size_sar=50_000_000_000, growth_rate=0.18, digital_maturity=0.8,
                key_players=["STC Pay", "Tamara", "Lean", "Geidea"],
                pain_points=["الامتثال التنظيمي", "اكتشاف الاحتيال", "خدمة العملاء"],
                regulations=["SAMA", "CMA", "Open Banking"],
                vision_2030_alignment="Financial Sector Development Program",
            ),
            "retail": SectorProfile(
                sector_key="retail", name_ar="التجزئة", name_en="Retail",
                market_size_sar=250_000_000_000, growth_rate=0.09, digital_maturity=0.6,
                key_players=["Panda", "Othaim", "Noon", "Amazon.sa"],
                pain_points=["إدارة المخزون", "خدمة العملاء", "التسويق"],
                regulations=["MoCI", "SASO", "VAT"],
                vision_2030_alignment="Quality of Life Program",
            ),
            "education": SectorProfile(
                sector_key="education", name_ar="التعليم", name_en="Education",
                market_size_sar=50_000_000_000, growth_rate=0.12, digital_maturity=0.7,
                key_players=["Ministry of Education", "Classera", "Noor"],
                pain_points=["إدارة الطلاب", "التقييم", "المحتوى التعليمي"],
                regulations=["Tatweer", "National Curriculum"],
                vision_2030_alignment="Human Capability Development",
            ),
            "technology": SectorProfile(
                sector_key="technology", name_ar="التقنية", name_en="Technology",
                market_size_sar=130_000_000_000, growth_rate=0.14, digital_maturity=0.85,
                key_players=["STC", "Mobily", "Elm", "SDAIA"],
                pain_points=["فجوة المواهب", "التوسع", "التوطين"],
                regulations=["NCA", "SDAIA", "PDPL"],
                vision_2030_alignment="Digital Transformation Program",
            ),
            "manufacturing": SectorProfile(
                sector_key="manufacturing", name_ar="التصنيع", name_en="Manufacturing",
                market_size_sar=220_000_000_000, growth_rate=0.07, digital_maturity=0.5,
                key_players=["SABIC", "Maaden", "Al-Yamamah Steel"],
                pain_points=["الصيانة التنبؤية", "مراقبة الجودة", "سلسلة التوريد"],
                regulations=["SASO", "MODON"],
                vision_2030_alignment="NIDLP",
            ),
            "oil_gas": SectorProfile(
                sector_key="oil_gas", name_ar="النفط والغاز", name_en="Oil & Gas",
                market_size_sar=800_000_000_000, growth_rate=0.03, digital_maturity=0.7,
                key_players=["Saudi Aramco", "SABIC", "Maaden"],
                pain_points=["الصيانة التنبؤية", "السلامة", "مراجعة المستندات"],
                regulations=["MoEnergy", "Aramco standards"],
                vision_2030_alignment="Sustainability + downstream localization",
            ),
            "tourism": SectorProfile(
                sector_key="tourism", name_ar="السياحة", name_en="Tourism",
                market_size_sar=90_000_000_000, growth_rate=0.20, digital_maturity=0.55,
                key_players=["STA", "Red Sea Global", "Diriyah Gate"],
                pain_points=["الدعم متعدد اللغات", "التنبؤ بالطلب", "التخصيص"],
                regulations=["STA", "SAGIA"],
                vision_2030_alignment="Tourism — 10% GDP target",
            ),
        }
        return base_profiles.get(sector_key)

    def get_profile(self, sector: str) -> SectorProfile | None:
        return self._profiles.get(sector.lower().replace(" ", "_"))

    def list_sectors(self) -> list[str]:
        return list(self.ALL_SECTORS)


# ── Legacy aliases for backward compatibility ──────────────────────
class SaudiSector:
    """Legacy alias."""


@dataclass
class SectorIntel:
    """Legacy alias for backward compatibility."""
    sector: str
    name_ar: str = ""
    name_en: str = ""
    market_size_sar: float = 0.0
    growth_rate: float = 0.0
    digital_maturity: float = 0.0
    key_players: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    regulations: list[str] = field(default_factory=list)
    vision_2030_alignment: str = ""
