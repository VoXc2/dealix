"""
Marketing Orchestrator — master coordinator for all marketing activities.
منسّق التسويق الرئيسي — ينسق جميع أنشطة التسويق.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

from autonomous_growth.content_calendar import ContentCalendar
from autonomous_growth.distribution_engine import DistributionEngine, DistributionResult
from autonomous_growth.seo_cluster_engine import SEOClusterEngine
from autonomous_growth.social_proof_aggregator import SocialProofAggregator
from autonomous_growth.case_study_pipeline import CaseStudyPipeline
from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class ContentItem:
    id: str
    topic: str
    content_type: str
    locale: str
    body_markdown: str
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "content_type": self.content_type,
            "locale": self.locale,
            "body_markdown": self.body_markdown,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ContentQueueItem:
    id: str
    content: ContentItem
    channels: list[str]
    scheduled_for: date | None = None
    status: str = "queued"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content.to_dict(),
            "channels": self.channels,
            "scheduled_for": self.scheduled_for.isoformat() if self.scheduled_for else None,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class DailyMarketingPlan:
    date: date
    content_queue: list[ContentQueueItem] = field(default_factory=list)
    seo_clusters_to_build: list[str] = field(default_factory=list)
    case_studies_to_generate: list[str] = field(default_factory=list)
    social_proof_refresh: bool = False
    distribution_tasks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date.isoformat(),
            "content_queue": [c.to_dict() for c in self.content_queue],
            "seo_clusters_to_build": self.seo_clusters_to_build,
            "case_studies_to_generate": self.case_studies_to_generate,
            "social_proof_refresh": self.social_proof_refresh,
            "distribution_tasks": self.distribution_tasks,
        }


@dataclass
class WeeklyMarketingPlan:
    week_start: date
    daily_plans: list[DailyMarketingPlan] = field(default_factory=list)
    weekly_goals: dict[str, Any] = field(default_factory=dict)
    campaigns: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "week_start": self.week_start.isoformat(),
            "daily_plans": [d.to_dict() for d in self.daily_plans],
            "weekly_goals": self.weekly_goals,
            "campaigns": self.campaigns,
        }


class MarketingOrchestrator:
    def __init__(self, db_session=None, llm_router=None):
        self.db_session = db_session
        self.llm_router = llm_router
        self.content_calendar = ContentCalendar()
        self.distribution_engine = DistributionEngine()
        self.seo_engine = SEOClusterEngine()
        self.proof_aggregator = SocialProofAggregator()
        self.case_study_pipeline = CaseStudyPipeline()
        self._queue: list[ContentQueueItem] = []
        self.log = logger.bind(component="marketing_orchestrator")

    async def orchestrate_daily(self) -> DailyMarketingPlan:
        today = utcnow().date()
        plan = DailyMarketingPlan(date=today)

        week_schedule = await self.content_calendar.get_week(today)
        if week_schedule:
            for item in week_schedule.scheduled_items:
                if item.scheduled_date == today:
                    q_item = ContentQueueItem(
                        id=generate_id("cq"),
                        content=item.content,
                        channels=item.channels,
                        scheduled_for=today,
                        status="scheduled",
                    )
                    self._queue.append(q_item)
                    plan.content_queue.append(q_item)

        sectors_needing_clusters = await self.seo_engine.identify_gaps("all")
        for gap in sectors_needing_clusters[:3]:
            plan.seo_clusters_to_build.append(gap.sector)

        proof_bundle = await self.proof_aggregator.aggregate()
        if proof_bundle.l3_plus_events:
            for event in proof_bundle.l3_plus_events[:2]:
                plan.case_studies_to_generate.append(event.proof_id)

        plan.social_proof_refresh = (today.day % 3 == 0)

        for q_item in plan.content_queue:
            result = await self.distribution_engine.distribute(q_item.id)
            if result.success:
                plan.distribution_tasks.append(q_item.id)

        self.log.info("daily_plan_generated", date=today.isoformat(), items=len(plan.content_queue))
        return plan

    async def orchestrate_weekly(self) -> WeeklyMarketingPlan:
        today = utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        plan = WeeklyMarketingPlan(week_start=week_start)

        for day_offset in range(7):
            day_date = week_start + timedelta(days=day_offset)
            day_plan = DailyMarketingPlan(date=day_date)

            week_schedule = await self.content_calendar.get_week(day_date)
            if week_schedule:
                for item in week_schedule.scheduled_items:
                    if item.scheduled_date == day_date:
                        q_item = ContentQueueItem(
                            id=generate_id("cq"),
                            content=item.content,
                            channels=item.channels,
                            scheduled_for=day_date,
                            status="planned",
                        )
                        day_plan.content_queue.append(q_item)

            plan.daily_plans.append(day_plan)

        all_clusters = await self.seo_engine.get_all_clusters()
        plan.weekly_goals = {
            "total_clusters": len(all_clusters),
            "sectors_covered": list(all_clusters.keys()),
            "proof_events_aggregated": 0,
        }

        plan.campaigns = [
            {
                "name": f"Sector Campaign - {s}",
                "sector": s,
                "status": "planned",
            }
            for s in list(all_clusters.keys())[:5]
        ]

        self.log.info("weekly_plan_generated", week=week_start.isoformat())
        return plan

    async def queue_content(self, content: ContentItem) -> ContentQueueItem:
        item = ContentQueueItem(
            id=generate_id("cq"),
            content=content,
            channels=["linkedin", "blog"],
            status="queued",
        )
        self._queue.append(item)
        self.log.info("content_queued", item_id=item.id, topic=content.topic)
        return item

    async def distribute_content(self, item_id: str) -> DistributionResult:
        for item in self._queue:
            if item.id == item_id:
                result = await self.distribution_engine.distribute(item_id)
                item.status = "distributed" if result.success else "failed"
                return result
        return DistributionResult(success=False, errors=["Content item not found"])

    def get_queue(self) -> list[ContentQueueItem]:
        return list(self._queue)

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_queued": len(self._queue),
            "pending": sum(1 for q in self._queue if q.status == "queued"),
            "scheduled": sum(1 for q in self._queue if q.status == "scheduled"),
            "distributed": sum(1 for q in self._queue if q.status == "distributed"),
            "failed": sum(1 for q in self._queue if q.status == "failed"),
        }


# ── Legacy alias for backward compatibility ──────────────────────
GrowthOrchestrator = MarketingOrchestrator
