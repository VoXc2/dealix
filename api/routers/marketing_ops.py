"""Marketing Factory admin API — calendar, UTM, weekly drafts (governed)."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from dealix.marketing_factory.schemas import CalendarSlotRecord, ContentStatus, UtmLinkRecord
from dealix.marketing_factory.store import get_marketing_store, uid
from dealix.marketing_factory.utm import build_utm_url
from dealix.marketing_factory.weekly_pack import generate_weekly_pack
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent
from dealix.revenue_ops_autopilot.store import get_autopilot_store
from dealix.revenue_ops_autopilot.store import uid as ev_uid

router_marketing = APIRouter(
    prefix="/api/v1/ops-autopilot/marketing",
    dependencies=[Depends(require_admin_key)],
    tags=["marketing-factory"],
)


def _log_marketing_evidence(*, event_type: str, summary: str, entity_id: str = "") -> None:
    get_autopilot_store().append_evidence(
        EvidenceEvent(
            id=ev_uid("ev"),
            event_type=event_type,
            entity_type="marketing_factory",
            entity_id=entity_id,
            source="marketing_ops",
            summary=summary,
        ),
    )


class CalendarCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scheduled_date: str = Field(..., min_length=8, max_length=12)
    channel: str = Field(..., min_length=1, max_length=64)
    title_ar: str = Field(..., min_length=1, max_length=300)
    body_draft_ar: str = Field(..., min_length=1, max_length=8000)
    cta_label_ar: str = "اطلب Risk Score"
    cta_path: str = "/dealix-diagnostic"
    utm_campaign: str = ""
    utm_medium: str = "social"
    utm_source: str = "dealix"
    status: ContentStatus = "draft"


class UtmBuildPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_url: str = Field(default="https://dealix.ai")
    utm_source: str = "dealix"
    utm_medium: str = "social"
    utm_campaign: str = Field(..., min_length=1, max_length=120)
    utm_content: str = ""
    calendar_slot_id: str | None = None


class WeeklyPackApplyPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    queue_approvals: bool = True


class CalendarPatchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ContentStatus
    evidence_note: str = ""


@router_marketing.get("/calendar")
async def marketing_list_calendar(
    limit: Annotated[int, Query(ge=1, le=300)] = 80,
) -> dict[str, Any]:
    st = get_marketing_store()
    st.ensure_seed_loaded()
    rows = st.list_calendar(limit=limit)
    social_items: list[dict[str, Any]] = []
    try:
        from dealix.commercial_ops.social_queue import load_social_queue

        for post in load_social_queue().get("posts") or []:
            if not isinstance(post, dict):
                continue
            social_items.append(
                {
                    "id": f"social_w{post.get('week')}d{post.get('day')}",
                    "source": "social_content_queue.yaml",
                    "scheduled_date": post.get("calendar_date") or "",
                    "channel": "linkedin",
                    "title_ar": post.get("title_ar") or "",
                    "body_draft_ar": post.get("body_ar") or "",
                    "status": post.get("status") or "draft",
                    "pillar": post.get("pillar"),
                },
            )
    except Exception:
        social_items = []
    return {
        "count": len(rows),
        "items": [r.model_dump(mode="json") for r in rows],
        "social_queue_items": social_items,
        "primary_content_source": "dealix/config/social_content_queue.yaml",
        "stats": st.stats(),
    }


@router_marketing.post("/calendar")
async def marketing_create_calendar_slot(body: CalendarCreatePayload) -> dict[str, Any]:
    st = get_marketing_store()
    slot = CalendarSlotRecord(
        id=uid("cal"),
        scheduled_date=body.scheduled_date,
        channel=body.channel,
        title_ar=body.title_ar,
        body_draft_ar=body.body_draft_ar,
        cta_label_ar=body.cta_label_ar,
        cta_path=body.cta_path,
        utm_campaign=body.utm_campaign,
        utm_medium=body.utm_medium,
        utm_source=body.utm_source,
        status=body.status,
    )
    st.upsert_calendar_slot(slot)
    _log_marketing_evidence(
        event_type="content_calendar_slot_created",
        summary=f"channel={body.channel} date={body.scheduled_date}",
        entity_id=slot.id,
    )
    return {"item": slot.model_dump(mode="json")}


@router_marketing.patch("/calendar/{slot_id}")
async def marketing_patch_calendar_slot(slot_id: str, body: CalendarPatchPayload) -> dict[str, Any]:
    st = get_marketing_store()
    rows = {r.id: r for r in st.list_calendar(limit=500)}
    hit = rows.get(slot_id)
    if not hit:
        raise HTTPException(status_code=404, detail="calendar_slot_not_found")
    updated = hit.model_copy(
        update={
            "status": body.status,
            "evidence_note": body.evidence_note or hit.evidence_note,
            "updated_at": datetime.now(UTC),
        },
    )
    st.upsert_calendar_slot(updated)
    _log_marketing_evidence(
        event_type="content_calendar_status_updated",
        summary=f"id={slot_id} status={body.status}",
        entity_id=slot_id,
    )
    return {"item": updated.model_dump(mode="json")}


@router_marketing.get("/calendar/{slot_id}/publish-kit")
async def marketing_publish_kit(slot_id: str) -> dict[str, Any]:
    """Copy-ready post text + latest UTM for manual publish."""

    st = get_marketing_store()
    hit = next((r for r in st.list_calendar(limit=500) if r.id == slot_id), None)
    if not hit:
        raise HTTPException(status_code=404, detail="calendar_slot_not_found")
    utm = next(
        (u for u in st.list_utm_links(limit=200) if u.calendar_slot_id == slot_id),
        None,
    )
    disclosure_ar = (
        "إفصاح: محتوى ترويجي · شراكة/تسويق مع Dealix — راجع السياسات قبل النشر."
    )
    post = f"{hit.title_ar}\n\n{hit.body_draft_ar}\n\n{hit.cta_label_ar}"
    return {
        "slot_id": slot_id,
        "post_text_ar": post.strip(),
        "utm_url": utm.full_url if utm else None,
        "disclosure_ar": disclosure_ar,
        "status": hit.status,
        "policy_ar": "انسخ والصق يدوياً بعد الموافقة — لا نشر تلقائي.",
    }


@router_marketing.post("/utm")
async def marketing_build_utm(body: UtmBuildPayload) -> dict[str, Any]:
    full = build_utm_url(
        body.base_url,
        utm_source=body.utm_source,
        utm_medium=body.utm_medium,
        utm_campaign=body.utm_campaign,
        utm_content=body.utm_content,
    )
    st = get_marketing_store()
    rec = UtmLinkRecord(
        id=uid("utm"),
        base_url=body.base_url,
        full_url=full,
        utm_source=body.utm_source,
        utm_medium=body.utm_medium,
        utm_campaign=body.utm_campaign,
        utm_content=body.utm_content,
        calendar_slot_id=body.calendar_slot_id,
    )
    st.append_utm_link(rec)
    _log_marketing_evidence(
        event_type="utm_link_created",
        summary=f"campaign={body.utm_campaign}",
        entity_id=rec.id,
    )
    return {"item": rec.model_dump(mode="json"), "full_url": full}


@router_marketing.get("/weekly-pack")
async def marketing_weekly_pack_preview() -> dict[str, Any]:
    return generate_weekly_pack()


@router_marketing.post("/weekly-pack/apply")
async def marketing_weekly_pack_apply(body: WeeklyPackApplyPayload) -> dict[str, Any]:
    pack = generate_weekly_pack()
    st = get_marketing_store()
    created: list[str] = []
    approval_ids: list[str] = []

    for row in pack["slots"]:
        slot = CalendarSlotRecord(
            id=uid("cal"),
            scheduled_date=str(row["scheduled_date"]),
            channel=str(row["channel"]),
            title_ar=str(row["title_ar"]),
            body_draft_ar=str(row["body_draft_ar"]),
            cta_label_ar=str(row["cta_label_ar"]),
            cta_path=str(row["cta_path"]),
            utm_campaign=str(row["utm_campaign"]),
            utm_medium=str(row["utm_medium"]),
            utm_source=str(row["utm_source"]),
            status="approval_pending" if body.queue_approvals else "draft",
        )
        st.upsert_calendar_slot(slot)
        created.append(slot.id)

        base = os.getenv("DEALIX_PUBLIC_BASE_URL", "https://dealix.ai").rstrip("/")
        path = slot.cta_path.lstrip("/")
        full = build_utm_url(
            f"{base}/{path}",
            utm_source=slot.utm_source,
            utm_medium=slot.utm_medium,
            utm_campaign=slot.utm_campaign,
            utm_content=slot.channel,
        )
        st.append_utm_link(
            UtmLinkRecord(
                id=uid("utm"),
                base_url=base,
                full_url=full,
                utm_source=slot.utm_source,
                utm_medium=slot.utm_medium,
                utm_campaign=slot.utm_campaign,
                utm_content=slot.channel,
                calendar_slot_id=slot.id,
            ),
        )

        if body.queue_approvals:
            try:
                from auto_client_acquisition.approval_center import get_default_approval_store
                from auto_client_acquisition.approval_center.schemas import ApprovalRequest

                apr = ApprovalRequest(
                    object_type="marketing_content",
                    object_id=slot.id,
                    action_type="external_publish",
                    action_mode="approval_required",
                    channel=slot.channel,
                    summary_ar=f"مراجعة نشر: {slot.title_ar[:80]}",
                    summary_en=f"Review publish draft: {slot.title_ar[:80]}",
                    risk_level="medium",
                    proof_impact="marketing_governed_publish",
                )
                saved = get_default_approval_store().create(apr)
                approval_ids.append(getattr(saved, "id", "") or "")
            except Exception:
                pass

    _log_marketing_evidence(
        event_type="weekly_content_pack_applied",
        summary=f"slots={len(created)} approvals={len(approval_ids)}",
    )
    return {
        "week_start": pack["week_start"],
        "created_slot_ids": created,
        "approval_ids": [a for a in approval_ids if a],
        "policy_ar": "لا نشر خارجي تلقائي — الموافقة ثم النشر اليدوي فقط.",
    }
