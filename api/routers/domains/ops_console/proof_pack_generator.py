"""Ops Console — Proof Pack Generator.

مولّد حزمة الإثبات.

GET  /api/v1/ops/proof-pack/template  — the empty proof-pack v2 template.
POST /api/v1/ops/proof-pack/preview   — run a diagnostic + return the pack
                                        template to be completed from evidence.

Read-only/composition; admin-key gated. Proof-pack sections are NEVER
auto-filled — the operator completes them from real evidence (doctrine: no
fabricated proof). The diagnostic brief is the only generated artifact.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.schemas.ops_console import ProofPackPreviewRequest
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/proof-pack",
    tags=["Ops Console — Proof Pack Generator"],
    dependencies=[Depends(require_admin_key)],
)


def _proof_pack_template() -> dict[str, Any]:
    from auto_client_acquisition.proof_os import (
        PROOF_PACK_V2_SECTIONS,
        build_empty_proof_pack_v2,
        proof_pack_completeness_score,
        proof_strength_band,
    )

    empty = build_empty_proof_pack_v2()
    score = proof_pack_completeness_score(empty)
    return {
        "empty_pack": empty,
        "sections": list(PROOF_PACK_V2_SECTIONS),
        "completeness_score": score,
        "strength_band": proof_strength_band(score),
    }


def _run_diagnostic(body: ProofPackPreviewRequest) -> dict[str, Any]:
    try:
        from auto_client_acquisition.diagnostic_engine.engine import generate_diagnostic
        from auto_client_acquisition.diagnostic_engine.schemas import DiagnosticRequest

        result = generate_diagnostic(
            DiagnosticRequest(
                company=body.company,
                sector=body.sector,
                region=body.region,
                pipeline_state=body.pipeline_state,
            )
        )
        return {
            "company": result.company,
            "recommended_bundle": result.recommended_bundle,
            "bundle_name_ar": result.bundle_name_ar,
            "bundle_name_en": result.bundle_name_en,
            "services_in_bundle": list(result.services_in_bundle),
            "markdown_ar_en": result.markdown_ar_en,
            "approval_status": result.approval_status,
            "safety_notes": list(result.safety_notes),
        }
    except Exception as exc:  # noqa: BLE001
        return {"note": "diagnostic_engine_unavailable", "error": exc.__class__.__name__}


@router.get("/template")
async def proof_pack_template() -> dict[str, Any]:
    """The empty proof-pack v2 template and section list."""
    try:
        tpl = _proof_pack_template()
    except Exception:  # noqa: BLE001
        return governed({"sections": [], "note": "proof_os_unavailable"})
    return governed(tpl)


@router.post("/preview")
async def proof_pack_preview(body: ProofPackPreviewRequest) -> dict[str, Any]:
    """Run a diagnostic and return the proof-pack template to be completed."""
    diagnostic = _run_diagnostic(body)
    try:
        tpl = _proof_pack_template()
    except Exception:  # noqa: BLE001
        tpl = {"empty_pack": {}, "sections": [], "completeness_score": 0,
               "strength_band": "weak_proof"}
    return governed(
        {
            "diagnostic": diagnostic,
            "proof_pack": tpl["empty_pack"],
            "sections": tpl["sections"],
            "completeness_score": tpl["completeness_score"],
            "strength_band": tpl["strength_band"],
            "note": (
                "Proof-pack sections must be completed from real evidence — "
                "they are never auto-generated."
            ),
        }
    )
