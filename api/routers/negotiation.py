"""
Negotiation router — classify objection, suggest response, recommend close plan.

Endpoints:
    POST /api/v1/negotiation/classify
        body: {"text": "..."}
    POST /api/v1/negotiation/build-response
        body: {"text"?: "...", "objection_class"?: "..."}
        Returns suggested response + close plan (one call).
    POST /api/v1/negotiation/events
        body: {lead_id?, deal_id?, customer_id?, objection_class, raw_text?,
               response_variant?, outcome?}
        Persist an objection event (audit + future learning).
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.negotiation_engine.close_plan import recommend, to_dict
from auto_client_acquisition.negotiation_engine.objection_classifier import classify
from auto_client_acquisition.negotiation_engine.response_builder import build_response
from db.models import ObjectionEventRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/negotiation", tags=["negotiation"])


@router.post("/classify")
async def classify_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = str(body.get("text") or "")
    res = classify(text)
    return {
        "objection_class": res.objection_class,
        "matched_keyword": res.matched_keyword,
        "confidence": res.confidence,
    }


@router.post("/build-response")
async def respond(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    obj_class = str(body.get("objection_class") or "")
    text = str(body.get("text") or "")
    if not obj_class and text:
        obj_class = classify(text).objection_class
    response = build_response(obj_class)
    if response is None:
        raise HTTPException(status_code=400, detail="unknown_objection_class")
    plan = recommend(
        objection_class=obj_class,
        has_list=bool(body.get("has_list", False)),
        deal_stage=str(body.get("deal_stage", "new")),
    )
    return {
        "objection_class": obj_class,
        "suggested_response": {
            "response_ar": response.response_ar,
            "next_step_ar": response.next_step_ar,
            "proof_based": response.proof_based,
            "risk_note_ar": response.risk_note_ar,
        },
        "close_plan": to_dict(plan),
        "approval_first": True,
    }


@router.post("/events")
async def add_event(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    obj_class = str(body.get("objection_class") or "")
    if not obj_class:
        raise HTTPException(status_code=400, detail="objection_class_required")
    row_id = f"obj_{uuid.uuid4().hex[:14]}"
    async with get_session() as s:
        s.add(ObjectionEventRecord(
            id=row_id,
            lead_id=body.get("lead_id"),
            deal_id=body.get("deal_id"),
            customer_id=body.get("customer_id"),
            objection_class=obj_class,
            raw_text=body.get("raw_text"),
            response_variant=body.get("response_variant"),
            outcome=str(body.get("outcome") or "open"),
            meta_json=body.get("meta") or {},
        ))
    return {"id": row_id, "objection_class": obj_class}
