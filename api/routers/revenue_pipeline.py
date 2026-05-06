"""Revenue Pipeline router — truth-tracking endpoints."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_pipeline import (
    PipelineStage,
    snapshot_revenue_truth,
)
from auto_client_acquisition.revenue_pipeline.lead import Lead
from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.revenue_pipeline.revenue_truth import to_dict
from auto_client_acquisition.runtime_paths import resolve_proof_events_dir

router = APIRouter(prefix="/api/v1/revenue-pipeline", tags=["revenue-pipeline"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "no_silent_truth_label_flip": True,
    "approval_required_for_external_actions": True,
}


class _CreateLeadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    slot_id: str = Field(min_length=1, max_length=40)
    sector: str = "tbd"
    region: str = "tbd"
    relationship_strength: str = "warm_intro"


class _AdvanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lead_id: str
    target_stage: PipelineStage
    commitment_evidence: str = ""
    payment_evidence: str = ""
    actual_amount_sar: int | None = None


@router.get("/status")
async def revenue_pipeline_status() -> dict[str, Any]:
    pipeline = get_default_pipeline()
    return {
        "service": "revenue_pipeline",
        "module": "revenue_pipeline",
        "status": "operational",
        "version": "rx-v1",
        "degraded": False,
        "active_leads": len(pipeline.list_all()),
        "checks": {"in_memory_store": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "أنشئ lead ثم advance بشكل متوافق مع stage_policy",
        "next_action_en": "Create a lead then advance per stage_policy.",
    }


@router.post("/lead")
async def create_lead(req: _CreateLeadRequest) -> dict[str, Any]:
    pipeline = get_default_pipeline()
    lead = Lead.make(
        slot_id=req.slot_id,
        sector=req.sector,
        region=req.region,
        relationship_strength=req.relationship_strength,
    )
    pipeline.add(lead)
    return {"lead": lead.model_dump(mode="json"), "hard_gates": _HARD_GATES}


@router.post("/advance")
async def advance_lead(req: _AdvanceRequest) -> dict[str, Any]:
    pipeline = get_default_pipeline()
    try:
        updated = pipeline.advance(
            req.lead_id,
            req.target_stage,
            commitment_evidence=req.commitment_evidence,
            payment_evidence=req.payment_evidence,
            actual_amount_sar=req.actual_amount_sar,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"lead": updated.model_dump(mode="json"), "hard_gates": _HARD_GATES}


def _count_real_proof_events() -> int:
    """Count NON-template proof event files."""
    proof_dir = resolve_proof_events_dir()
    if not proof_dir.exists():
        return 0
    count = 0
    for f in proof_dir.iterdir():
        if not f.is_file():
            continue
        name_lower = f.name.lower()
        # Skip templates / examples / README / .gitkeep
        if any(s in name_lower for s in (
            ".gitkeep", "readme", "schema.example", ".example.",
            "template",
        )):
            continue
        if f.suffix.lower() not in (".json", ".jsonl", ".md"):
            continue
        count += 1
    return count


@router.get("/summary")
async def summary() -> dict[str, Any]:
    pipeline = get_default_pipeline()
    p_summary = pipeline.summary()
    truth = snapshot_revenue_truth(
        pipeline_summary=p_summary,
        proof_event_files_count=_count_real_proof_events(),
    )
    return {
        "schema_version": 1,
        "pipeline_summary": p_summary,
        "revenue_truth": to_dict(truth),
        "hard_gates": _HARD_GATES,
    }
