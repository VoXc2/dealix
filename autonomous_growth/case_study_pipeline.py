"""
Case Study Pipeline — converts L3+ proof events into LinkedIn-ready case studies.
خط أنابيب دراسة الحالة — يحول أحداث الإثبات L3+ إلى دراسات حالة جاهزة للينكدإن.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class CaseStudy:
    id: str
    title_ar: str
    title_en: str
    customer_handle: str
    sector: str
    challenge_ar: str
    challenge_en: str
    solution_ar: str
    solution_en: str
    results_ar: str
    results_en: str
    metrics: dict[str, Any] = field(default_factory=dict)
    evidence_level: int = 3
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "customer_handle": self.customer_handle,
            "sector": self.sector,
            "challenge_ar": self.challenge_ar,
            "challenge_en": self.challenge_en,
            "solution_ar": self.solution_ar,
            "solution_en": self.solution_en,
            "results_ar": self.results_ar,
            "results_en": self.results_en,
            "metrics": self.metrics,
            "evidence_level": self.evidence_level,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class LinkedInPost:
    id: str
    case_study_id: str
    body_ar: str
    body_en: str
    hashtags: list[str] = field(default_factory=list)
    media_urls: list[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "case_study_id": self.case_study_id,
            "body_ar": self.body_ar,
            "body_en": self.body_en,
            "hashtags": self.hashtags,
            "media_urls": self.media_urls,
            "status": self.status,
        }


@dataclass
class BlogPost:
    id: str
    case_study_id: str
    title_ar: str
    title_en: str
    body_markdown_ar: str
    body_markdown_en: str
    seo_keywords: list[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "case_study_id": self.case_study_id,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "body_markdown_ar": self.body_markdown_ar,
            "body_markdown_en": self.body_markdown_en,
            "seo_keywords": self.seo_keywords,
            "status": self.status,
        }


class CaseStudyPipeline:
    def __init__(self):
        self._case_studies: dict[str, CaseStudy] = {}
        self._linkedin_posts: dict[str, LinkedInPost] = {}
        self._blog_posts: dict[str, BlogPost] = {}
        self.log = logger.bind(component="case_study_pipeline")

    async def generate(self, proof_id: str) -> CaseStudy:
        case_study = CaseStudy(
            id=generate_id("cs"),
            title_ar=f"دراسة حالة: كيف ساعدنا 【{proof_id}】 في تحقيق نتائج ملموسة",
            title_en=f"Case Study: How We Helped 【{proof_id}】 Achieve Tangible Results",
            customer_handle=proof_id,
            sector="general",
            challenge_ar="التحدي: كان 【العميل】 يعاني من 【المشكلة】 مما أثر على كفاءة العمليات.",
            challenge_en="Challenge: 【Customer】 was struggling with 【problem】, impacting operational efficiency.",
            solution_ar="الحل: طبقنا 【حل Dealix】 المخصص لقطاع 【القطاع】 بنهج تدريجي.",
            solution_en="Solution: We deployed 【Dealix solution】 tailored to 【sector】 with a phased approach.",
            results_ar="النتائج: تحسن 【المؤشر】 بنسبة 【X%】 خلال 【المدة】.",
            results_en="Results: 【Metric】 improved by 【X%】 within 【period】.",
            metrics={"improvement_pct": 0, "timeframe_days": 30},
            evidence_level=3,
            status="draft",
        )
        self._case_studies[case_study.id] = case_study
        self.log.info("case_study_generated", id=case_study.id, proof_id=proof_id)
        return case_study

    async def render_linkedin(self, case_study_id: str) -> LinkedInPost:
        cs = self._case_studies.get(case_study_id)
        if not cs:
            raise ValueError(f"Case study {case_study_id} not found")

        post = LinkedInPost(
            id=generate_id("li"),
            case_study_id=case_study_id,
            body_ar=(
                f"🚀 **{cs.title_ar}**\n\n"
                f"{cs.challenge_ar}\n\n"
                f"{cs.solution_ar}\n\n"
                f"{cs.results_ar}\n\n"
                f"المؤشرات الرئيسية:\n"
                + "\n".join(f"• {k}: {v}" for k, v in cs.metrics.items())
                + "\n\n"
                f"احجز استشارة مجانية لمعرفة كيف يمكننا مساعدتك"
            ),
            body_en=(
                f"🚀 **{cs.title_en}**\n\n"
                f"{cs.challenge_en}\n\n"
                f"{cs.solution_en}\n\n"
                f"{cs.results_en}\n\n"
                f"Key metrics:\n"
                + "\n".join(f"• {k}: {v}" for k, v in cs.metrics.items())
                + "\n\n"
                f"Book a free consultation to learn how we can help you"
            ),
            hashtags=["#Dealix", "#AI", "#SaudiVision2030", f"#{cs.sector}"],
            status="draft",
        )
        self._linkedin_posts[post.id] = post
        self.log.info("linkedin_post_rendered", post_id=post.id, case_study_id=case_study_id)
        return post

    async def render_blog(self, case_study_id: str) -> BlogPost:
        cs = self._case_studies.get(case_study_id)
        if not cs:
            raise ValueError(f"Case study {case_study_id} not found")

        post = BlogPost(
            id=generate_id("blog"),
            case_study_id=case_study_id,
            title_ar=cs.title_ar,
            title_en=cs.title_en,
            body_markdown_ar=(
                f"# {cs.title_ar}\n\n"
                f"## التحدي\n{cs.challenge_ar}\n\n"
                f"## الحل\n{cs.solution_ar}\n\n"
                f"## النتائج\n{cs.results_ar}\n\n"
                f"### المؤشرات الرئيسية\n"
                + "\n".join(f"- **{k}**: {v}" for k, v in cs.metrics.items())
                + "\n\n"
                f"---\n*هذه دراسة حالة من Dealix. تواصل معنا لمعرفة المزيد.*"
            ),
            body_markdown_en=(
                f"# {cs.title_en}\n\n"
                f"## The Challenge\n{cs.challenge_en}\n\n"
                f"## The Solution\n{cs.solution_en}\n\n"
                f"## The Results\n{cs.results_en}\n\n"
                f"### Key Metrics\n"
                + "\n".join(f"- **{k}**: {v}" for k, v in cs.metrics.items())
                + "\n\n"
                f"---\n*This is a Dealix case study. Contact us to learn more.*"
            ),
            seo_keywords=[cs.sector, "AI case study", "Saudi Arabia", "digital transformation"],
            status="draft",
        )
        self._blog_posts[post.id] = post
        self.log.info("blog_post_rendered", post_id=post.id, case_study_id=case_study_id)
        return post

    def get_case_study(self, case_study_id: str) -> CaseStudy | None:
        return self._case_studies.get(case_study_id)

    def get_linkedin_post(self, post_id: str) -> LinkedInPost | None:
        return self._linkedin_posts.get(post_id)

    def get_blog_post(self, post_id: str) -> BlogPost | None:
        return self._blog_posts.get(post_id)

    def list_case_studies(self) -> list[CaseStudy]:
        return list(self._case_studies.values())

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_case_studies": len(self._case_studies),
            "total_linkedin_posts": len(self._linkedin_posts),
            "total_blog_posts": len(self._blog_posts),
            "by_status": {
                "draft": sum(1 for cs in self._case_studies.values() if cs.status == "draft"),
                "published": sum(1 for cs in self._case_studies.values() if cs.status == "published"),
            },
        }
