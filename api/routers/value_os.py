"""Value OS router — add events + generate Monthly Value Report.

Tier discipline enforced: verified requires source_ref; client_confirmed
requires both refs. Markdown render always carries the bilingual
disclaimer and a ## Limitations section.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.value_os.monthly_report import generate as generate_monthly
from auto_client_acquisition.value_os.value_ledger import (
    ValueDisciplineError,
    add_event,
)

router = APIRouter(prefix="/api/v1/value", tags=["value-os"])


class ValueEventBody(BaseModel):
    kind: str = Field(..., min_length=1)
    amount: float = 0.0
    tier: str = Field(..., min_length=1)
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""


@router.post("/event/{customer_id}")
async def post_value_event(customer_id: str, body: ValueEventBody) -> dict[str, Any]:
    try:
        event = add_event(
            customer_id=customer_id,
            kind=body.kind,
            amount=body.amount,
            tier=body.tier,
            source_ref=body.source_ref,
            confirmation_ref=body.confirmation_ref,
            notes=body.notes,
        )
    except ValueDisciplineError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return {
        "event": event.to_dict(),
        "governance_decision": GovernanceDecision.ALLOW_WITH_REVIEW.value,
    }


@router.get("/{customer_id}/report/monthly")
async def get_monthly_report(
    customer_id: str,
    month: str | None = Query(None, description="YYYY-MM; defaults to current"),
    previous_adoption: float | None = Query(None),
    current_adoption: float | None = Query(None),
) -> dict[str, Any]:
    report = generate_monthly(
        customer_id=customer_id,
        month=month,
        previous_adoption=previous_adoption,
        current_adoption=current_adoption,
    )
    return report.to_dict()


@router.get("/{customer_id}/report/monthly/markdown", response_class=PlainTextResponse)
async def get_monthly_report_markdown(
    customer_id: str,
    month: str | None = Query(None),
    previous_adoption: float | None = Query(None),
    current_adoption: float | None = Query(None),
) -> str:
    report = generate_monthly(
        customer_id=customer_id,
        month=month,
        previous_adoption=previous_adoption,
        current_adoption=current_adoption,
    )
    return report.to_markdown()


# ── Trust Pack endpoint (enterprise procurement preview) ─────────────


@router.get("/trust-pack/{customer_handle}/markdown", response_class=PlainTextResponse)
async def trust_pack_markdown(customer_handle: str) -> str:
    from auto_client_acquisition.trust_os.trust_pack import assemble_trust_pack
    pack = assemble_trust_pack(customer_handle=customer_handle)
    return pack.to_markdown()


@router.get("/trust-pack/{customer_handle}")
async def trust_pack_json(customer_handle: str) -> dict[str, Any]:
    from auto_client_acquisition.trust_os.trust_pack import assemble_trust_pack
    pack = assemble_trust_pack(customer_handle=customer_handle)
    return pack.to_dict()
