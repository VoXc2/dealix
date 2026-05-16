"""Board Decision OS router — strategic decision surface.

Read-only taxonomy + pure validators over ``board_decision_os``:
- GET  /api/v1/board-decision-os/overview            — memo/risk/capital taxonomy
- POST /api/v1/board-decision-os/memo                — board-memo completeness check
- GET  /api/v1/board-decision-os/risks               — risk register → mitigations
- GET  /api/v1/board-decision-os/capital-allocation  — must/should/hold/kill buckets

Hard rules: this surface never executes an external action and never
returns fake-revenue numbers — it classifies and reports only.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.board_decision_os import (
    BOARD_MEMO_SECTIONS,
    CAPITAL_BOARD_BUCKETS,
    RISK_REGISTER_CODES,
    board_memo_sections_complete,
    capital_board_bucket,
    risk_to_mitigation_decision,
)

router = APIRouter(
    prefix="/api/v1/board-decision-os", tags=["board-decision-os"]
)


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "read_only_decision_surface": True,
}


class _MemoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sections_present: list[str] = Field(default_factory=list)


@router.get("/overview")
async def overview() -> dict[str, Any]:
    """Board Decision OS taxonomy — memo sections, risk codes, capital buckets."""
    return {
        "service": "board_decision_os",
        "memo_sections": list(BOARD_MEMO_SECTIONS),
        "memo_section_count": len(BOARD_MEMO_SECTIONS),
        "risk_codes": list(RISK_REGISTER_CODES),
        "risk_count": len(RISK_REGISTER_CODES),
        "capital_buckets": list(CAPITAL_BOARD_BUCKETS),
        "hard_gates": _HARD_GATES,
    }


@router.post("/memo")
async def memo(req: _MemoRequest) -> dict[str, Any]:
    """Check which of the 12 canonical board-memo sections are still missing."""
    complete, missing = board_memo_sections_complete(
        frozenset(req.sections_present)
    )
    return {
        "all_sections": list(BOARD_MEMO_SECTIONS),
        "sections_present": req.sections_present,
        "complete": complete,
        "missing_sections": list(missing),
        "hard_gates": _HARD_GATES,
    }


@router.get("/risks")
async def risks() -> dict[str, Any]:
    """The board risk register — each risk code mapped to its mitigation decision."""
    register = [
        {"code": code, "mitigation_decision": risk_to_mitigation_decision(code)}
        for code in RISK_REGISTER_CODES
    ]
    return {
        "risk_register": register,
        "count": len(register),
        "hard_gates": _HARD_GATES,
    }


@router.get("/capital-allocation")
async def capital_allocation(investments: str = "") -> dict[str, Any]:
    """Classify investment slugs into must-fund / should-test / hold / kill.

    Pass a comma-separated ``investments`` query to classify each;
    omit it to read the bucket taxonomy only.
    """
    slugs = [s.strip() for s in investments.split(",") if s.strip()]
    classified = [
        {"investment": s, "bucket": capital_board_bucket(s)} for s in slugs
    ]
    return {
        "buckets": list(CAPITAL_BOARD_BUCKETS),
        "classified": classified,
        "hard_gates": _HARD_GATES,
    }
