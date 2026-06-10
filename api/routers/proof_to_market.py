"""V12.5 Proof-to-Market router."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.proof_to_market import (
    approval_gate_check,
    case_study_candidate,
    proof_to_snippet,
    sector_learning_summary,
    select_publishable_proofs,
)

router = APIRouter(prefix="/api/v1/proof-to-market", tags=["proof-to-market"])


# ── Wave 14D.2 + 14D.4: case-safe export + PDF ───────────────────────


@router.get("/case-safe/{engagement_id}")
async def case_safe_export(
    engagement_id: str,
    customer_id: str = Query(...),
    sector: str = Query("b2b_services"),
) -> dict[str, Any]:
    """Export a case-safe summary for the engagement (Wave 14D.2)."""
    from auto_client_acquisition.proof_to_market.case_study_exporter import export_case_safe
    export = export_case_safe(
        engagement_id=engagement_id, customer_id=customer_id, sector=sector
    )
    return export.to_dict()


@router.get("/case-safe/{engagement_id}/markdown", response_class=PlainTextResponse)
async def case_safe_markdown(
    engagement_id: str,
    customer_id: str = Query(...),
    sector: str = Query("b2b_services"),
) -> str:
    from auto_client_acquisition.proof_to_market.case_study_exporter import export_case_safe
    export = export_case_safe(
        engagement_id=engagement_id, customer_id=customer_id, sector=sector
    )
    return export.to_markdown()


@router.get("/case-safe/{engagement_id}/pdf")
async def case_safe_pdf(
    engagement_id: str,
    customer_id: str = Query(...),
    sector: str = Query("b2b_services"),
):
    from auto_client_acquisition.proof_to_market.case_study_exporter import export_case_safe
    from auto_client_acquisition.proof_to_market.pdf_renderer import render_markdown_to_pdf
    export = export_case_safe(
        engagement_id=engagement_id, customer_id=customer_id, sector=sector
    )
    md = export.to_markdown()
    pdf = render_markdown_to_pdf(md, title=f"Case-safe summary — {engagement_id}")
    if pdf is None:
        return PlainTextResponse(
            content=md,
            headers={"X-PDF-Renderer": "unavailable; markdown returned as fallback"},
        )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=\"case_safe_{engagement_id}.pdf\""},
    )

_HARD_GATES = {
    "no_fake_proof": True,
    "signed_permission_required_for_external": True,
    "internal_only_default": True,
    "approval_required_for_external_actions": True,
}


class _EventsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    events: list[dict] = Field(default_factory=list)


class _SingleEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event: dict


@router.get("/status")
async def status() -> dict[str, Any]:
    return {"service": "proof_to_market", "version": "v12.5",
            "hard_gates": _HARD_GATES,
            "next_action_ar": "أرسل proof events لتختار الصالح للنشر",
            "next_action_en": "POST proof events to select publishable ones."}


@router.post("/select")
async def select(req: _EventsRequest) -> dict[str, Any]:
    publishable = select_publishable_proofs(req.events)
    return {"total_input": len(req.events),
            "publishable_count": len(publishable),
            "publishable": publishable,
            "hard_gates": _HARD_GATES}


@router.post("/snippet")
async def snippet(req: _SingleEventRequest) -> dict[str, Any]:
    return {"snippet": proof_to_snippet(req.event), "hard_gates": _HARD_GATES}


@router.post("/case-study-candidate")
async def case_candidate(req: _EventsRequest) -> dict[str, Any]:
    return {"candidate": case_study_candidate(req.events),
            "hard_gates": _HARD_GATES}


@router.get("/sector-learning")
async def sector_learning() -> dict[str, Any]:
    """Reads from proof-events directory if available."""
    try:
        import json

        from auto_client_acquisition.runtime_paths import resolve_proof_events_dir
        proof_dir = resolve_proof_events_dir()
        events: list[dict] = []
        if proof_dir.exists():
            for f in proof_dir.iterdir():
                if not f.is_file() or f.suffix.lower() not in (".json",):
                    continue
                if any(s in f.name.lower() for s in
                       (".gitkeep", "readme", "schema.example",
                        ".example.", "template")):
                    continue
                try:
                    events.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:
                    continue
        return {"learning": sector_learning_summary(events),
                "events_loaded": len(events),
                "hard_gates": _HARD_GATES}
    except Exception as exc:
        return {"learning": {"insufficient_data": True, "error": str(exc)},
                "events_loaded": 0, "hard_gates": _HARD_GATES}
