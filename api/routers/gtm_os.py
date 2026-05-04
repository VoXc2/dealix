"""GTM OS v5 — content_calendar + message_experiment endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.gtm_os import (
    build_weekly_calendar,
    draft_experiment,
)

router = APIRouter(prefix="/api/v1/gtm", tags=["gtm-os"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "gtm_os",
        "guardrails": {
            "draft_only": True,
            "no_auto_publish": True,
            "no_scaled_low_value_ai_pages": True,
            "no_scraping": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/content-calendar")
async def content_calendar(slots_per_week: int = 5) -> dict:
    """Generate a draft weekly content calendar.

    Anchors each slot to a real signal (lowest-scoring landing
    page from geo_aio_radar). NEVER publishes.
    """
    slots_per_week = max(1, min(int(slots_per_week), 14))
    return build_weekly_calendar(slots_per_week=slots_per_week)


@router.post("/experiment/draft")
async def experiment_draft(payload: dict = Body(...)) -> dict:
    required = (
        "name", "hypothesis_ar", "hypothesis_en",
        "variant_a_ar", "variant_a_en", "variant_b_ar", "variant_b_en",
        "success_metric", "target_audience",
    )
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise HTTPException(
            status_code=400, detail=f"missing required fields: {missing}",
        )
    exp = draft_experiment(
        name=payload["name"],
        hypothesis_ar=payload["hypothesis_ar"],
        hypothesis_en=payload["hypothesis_en"],
        variant_a_ar=payload["variant_a_ar"],
        variant_a_en=payload["variant_a_en"],
        variant_b_ar=payload["variant_b_ar"],
        variant_b_en=payload["variant_b_en"],
        success_metric=payload["success_metric"],
        target_audience=payload["target_audience"],
        expected_sample_size=int(payload.get("expected_sample_size", 0)),
        channel_hint=str(payload.get("channel_hint", "founder_warm_intro")),
    )
    return exp.model_dump(mode="json")
