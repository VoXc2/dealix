from __future__ import annotations

from fastapi import APIRouter, Body

from auto_client_acquisition.lead_machine_tier1.lead_machine import Tier1LeadMachine
from auto_client_acquisition.lead_machine_tier1.schemas import LeadCompany, LeadMachineRunRequest, ProvenanceRecord
from auto_client_acquisition.lead_machine_tier1.source_registry import SOURCE_REGISTRY

router = APIRouter(prefix="/api/v1/lead-machine-tier1", tags=["lead-machine-tier1"])

_machine = Tier1LeadMachine()


@router.get("/status")
async def status() -> dict[str, object]:
    return {
        "module": "lead_machine_tier1",
        "status": "ready",
        "hard_gates": {
            "no_cold_whatsapp": True,
            "draft_only_external_actions": True,
            "no_scraping": True,
            "unknown_states_safe": True,
        },
    }


@router.get("/sources")
async def sources() -> dict[str, object]:
    return {"count": len(SOURCE_REGISTRY), "sources": [source.model_dump(mode="json") for source in SOURCE_REGISTRY.values()]}


@router.post("/enrich")
async def enrich(payload: LeadMachineRunRequest) -> dict[str, object]:
    result = _machine.run(payload)
    return {"enrichment": [item.model_dump(mode="json") for item in result.enrichment]}


@router.post("/dedupe")
async def dedupe(payload: LeadMachineRunRequest) -> dict[str, object]:
    result = _machine.run(payload)
    return {"dedupe": result.dedupe.model_dump(mode="json")}


@router.post("/score")
async def score(payload: LeadMachineRunRequest) -> dict[str, object]:
    result = _machine.run(payload)
    return {"score": result.score.model_dump(mode="json")}


@router.post("/rank")
async def rank(payload: list[LeadMachineRunRequest]) -> dict[str, object]:
    results = [_machine.run(item) for item in payload]
    ranked = sorted(results, key=lambda item: item.score.final_priority.value)
    return {"ranked": [item.model_dump(mode="json") for item in ranked]}


@router.post("/warm-route")
async def warm_route(payload: LeadMachineRunRequest) -> dict[str, object]:
    result = _machine.run(payload)
    return {"warm_route": result.warm_route.model_dump(mode="json")}


@router.post("/check-compliance")
async def check_compliance(payload: LeadMachineRunRequest) -> dict[str, object]:
    result = _machine.run(payload)
    return {"compliance": result.compliance.model_dump(mode="json")}


@router.post("/run")
async def run(payload: LeadMachineRunRequest) -> dict[str, object]:
    return _machine.run(payload).model_dump(mode="json")


@router.get("/demo-output")
async def demo_output() -> dict[str, object]:
    payload = LeadMachineRunRequest(
        lead=LeadCompany(company_name="شركة تجريبية", domain="example.sa", city="Riyadh", sector="SaaS", metadata={"crm_installed": True, "payment_provider": True, "founder_intro": True, "inbound": True}),
        provenance=ProvenanceRecord(source_name="manual_warm_network", source_type="manual", collected_at=__import__("datetime").datetime.utcnow(), allowed_use="warm_manual_only", consent_state="granted", confidence=0.9, refresh_needed=False, risk_level="low"),
    )
    return _machine.run(payload).model_dump(mode="json")