"""Sprint runner router — exposes the 10-step orchestrator from
auto_client_acquisition.delivery_factory.delivery_sprint.

POST /api/v1/sprint/run   →  full orchestrated 10-step result
GET  /api/v1/sprint/sample → run on demo CSV + accounts (smoke / live demo)
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/sprint", tags=["sprint"])


class _SprintRunBody(BaseModel):
    engagement_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    source_passport: dict[str, Any] | None = None
    raw_csv: str = ""
    accounts: list[dict[str, Any]] | None = None
    problem_summary: str = ""
    workflow_owner_present: bool = True


def _run(body: _SprintRunBody):
    """Run the 10-step orchestrator, mapping failures to HTTP 500."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    try:
        return run_sprint(
            engagement_id=body.engagement_id,
            customer_id=body.customer_id,
            source_passport=body.source_passport,
            raw_csv=body.raw_csv,
            accounts=body.accounts,
            problem_summary=body.problem_summary,
            workflow_owner_present=body.workflow_owner_present,
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"sprint_run_failed: {e}") from e


@router.post("/run")
async def run_sprint_endpoint(body: _SprintRunBody) -> dict[str, Any]:
    """Run the 10-step Sprint orchestrator. Returns the full run record
    including each step's output, the Proof Pack, capital assets, and
    retainer eligibility."""
    return _run(body).to_dict()


@router.post("/render/markdown", response_class=PlainTextResponse)
async def render_proof_pack_markdown(body: _SprintRunBody) -> str:
    """Run the Sprint and render its Proof Pack as a customer-facing
    bilingual markdown report."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_markdown,
    )

    run = _run(body)
    return proof_pack_to_markdown(run.proof_pack, customer_handle=body.customer_id)


@router.post("/render/pdf")
async def render_proof_pack_pdf(body: _SprintRunBody):
    """Run the Sprint and render its Proof Pack as PDF. Falls back to
    markdown with an ``X-PDF-Renderer`` header when no PDF renderer is
    installed."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_markdown,
        proof_pack_to_pdf,
    )

    run = _run(body)
    pdf = proof_pack_to_pdf(run.proof_pack, customer_handle=body.customer_id)
    if pdf is None:
        return PlainTextResponse(
            content=proof_pack_to_markdown(
                run.proof_pack, customer_handle=body.customer_id
            ),
            headers={"X-PDF-Renderer": "unavailable; markdown returned as fallback"},
        )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'inline; filename="proof_pack_{body.engagement_id}.pdf"'
            )
        },
    )


@router.post("/render/email-body", response_class=PlainTextResponse)
async def render_proof_pack_email_body(body: _SprintRunBody) -> str:
    """Run the Sprint and render a short bilingual cover note the founder
    copies into their own mailbox. Render-only — never auto-sent."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_email_body,
    )

    run = _run(body)
    return proof_pack_email_body(run.proof_pack, customer_handle=body.customer_id)


@router.get("/sample")
async def sample_sprint() -> dict[str, Any]:
    """Run the sprint on the synthetic Saudi B2B demo CSV bundled in
    data/demo/saudi_b2b_demo.csv. Used by the landing page + smoke tests.
    """
    import csv
    from pathlib import Path
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    demo_path = Path(__file__).resolve().parent.parent.parent / "data" / "demo" / "saudi_b2b_demo.csv"
    raw = demo_path.read_text(encoding="utf-8") if demo_path.exists() else ""
    accounts: list[dict[str, Any]] = []
    if raw:
        reader = csv.DictReader(raw.splitlines())
        accounts = list(reader)

    passport = {
        "source_id": "DEMO-SAUDI-B2B-001",
        "source_type": "client_upload",
        "owner": "dealix",
        "allowed_use": ["internal_analysis", "scoring"],
        "contains_pii": False,
        "sensitivity": "low",
        "ai_access_allowed": True,
        "external_use_allowed": False,
        "retention_policy": "project_duration",
    }
    run = run_sprint(
        engagement_id="demo_sprint_001",
        customer_id="dealix_internal_demo",
        source_passport=passport,
        raw_csv=raw,
        accounts=accounts,
        problem_summary="Demo: rank Saudi B2B accounts by relationship + sector.",
        workflow_owner_present=True,
    )
    return run.to_dict()
