"""Weekly Business Reports API Router.

Auto-generates comprehensive weekly business reports from operational data.
All reports require founder review before distribution.

Prefix: /api/v1/reports
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/reports", tags=["Analytics"])

_ADMIN_KEY = os.getenv("DEALIX_ADMIN_API_KEY", "")


def _require_admin(x_api_key: str = Header(default="", alias="X-Admin-API-Key")) -> None:
    if not _ADMIN_KEY:
        return
    if x_api_key != _ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin API key")


class WeekDataInput(BaseModel):
    week_label: str = ""

    # Revenue
    mrr_sar: float = 0
    new_deals_sar: float = 0
    pipeline_value_sar: float = 0
    deals_closed_count: int = 0
    deals_lost_count: int = 0

    # Leads
    leads_generated: int = 0
    leads_qualified: int = 0
    leads_hot: int = 0

    # Delivery
    sprints_active: int = 0
    sprints_completed: int = 0
    deliverables_on_time: int = 0
    deliverables_total: int = 0

    # Customer success
    avg_health_score: float = 0
    nps_responses: int = 0
    avg_nps: float | None = None

    # Content/marketing
    posts_published: int = 0
    content_engagement: int = 0
    website_leads: int = 0


@router.post("/weekly/generate")
async def generate_weekly_report(
    data: WeekDataInput,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Generate a comprehensive weekly business report.

    Returns structured JSON report + Markdown (AR+EN) for founder review.
    Report requires founder approval before distribution.
    """
    from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator

    gen = WeeklyReportGenerator()

    # Convert pydantic model to dict for generator
    week_dict = {
        "week_label": data.week_label or _current_week_label(),
        "revenue": {
            "mrr_sar": data.mrr_sar,
            "new_deals_sar": data.new_deals_sar,
            "pipeline_value_sar": data.pipeline_value_sar,
            "deals_closed_count": data.deals_closed_count,
            "deals_lost_count": data.deals_lost_count,
        },
        "leads": {
            "generated": data.leads_generated,
            "qualified": data.leads_qualified,
            "hot": data.leads_hot,
        },
        "delivery": {
            "sprints_active": data.sprints_active,
            "sprints_completed": data.sprints_completed,
            "deliverables_on_time": data.deliverables_on_time,
            "deliverables_total": data.deliverables_total,
        },
        "customer_success": {
            "avg_health_score": data.avg_health_score,
            "nps_responses": data.nps_responses,
            "avg_nps": data.avg_nps,
        },
        "content": {
            "posts_published": data.posts_published,
            "engagement": data.content_engagement,
            "website_leads": data.website_leads,
        },
    }

    report = gen.generate(week_dict)
    result = report.to_dict()
    result["governance_note"] = "Requires founder review before distribution"
    result["approval_status"] = "approval_required"
    return result


@router.post("/weekly/generate/markdown", response_class=PlainTextResponse)
async def generate_weekly_report_markdown(
    data: WeekDataInput,
    _: None = Depends(_require_admin),
) -> str:
    """Generate weekly report as Markdown (AR+EN) — for copy/paste or PDF export."""
    from dealix.commercial_ops.weekly_report_generator import WeeklyReportGenerator
    gen = WeeklyReportGenerator()
    week_dict = {"week_label": data.week_label or _current_week_label()}
    report = gen.generate(week_dict)
    return report.as_markdown()


@router.get("/weekly/template")
async def get_weekly_template() -> dict[str, Any]:
    """Returns an empty weekly report template with field descriptions."""
    return {
        "week_label": f"Week ending {_current_week_label()}",
        "fields": {
            "mrr_sar": "Monthly Recurring Revenue in SAR",
            "new_deals_sar": "New deals signed this week in SAR",
            "pipeline_value_sar": "Total pipeline value in SAR",
            "deals_closed_count": "Number of deals closed",
            "deals_lost_count": "Number of deals lost",
            "leads_generated": "New leads generated",
            "leads_qualified": "Leads that passed qualification",
            "leads_hot": "HOT leads (score 80+)",
            "sprints_active": "Active client sprints",
            "sprints_completed": "Sprints completed this week",
            "deliverables_on_time": "Deliverables delivered on time",
            "deliverables_total": "Total deliverables due",
            "avg_health_score": "Average customer health score (0-100)",
            "nps_responses": "NPS survey responses received",
            "avg_nps": "Average NPS score (-100 to 100) or null",
            "posts_published": "LinkedIn/social posts published",
            "content_engagement": "Total engagement on content",
            "website_leads": "Leads from website this week",
        },
        "instructions_ar": "أدخل البيانات الأسبوعية ثم اطلب التقرير — يتطلب مراجعة المؤسس",
        "instructions_en": "Enter weekly data then request report — requires founder review",
    }


def _current_week_label() -> str:
    today = datetime.now(UTC)
    monday = today - timedelta(days=today.weekday())
    return monday.strftime("%Y-%m-%d")
