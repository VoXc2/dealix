"""
SEO Cluster Engine — generates content clusters for each Saudi sector.
محرك عناقيد تحسين محركات البحث — يُنشئ عناقيد محتوى لكل قطاع سعودي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class ContentGap:
    sector: str
    gap_type: str
    keyword: str
    priority: int = 5

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector": self.sector,
            "gap_type": self.gap_type,
            "keyword": self.keyword,
            "priority": self.priority,
        }


@dataclass
class PillarPage:
    keyword: str
    title_ar: str
    title_en: str
    search_volume: int = 0
    difficulty: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "keyword": self.keyword,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "search_volume": self.search_volume,
            "difficulty": self.difficulty,
        }


@dataclass
class SupportingArticle:
    keyword: str
    title_ar: str
    title_en: str
    pillar_keyword: str
    word_count: int = 800

    def to_dict(self) -> dict[str, Any]:
        return {
            "keyword": self.keyword,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "pillar_keyword": self.pillar_keyword,
            "word_count": self.word_count,
        }


@dataclass
class SEOCluster:
    sector: str
    pillar: PillarPage
    supporting_articles: list[SupportingArticle] = field(default_factory=list)
    created_at: datetime = field(default_factory=utcnow)
    cluster_id: str = ""

    def __post_init__(self):
        if not self.cluster_id:
            self.cluster_id = generate_id("seo")

    def to_dict(self) -> dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "sector": self.sector,
            "pillar": self.pillar.to_dict(),
            "supporting_articles": [a.to_dict() for a in self.supporting_articles],
            "created_at": self.created_at.isoformat(),
        }


class SEOClusterEngine:
    SECTORS = [
        "healthcare", "real_estate", "logistics", "retail", "fintech",
        "education", "technology", "manufacturing", "oil_gas", "tourism",
        "construction", "consulting", "hospitality", "government",
        "saudi_saas", "ecommerce", "telecom", "agriculture",
        "transportation", "energy", "mining", "defense",
        "sports", "entertainment", "media", "nonprofit",
        "legal", "insurance", "pharma", "food_beverage",
    ]

    def __init__(self):
        self._clusters: dict[str, SEOCluster] = {}
        self.log = logger.bind(component="seo_cluster_engine")

    async def generate_cluster(self, sector: str) -> SEOCluster:
        sector_key = sector.lower().replace(" ", "_")
        pillar_keyword = f"الذكاء الاصطناعي في قطاع {sector} السعودي"
        pillar_en_keyword = f"AI in Saudi {sector} sector"

        pillar = PillarPage(
            keyword=pillar_keyword,
            title_ar=f"دليل شامل: تطبيقات الذكاء الاصطناعي في قطاع {sector} في السعودية",
            title_en=f"Complete Guide: AI Applications in Saudi {sector.title()} Sector",
            search_volume=100 + len(sector) * 10,
            difficulty=0.3 + (hash(sector) % 40) / 100,
        )

        articles = [
            SupportingArticle(
                keyword=f"أتمتة {sector} بالذكاء الاصطناعي",
                title_ar=f"كيف تؤتمت قطاع {sector} بالذكاء الاصطناعي: دليل عملي",
                title_en=f"How to Automate {sector.title()} with AI: A Practical Guide",
                pillar_keyword=pillar_keyword,
                word_count=1200,
            ),
            SupportingArticle(
                keyword=f"تحليل بيانات {sector}",
                title_ar=f"تحليل بيانات {sector} باستخدام الذكاء الاصطناعي",
                title_en=f"AI-Powered Data Analysis for {sector.title()}",
                pillar_keyword=pillar_keyword,
                word_count=1000,
            ),
            SupportingArticle(
                keyword=f"تكلفة حلول AI في {sector}",
                title_ar=f"تكلفة حلول الذكاء الاصطناعي في قطاع {sector}: مقارنة شاملة",
                title_en=f"Cost of AI Solutions in Saudi {sector.title()}: Complete Comparison",
                pillar_keyword=pillar_keyword,
                word_count=800,
            ),
            SupportingArticle(
                keyword=f"أفضل شركات AI في {sector} السعودية",
                title_ar=f"أفضل شركات الذكاء الاصطناعي في قطاع {sector} السعودي",
                title_en=f"Top AI Companies in Saudi {sector.title()} Sector",
                pillar_keyword=pillar_keyword,
                word_count=900,
            ),
            SupportingArticle(
                keyword=f"رؤية 2030 و {sector} الرقمي",
                title_ar=f"رؤية 2030 والتحول الرقمي في قطاع {sector} السعودي",
                title_en=f"Saudi Vision 2030 and Digital Transformation in {sector.title()}",
                pillar_keyword=pillar_keyword,
                word_count=1100,
            ),
        ]

        cluster = SEOCluster(
            sector=sector_key,
            pillar=pillar,
            supporting_articles=articles,
        )
        self._clusters[sector_key] = cluster
        self.log.info("cluster_generated", sector=sector_key, articles=len(articles))
        return cluster

    async def identify_gaps(self, sector: str) -> list[ContentGap]:
        gaps: list[ContentGap] = []

        if sector == "all":
            for s in self.SECTORS:
                if s not in self._clusters:
                    gaps.append(ContentGap(sector=s, gap_type="missing_cluster", keyword=s, priority=10))
            return gaps

        s = sector.lower().replace(" ", "_")
        if s not in self._clusters:
            gaps.append(ContentGap(sector=s, gap_type="missing_cluster", keyword=s, priority=10))
        else:
            cluster = self._clusters[s]
            if len(cluster.supporting_articles) < 3:
                gaps.append(ContentGap(
                    sector=s, gap_type="insufficient_articles",
                    keyword=cluster.pillar.keyword, priority=7,
                ))

        return gaps

    async def get_all_clusters(self) -> dict[str, SEOCluster]:
        return dict(self._clusters)

    def get_cluster(self, sector: str) -> SEOCluster | None:
        return self._clusters.get(sector.lower().replace(" ", "_"))

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_clusters": len(self._clusters),
            "sectors": list(self._clusters.keys()),
            "total_articles": sum(len(c.supporting_articles) for c in self._clusters.values()),
            "available_sectors": len(self.SECTORS),
        }
