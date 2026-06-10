"""
Commercial Ops Router — auto-graduation, expansion, churn prevention, upsell, contracts.
موجه العمليات التجارية — التخرّج التلقائي، التوسع، منع التوقف، البيع الإضافي، العقود.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial_ops.auto_graduation import AutoGraduationEngine
from dealix.commercial_ops.churn_prevention import ChurnPreventionEngine
from dealix.commercial_ops.contract_engine import ContractEngine
from dealix.commercial_ops.expansion_triggers import ExpansionTriggerEngine
from dealix.commercial_ops.upsell_automaton import UpsellAutomaton

router = APIRouter(prefix="/api/v1/commercial-ops", tags=["commercial-ops"])

_graduation = AutoGraduationEngine()
_expansion = ExpansionTriggerEngine()
_churn = ChurnPreventionEngine()
_upsell = UpsellAutomaton()
_contracts = ContractEngine()

_HARD_GATES = {
    "no_auto_upgrade_without_consent": True,
    "no_auto_charge_without_invoice": True,
    "approval_required_for_external_actions": True,
    "intervention_requires_review": True,
}


class GraduationCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str


class GraduationExecuteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str


class ExpansionTriggerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    opportunity_id: str


class ChurnInterveneRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    risk_id: str


class UpsellProposalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    opportunity_id: str


class UpsellSendRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    opportunity_id: str


class ContractGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str
    plan: str = Field(..., pattern=r"^(starter|growth|scale|enterprise)$")
    duration_months: int = Field(default=12, ge=1, le=60)


class ContractSignRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contract_id: str


@router.get("/graduation/pending")
async def graduation_pending() -> dict[str, Any]:
    pending = await _graduation.get_pending()
    return {
        "count": len(pending),
        "pending": [p.to_dict() for p in pending],
        "stats": _graduation.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/graduation/check")
async def graduation_check(body: GraduationCheckRequest) -> dict[str, Any]:
    eligibility = await _graduation.check_eligibility(body.customer_id)
    return {"eligibility": eligibility.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/graduation/execute")
async def graduation_execute(body: GraduationExecuteRequest) -> dict[str, Any]:
    result = await _graduation.graduate(body.customer_id)
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/expansion/scan")
async def expansion_scan() -> dict[str, Any]:
    opportunities = await _expansion.scan()
    return {
        "count": len(opportunities),
        "opportunities": [o.to_dict() for o in opportunities],
        "stats": _expansion.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/expansion/opportunities")
async def expansion_list(status: str | None = None) -> dict[str, Any]:
    opps = _expansion.list_opportunities(status)
    return {
        "count": len(opps),
        "opportunities": [o.to_dict() for o in opps],
        "stats": _expansion.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/expansion/trigger")
async def expansion_trigger(body: ExpansionTriggerRequest) -> dict[str, Any]:
    result = await _expansion.trigger(body.opportunity_id)
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/churn/scan")
async def churn_scan() -> dict[str, Any]:
    risks = await _churn.scan()
    return {
        "count": len(risks),
        "risks": [r.to_dict() for r in risks],
        "stats": _churn.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/churn/risks")
async def churn_list(status: str | None = None, min_score: float = 0.0) -> dict[str, Any]:
    risks = _churn.list_risks(status, min_score)
    return {
        "count": len(risks),
        "risks": [r.to_dict() for r in risks],
        "stats": _churn.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/churn/intervene")
async def churn_intervene(body: ChurnInterveneRequest) -> dict[str, Any]:
    result = await _churn.intervene(body.risk_id)
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/upsell/scan")
async def upsell_scan() -> dict[str, Any]:
    opportunities = await _upsell.scan_for_upsells()
    return {
        "count": len(opportunities),
        "opportunities": [o.to_dict() for o in opportunities],
        "stats": _upsell.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/upsell/opportunities")
async def upsell_list(status: str | None = None) -> dict[str, Any]:
    opps = _upsell.list_opportunities(status)
    return {
        "count": len(opps),
        "opportunities": [o.to_dict() for o in opps],
        "stats": _upsell.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/upsell/generate-proposal")
async def upsell_generate_proposal(body: UpsellProposalRequest) -> dict[str, Any]:
    try:
        proposal = await _upsell.generate_proposal(body.opportunity_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"proposal": proposal.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/upsell/send")
async def upsell_send(body: UpsellSendRequest) -> dict[str, Any]:
    result = await _upsell.send_offer(body.opportunity_id)
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/contracts/generate")
async def contract_generate(body: ContractGenerateRequest) -> dict[str, Any]:
    try:
        contract = await _contracts.generate(body.customer_id, body.plan, body.duration_months)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"contract": contract.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/contracts")
async def contract_list(customer_id: str | None = None) -> dict[str, Any]:
    contracts = _contracts.list_contracts(customer_id)
    return {
        "count": len(contracts),
        "contracts": [c.to_dict() for c in contracts],
        "stats": _contracts.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/contracts/{contract_id}")
async def contract_get(contract_id: str) -> dict[str, Any]:
    contract = _contracts.get_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"contract": contract.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/contracts/{contract_id}/pdf")
async def contract_pdf(contract_id: str) -> dict[str, Any]:
    try:
        pdf_bytes = await _contracts.render_pdf(contract_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {
        "contract_id": contract_id,
        "content_type": "text/plain",
        "size_bytes": len(pdf_bytes),
        "preview": pdf_bytes[:500].decode("utf-8"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/contracts/send-for-signature")
async def contract_send_sign(body: ContractSignRequest) -> dict[str, Any]:
    result = await _contracts.send_for_signature(body.contract_id)
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}
