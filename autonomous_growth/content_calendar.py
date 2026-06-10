"""
Smart Content Calendar — adjusts to campaigns, seasons, and sector opportunities.
تقويم المحتوى الذكي — يتكيف مع الحملات والمواسم وفرص القطاعات.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

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
class ScheduledItem:
    scheduled_date: date
    content: ContentItem
    channels: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scheduled_date": self.scheduled_date.isoformat(),
            "content": self.content.to_dict(),
            "channels": self.channels,
        }


@dataclass
class WeekSchedule:
    week_start: date
    scheduled_items: list[ScheduledItem] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "week_start": self.week_start.isoformat(),
            "scheduled_items": [i.to_dict() for i in self.scheduled_items],
        }


@dataclass
class ContentSchedule:
    weeks: list[WeekSchedule] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "weeks": [w.to_dict() for w in self.weeks],
        }


SEASONS = {
    "ramadan": {"months": [3, 4], "theme_ar": "رمضان", "theme_en": "Ramadan"},
    "hajj": {"months": [6, 7], "theme_ar": "الحج", "theme_en": "Hajj"},
    "q4_budget": {"months": [10, 11, 12], "theme_ar": "ميزانية Q4", "theme_en": "Q4 Budget Planning"},
    "vision_2030": {"months": [1, 2], "theme_ar": "رؤية 2030", "theme_en": "Vision 2030"},
    "summer": {"months": [6, 7, 8], "theme_ar": "الصيف", "theme_en": "Summer"},
    "back_to_work": {"months": [9], "theme_ar": "العودة للعمل", "theme_en": "Back to Work"},
}


class ContentCalendar:
    def __init__(self):
        self._schedules: list[WeekSchedule] = []
        self._active_season: str | None = None
        self._campaigns: list[dict[str, Any]] = []
        self.log = logger.bind(component="content_calendar")

    async def generate(self, weeks: int = 4) -> ContentSchedule:
        today = utcnow().date()
        schedule = ContentSchedule()

        for week_offset in range(weeks):
            week_start = today + timedelta(weeks=week_offset)
            week_start = week_start - timedelta(days=week_start.weekday())
            week_schedule = WeekSchedule(week_start=week_start)

            for day_offset in range(5):
                day_date = week_start + timedelta(days=day_offset)

                season = self._detect_season(day_date)
                campaign = self._find_active_campaign(day_date)

                topic = self._generate_topic(day_offset, season, campaign)
                content_type = self._content_type_for_day(day_offset)

                content = ContentItem(
                    id=generate_id("cnt"),
                    topic=topic,
                    content_type=content_type,
                    locale="ar",
                    body_markdown=f"# {topic}\n\nمحتوى يتم إنشاؤه لـ {day_date.isoformat()}",
                    tags=[season] if season else [],
                )

                channels = ["linkedin", "blog"]
                if day_offset == 2:
                    channels.append("email")

                week_schedule.scheduled_items.append(
                    ScheduledItem(scheduled_date=day_date, content=content, channels=channels)
                )

            self._schedules.append(week_schedule)
            schedule.weeks.append(week_schedule)

        self.log.info("calendar_generated", weeks=weeks, total_items=sum(len(w.scheduled_items) for w in schedule.weeks))
        return schedule

    async def get_week(self, week_date: date) -> WeekSchedule | None:
        week_start = week_date - timedelta(days=week_date.weekday())

        for ws in self._schedules:
            if ws.week_start == week_start:
                return ws

        return None

    async def adjust_for_season(self, season: str) -> None:
        if season not in SEASONS:
            self.log.warning("unknown_season", season=season)
            return

        self._active_season = season
        season_info = SEASONS[season]

        for ws in self._schedules:
            for item in ws.scheduled_items:
                month = item.scheduled_date.month
                if month in season_info["months"]:
                    item.content.tags.append(season)
                    item.content.topic = f"{season_info['theme_ar']} | {item.content.topic}"

        self.log.info("calendar_adjusted_for_season", season=season)

    def add_campaign(self, campaign: dict[str, Any]) -> None:
        self._campaigns.append(campaign)
        self.log.info("campaign_added", name=campaign.get("name"))

    def _detect_season(self, day: date) -> str:
        if self._active_season:
            return self._active_season
        for season_name, info in SEASONS.items():
            if day.month in info["months"]:
                return season_name
        return "default"

    def _find_active_campaign(self, day: date) -> dict[str, Any] | None:
        for campaign in self._campaigns:
            start = campaign.get("start_date")
            end = campaign.get("end_date")
            if start and end and start <= day <= end:
                return campaign
        return None

    def _generate_topic(self, day_offset: int, season: str, campaign: dict[str, Any] | None) -> str:
        if campaign:
            return campaign.get("topic", "Campaign content")

        topics_ar = {
            0: "أحدث توجهات الذكاء الاصطناعي في السعودية",
            1: "كيف تحسن أداء أعمالك باستخدام AI",
            2: "قصة نجاح: عميل حقق نتائج مذهلة",
            3: "نصائح للتحول الرقمي في شركتك",
            4: "فرص النمو في القطاعات السعودية",
        }
        return topics_ar.get(day_offset, "محتوى تسويقي")

    def _content_type_for_day(self, day_offset: int) -> str:
        types = {
            0: "article",
            1: "linkedin_post",
            2: "case_study",
            3: "newsletter",
            4: "sector_insight",
        }
        return types.get(day_offset, "article")

    def get_stats(self) -> dict[str, Any]:
        total_items = sum(len(ws.scheduled_items) for ws in self._schedules)
        return {
            "total_weeks": len(self._schedules),
            "total_items": total_items,
            "active_season": self._active_season,
            "active_campaigns": len(self._campaigns),
        }
