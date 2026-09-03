"""Business strategy and GTM API — commercial pricing authority is quote-only."""

from __future__ import annotations

from typing import Any, cast

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.ai.model_router import ModelTask, get_model_route, requires_guardrail
from auto_client_acquisition.business import (
    activation_metrics,
    ai_quality_metrics,
    channel_strategy,
    compare_competitors,
    dealix_differentiators,
    estimate_cac_payback,
    estimate_gross_margin,
    estimate_ltv,
    first_10_customers_plan,
    first_100_customers_plan,
    founder_led_sales_script,
    north_star_metrics,
    partner_strategy,
    positioning_statement,
    retention_metrics,
    revenue_metrics,
)
from auto_client_acquisition.business.market_positioning import Segment
from auto_client_acquisition.business.proof_pack import (
    build_demo_proof_pack,
    calculate_roi_summary,
    grade_account_health,
)
from auto_client_acquisition.business.verticals import get_vertical_playbooks, recommend_vertical

router = APIRouter(prefix="/api/v1/business", tags=["business"])

_CANONICAL_COMMERCIAL_PATH = [
    "free_mini_diagnostic",
    "qualified_discovery",
    "customer_specific_quote",
    "revenue_command_pilot_30d",
]
_PRICE_AUTHORITY = "customer_specific_quote_after_qualified_discovery"


def _legacy_pricing_retired_detail(*, use_endpoint: str | None = None) -> dict[str, Any]:
    detail: dict[str, Any] = {
        "reason": "legacy_pricing_authority_retired",
        "launch_authority": "revenue_command_pilot_30d",
        "commercial_path": list(_CANONICAL_COMMERCIAL_PATH),
        "price_authority": _PRICE_AUTHORITY,
        "public_fixed_price": False,
        "live_charge_allowed": False,
    }
    if use_endpoint:
        detail["use_endpoint"] = use_endpoint
    return detail


@router.get("/pricing")
async def pricing() -> dict[str, Any]:
    """Compatibility surface: never publishes a fixed price or tier catalogue."""
    return {
        "status": "quote_only",
        "launch_authority": "revenue_command_pilot_30d",
        "entry_offer_id": "free_mini_diagnostic",
        "commercial_path": list(_CANONICAL_COMMERCIAL_PATH),
        "price_authority": _PRICE_AUTHORITY,
        "public_fixed_price": False,
        "live_charge_allowed": False,
    }


@router.post("/recommend-plan")
async def recommend_plan_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    del body
    raise HTTPException(status_code=409, detail=_legacy_pricing_retired_detail())


@router.post("/roi")
async def roi_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    del body
    raise HTTPException(
        status_code=409,
        detail=_legacy_pricing_retired_detail(use_endpoint="/api/v1/commercial/roi/estimate"),
    )


@router.get("/competitors")
async def competitors() -> dict[str, Any]:
    return {"items": compare_competitors()}


@router.get("/differentiators")
async def differentiators() -> dict[str, Any]:
    return {"differentiators": dealix_differentiators()}


@router.get("/gtm/first-10")
async def gtm_first_10() -> dict[str, Any]:
    return first_10_customers_plan()


@router.get("/gtm/first-100")
async def gtm_first_100() -> dict[str, Any]:
    return first_100_customers_plan()


@router.get("/metrics")
async def metrics() -> dict[str, Any]:
    return {
        "north_star": north_star_metrics(),
        "activation": activation_metrics(),
        "retention": retention_metrics(),
        "revenue": revenue_metrics(),
        "ai_quality": ai_quality_metrics(),
    }


@router.get("/unit-economics/demo")
async def unit_economics_demo() -> dict[str, Any]:
    return {
        "status": "internal_estimate_only",
        "customer_value_claim": False,
        "price_authority": _PRICE_AUTHORITY,
        "public_fixed_price": False,
        "gross_margin": estimate_gross_margin(),
        "cac_payback": estimate_cac_payback(),
        "ltv": estimate_ltv(),
    }


@router.post("/performance-fee/demo")
async def performance_fee_demo(body: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    del body
    raise HTTPException(status_code=409, detail=_legacy_pricing_retired_detail())


@router.get("/positioning/{segment}")
async def positioning(segment: str) -> dict[str, Any]:
    allowed: tuple[Segment, ...] = ("founder", "sme", "enterprise", "agency")
    seg = cast(Segment, segment if segment in allowed else "founder")
    return {"segment": seg, "statement_ar": positioning_statement(seg)}


@router.get("/channels")
async def channels() -> dict[str, Any]:
    return channel_strategy()


@router.get("/partners")
async def partners() -> dict[str, Any]:
    return partner_strategy()


@router.get("/sales-script")
async def sales_script() -> dict[str, Any]:
    return founder_led_sales_script()


@router.get("/verticals")
async def verticals() -> dict[str, Any]:
    return get_vertical_playbooks()


@router.post("/verticals/recommend")
async def vertical_recommend(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return recommend_vertical(
        industry=str(body.get("industry", "b2b")),
        city=str(body.get("city", "Riyadh")),
        goal=str(body.get("goal", "pipeline")),
    )


@router.get("/proof-pack/demo")
async def proof_pack_demo() -> dict[str, Any]:
    return build_demo_proof_pack()


@router.post("/proof-pack/roi-summary")
async def proof_pack_roi(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    if "subscription_sar" not in body:
        raise HTTPException(
            status_code=422,
            detail="customer_specific_quote_amount_required",
        )
    try:
        quote_amount_sar = float(body["subscription_sar"])
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="invalid_customer_specific_quote_amount") from exc
    if quote_amount_sar <= 0:
        raise HTTPException(status_code=422, detail="invalid_customer_specific_quote_amount")
    result = calculate_roi_summary(
        subscription_sar=quote_amount_sar,
        influenced_revenue_sar=float(body.get("influenced_revenue_sar", 0)),
        hours_saved=float(body.get("hours_saved", 0)),
    )
    return {
        "status": "internal_estimate_only",
        "customer_value_claim": False,
        "guarantee": False,
        "quote_amount_source": "caller_supplied_customer_specific_quote",
        "result": result,
    }


@router.post("/account-health")
async def account_health(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return grade_account_health(
        brief_opens_4w=int(body.get("brief_opens_4w", 8)),
        approvals_4w=int(body.get("approvals_4w", 5)),
        blocks_4w=int(body.get("blocks_4w", 2)),
    )


@router.get("/model-routes")
async def model_routes() -> dict[str, Any]:
    routes = []
    for task in ModelTask:
        r = get_model_route(task)
        routes.append(
            {
                "task": task.value,
                "quality_tier": r.quality_tier,
                "latency": r.latency,
                "cost_class": r.cost_class,
                "guardrail_required": r.guardrail_required,
                "eval_metric": r.eval_metric,
            }
        )
    return {"routes": routes}


@router.get("/model-routes/guardrail-tasks")
async def guardrail_tasks() -> dict[str, Any]:
    return {"tasks": [t.value for t in ModelTask if requires_guardrail(t)]}
