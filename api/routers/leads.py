"""Leads (Phase 8) endpoints + Local/Web Discovery + Enrichment + Outreach Prepare."""

from __future__ import annotations

import logging
import uuid
from dataclasses import asdict
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select

from api.dependencies import get_acquisition_pipeline
from api.schemas import (
    LeadCreateRequest,
    LeadResponse,
    LeadsBatchItemResult,
    LeadsBatchRequest,
    LeadsBatchResponse,
    PipelineResponse,
)
from auto_client_acquisition.agents.intake import LeadSource
from auto_client_acquisition.connectors.google_maps import (
    INDUSTRY_QUERIES as _LOCAL_INDUSTRY_QUERIES,
)
from auto_client_acquisition.connectors.google_maps import (
    SAUDI_CITIES as _LOCAL_SAUDI_CITIES,
)
from auto_client_acquisition.customer_readiness.scores import from_passport_meta
from auto_client_acquisition.decision_passport import build_from_pipeline_result
from auto_client_acquisition.notifications import notify_founder_on_intake
from auto_client_acquisition.pipeline import AcquisitionPipeline, PipelineResult
from auto_client_acquisition.pipelines.enrichment import enrich_account
from auto_client_acquisition.providers.maps import (
    discover_with_chain as _discover_with_chain,
)
from auto_client_acquisition.providers.maps import (
    get_maps_chain as _get_maps_chain,
)
from auto_client_acquisition.providers.search import (
    get_search_chain as _get_search_chain,
)
from auto_client_acquisition.revenue_os.dedupe import suggest_dedupe_fingerprint
from auto_client_acquisition.revenue_os.saudi_targeting_profile import (
    anti_waste_violations_for_tier1_intake,
    assert_tier1_storage_allowed,
    map_tier1_to_intake_lead_source,
    merge_targeting_into_discover_body,
    parse_tier1_lead_source,
)
from db.models import (
    AccountRecord,
    ContactRecord,
    LeadRecord,
    LeadScoreRecord,
    OutreachQueueRecord,
    SuppressionRecord,
)
from db.session import async_session_factory

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])
log = logging.getLogger(__name__)


def _new_id(prefix: str = "") -> str:
    suffix = uuid.uuid4().hex[:24]
    return f"{prefix}{suffix}" if prefix else suffix


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _pipeline_response_from_result(result: PipelineResult) -> PipelineResponse:
    passport = build_from_pipeline_result(result)
    passport_d = passport.model_dump()
    readiness = from_passport_meta(passport_d)
    return PipelineResponse(
        lead=LeadResponse(
            id=result.lead.id,
            source=result.lead.source.value,
            company_name=result.lead.company_name,
            contact_name=result.lead.contact_name,
            contact_email=result.lead.contact_email,
            contact_phone=result.lead.contact_phone,
            sector=result.lead.sector,
            region=result.lead.region,
            status=result.lead.status.value,
            fit_score=result.lead.fit_score,
            urgency_score=result.lead.urgency_score,
            pain_points=result.lead.pain_points,
            locale=result.lead.locale,
            created_at=result.lead.created_at,
        ),
        fit_score=result.fit_score.to_dict() if result.fit_score else None,
        extraction=result.extraction.to_dict() if result.extraction else None,
        qualification=result.qualification.to_dict() if result.qualification else None,
        crm_sync=result.crm_sync.to_dict() if result.crm_sync else None,
        booking=result.booking.to_dict() if result.booking else None,
        proposal=result.proposal.to_dict() if result.proposal else None,
        warnings=result.warnings,
        decision_passport=passport_d,
        customer_readiness=readiness,
    )


async def _persist_lead_row(
    *,
    tier1_value: str,
    result: PipelineResult,
    hint_dict: dict[str, Any],
    targeting_profile: dict[str, Any] | None,
) -> None:
    lead = result.lead
    meta = dict(lead.metadata)
    meta["tier1_source"] = tier1_value
    meta["dedupe_hint"] = hint_dict
    if targeting_profile is not None:
        meta["targeting_profile"] = targeting_profile
    async with async_session_factory() as session:
        try:
            session.add(
                LeadRecord(
                    id=lead.id,
                    source=lead.source.value,
                    company_name=lead.company_name,
                    contact_name=lead.contact_name,
                    contact_email=lead.contact_email,
                    contact_phone=lead.contact_phone,
                    sector=lead.sector,
                    region=lead.region,
                    company_size=lead.company_size,
                    budget=lead.budget,
                    status=lead.status.value,
                    fit_score=lead.fit_score,
                    urgency_score=lead.urgency_score,
                    locale=lead.locale,
                    message=lead.message,
                    pain_points=lead.pain_points,
                    meta_json=meta,
                    dedup_hash=lead.dedup_hash,
                )
            )
            await session.commit()
        except Exception as exc:
            await session.rollback()
            log.warning("lead_batch_persist_skipped: %s", exc)


