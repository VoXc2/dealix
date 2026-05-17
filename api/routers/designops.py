"""DesignOps Router — bilingual artifact composition endpoints.

موجِّه DesignOps — نقاط نهاية تأليف القطع ثنائيّة اللغة.

Endpoints under /api/v1/designops/:
    GET  /status                        — module info + guardrails
    GET  /skills                        — list registered skills
    GET  /skills/{name}                 — fetch one skill spec
    POST /brief                         — proxy brief_builder.build_brief
    POST /check-artifact                — proxy safety_gate.check_artifact
    POST /generate/mini-diagnostic      — bilingual mini diagnostic
    POST /generate/proof-pack           — bilingual proof pack
    POST /generate/executive-weekly-pack — bilingual executive weekly pack
    POST /generate/proposal-page        — bilingual proposal
    POST /generate/pricing-page         — bilingual pricing page
    POST /generate/customer-room-dashboard — bilingual customer room

Pure local composition: no LLM calls, no live sends, no external HTTP.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.designops.generators import (
    generate_customer_room_dashboard,
    generate_executive_weekly_pack,
    generate_mini_diagnostic,
    generate_pricing_page,
    generate_proof_pack,
    generate_proposal_page,
)


router = APIRouter(prefix="/api/v1/designops", tags=["designops"])


# ── Request bodies ─────────────────────────────────────────────────


class MiniDiagnosticRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    region: str = "ksa"
    pipeline_state: str = ""
    language: str = "bilingual"


class ProofPackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_handle: str = Field(..., min_length=1)
    events: list[dict[str, Any]] = Field(default_factory=list)
    period_label: str = ""


class ExecutiveWeeklyPackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    week_label: str = ""


class ProposalPageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_handle: str = Field(..., min_length=1)
    recommended_service: str = "growth_starter"
    scope_ar: str = ""
    scope_en: str = ""
    deliverables: list[str] = Field(default_factory=list)
    timeline_days: int = 7
    price_band_sar: str = "499"
    blocked_actions: list[str] = Field(default_factory=list)
    proof_plan: list[str] = Field(default_factory=list)


class PricingPageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    highlight: str | None = None


class CustomerRoomDashboardRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_handle: str = Field(..., min_length=1)
    customer_payload: dict[str, Any] = Field(default_factory=dict)


class BriefRequest(BaseModel):
    """Loose-typed brief body — forwards to brief_builder.build_brief.

    Schema is owned by Agent B's brief_builder; we accept any dict.
    """

    model_config = ConfigDict(extra="allow")


class ArtifactCheckRequest(BaseModel):
    """Loose-typed artifact-check body — forwards to safety_gate.check_artifact."""

    model_config = ConfigDict(extra="allow")


# ── Endpoints ──────────────────────────────────────────────────────


@router.get("/status")
async def designops_status() -> dict[str, Any]:
    return {
        "module": "designops",
        "version": 1,
        "phase": "5+6+7",
        "generators": [
            "mini_diagnostic",
            "proof_pack",
            "executive_weekly_pack",
            "proposal_page",
            "pricing_page",
            "customer_room_dashboard",
        ],
        "guardrails": {
            "no_llm_call": True,
            "no_external_http": True,
            "no_live_send": True,
            "approval_required_on_every_artifact": True,
            "safe_to_send_default": False,
            "no_marketing_claim_leaks": True,
        },
    }


@router.get("/skills")
async def designops_skills() -> dict[str, Any]:
    """Return the list of registered DesignOps skills.

    Defensive: if Agent A's skill_registry is missing, returns []."""
    try:
        from auto_client_acquisition.designops import skill_registry  # type: ignore

        skills = skill_registry.list_skills()
        return {"skills": list(skills) if skills else []}
    except Exception:
        return {"skills": []}


@router.get("/skills/{name}")
async def designops_skill(name: str) -> dict[str, Any]:
    """Return one skill spec. 404 if not found."""
    try:
        from auto_client_acquisition.designops import skill_registry  # type: ignore

        skill = skill_registry.get_skill(name)
        if not skill:
            raise HTTPException(status_code=404, detail=f"skill {name!r} not found")
        if isinstance(skill, dict):
            return skill
        # If it's a pydantic model, serialise.
        try:
            return skill.model_dump(mode="json")  # type: ignore[attr-defined]
        except Exception:
            return {"name": name, "spec": str(skill)}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="skill_registry not available yet",
        )


@router.post("/brief")
async def designops_brief(payload: BriefRequest) -> dict[str, Any]:
    """Proxy to brief_builder.build_brief — defensive if not shipped."""
    try:
        from auto_client_acquisition.designops import brief_builder  # type: ignore

        result = brief_builder.build_brief(payload.model_dump())
        if hasattr(result, "model_dump"):
            return result.model_dump(mode="json")
        return dict(result) if result else {}
    except Exception as exc:  # noqa: BLE001 — defensive
        raise HTTPException(
            status_code=503,
            detail=f"brief_builder unavailable: {exc!s}",
        )


