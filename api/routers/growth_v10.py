"""Growth v10 — PostHog-inspired event taxonomy + funnel + experiments API."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.growth_v10 import (
    Campaign,
    EventRecord,
    Experiment,
    attribute_revenue,
    compute_funnel,
    evaluate_experiment,
    list_event_names,
    transition_campaign,
    validate_event,
)

router = APIRouter(prefix="/api/v1/growth-v10", tags=["growth-v10"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "growth_v10",
        "guardrails": {
            "no_pii_in_events": True,
            "no_auto_publish": True,
            "no_marketing_claims": True,
            "approval_required_for_campaign_run": True,
            "consent_required_default": True,
        },
    }


@router.get("/event-taxonomy")
async def event_taxonomy() -> dict:
    names = list_event_names()
    return {
        "schema_version": 1,
        "count": len(names),
        "events": names,
    }


@router.post("/events/validate")
async def events_validate(payload: dict = Body(...)) -> dict:
    try:
        ev = validate_event(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ev.model_dump(mode="json")


@router.post("/funnel/compute")
async def funnel_compute(payload: dict = Body(...)) -> dict:
    raw_events = payload.get("events") or []
    if not isinstance(raw_events, list):
        raise HTTPException(status_code=400, detail="events must be a list")
    records: list[EventRecord] = []
    for raw in raw_events:
        try:
            records.append(EventRecord.model_validate(raw))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"invalid event: {exc}") from exc
    report = compute_funnel(records)
    return report.model_dump(mode="json")


@router.post("/experiment/evaluate")
async def experiment_evaluate(payload: dict = Body(...)) -> dict:
    raw_exp = payload.get("experiment")
    if not isinstance(raw_exp, dict):
        raise HTTPException(status_code=400, detail="experiment dict required")
    try:
        exp = Experiment.model_validate(raw_exp)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    control = payload.get("control_results") or []
    variant = payload.get("variant_results") or []
    if not isinstance(control, list) or not isinstance(variant, list):
        raise HTTPException(
            status_code=400,
            detail="control_results and variant_results must be lists",
        )
    return evaluate_experiment(
        exp,
        [float(x) for x in control],
        [float(x) for x in variant],
    )


@router.post("/campaign/transition")
async def campaign_transition(payload: dict = Body(...)) -> dict:
    raw_camp = payload.get("campaign")
    target = payload.get("target")
    if not isinstance(raw_camp, dict) or not target:
        raise HTTPException(status_code=400, detail="campaign and target required")
    try:
        c = Campaign.model_validate(raw_camp)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    consent_evidence = payload.get("consent_evidence")
    out = transition_campaign(c, str(target), consent_evidence=consent_evidence)
    return out.model_dump(mode="json")


@router.post("/attribute-revenue")
async def attribute_revenue_endpoint(payload: dict = Body(...)) -> dict:
    raw_rev = payload.get("revenue_event")
    raw_priors = payload.get("prior_events") or []
    if not isinstance(raw_rev, dict):
        raise HTTPException(status_code=400, detail="revenue_event dict required")
    if not isinstance(raw_priors, list):
        raise HTTPException(status_code=400, detail="prior_events must be a list")
    try:
        rev_ev = EventRecord.model_validate(raw_rev)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    priors: list[EventRecord] = []
    for raw in raw_priors:
        try:
            priors.append(EventRecord.model_validate(raw))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"invalid prior event: {exc}") from exc
    return attribute_revenue(rev_ev, priors)
