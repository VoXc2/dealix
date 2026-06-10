"""
Content Agent — Hermes-style content creation for all channels.
وكيل المحتوى — إنشاء محتوى بأسلوب Hermes لجميع القنوات.
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
class LinkedInPost:
    id: str
    body: str
    hashtags: list[str] = field(default_factory=list)
    media_urls: list[str] = field(default_factory=list)
    locale: str = "ar"
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "body": self.body,
            "hashtags": self.hashtags,
            "media_urls": self.media_urls,
            "locale": self.locale,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ArticleBrief:
    topic: str
    sector: str
    target_audience: str
    key_points: list[str] = field(default_factory=list)
    word_count: int = 800
    locale: str = "ar"


@dataclass
class BlogArticle:
    id: str
    title: str
    body_markdown: str
    seo_keywords: list[str] = field(default_factory=list)
    word_count: int = 0
    locale: str = "ar"
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "body_markdown": self.body_markdown,
            "seo_keywords": self.seo_keywords,
            "word_count": self.word_count,
            "locale": self.locale,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SEOArticle:
    id: str
    keyword: str
    title: str
    body_markdown: str
    meta_description: str = ""
    word_count: int = 0
    locale: str = "ar"
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "keyword": self.keyword,
            "title": self.title,
            "body_markdown": self.body_markdown,
            "meta_description": self.meta_description,
            "word_count": self.word_count,
            "locale": self.locale,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ProofData:
    customer_handle: str
    sector: str
    challenge: str
    solution: str
    results: str
    metrics: dict[str, Any] = field(default_factory=dict)
    evidence_level: int = 3


@dataclass
class CaseStudy:
    id: str
    title_ar: str
    title_en: str
    body_ar: str
    body_en: str
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "body_ar": self.body_ar,
            "body_en": self.body_en,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class ContentAgent(BaseAgent):
    name = "content_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generated: list[dict[str, Any]] = []

    async def write_linkedin_post(self, topic: str, audience: str) -> LinkedInPost:
        prompt = (
            f"Write a LinkedIn post in Arabic about: {topic}\n"
            f"Target audience: {audience}\n"
            f"Keep it under 300 words. Include hashtags. End with a soft CTA.\n"
            f"Format: engaging hook → insight → CTA."
        )
        response = await self.router.run(
            task=Task.SOCIAL_MEDIA,
            messages=[Message(role="user", content=prompt)],
            max_tokens=600,
            temperature=0.7,
        )
        body = response.content.strip()
        post = LinkedInPost(
            id=generate_id("li"),
            body=body,
            hashtags=["#Dealix", "#AI", "#SaudiVision2030"],
            locale="ar",
        )
        self._generated.append({"type": "linkedin_post", "id": post.id})
        self.log.info("linkedin_post_written", id=post.id, topic=topic)
        return post

    async def write_blog_article(self, brief: ArticleBrief) -> BlogArticle:
        prompt = (
            f"Write a blog article in {brief.locale} about: {brief.topic}\n"
            f"Sector: {brief.sector}\n"
            f"Target audience: {brief.target_audience}\n"
            f"Key points: {', '.join(brief.key_points)}\n"
            f"Target word count: {brief.word_count}\n"
            f"Include SEO keywords naturally. Structure with H2 headings."
        )
        response = await self.router.run(
            task=Task.PAGE_COPY,
            messages=[Message(role="user", content=prompt)],
            max_tokens=2000,
            temperature=0.6,
        )
        body = response.content.strip()
        title = self._extract_title(body) or brief.topic
        article = BlogArticle(
            id=generate_id("blog"),
            title=title,
            body_markdown=body,
            seo_keywords=[brief.sector, brief.topic],
            word_count=len(body.split()),
            locale=brief.locale,
        )
        self._generated.append({"type": "blog_article", "id": article.id})
        self.log.info("blog_article_written", id=article.id, topic=brief.topic)
        return article

    async def write_seo_article(self, keyword: str, sector: str) -> SEOArticle:
        prompt = (
            f"Write an SEO-optimized article in Arabic targeting keyword: '{keyword}'\n"
            f"Sector: {sector}\n"
            f"Structure: H1 title, H2 sections, FAQs at end.\n"
            f"Target word count: 1000-1200.\n"
            f"Meta description: compelling 150-char summary.\n"
            f"Use keyword naturally in H1, first paragraph, and one H2."
        )
        response = await self.router.run(
            task=Task.PAGE_COPY,
            messages=[Message(role="user", content=prompt)],
            max_tokens=2500,
            temperature=0.5,
        )
        body = response.content.strip()
        title = self._extract_title(body) or keyword
        article = SEOArticle(
            id=generate_id("seo"),
            keyword=keyword,
            title=title,
            body_markdown=body,
            meta_description=keyword,
            word_count=len(body.split()),
        )
        self._generated.append({"type": "seo_article", "id": article.id})
        self.log.info("seo_article_written", id=article.id, keyword=keyword)
        return article

    async def write_case_study(self, data: ProofData) -> CaseStudy:
        prompt_ar = (
            f"Write a case study in Arabic for customer: {data.customer_handle}\n"
            f"Sector: {data.sector}\n"
            f"Challenge: {data.challenge}\n"
            f"Solution: {data.solution}\n"
            f"Results: {data.results}\n"
            f"Metrics: {data.metrics}\n\n"
            f"Structure: title, challenge section, solution section, "
            f"results with numbers, closing with CTA."
        )
        response = await self.router.run(
            task=Task.ARABIC_TASKS,
            messages=[Message(role="user", content=prompt_ar)],
            max_tokens=2000,
            temperature=0.6,
        )
        body_ar = response.content.strip()
        title_ar = self._extract_title(body_ar) or f"دراسة حالة: {data.customer_handle}"

        prompt_en = (
            f"Write a case study in English for customer: {data.customer_handle}\n"
            f"Sector: {data.sector}\n"
            f"Challenge: {data.challenge}\n"
            f"Solution: {data.solution}\n"
            f"Results: {data.results}\n"
            f"Metrics: {data.metrics}\n\n"
            f"Structure: title, challenge, solution, results with numbers, CTA."
        )
        response_en = await self.router.run(
            task=Task.PAGE_COPY,
            messages=[Message(role="user", content=prompt_en)],
            max_tokens=1500,
            temperature=0.6,
        )
        body_en = response_en.content.strip()
        title_en = self._extract_title(body_en) or f"Case Study: {data.customer_handle}"

        case_study = CaseStudy(
            id=generate_id("cs"),
            title_ar=title_ar,
            title_en=title_en,
            body_ar=body_ar,
            body_en=body_en,
        )
        self._generated.append({"type": "case_study", "id": case_study.id})
        self.log.info("case_study_written", id=case_study.id, customer=data.customer_handle)
        return case_study

    async def generate_variants(self, content: str, count: int = 3) -> list[str]:
        variants = []
        for i in range(count):
            prompt = (
                f"Rewrite the following content in a different style (variant {i+1}):\n"
                f"Keep the same message but change tone and phrasing.\n\n"
                f"---\n{content}\n---"
            )
            response = await self.router.run(
                task=Task.PAGE_COPY,
                messages=[Message(role="user", content=prompt)],
                max_tokens=1000,
                temperature=0.8,
            )
            variants.append(response.content.strip())
        return variants

    def _extract_title(self, body: str) -> str | None:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped.lstrip("# ").strip()
            if stripped.startswith("**") and stripped.endswith("**"):
                return stripped.strip("*")
            if stripped and not stripped.startswith("#"):
                return stripped[:120]
        return None

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_generated": len(self._generated),
            "by_type": {
                "linkedin_post": sum(1 for g in self._generated if g["type"] == "linkedin_post"),
                "blog_article": sum(1 for g in self._generated if g["type"] == "blog_article"),
                "seo_article": sum(1 for g in self._generated if g["type"] == "seo_article"),
                "case_study": sum(1 for g in self._generated if g["type"] == "case_study"),
            },
        }


# ── Legacy aliases for backward compatibility ──────────────────────
ContentCreatorAgent = ContentAgent


@dataclass
class ContentPiece:
    """Legacy alias for backward compatibility."""
    content: str
    content_type: str
    metadata: dict | None = None
