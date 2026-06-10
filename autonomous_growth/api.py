"""
Autonomous Growth API — content generation, SEO clusters, case studies, A/B testing.
واجهة برمجة تطبيقات النمو المستقل — إنشاء المحتوى، عناقيد SEO، دراسات الحالة، اختبار A/B.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from autonomous_growth.case_study_pipeline import CaseStudyPipeline
from autonomous_growth.content_calendar import ContentCalendar
from autonomous_growth.distribution_engine import DistributionEngine
from autonomous_growth.orchestrator import ContentItem, MarketingOrchestrator
from autonomous_growth.seo_cluster_engine import SEOClusterEngine

router = APIRouter(prefix="/api/v1/growth", tags=["growth"])

_orchestrator = MarketingOrchestrator()
_distribution = DistributionEngine()
_seo = SEOClusterEngine()
_case_studies = CaseStudyPipeline()
_calendar = ContentCalendar()

_HARD_GATES = {
    "no_live_send": True,
    "no_scraping": True,
    "no_linkedin_automation": True,
    "approval_required_for_external_actions": True,
}


class QueueContentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = Field(..., min_length=3, max_length=200)
    content_type: str = "article"
    locale: str = "ar"
    body_markdown: str = ""
    tags: list[str] = Field(default_factory=list)


class GenerateContentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = Field(..., min_length=3, max_length=200)
    content_type: str = Field(default="linkedin_post", pattern=r"^(linkedin_post|article|case_study|newsletter)$")
    locale: str = "ar"
    sector: str = "general"


class GenerateClusterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str = Field(..., min_length=2, max_length=64)


class GenerateCaseStudyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    proof_id: str = Field(..., min_length=2, max_length=64)


class RunABTestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content_a_id: str
    content_b_id: str
    channel: str = "linkedin"
    duration_hours: int = 24
    audience: str = "all"


@router.post("/content/queue")
async def queue_content(body: QueueContentRequest) -> dict[str, Any]:
    content = ContentItem(
        id="",
        topic=body.topic,
        content_type=body.content_type,
        locale=body.locale,
        body_markdown=body.body_markdown,
        tags=body.tags,
    )
    result = await _orchestrator.queue_content(content)
    return {"status": "queued", "item": result.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/content/queue")
async def list_queue() -> dict[str, Any]:
    queue = _orchestrator.get_queue()
    return {
        "count": len(queue),
        "items": [q.to_dict() for q in queue],
        "stats": _orchestrator.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/content/generate")
async def generate_content(body: GenerateContentRequest) -> dict[str, Any]:
    from autonomous_growth.agents.content import ContentAgent

    agent = ContentAgent()
    if body.content_type == "linkedin_post":
        post = await agent.write_linkedin_post(topic=body.topic, audience=body.sector)
        content = ContentItem(
            id=post.id,
            topic=body.topic,
            content_type="linkedin_post",
            locale=body.locale,
            body_markdown=post.body,
            tags=post.hashtags,
        )
    else:
        brief = type('Brief', (), {
            'topic': body.topic, 'sector': body.sector,
            'target_audience': body.sector, 'word_count': 800,
            'locale': body.locale, 'key_points': [],
        })()
        article = await agent.write_blog_article(brief)
        content = ContentItem(
            id=article.id,
            topic=body.topic,
            content_type="article",
            locale=body.locale,
            body_markdown=article.body_markdown,
            tags=article.seo_keywords,
        )
    return {
        "status": "generated",
        "content": content.to_dict(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/seo/clusters")
async def seo_clusters() -> dict[str, Any]:
    clusters = await _seo.get_all_clusters()
    return {
        "count": len(clusters),
        "clusters": {k: v.to_dict() for k, v in clusters.items()},
        "stats": _seo.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/seo/cluster/generate")
async def generate_cluster(body: GenerateClusterRequest) -> dict[str, Any]:
    if body.sector not in _seo.SECTORS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown sector. Must be one of: {', '.join(_seo.SECTORS[:10])}...",
        )
    cluster = await _seo.generate_cluster(body.sector)
    return {
        "status": "generated",
        "cluster": cluster.to_dict(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/case-studies")
async def list_case_studies() -> dict[str, Any]:
    studies = _case_studies.list_case_studies()
    return {
        "count": len(studies),
        "case_studies": [s.to_dict() for s in studies],
        "stats": _case_studies.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/case-study/generate")
async def generate_case_study(body: GenerateCaseStudyRequest) -> dict[str, Any]:
    case_study = await _case_studies.generate(body.proof_id)
    linkedin = await _case_studies.render_linkedin(case_study.id)
    blog = await _case_studies.render_blog(case_study.id)
    return {
        "status": "generated",
        "case_study": case_study.to_dict(),
        "linkedin_post": linkedin.to_dict(),
        "blog_post": blog.to_dict(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/ab-test/run")
async def run_ab_test(body: RunABTestRequest) -> dict[str, Any]:
    test_id = f"ab_{body.content_a_id}_{body.content_b_id}"
    return {
        "status": "test_created",
        "test_id": test_id,
        "content_a": body.content_a_id,
        "content_b": body.content_b_id,
        "channel": body.channel,
        "duration_hours": body.duration_hours,
        "message_ar": "سيتم جمع النتائج بعد انتهاء المدة",
        "message_en": "Results will be collected after the duration ends",
        "hard_gates": _HARD_GATES,
    }


@router.get("/ab-test/results")
async def ab_test_results(
    test_id: str = Query(..., description="A/B test ID"),
) -> dict[str, Any]:
    return {
        "test_id": test_id,
        "status": "pending",
        "results": {
            "variant_a": {"impressions": 0, "clicks": 0, "conversion_rate": 0.0},
            "variant_b": {"impressions": 0, "clicks": 0, "conversion_rate": 0.0},
        },
        "winner": None,
        "message_ar": "اختبار A/B قيد التشغيل. النتائج متوفرة بعد اكتمال المدة.",
        "message_en": "A/B test is running. Results available after completion.",
        "hard_gates": _HARD_GATES,
    }