@router.post("", response_model=PipelineResponse)
async def create_lead(
    payload: LeadCreateRequest,
    pipeline: AcquisitionPipeline = Depends(get_acquisition_pipeline),
    auto_book: bool = True,
    auto_proposal: bool = False,
) -> PipelineResponse:
    """Submit a new lead — runs through the full acquisition pipeline."""
    try:
        source = LeadSource(payload.source)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid source: {e}") from e

    result = await pipeline.run(
        payload=payload.model_dump(exclude_none=True),
        source=source,
        auto_book=auto_book,
        auto_proposal=auto_proposal,
    )

    # Fire-and-log founder alert. Failures here NEVER fail the intake.
    try:
        await notify_founder_on_intake(result.lead)
    except Exception as exc:
        log.warning("founder_alert_dispatch_failed: %s", exc)

    return _pipeline_response_from_result(result)


@router.post("/batch", response_model=LeadsBatchResponse)
async def create_leads_batch(
    body: LeadsBatchRequest,
    pipeline: AcquisitionPipeline = Depends(get_acquisition_pipeline),
    auto_book: bool = True,
    auto_proposal: bool = False,
) -> LeadsBatchResponse:
    """Batch intake with a single Tier1 source + optional targeting profile metadata."""
    try:
        tier1 = parse_tier1_lead_source(body.tier1_source)
        assert_tier1_storage_allowed(tier1)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    vio = anti_waste_violations_for_tier1_intake(tier1)
    if vio:
        raise HTTPException(
            status_code=422,
            detail=[{"code": v.code, "ar": v.detail_ar, "en": v.detail_en} for v in vio],
        )

    intake_src = map_tier1_to_intake_lead_source(tier1)
    results: list[LeadsBatchItemResult] = []
    ok_count = 0

    for idx, item in enumerate(body.items):
        payload = item.model_dump(exclude_none=True)
        payload["tier1_source"] = tier1.value
        try:
            result = await pipeline.run(
                payload=payload,
                source=intake_src,
                auto_book=auto_book,
                auto_proposal=auto_proposal,
            )
            try:
                await notify_founder_on_intake(result.lead)
            except Exception as exc:
                log.warning("founder_alert_dispatch_failed: %s", exc)

            hint = suggest_dedupe_fingerprint(
                company_name=item.company,
                domain=None,
                phone=item.phone,
                email=str(item.email) if item.email else None,
            )
            hint_d = asdict(hint)
            result.lead.metadata = dict(result.lead.metadata)
            result.lead.metadata["tier1_source"] = tier1.value
            result.lead.metadata["dedupe_hint"] = hint_d
            if body.targeting_profile is not None:
                result.lead.metadata["targeting_profile"] = body.targeting_profile

            await _persist_lead_row(
                tier1_value=tier1.value,
                result=result,
                hint_dict=hint_d,
                targeting_profile=body.targeting_profile,
            )
            resp = _pipeline_response_from_result(result)
            results.append(
                LeadsBatchItemResult(
                    index=idx, ok=True, lead_id=result.lead.id, pipeline=resp, error=None
                )
            )
            ok_count += 1
        except Exception as exc:
            log.warning("lead_batch_item_failed", index=idx, error=str(exc))
            results.append(
                LeadsBatchItemResult(
                    index=idx, ok=False, lead_id=None, pipeline=None, error=str(exc)[:500]
                )
            )

    return LeadsBatchResponse(
        tier1_source=tier1.value,
        total=len(body.items),
        succeeded=ok_count,
        failed=len(body.items) - ok_count,
        results=results,
    )


# ── Local Saudi Lead Engine (Google Places) ────────────────────────
@router.get("/discover/local-industries")
async def list_local_industries() -> dict[str, Any]:
    return {
        "industries": [
            {"key": k, "queries": v} for k, v in _LOCAL_INDUSTRY_QUERIES.items()
        ],
        "cities": [
            {"key": k, "ar": ar, "en": en}
            for k, (ar, en) in _LOCAL_SAUDI_CITIES.items()
        ],
        "notes": (
            "POST /api/v1/leads/discover/local with body "
            "{industry, city, max_results, hydrate_details, custom_query, page_token}. "
            "Set GOOGLE_MAPS_API_KEY in Railway env to enable."
        ),
    }


