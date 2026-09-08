"""Tenant-bound Market-to-Delivery intake into existing Commercial Intelligence.

Persists only an L1 signal. No relationship, consent, quote, workers, or send.
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api.security.auth_deps import require_sales_manager
from auto_client_acquisition.service_catalog.intake_request_contract import (
    REQUEST_SCHEMA,
    MarketToDeliveryIntakeBody,
    intake_request_fingerprint,
)
from auto_client_acquisition.service_catalog.market_to_delivery import prepare
from db.models_commercial_intelligence import CommercialSignalRecord, CommercialSourceRecord
from db.session import async_session_factory
from dealix.commercial_intelligence import EvidenceLevel, SourceKind, SourcePolicyStatus

router = APIRouter(
    prefix="/api/v1/commercial-intelligence/market-to-delivery", tags=["Sales"],
)
_ALLOWED_SOURCE_KINDS = {
    SourceKind.OWNED.value, SourceKind.CRM.value, SourceKind.EMAIL.value,
    SourceKind.CLIENT_PROVIDED.value, SourceKind.PARTNER.value, SourceKind.MANUAL.value,
}


def _tenant_id(current_user: Any) -> str:
    value = (current_user.get("tenant_id") if isinstance(current_user, dict)
             else getattr(current_user, "tenant_id", None))
    if not value:
        raise HTTPException(403, "authenticated_tenant_required")
    if not isinstance(value, str):
        raise HTTPException(403, "authenticated_tenant_invalid")
    clean = value.strip()
    if not clean or len(clean) > 64:
        raise HTTPException(403, "authenticated_tenant_invalid")
    return clean


def _preparation_payload(body: MarketToDeliveryIntakeBody, tenant_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id, "request_id": body.request_id,
        "project_id": body.project_id, "problem": body.problem,
        "customer_context": body.customer_context, "current_workflow": body.current_workflow,
        "baseline": body.baseline, "desired_outcome": body.desired_outcome,
        "constraints": body.constraints,
        "evidence_refs": [
            {"ref": item.ref, "sha256": item.sha256, "tenant_id": tenant_id}
            for item in body.evidence_refs
        ],
        "data_authorized": body.data_authorized,
        "estimated_cost_sar": str(body.estimated_cost_sar) if body.estimated_cost_sar is not None else None,
        "target_margin_pct": str(body.target_margin_pct) if body.target_margin_pct is not None else None,
    }


def _prepare(body: MarketToDeliveryIntakeBody, tenant_id: str) -> dict[str, Any]:
    try:
        return prepare(_preparation_payload(body, tenant_id))
    except ValueError as exc:
        reason = str(exc)
        if len(reason) > 160 or not reason.replace("_", "").isalnum():
            reason = "invalid_market_to_delivery_intake"
        raise HTTPException(422, reason) from exc


def _signal_evidence_ref(body: MarketToDeliveryIntakeBody) -> str:
    return f"mtd://request/{body.request_id}"


def _signal_payload(*, body: MarketToDeliveryIntakeBody, preparation: dict[str, Any],
                    request_digest: str) -> dict[str, Any]:
    return {
        "schema_version": "dealix.market-to-delivery.intake-signal.v1",
        "request_id": body.request_id, "company_name": body.company_name,
        "project_id": body.project_id, "request_digest": request_digest,
        "request_digest_version": REQUEST_SCHEMA,
        "artifact_digest": preparation["artifact_digest"],
        "engine_sha256": preparation["engine_sha256"], "catalog_digest": preparation["catalog_digest"],
        "preparation_status": preparation["status"], "missing_inputs": preparation["missing_inputs"],
        "diagnostic": preparation["diagnostic"], "routing": preparation["routing"],
        "data_authorized_for_preparation": True,
        "data_authority_evidence": "OPERATOR_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED",
        "relationship_inferred": False, "consent_inferred": False,
        "opportunity_created": False, "external_action_allowed": False,
    }


async def _find_existing(session: Any, *, tenant_id: str, account_id: str,
                         source_id: str, evidence_ref: str) -> CommercialSignalRecord | None:
    result = await session.execute(
        select(CommercialSignalRecord).where(
            CommercialSignalRecord.tenant_id == tenant_id,
            CommercialSignalRecord.account_id == account_id,
            CommercialSignalRecord.source_id == source_id,
            CommercialSignalRecord.evidence_ref == evidence_ref,
        )
    )
    return result.scalars().first()


def _require_same_replay(record: CommercialSignalRecord, *, request_digest: str,
                         body: MarketToDeliveryIntakeBody, tenant_id: str) -> None:
    stored = record.payload_json if isinstance(record.payload_json, dict) else {}
    if "request_digest" in stored:
        if (stored["request_digest"] != request_digest
                or stored.get("request_digest_version") != REQUEST_SCHEMA):
            raise HTTPException(409, "market_to_delivery_request_id_payload_conflict")
        return
    if stored.get("company_name") != body.company_name:
        raise HTTPException(409, "market_to_delivery_legacy_request_requires_review")
    if stored.get("artifact_digest") != _prepare(body, tenant_id)["artifact_digest"]:
        raise HTTPException(409, "market_to_delivery_legacy_request_requires_review")


def _response(record: CommercialSignalRecord, *, replay: bool) -> dict[str, Any]:
    return {
        "status": "existing" if replay else "created", "signal_id": record.id,
        "evidence_level": record.evidence_level,
        "preparation_status": (record.payload_json or {}).get("preparation_status"),
        "relationship_created": False, "consent_created": False,
        "opportunity_created": False, "external_side_effect": False,
        "next_step": "QUALIFY_SIGNAL_IN_EXISTING_COMMERCIAL_INTELLIGENCE",
    }


@router.post("/intake", status_code=201)
async def persist_market_to_delivery_intake(
    body: MarketToDeliveryIntakeBody, current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    """Record caller intent once; retries never upgrade commercial authority."""
    tenant_id = _tenant_id(current_user)
    if body.data_authorized is not True:
        raise HTTPException(422, "authorized_data_required_even_for_preparation")
    try:
        request_digest = intake_request_fingerprint(body, tenant_id)
    except ValueError as exc:
        raise HTTPException(403, "authenticated_tenant_invalid") from exc
    evidence_ref = _signal_evidence_ref(body)
    observed_at = datetime.now(UTC)
    async with async_session_factory()() as session:
        source = await session.get(CommercialSourceRecord, body.source_id)
        if source is None or source.tenant_id != tenant_id or not source.active:
            raise HTTPException(404, "tenant_intake_source_not_found")
        if source.policy_status == SourcePolicyStatus.BLOCKED.value:
            raise HTTPException(409, "blocked_source_cannot_accept_intake")
        if source.policy_status != SourcePolicyStatus.APPROVED.value:
            raise HTTPException(409, "intake_source_policy_approval_required")
        if source.kind not in _ALLOWED_SOURCE_KINDS:
            raise HTTPException(409, "source_kind_not_eligible_for_customer_intake")
        existing = await _find_existing(
            session, tenant_id=tenant_id, account_id=body.account_id,
            source_id=source.id, evidence_ref=evidence_ref,
        )
        if existing is not None:
            _require_same_replay(existing, request_digest=request_digest, body=body, tenant_id=tenant_id)
            return _response(existing, replay=True)
        preparation = _prepare(body, tenant_id)
        record = CommercialSignalRecord(
            id=f"sig_{uuid.uuid4().hex}", tenant_id=tenant_id, account_id=body.account_id,
            source_id=source.id, signal_type="market_to_delivery_intake", claim=body.problem,
            evidence_ref=evidence_ref, evidence_level=EvidenceLevel.L1_HYPOTHESIS.value,
            confidence=40, observed_at=observed_at,
            expires_at=observed_at + timedelta(days=source.freshness_days), status="active",
            payload_json=_signal_payload(body=body, preparation=preparation, request_digest=request_digest),
        )
        response = _response(record, replay=False)
        session.add(record)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            existing = await _find_existing(
                session, tenant_id=tenant_id, account_id=body.account_id,
                source_id=source.id, evidence_ref=evidence_ref,
            )
            if existing is None:
                raise HTTPException(409, "market_to_delivery_intake_conflict")
            _require_same_replay(existing, request_digest=request_digest, body=body, tenant_id=tenant_id)
            return _response(existing, replay=True)
        except Exception as exc:
            await session.rollback()
            raise HTTPException(503, "market_to_delivery_intake_not_persisted") from exc
    return response
