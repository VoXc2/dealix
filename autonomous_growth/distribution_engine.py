"""
Content Distribution Engine — schedules and distributes content across channels.
محرك توزيع المحتوى — يجدول ويوزع المحتوى عبر القنوات.
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
class ScheduleResult:
    schedule_id: str
    content_id: str
    channels: list[str]
    scheduled_dates: dict[str, date]
    status: str = "scheduled"
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schedule_id": self.schedule_id,
            "content_id": self.content_id,
            "channels": self.channels,
            "scheduled_dates": {k: v.isoformat() for k, v in self.scheduled_dates.items()},
            "status": self.status,
            "warnings": self.warnings,
        }


@dataclass
class DistributionResult:
    success: bool
    schedule_id: str = ""
    channel_results: dict[str, bool] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "schedule_id": self.schedule_id,
            "channel_results": self.channel_results,
            "errors": self.errors,
        }


@dataclass
class CalendarEntry:
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
class ContentCalendar:
    entries: list[CalendarEntry] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entries": [e.to_dict() for e in self.entries],
        }


class DistributionEngine:
    CHANNELS = ["linkedin", "blog", "email", "whatsapp"]

    def __init__(self):
        self._schedules: dict[str, ScheduleResult] = {}
        self._calendar: ContentCalendar = ContentCalendar()
        self.log = logger.bind(component="distribution_engine")

    async def schedule(self, content: ContentItem, channels: list[str]) -> ScheduleResult:
        valid_channels = [c for c in channels if c in self.CHANNELS]
        invalid = [c for c in channels if c not in self.CHANNELS]

        schedule_id = generate_id("sched")
        today = utcnow().date()
        scheduled_dates: dict[str, date] = {}

        for i, channel in enumerate(valid_channels):
            scheduled_dates[channel] = today + timedelta(days=i)

        warnings = []
        if invalid:
            warnings.append(f"Invalid channels ignored: {invalid}")

        if "whatsapp" in valid_channels:
            warnings.append("WhatsApp requires explicit approval before send")

        result = ScheduleResult(
            schedule_id=schedule_id,
            content_id=content.id,
            channels=valid_channels,
            scheduled_dates=scheduled_dates,
            warnings=warnings,
        )

        self._schedules[schedule_id] = result

        for channel, sched_date in scheduled_dates.items():
            entry = CalendarEntry(
                scheduled_date=sched_date,
                content=content,
                channels=[channel],
            )
            self._calendar.entries.append(entry)

        self.log.info(
            "content_scheduled",
            schedule_id=schedule_id,
            channels=valid_channels,
            warnings=warnings,
        )
        return result

    async def distribute(self, schedule_id: str) -> DistributionResult:
        schedule = self._schedules.get(schedule_id)
        if not schedule:
            return DistributionResult(success=False, errors=["Schedule not found"])

        channel_results: dict[str, bool] = {}
        errors: list[str] = []

        for channel in schedule.channels:
            try:
                success = await self._send_to_channel(channel, schedule)
                channel_results[channel] = success
                if not success:
                    errors.append(f"Failed to distribute to {channel}")
            except Exception as e:
                channel_results[channel] = False
                errors.append(f"Error distributing to {channel}: {e}")

        success = len(errors) == 0

        self.log.info(
            "distribution_complete",
            schedule_id=schedule_id,
            success=success,
            channel_results=channel_results,
        )
        return DistributionResult(
            success=success,
            schedule_id=schedule_id,
            channel_results=channel_results,
            errors=errors,
        )

    async def _send_to_channel(self, channel: str, schedule: ScheduleResult) -> bool:
        if channel == "linkedin":
            return await self._post_linkedin(schedule)
        elif channel == "blog":
            return await self._publish_blog(schedule)
        elif channel == "email":
            return await self._send_email(schedule)
        elif channel == "whatsapp":
            return await self._send_whatsapp(schedule)
        return False

    async def _post_linkedin(self, schedule: ScheduleResult) -> bool:
        self.log.info("linkedin_post_queued", schedule_id=schedule.schedule_id)
        return True

    async def _publish_blog(self, schedule: ScheduleResult) -> bool:
        self.log.info("blog_publish_queued", schedule_id=schedule.schedule_id)
        return True

    async def _send_email(self, schedule: ScheduleResult) -> bool:
        self.log.info("email_send_queued", schedule_id=schedule.schedule_id)
        return True

    async def _send_whatsapp(self, schedule: ScheduleResult) -> bool:
        self.log.info("whatsapp_send_gated_requires_approval", schedule_id=schedule.schedule_id)
        return False

    async def get_calendar(self, start: date, end: date) -> ContentCalendar:
        filtered = ContentCalendar()
        for entry in self._calendar.entries:
            if start <= entry.scheduled_date <= end:
                filtered.entries.append(entry)
        return filtered

    def get_schedule(self, schedule_id: str) -> ScheduleResult | None:
        return self._schedules.get(schedule_id)

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_schedules": len(self._schedules),
            "calendar_entries": len(self._calendar.entries),
            "channels": self.CHANNELS,
        }


# ── Legacy alias for backward compatibility ──────────────────────────
class AutonomousDistributionEngine(DistributionEngine):
    """Legacy alias retained for pipeline imports."""


@dataclass
class DistributionEngineResult:
    """Result from the distribution engine."""
    success: bool
    schedule_id: str
    channels_used: list[str]
    error: str | None = None