@router.post("/check-artifact")
async def designops_check_artifact(payload: ArtifactCheckRequest) -> dict[str, Any]:
    """Proxy to safety_gate.check_artifact — defensive if not shipped."""
    try:
        from auto_client_acquisition.designops import safety_gate  # type: ignore

        result = safety_gate.check_artifact(payload.model_dump())
        if hasattr(result, "model_dump"):
            return result.model_dump(mode="json")
        return dict(result) if result else {}
    except Exception as exc:  # noqa: BLE001 — defensive
        raise HTTPException(
            status_code=503,
            detail=f"safety_gate unavailable: {exc!s}",
        )


@router.post("/generate/mini-diagnostic")
async def generate_mini_diagnostic_endpoint(
    payload: MiniDiagnosticRequest,
) -> dict[str, Any]:
    return generate_mini_diagnostic(
        company=payload.company,
        sector=payload.sector,
        region=payload.region,
        pipeline_state=payload.pipeline_state,
        language=payload.language,
    )


@router.post("/generate/proof-pack")
async def generate_proof_pack_endpoint(
    payload: ProofPackRequest,
) -> dict[str, Any]:
    return generate_proof_pack(
        customer_handle=payload.customer_handle,
        events=payload.events,
        period_label=payload.period_label,
    )


@router.post("/generate/executive-weekly-pack")
async def generate_executive_weekly_pack_endpoint(
    payload: ExecutiveWeeklyPackRequest,
) -> dict[str, Any]:
    return generate_executive_weekly_pack(week_label=payload.week_label)


@router.post("/generate/proposal-page")
async def generate_proposal_page_endpoint(
    payload: ProposalPageRequest,
) -> dict[str, Any]:
    return generate_proposal_page(
        customer_handle=payload.customer_handle,
        recommended_service=payload.recommended_service,
        scope_ar=payload.scope_ar,
        scope_en=payload.scope_en,
        deliverables=payload.deliverables,
        timeline_days=payload.timeline_days,
        price_band_sar=payload.price_band_sar,
        blocked_actions=payload.blocked_actions,
        proof_plan=payload.proof_plan,
    )


@router.post("/generate/pricing-page")
async def generate_pricing_page_endpoint(
    payload: PricingPageRequest,
) -> dict[str, Any]:
    return generate_pricing_page(highlight=payload.highlight)


@router.post("/generate/customer-room-dashboard")
async def generate_customer_room_dashboard_endpoint(
    payload: CustomerRoomDashboardRequest,
) -> dict[str, Any]:
    return generate_customer_room_dashboard(
        customer_handle=payload.customer_handle,
        customer_payload=payload.customer_payload,
    )


# ── Content Assets store — approval-gated ─────────────────────────


class ContentAssetCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_type: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    tenant_id: str | None = None
    uri: str = ""
    template_id: str | None = None
    linked_deal_id: str | None = None
    meta_json: dict[str, Any] = Field(default_factory=dict)


class ContentAssetApproveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approver: str = Field(..., min_length=1)


@router.post("/assets")
async def create_content_asset(payload: ContentAssetCreateRequest) -> dict[str, Any]:
    """Create one content asset. Always created in ``draft`` — no approver."""
    from auto_client_acquisition.designops.asset_store import (
        get_default_content_asset_store,
    )

    row = get_default_content_asset_store().add(
        asset_type=payload.asset_type,
        title=payload.title,
        tenant_id=payload.tenant_id,
        uri=payload.uri,
        template_id=payload.template_id,
        linked_deal_id=payload.linked_deal_id,
        meta_json=payload.meta_json,
    )
    return {"asset": row, "governance_decision": "allow"}


@router.get("/assets")
async def list_content_assets(
    tenant_id: str | None = None,
    asset_type: str | None = None,
    status: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """List active content assets, newest first."""
    from auto_client_acquisition.designops.asset_store import (
        get_default_content_asset_store,
    )

    rows = get_default_content_asset_store().list(
        tenant_id=tenant_id,
        asset_type=asset_type,
        status=status,
        limit=max(1, min(int(limit), 1000)),
    )
    return {"count": len(rows), "assets": rows, "governance_decision": "allow"}


@router.get("/assets/{asset_id}")
async def get_content_asset(asset_id: str) -> dict[str, Any]:
    """Fetch one content asset by id."""
    from auto_client_acquisition.designops.asset_store import (
        get_default_content_asset_store,
    )

    row = get_default_content_asset_store().get(asset_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"asset {asset_id!r} not found")
    return {"asset": row, "governance_decision": "allow"}


@router.post("/assets/{asset_id}/approve")
async def approve_content_asset(
    asset_id: str, payload: ContentAssetApproveRequest
) -> dict[str, Any]:
    """Approve a content asset. The only path from ``draft`` to ``approved``."""
    from auto_client_acquisition.designops.asset_store import (
        get_default_content_asset_store,
    )

    try:
        row = get_default_content_asset_store().approve(
            asset_id, approver=payload.approver
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if row is None:
        raise HTTPException(status_code=404, detail=f"asset {asset_id!r} not found")
    return {"asset": row, "governance_decision": "allow"}
