"""Sprint runner router — exposes the 10-step orchestrator from
auto_client_acquisition.delivery_factory.delivery_sprint.

POST /api/v1/sprint/run         →  full orchestrated 10-step result
POST /api/v1/sprint/render/*    →  render an existing Proof Pack (no re-run)
GET  /api/v1/sprint/sample      → run on demo CSV + accounts (smoke / demo)

The ``/render/*`` routes are pure formatting: they take the Proof Pack from
a prior ``/run`` response and never execute the Sprint again — re-running
would duplicate ledger and capital-asset side effects.
"""
from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/sprint", tags=["sprint"])

# ---------------------------------------------------------------------------
# Admin auth dependency
# ---------------------------------------------------------------------------

_ADMIN_KEY_HEADER = "X-Admin-API-Key"


def _require_admin(x_admin_api_key: str | None = Header(default=None, alias=_ADMIN_KEY_HEADER)) -> str:
    """FastAPI dependency — validates the X-Admin-API-Key header."""
    if not x_admin_api_key:
        raise HTTPException(status_code=401, detail="X-Admin-API-Key header is required.")
    from core.config.settings import get_settings
    settings = get_settings()
    allowed_keys = settings.admin_api_key_list
    # When no keys are configured (dev / test), any non-empty key is accepted.
    if allowed_keys and x_admin_api_key not in allowed_keys:
        raise HTTPException(status_code=403, detail="Invalid admin API key.")
    return x_admin_api_key


class _SprintRunBody(BaseModel):
    engagement_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    source_passport: dict[str, Any] | None = None
    raw_csv: str = ""
    accounts: list[dict[str, Any]] | None = None
    problem_summary: str = ""
    workflow_owner_present: bool = True


class _ProofPackRenderBody(BaseModel):
    """Render input — the Proof Pack from a prior ``/run`` response.

    ``proof_pack`` is the ``proof_pack`` object of a SprintRun. ``run`` is
    accepted as a convenience: the whole ``/run`` response can be posted back
    and the Proof Pack is extracted from it.
    """

    customer_handle: str = Field(..., min_length=1)
    engagement_id: str = "proof_pack"
    proof_pack: dict[str, Any] | None = None
    run: dict[str, Any] | None = None

    def pack(self) -> dict[str, Any] | None:
        if self.proof_pack is not None:
            return self.proof_pack
        if self.run is not None:
            return self.run.get("proof_pack")
        return None


@router.post("/run")
async def run_sprint_endpoint(body: _SprintRunBody) -> dict[str, Any]:
    """Run the 10-step Sprint orchestrator. Returns the full run record
    including each step's output, the Proof Pack, capital assets, and
    retainer eligibility."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    try:
        run = run_sprint(
            engagement_id=body.engagement_id,
            customer_id=body.customer_id,
            source_passport=body.source_passport,
            raw_csv=body.raw_csv,
            accounts=body.accounts,
            problem_summary=body.problem_summary,
            workflow_owner_present=body.workflow_owner_present,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"sprint_run_failed: {e}") from e
    return run.to_dict()


@router.post("/render/markdown", response_class=PlainTextResponse)
async def render_proof_pack_markdown(body: _ProofPackRenderBody) -> str:
    """Render an existing Proof Pack as a customer-facing bilingual markdown
    report. Does not run the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_markdown,
    )

    return proof_pack_to_markdown(body.pack(), customer_handle=body.customer_handle)


@router.post("/render/pdf")
async def render_proof_pack_pdf(body: _ProofPackRenderBody):
    """Render an existing Proof Pack as PDF. Falls back to markdown with an
    ``X-PDF-Renderer`` header when no PDF renderer is installed. Does not run
    the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_markdown,
        proof_pack_to_pdf,
    )

    pack = body.pack()
    pdf = proof_pack_to_pdf(pack, customer_handle=body.customer_handle)
    if pdf is None:
        return PlainTextResponse(
            content=proof_pack_to_markdown(
                pack, customer_handle=body.customer_handle
            ),
            headers={"X-PDF-Renderer": "unavailable; markdown returned as fallback"},
        )
    # Sanitize the client-supplied id before it reaches a response header —
    # strip anything outside [A-Za-z0-9._-] to prevent CR/LF header injection.
    safe_id = re.sub(r"[^A-Za-z0-9._-]", "_", body.engagement_id)[:64] or "proof_pack"
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="proof_pack_{safe_id}.pdf"'
        },
    )


@router.post("/render/email-body", response_class=PlainTextResponse)
async def render_proof_pack_email_body(body: _ProofPackRenderBody) -> str:
    """Render a short bilingual cover note from an existing Proof Pack — the
    founder copies it into their own mailbox. Render-only — never auto-sent,
    never runs the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_email_body,
    )

    return proof_pack_email_body(body.pack(), customer_handle=body.customer_handle)


# ---------------------------------------------------------------------------
# New delivery endpoints — all require admin auth
# ---------------------------------------------------------------------------


