"""Tenant-bound Market-to-Delivery intake bridge into Commercial Intelligence.

This module deliberately creates ONLY a canonical CommercialSignalRecord.  It
never creates a relationship, consent record, opportunity, quote approval,
external send, or project worker.  Qualification remains owned by the existing
Commercial Intelligence flow.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api.security.auth_deps import require_sales_manager
from auto_client_acquisition.service_catalog.market_to_delivery import prepare
from db.models_commercial_intelligence import CommercialSignalRecord, CommercialSourceRecord
from db.session import async_session_factory
from dealix.commercial_intelligence import EvidenceLevel, SourceKind, SourcePolicyStatus

router = APIRouter(
    prefix="/api/v1/commercial-intelligence/market-to-delivery",
    tags=["Sales"],
)

_ALLOWED_SOURCE_KINDS = {
    SourceKind.OWNED.value,
    SourceKind.CRM.value,
    SourceKind.EMAIL.value,
    SourceKind.CLIENT_PROVIDED.value,
    SourceKind.PARTNER.value,
    SourceKind.MANUAL.value,
}


class _StrictBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IntakeEvidenceRef(_StrictBody):
    ref: str = Field(min_length=1, max_length=256)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class MarketToDeliveryIntakeBody(_StrictBody):
    request_id: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")
    account_id: str = Field(min_length=1, max_length=64)
    company_name: str = Field(min_length=1, max_length=255)
    source_id: str = Field(min_length=1, max_length=64)
    project_id: str = Field(min_length=1, max_length=80)
    problem: str = Field(min_length=1, max_length=4000)
    customer_context: str | None = Field(default=None, max_length=4000)
    current_workflow: str | None = Field(default=None, max_length=4000)
    baseline: str | None = Field(default=None, max_length=4000)
    desired_outcome: str | None = Field(default=None, max_length=4000)
    constraints: str | None = Field(default=None, max_length=4000)
    evidence_refs: list[IntakeEvidenceRef] = Field(default_factory=list, max_length=20)
    data_authorized: bool
    estimated_cost_sar: Decimal | None = Field(default=None, ge=0, le=1_000_000_000, decimal_places=2)
    target_margin_pct: Decimal | None = Field(default=None, ge=0, le=90, decimal_places=2)


def _tenant_id(current_user: Any) -> str:
    value = (
        current_user.get("tenant_id")
        if isinstance(current_user, dict)
        else getattr(current_user, "tenant_id", None)
    )
    if not value:
        raise HTTPException(403, "authenticated_tenant_required")
    clean = str(value).strip()
    if not clean or len(clean) > 64:
        raise HTTPException(403, "authenticated_tenant_invalid")
    return clean


def _preparation_payload(body: MarketToDeliveryIntakeBody, tenant_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "request_id": body.request_id,
        "project_id": body.project_id,
        "problem": body.problem,
        "customer_context": body.customer_context,
        "current_workflow": body.current_workflow,
        "baseline": body.baseline,
        "desired_outcome": body.desired_outcome,
        "constraints": body.constraints,
        "evidence_refs": [
            {"ref": item.ref, "sha256": item.sha256, "tenant_id": tenant_id}
            for item in body.evidence_refs
        ],
        "data_authorized": body.data_authorized,
        "estimated_cost_sar": str(body.estimated_cost_sar) if body.estimated_cost_sar is not None else None,
        "target_margin_pct": str(body.target_margin_pct) if body.target_margin_pct is not None else None,
    }


def _signal_evidence_ref(body: MarketToDeliveryIntakeBody, artifact_digest: str) -> str:
    return f"mtd://{body.request_id}/{artifact_digest}"


def _signal_payload(
    *,
    body: MarketToDeliveryIntakeBody,
    preparation: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dealix.market-to-delivery.intake-signal.v1",
        "request_id": body.request_id,
        "company_name": body.company_name.strip(),
        "project_id": body.project_id,
        "artifact_digest": preparation["artifact_digest"],
        "engine_sha256": preparation["engine_sha256"],
        "catalog_digest": preparation["catalog_digest"],
        "preparation_status": preparation["status"],
        "missing_inputs": preparation["missing_inputs"],
        "diagnostic": preparation["diagnostic"],
        "routing": preparation["routing"],
        "data_authorized_for_preparation": True,
        "relationship_inferred": False,
        "consent_inferred": False,
        "opportunity_created": False,
        "external_action_allowed": False,
    }


async def _find_existing(
    session: Any,
    *,
    tenant_id: str,
    account_id: str,
    source_id: str,
    evidence_ref: str,
) -> CommercialSignalRecord | None:
    result = await session.execute(
        select(CommercialSignalRecord).where(
            CommercialSignalRecord.tenant_id == tenant_id,
            CommercialSignalRecord.account_id == account_id,
            CommercialSignalRecord.source_id == source_id,
            CommercialSignalRecord.evidence_ref == evidence_ref,
        )
    )
    return result.scalars().first()


def _response(record: CommercialSignalRecord, *, replay: bool) -> dict[str, Any]:
    return {
        "status": "existing" if replay else "created",
        "signal_id": record.id,
        "evidence_level": record.evidence_level,
        "preparation_status": (record.payload_json or {}).get("preparation_status"),
        "relationship_created": False,
        "consent_created": False,
        "opportunity_created": False,
        "external_side_effect": False,
        "next_step": "QUALIFY_SIGNAL_IN_EXISTING_COMMERCIAL_INTELLIGENCE",
    }


@router.post("/intake", status_code=201)
async def persist_market_to_delivery_intake(
    body: MarketToDeliveryIntakeBody,
    current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    """Persist a tenant-bound problem signal without upgrading its commercial state."""
    tenant_id = _tenant_id(current_user)
    try:
        preparation = prepare(_preparation_payload(body, tenant_id))
    except ValueError as exc:
        reason = str(exc)
        if not reason.replace("_", "").isalnum():
            reason = "invalid_market_to_delivery_intake"
        raise HTTPException(422, reason) from exc

    evidence_ref = _signal_evidence_ref(body, preparation["artifact_digest"])
    observed_at = datetime.now(UTC)

    async with async_session_factory()() as session:
        source = await session.get(CommercialSourceRecord, body.source_id)
        if source is None or source.tenant_id != tenant_id or not source.active:
            raise HTTPException(404, "tenant_intake_source_not_found")
        if source.policy_status == SourcePolicyStatus.BLOCKED.value:
            raise HTTPException(409, "blocked_source_cannot_accept_intake")
        if source.kind not in _ALLOWED_SOURCE_KINDS:
            raise HTTPException(409, "source_kind_not_eligible_for_customer_intake")

        existing = await _find_existing(
            session,
            tenant_id=tenant_id,
            account_id=body.account_id,
            source_id=source.id,
            evidence_ref=evidence_ref,
        )
        if existing is not None:
            return _response(existing, replay=True)

        record = CommercialSignalRecord(
            id=f"sig_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            account_id=body.account_id.strip(),
            source_id=source.id,
            signal_type="market_to_delivery_intake",
            claim=body.problem.strip(),
            evidence_ref=evidence_ref,
            # Intake is a stated problem/hypothesis until independent/current evidence
            # is attached through the canonical Commercial Intelligence flow.
            evidence_level=EvidenceLevel.L1_HYPOTHESIS.value,
            confidence=40,
            observed_at=observed_at,
            expires_at=observed_at + timedelta(days=source.freshness_days),
            status="active",
            payload_json=_signal_payload(body=body, preparation=preparation),
        )
        session.add(record)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            # Race-safe replay: the canonical uniqueness constraint is
            # (tenant, account, source, evidence_ref).
            existing = await _find_existing(
                session,
                tenant_id=tenant_id,
                account_id=body.account_id,
                source_id=source.id,
                evidence_ref=evidence_ref,
            )
            if existing is None:
                raise HTTPException(409, "market_to_delivery_intake_conflict")
            return _response(existing, replay=True)
        except Exception as exc:
            await session.rollback()
            raise HTTPException(503, "market_to_delivery_intake_not_persisted") from exc

    return _response(record, replay=False)