@router.post("/discover/local")
async def discover_local_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Saudi local lead engine — chains Google Places → SerpApi → Apify → static."""
    try:
        body = merge_targeting_into_discover_body(dict(body))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    industry = str(body.get("industry") or "").strip()
    city = str(body.get("city") or "").strip()
    max_results = int(body.get("max_results") or 20)
    hydrate_details = bool(body.get("hydrate_details", True))
    custom_query = body.get("custom_query")
    page_token = body.get("page_token")

    if not industry and not custom_query:
        raise HTTPException(400, "industry_required")
    if not city:
        raise HTTPException(400, "city_required")
    if max_results < 1 or max_results > 40:
        raise HTTPException(400, "max_results_out_of_range: 1..40")

    chain_result = await _discover_with_chain(
        industry=industry or "custom",
        city=city,
        max_results=max_results,
        page_token=str(page_token) if page_token else None,
        hydrate_details=hydrate_details,
        custom_query=str(custom_query) if custom_query else None,
    )
    payload = chain_result.to_dict()
    payload["chain"] = [
        {"name": p.name, "available": p.is_available()} for p in _get_maps_chain()
    ]
    return payload


# ── Web Lead Discovery ────────────────────────────────────────────
@router.post("/discover/web")
async def discover_web_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Web lead discovery via SearchProvider chain (Google CSE → Tavily → static)."""
    query = str(body.get("query") or "").strip()
    num = int(body.get("num") or 10)
    site = body.get("site")
    lang = body.get("lang")

    if len(query) < 5:
        raise HTTPException(400, "query_too_short: min 5 chars")
    if num < 1 or num > 10:
        raise HTTPException(400, "num_out_of_range: 1..10")

    chain_result = await _search_with_chain(
        query, num=num,
        site=str(site) if site else None,
        lang=str(lang) if lang else None,
    )
    payload = chain_result.to_dict()
    payload["chain"] = [
        {"name": p.name, "available": p.is_available()} for p in _get_search_chain()
    ]
    return payload


# ── Full enrichment (single account) ──────────────────────────────
@router.post("/enrich/full")
async def enrich_full_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Full enrichment for a single account.
    Body: {company_name?, domain?, website?, city?, sector?, place_id?, level?}
    Level: basic | standard (default) | deep.
    """
    if not (body.get("company_name") or body.get("domain") or body.get("website")):
        raise HTTPException(400, "must_provide_company_name_or_domain_or_website")
    level = str(body.get("level") or "standard")
    if level not in {"basic", "standard", "deep"}:
        raise HTTPException(400, "level_must_be: basic | standard | deep")

    account = {
        "company_name": body.get("company_name") or "",
        "domain": body.get("domain"),
        "website": body.get("website"),
        "city": body.get("city"),
        "country": body.get("country") or "SA",
        "sector": body.get("sector"),
        "google_place_id": body.get("place_id"),
        "best_source": body.get("source") or "manual",
        "allowed_use": body.get("allowed_use") or "business_contact_research_only",
        "risk_level": body.get("risk_level") or "medium",
    }
    return await enrich_account(account, enrichment_level=level)


# ── Batch enrichment over existing accounts ───────────────────────
@router.post("/enrich/batch")
async def enrich_batch_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Enrich a batch of accounts already in the graph.
    Body: {account_ids: [...], level: basic|standard|deep}
    """
    ids = body.get("account_ids")
    level = str(body.get("level") or "standard")
    if not isinstance(ids, list) or not ids:
        raise HTTPException(400, "account_ids_required")
    if len(ids) > 100:
        raise HTTPException(400, "too_many: max 100 per batch")

    async with async_session_factory() as session:
        try:
            accs = (await session.execute(
                select(AccountRecord).where(AccountRecord.id.in_(ids))
            )).scalars().all()
        except Exception as exc:
            return {"status": "skipped_db_unreachable", "error": str(exc), "items": []}

        results: list[dict[str, Any]] = []
        for acc in accs:
            account_dict = {
                "id": acc.id, "company_name": acc.company_name,
                "domain": acc.domain, "website": acc.website,
                "city": acc.city, "country": acc.country, "sector": acc.sector,
                "google_place_id": acc.google_place_id, "best_source": acc.best_source,
                "risk_level": acc.risk_level,
                "allowed_use": (acc.extra or {}).get("allowed_use"),
            }
            try:
                result = await enrich_account(account_dict, enrichment_level=level)
            except Exception as exc:
                results.append({"id": acc.id, "status": "error", "error": str(exc)})
                continue
            score = result.get("score", {})
            session.add(LeadScoreRecord(
                id=_new_id("ls_"), account_id=acc.id,
                fit_score=float(score.get("fit") or 0),
                intent_score=float(score.get("intent") or 0),
                urgency_score=float(score.get("urgency") or 0),
                risk_score=float(score.get("risk") or 0),
                total_score=float(score.get("total") or 0),
                priority=str(score.get("priority") or "P3")[:8],
                recommended_channel=score.get("recommended_channel"),
                reason=score.get("reason"),
            ))
            acc.data_quality_score = float(result.get("data_quality", {}).get("score", 0))
            acc.status = "enriched"
            acc.updated_at = _utcnow()
            results.append({
                "id": acc.id, "status": "ok",
                "score": score, "dq": result.get("data_quality"),
                "providers_used": result.get("providers_used"),
            })

        try:
            await session.commit()
        except Exception as exc:
            await session.rollback()
            return {"status": "commit_failed", "error": str(exc), "items": results}

    return {"count": len(results), "items": results}