class _SourcePassportBody(BaseModel):
    sources: list[dict[str, Any]] = Field(
        ..., description="List of raw source dicts matching the LeadSource schema."
    )


class _AccountScoringBody(BaseModel):
    accounts: list[dict[str, Any]] = Field(
        ..., description="List of raw account dicts matching the AccountProfile schema."
    )


class _RetainerCheckBody(BaseModel):
    account_id: str = Field(..., min_length=1)
    proof_level: str = Field(..., description="Highest proof level, e.g. 'L2'.")
    satisfaction_score: float = Field(..., ge=0.0, le=10.0)
    measurable_result_achieved: bool = Field(default=False)


@router.post("/{sprint_id}/source-passport")
async def run_source_passport(
    sprint_id: str,
    body: _SourcePassportBody,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Run source passport analysis for a sprint engagement.

    Validates and DQ-scores all supplied lead sources. Returns a SourcePassport
    with overall_dq_score, red_flags, and bilingual recommendations.
    """
    from dealix.revenue_ops_autopilot.source_passport import SourcePassportBuilder

    try:
        passport = SourcePassportBuilder().build(body.sources)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"source_passport_error: {e}") from e
    result = passport.model_dump()
    result["sprint_id"] = sprint_id
    return result


@router.post("/{sprint_id}/account-scoring")
async def run_account_scoring(
    sprint_id: str,
    body: _AccountScoringBody,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Score and rank accounts by composite revenue potential.

    Returns up to the top 10 scored accounts with priority ranks and bilingual
    recommended actions.
    """
    from dealix.revenue_ops_autopilot.account_scoring_matrix import (
        AccountProfile,
        AccountScoringMatrix,
    )

    try:
        profiles = [AccountProfile(**a) for a in body.accounts]
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"account_profile_parse_error: {e}") from e

    try:
        scored = AccountScoringMatrix().score_accounts(profiles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"account_scoring_error: {e}") from e

    top10 = scored[:10]
    return {
        "sprint_id": sprint_id,
        "total_accounts_scored": len(scored),
        "top_accounts": [s.model_dump() for s in top10],
    }


@router.post("/{sprint_id}/retainer-check")
async def run_retainer_check(
    sprint_id: str,
    body: _RetainerCheckBody,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Check whether this sprint's client qualifies for a Managed Ops retainer.

    Returns eligibility status, recommended tier, and bilingual upsell pitch.
    """
    from dealix.revenue_ops_autopilot.retainer_eligibility import (
        RetainerEligibilityEngine,
    )

    sprint_result = {
        "sprint_id": sprint_id,
        "account_id": body.account_id,
        "proof_level": body.proof_level,
        "satisfaction_score": body.satisfaction_score,
        "measurable_result_achieved": body.measurable_result_achieved,
    }
    try:
        check = RetainerEligibilityEngine().check(sprint_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"retainer_check_error: {e}") from e
    return check.model_dump()


@router.get("/{sprint_id}/capital-assets")
async def list_capital_assets(
    sprint_id: str,
    account_id: str,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """List all capital assets registered for the account associated with this sprint.

    Requires an ``account_id`` query parameter to look up assets in the registry.
    Also returns the total estimated value in SAR.
    """
    from dealix.revenue_ops_autopilot.capital_asset_registry import CapitalAssetRegistry

    try:
        registry = CapitalAssetRegistry()
        assets = registry.get_by_account(account_id)
        total_value = registry.get_total_value_by_account(account_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"capital_assets_error: {e}") from e

    return {
        "sprint_id": sprint_id,
        "account_id": account_id,
        "total_assets": len(assets),
        "total_value_sar": total_value,
        "assets": [a.model_dump() for a in assets],
    }


@router.get("/sample")
async def sample_sprint() -> dict[str, Any]:
    """Run the sprint on the synthetic Saudi B2B demo CSV bundled in
    data/demo/saudi_b2b_demo.csv. Cached in Redis for 1 hour — demo calls
    return in <100ms after first run.
    """
    import csv
    import json
    from pathlib import Path

    _DEMO_CACHE_KEY = "dealix:demo:sprint:sample:v2"
    _DEMO_CACHE_TTL = 3600  # 1 hour

    # Try Redis cache first — short timeout so a missing Redis never delays demo
    redis_client = None
    try:
        from redis.asyncio import Redis as AsyncRedis

        from core.config.settings import get_settings
        settings = get_settings()
        redis_client = AsyncRedis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2)
        cached_raw = await redis_client.get(_DEMO_CACHE_KEY)
        if cached_raw:
            return json.loads(cached_raw)
    except Exception:  # Redis unavailable — fall through to live run
        pass

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
    result = run.to_dict()

    # Cache the result for 1 hour — best-effort, never fatal
    try:
        if redis_client:
            await redis_client.setex(_DEMO_CACHE_KEY, _DEMO_CACHE_TTL, json.dumps(result, default=str))
    except Exception:  # Redis write failure is non-fatal; next call will re-run sprint
        pass

    return result
