"""Board Decision OS — read-only strategic intelligence & scorecards."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auto_client_acquisition.board_decision_os import (
    board_memo_template_markdown,
    build_board_memo,
    build_top_decisions,
    classify_initiative,
    default_capital_allocation,
    evaluate_agent_gate,
    list_risk_register,
    score_client,
    score_offer,
    score_productization,
    validate_monthly_bets,
)
from auto_client_acquisition.board_decision_os.schemas import (
    AgentGateInput,
    BoardMemoMetrics,
    CEOSignals,
    ClientScorecardInput,
    OfferScorecardInput,
    ProductizationScorecardInput,
    StrategicBetsInput,
)
from auto_client_acquisition.board_decision_os.strategic_bets import StrategicBetsError

router = APIRouter(prefix="/api/v1/board-decision-os", tags=["board-decision-os"])


@router.get("/overview")
async def overview() -> dict[str, Any]:
    return {
        "system": "Dealix Board Decision OS",
        "loop": "Signals → Decisions → Actions → Proof → Learning",
        "docs": "docs/board_decision_system/STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md",
        "endpoints": [
            "POST /scorecards/offer",
            "POST /scorecards/client",
            "POST /scorecards/productization",
            "POST /ceo-top-decisions",
            "GET /board-memo-template",
            "POST /board-memo",
            "POST /strategic-bets/validate",
            "POST /agent-gate/evaluate",
            "GET /risk-register",
            "GET /capital-allocation",
            "GET /initiative-bucket",
        ],
    }


@router.post("/scorecards/offer")
async def post_offer_scorecard(body: OfferScorecardInput) -> dict[str, Any]:
    r = score_offer(body)
    return {"scorecard": "offer", "result": r.model_dump()}


@router.post("/scorecards/client")
async def post_client_scorecard(body: ClientScorecardInput) -> dict[str, Any]:
    r = score_client(body)
    return {"scorecard": "client", "result": r.model_dump()}


@router.post("/scorecards/productization")
async def post_product_scorecard(body: ProductizationScorecardInput) -> dict[str, Any]:
    r = score_productization(body)
    return {"scorecard": "productization", "result": r.model_dump()}


@router.post("/ceo-top-decisions")
async def post_ceo_top_decisions(body: CEOSignals, limit: int = 5) -> dict[str, Any]:
    decisions = [d.model_dump() for d in build_top_decisions(body, limit=limit)]
    return {"decisions": decisions}


@router.get("/board-memo-template")
async def get_board_memo_template() -> dict[str, str]:
    return {"format": "markdown", "body": board_memo_template_markdown()}


@router.post("/board-memo")
async def post_board_memo(body: BoardMemoMetrics, locale: str = "bilingual") -> dict[str, str]:
    if locale not in ("ar", "en", "bilingual"):
        raise HTTPException(status_code=400, detail="locale must be ar|en|bilingual")
    return {"format": "markdown", "body": build_board_memo(body, locale=locale)}


class StrategicBetsValidateResponse(BaseModel):
    ok: bool
    month_label: str
    bet_count: int


@router.post("/strategic-bets/validate", response_model=StrategicBetsValidateResponse)
async def post_validate_bets(body: StrategicBetsInput) -> StrategicBetsValidateResponse:
    try:
        v = validate_monthly_bets(body)
    except StrategicBetsError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return StrategicBetsValidateResponse(ok=True, month_label=v.month_label, bet_count=len(v.bets))


@router.post("/agent-gate/evaluate")
async def post_agent_gate(body: AgentGateInput) -> dict[str, Any]:
    r = evaluate_agent_gate(body)
    return r.model_dump()


@router.get("/risk-register")
async def get_risk_register() -> dict[str, Any]:
    return {"risks": list_risk_register()}


@router.get("/capital-allocation")
async def get_capital_allocation() -> dict[str, list[str]]:
    return default_capital_allocation()


@router.get("/initiative-bucket")
async def get_initiative_bucket(q: str) -> dict[str, Any]:
    b = classify_initiative(q)
    return {"query": q, "bucket": b}
