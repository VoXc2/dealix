"""Weekly content calendar — draft slots anchored to real measurements."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.self_growth_os import geo_aio_radar


class ContentCalendarSlot(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    slot_date: str
    channel: str  # "landing_page" | "linkedin_manual_post" | "x_manual_post" | "email_draft"
    topic_ar: str
    topic_en: str
    audience: str
    rationale: str  # which signal triggered this slot
    approval_status: str = "approval_required"
    forbidden_actions: list[str] = Field(default_factory=lambda: [
        "scaled_low_value_ai_pages",
        "auto_publish",
        "scrape_competitor_content",
    ])


_BLOCK_TEMPLATE_AR = "تحسين صفحة {path} (نقاط GEO: {score})"
_BLOCK_TEMPLATE_EN = "Improve {path} page (GEO score: {score})"


def build_weekly_calendar(
    *,
    week_start: datetime | None = None,
    slots_per_week: int = 5,
) -> dict[str, Any]:
    """Return a draft weekly calendar of content slots.

    Each slot is anchored to a real signal (lowest-scoring landing
    page from geo_aio_radar). NEVER auto-publishes; every slot is
    approval_required.
    """
    week_start = week_start or datetime.now(UTC)
    pages = geo_aio_radar.top_priority_pages(limit=slots_per_week)
    slots: list[ContentCalendarSlot] = []

    for i, page in enumerate(pages):
        slot_date = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
        slots.append(ContentCalendarSlot(
            slot_date=slot_date,
            channel="landing_page",
            topic_ar=_BLOCK_TEMPLATE_AR.format(path=page["path"], score=page["score"]),
            topic_en=_BLOCK_TEMPLATE_EN.format(path=page["path"], score=page["score"]),
            audience="saudi_b2b_buyers",
            rationale=(
                f"page {page['path']} is among the lowest-scoring on "
                f"GEO/AIO readiness ({page['score']}) — gaps: "
                f"{', '.join(page.get('gaps', [])[:3])}"
            ),
        ))

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "week_start": week_start.strftime("%Y-%m-%d"),
        "slots_total": len(slots),
        "slots": [s.model_dump(mode="json") for s in slots],
        "guardrails": {
            "no_auto_publish": True,
            "every_slot_requires_approval": True,
            "no_scraping": True,
            "no_low_value_ai_pages": True,
        },
    }
