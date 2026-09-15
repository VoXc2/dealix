"""Canonical commercial runtime surfaces that quarantine retired price/offer authority."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.approval_center.schemas import ApprovalRequest, ApprovalStatus
from dealix.commercial_ops.objections import match_objections
from dealix.revenue_ops_autopilot.policies import INVOICE_DRAFT_ALLOWED_LEAD_STAGES
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent, InvoiceDraftRecord
from dealix.revenue_ops_autopilot.store import get_autopilot_store, uid
from dealix.revenue_ops_autopilot.war_room import normalize_lead

router = APIRouter(tags=["commercial-runtime-truth"])

CANONICAL_PRIMARY_OFFER_ID = "revenue_command_pilot_30d"
CANONICAL_ENTRY_OFFER_ID = "free_mini_diagnostic"
QUOTE_AUTHORITY_SCHEMA = "dealix.customer-specific-quote-authority.v1"
QUOTE_AUTHORITY_OBJECT_TYPE = "customer_specific_quote"
QUOTE_AUTHORITY_ACTION_TYPE = "customer_specific_quote"
QUOTE_AUTHORITY_TTL_DAYS = 14
QUOTE_AUTHORITY_ELIGIBLE_LEAD_STAGES = {"meeting_done", "scope_requested", "scope_sent"}


def _canonical_commercial_map() -> dict[str, Any]:
    return {
        "authority": "launch_commercial_truth",
        "entry_offer": {
            "id": CANONICAL_ENTRY_OFFER_ID,
            "label_ar": "Mini Diagnostic مجاني",
            "label_en": "Free Mini Diagnostic",
            "price_model": "free",
            "public_checkout": False,
        },
        "primary_offer": {
            "id": CANONICAL_PRIMARY_OFFER_ID,
            "label_ar": "Revenue Command Pilot",
            "label_en": "Revenue Command Pilot",
            "duration_days": None,
            "duration_model": "customer_specific_after_qualified_discovery",
            "duration_policy": "customer_specific_after_qualified_discovery",
            "legacy_id_semantics": "identifier_only_no_fixed_duration_authority",
            "price_model": "customer_specific_quote_only",
            "public_fixed_pricing": False,
            "public_checkout": False,
        },
        "buying_path": [
            "FREE_MINI_DIAGNOSTIC",
            "QUALIFIED_DISCOVERY",
            "CUSTOMER_SPECIFIC_QUOTE",
            "CUSTOMER_SPECIFIC_INTERVENTION",
            "VERIFIED_PAYMENT",
            "DELIVERY",
            "CUSTOMER_VALIDATED_PROOF",
            "STOP_EXPAND_REDESIGN",
        ],
        "guardrails": {
            "no_public_fixed_price": True,
            "no_public_checkout": True,
            "quote_requires_qualified_discovery": True,
            "quote_requires_explicit_authority": True,
            "invoice_requires_approved_quote_fingerprint": True,
            "invoice_requires_approval_record_before_persistence": True,
            "invoice_draft_is_idempotent": True,
            "invoice_is_not_payment": True,
            "payment_requires_independent_evidence": True,
            "no_automatic_discount": True,
            "no_automatic_payment": True,
        },
    }


class CustomerSpecificQuoteAuthorityPayload(BaseModel):
    """Named-customer quote facts that must be approved before invoicing.

    This endpoint does not calculate a price. The caller supplies the exact named-customer
    amount after qualified discovery; Dealix binds those facts into an Approval Center
    fingerprint so a later invoice cannot substitute a different amount or scope.
    """

    model_config = ConfigDict(extra="forbid")

    lead_id: str = Field(..., min_length=1)
    approved_amount_sar: float = Field(..., gt=0)
    qualified_discovery_ref: str = Field(..., min_length=1)
    customer_specific_scope_ref: str = Field(..., min_length=1)


class CustomerSpecificInvoiceDraftPayload(CustomerSpecificQuoteAuthorityPayload):
    """Record an idempotent invoice draft from an approved quote fingerprint."""

    quote_authority_ref: str = Field(..., min_length=1)
    idempotency_key: str = Field(..., min_length=8, max_length=512)


def _require_non_blank(value: str, *, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise HTTPException(
            status_code=422,
            detail={"reason": "commercial_authority_ref_required", "field": field_name},
        )
    return cleaned


def _canonical_sar_amount(value: float) -> str:
    """Return an exact two-decimal SAR amount for quote fingerprinting."""
    try:
        raw = Decimal(str(value))
        amount = raw.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail={"reason": "invalid_customer_specific_quote_amount"},
        ) from exc
    if raw != amount or amount <= 0:
        raise HTTPException(
            status_code=422,
            detail={
                "reason": "invalid_customer_specific_quote_amount",
                "message": "SAR amount must be positive with at most two decimal places.",
            },
        )
    return format(amount, ".2f")


def _quote_authority_material(
    *,
    lead_id: str,
    approved_amount_sar: float,
    qualified_discovery_ref: str,
    customer_specific_scope_ref: str,
) -> dict[str, str]:
    return {
        "schema": QUOTE_AUTHORITY_SCHEMA,
        "lead_id": _require_non_blank(lead_id, field_name="lead_id"),
        "offer_id": CANONICAL_PRIMARY_OFFER_ID,
        "approved_amount_sar": _canonical_sar_amount(approved_amount_sar),
        "qualified_discovery_ref": _require_non_blank(
            qualified_discovery_ref,
            field_name="qualified_discovery_ref",
        ),
        "customer_specific_scope_ref": _require_non_blank(
            customer_specific_scope_ref,
            field_name="customer_specific_scope_ref",
        ),
    }


def _quote_authority_fingerprint(material: dict[str, str]) -> str:
    encoded = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _invoice_identity(
    *,
    quote_fingerprint: str,
    idempotency_key: str,
) -> tuple[str, str, str, str]:
    normalized_key = _require_non_blank(idempotency_key, field_name="idempotency_key")
    digest = hashlib.sha256(
        f"{quote_fingerprint}\n{normalized_key}".encode()
    ).hexdigest()
    return (
        normalized_key,
        digest,
        f"inv_{digest[:32]}",
        f"apr_invoice_{digest[:24]}",
    )


def _append_evidence_event(
    *,
    event_type: str,
    summary: str,
    entity_type: str = "",
    entity_id: str = "",
    approval_id: str | None = None,
) -> EvidenceEvent:
    ev = EvidenceEvent(
        id=uid("ev"),
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        summary=summary,
        approval_id=approval_id,
    )
    return get_autopilot_store().append_evidence(ev)


def _approval_is_unexpired(approval: ApprovalRequest) -> bool:
    return approval.expires_at is None or approval.expires_at > datetime.now(UTC)


def _approval_contract(approval: ApprovalRequest) -> dict[str, Any]:
    """Immutable approval identity used to reject conflicting replays."""
    return {
        "approval_id": approval.approval_id,
        "object_type": approval.object_type,
        "object_id": approval.object_id,
        "action_type": approval.action_type,
        "action_mode": approval.action_mode,
        "channel": approval.channel,
        "risk_level": approval.risk_level,
        "proof_impact": approval.proof_impact,
        "action_id": approval.action_id,
        "lead_id": approval.lead_id,
        "audit_ref": approval.audit_ref,
        "proof_target": approval.proof_target,
    }


def _ensure_approval_request(req: ApprovalRequest) -> tuple[ApprovalRequest, bool]:
    """Create an approval once; fail closed on storage failure or ID conflict."""
    approval_store = get_default_approval_store()
    existing = approval_store.get(req.approval_id)
    if existing is not None:
        if _approval_contract(existing) != _approval_contract(req):
            raise HTTPException(
                status_code=409,
                detail={
                    "reason": "approval_idempotency_conflict",
                    "approval_id": req.approval_id,
                },
            )
        return existing, False
    try:
        return approval_store.create(req), True
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"reason": "approval_center_unavailable"},
        ) from exc


def _resolve_quote_authority(
    *,
    quote_authority_ref: str,
    material: dict[str, str],
) -> tuple[ApprovalRequest, str]:
    approval_store = get_default_approval_store()
    approval = approval_store.get(quote_authority_ref)
    if approval is None:
        raise HTTPException(
            status_code=422,
            detail={"reason": "quote_authority_not_found"},
        )

    status = ApprovalStatus(approval.status)
    if status != ApprovalStatus.APPROVED:
        raise HTTPException(
            status_code=422,
            detail={
                "reason": "quote_authority_not_approved",
                "approval_status": status.value,
            },
        )
    if not _approval_is_unexpired(approval):
        raise HTTPException(
            status_code=422,
            detail={"reason": "quote_authority_expired"},
        )

    fingerprint = _quote_authority_fingerprint(material)
    expected_action_id = f"quote:{fingerprint}"
    binding_matches = (
        approval.object_type == QUOTE_AUTHORITY_OBJECT_TYPE
        and approval.action_type == QUOTE_AUTHORITY_ACTION_TYPE
        and approval.object_id == fingerprint
        and approval.action_id == expected_action_id
        and approval.lead_id == material["lead_id"]
    )
    if not binding_matches:
        raise HTTPException(
            status_code=422,
            detail={"reason": "quote_authority_fingerprint_mismatch"},
        )
    return approval, fingerprint


@router.get("/api/v1/public/services")
async def public_services_catalog_canonical() -> dict[str, Any]:
    """Expose the current quote-only buying path with no public price authority."""
    return _canonical_commercial_map()


@router.get("/api/v1/commercial-map")
async def commercial_map_canonical() -> dict[str, Any]:
    """Compatibility URL backed only by the launch-authorized commercial truth."""
    return _canonical_commercial_map()


@router.get("/api/v1/commercial-map/markdown", response_class=PlainTextResponse)
async def commercial_map_markdown_canonical() -> str:
    """Human-readable compatibility view without fixed-price or checkout authority."""
    return "\n".join(
        [
            "# Dealix Commercial Path",
            "",
            "Free Mini Diagnostic",
            "→ Qualified Discovery",
            "→ Customer-Specific Quote",
            "→ Customer-Specific Intervention (scope + duration + acceptance criteria)",
            "→ Verified Payment",
            "→ Delivery",
            "→ Customer-Validated Proof",
            "→ Stop / Expand / Redesign",
            "",
            "Public fixed pricing: false",
            "Public checkout: false",
            "Price authority: customer-specific quote after qualified discovery",
            "Invoice is not payment.",
        ]
    ) + "\n"


@router.get(
    "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
    dependencies=[Depends(require_admin_key)],
)
async def ops_lead_meeting_brief_canonical(
    lead_id: str,
    locale: str = "ar",
) -> dict[str, Any]:
    lead = get_autopilot_store().get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    lead = normalize_lead(lead)

    questions_ar = [
        "أين يضيع الإيراد بعد أول تواصل؟",
        "من يملك المتابعة اليوم (اسم/دور)؟",
        "هل CRM موثوق للـ AI أم توجد فجوات مصدر؟",
        "هل توجد موافقة قبل أي إجراء خارجي؟",
        "ما المشكلة المحددة التي تستحق Mini Diagnostic الآن؟",
        "ما baseline وطريقة الإثبات ومعايير القبول التي ستحدد نجاح التدخل المخصص؟",
    ]
    pain_blob = " ".join(
        filter(
            None,
            [lead.pain_hypothesis, lead.pain, lead.company, lead.segment, lead.industry],
        ),
    )
    objection_hints = match_objections(pain_blob, limit=4)
    if not objection_hints:
        objection_hints = match_objections("crm وكالة سعر", limit=3)

    return {
        "lead_id": lead_id,
        "company": lead.company,
        "segment": lead.segment,
        "pain_hypothesis": lead.pain_hypothesis or lead.pain,
        "discovery_questions_ar": questions_ar,
        "demo_path": f"/{locale}/business-now#strategy",
        "entry_offer": CANONICAL_ENTRY_OFFER_ID,
        "recommended_offer": CANONICAL_PRIMARY_OFFER_ID,
        "offer_route": [
            "FREE_MINI_DIAGNOSTIC",
            "QUALIFIED_DISCOVERY",
            "CUSTOMER_SPECIFIC_QUOTE",
            "CUSTOMER_SPECIFIC_INTERVENTION",
        ],
        "outreach_draft_ar": lead.outreach_draft_snippet_ar,
        "objection_hints": objection_hints,
        "policy_ar": (
            "لا سعر عام · لا ضمان ROI · لا إرسال آلي · "
            "العرض المخصص فقط بعد Qualified Discovery."
        ),
    }


@router.post(
    "/api/v1/quotes/authority/request",
    dependencies=[Depends(require_admin_key)],
)
async def request_customer_specific_quote_authority(
    body: CustomerSpecificQuoteAuthorityPayload,
) -> dict[str, Any]:
    """Bind exact named-customer quote facts to the existing Approval Center.

    No price is calculated here and nothing is sent. The route only creates (or reuses)
    a pending/approved approval record whose object/action fingerprint commits to the
    exact lead, amount, discovery reference, scope reference, and canonical customer-specific intervention.
    """
    material = _quote_authority_material(
        lead_id=body.lead_id,
        approved_amount_sar=body.approved_amount_sar,
        qualified_discovery_ref=body.qualified_discovery_ref,
        customer_specific_scope_ref=body.customer_specific_scope_ref,
    )
    lead_id = material["lead_id"]
    lead = get_autopilot_store().get_lead(lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="lead_not_found")
    if lead.stage not in QUOTE_AUTHORITY_ELIGIBLE_LEAD_STAGES:
        raise HTTPException(
            status_code=422,
            detail={
                "reason": "quote_authority_blocked_until_qualified_discovery",
                "current_stage": lead.stage,
                "allowed_lead_stages": sorted(QUOTE_AUTHORITY_ELIGIBLE_LEAD_STAGES),
            },
        )

    fingerprint = _quote_authority_fingerprint(material)
    action_id = f"quote:{fingerprint}"
    approval_store = get_default_approval_store()

    existing: ApprovalRequest | None = None
    for candidate in approval_store.list_history(limit=500):
        if (
            candidate.object_type == QUOTE_AUTHORITY_OBJECT_TYPE
            and candidate.object_id == fingerprint
            and candidate.action_id == action_id
            and candidate.lead_id == lead_id
            and ApprovalStatus(candidate.status) in {ApprovalStatus.PENDING, ApprovalStatus.APPROVED}
            and _approval_is_unexpired(candidate)
        ):
            existing = candidate
            break

    if existing is None:
        try:
            existing = approval_store.create(
                ApprovalRequest(
                    object_type=QUOTE_AUTHORITY_OBJECT_TYPE,
                    object_id=fingerprint,
                    action_type=QUOTE_AUTHORITY_ACTION_TYPE,
                    action_mode="approval_required",
                    channel="finance_manual",
                    summary_ar=(
                        "موافقة عرض عميل مخصص — Revenue Command Pilot بنطاق ومدة خاصين بالعميل — "
                        f"المبلغ SAR {material['approved_amount_sar']}؛ لا إرسال ولا دفع تلقائي."
                    ),
                    summary_en=(
                        "Customer-specific quote approval — customer-specific Revenue Command Pilot — "
                        f"amount SAR {material['approved_amount_sar']}; no automatic send or charge."
                    ),
                    risk_level="high",
                    proof_impact=f"customer_specific_quote:{fingerprint}",
                    expires_at=datetime.now(UTC) + timedelta(days=QUOTE_AUTHORITY_TTL_DAYS),
                    action_id=action_id,
                    lead_id=lead_id,
                    audit_ref=material["qualified_discovery_ref"],
                    proof_target=f"invoice_authority:{fingerprint}",
                ),
            )
        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail={"reason": "approval_center_unavailable"},
            ) from exc

    _append_evidence_event(
        event_type="customer_specific_quote_authority_requested",
        summary=(
            f"lead_id={lead_id} quote_fingerprint={fingerprint} "
            f"approval_id={existing.approval_id} status={ApprovalStatus(existing.status).value} "
            "external_send=false live_charge=false"
        ),
        entity_type=QUOTE_AUTHORITY_OBJECT_TYPE,
        entity_id=fingerprint,
        approval_id=existing.approval_id,
    )
    return {
        "status": (
            "approved"
            if ApprovalStatus(existing.status) == ApprovalStatus.APPROVED
            else "approval_required"
        ),
        "quote_authority_ref": existing.approval_id,
        "quote_fingerprint": fingerprint,
        "approval": existing.model_dump(mode="json"),
        "authority": {
            "price_calculated_by_endpoint": False,
            "external_send_allowed": False,
            "live_charge_allowed": False,
            "invoice_allowed_only_after_approval": True,
        },
    }


@router.post(
    "/api/v1/invoices/draft",
    dependencies=[Depends(require_admin_key)],
)
async def invoice_create_draft_from_approved_quote(
    body: CustomerSpecificInvoiceDraftPayload,
) -> dict[str, Any]:
    material = _quote_authority_material(
        lead_id=body.lead_id,
        approved_amount_sar=body.approved_amount_sar,
        qualified_discovery_ref=body.qualified_discovery_ref,
        customer_specific_scope_ref=body.customer_specific_scope_ref,
    )
    lead_id = material["lead_id"]
    quote_authority_ref = _require_non_blank(
        body.quote_authority_ref,
        field_name="quote_authority_ref",
    )

    store = get_autopilot_store()
    lead_bind = store.get_lead(lead_id)
    if not lead_bind:
        raise HTTPException(status_code=404, detail="lead_not_found")
    if lead_bind.stage not in INVOICE_DRAFT_ALLOWED_LEAD_STAGES:
        raise HTTPException(
            status_code=422,
            detail={
                "reason": "invoice_draft_blocked_until_scope_sent",
                "current_stage": lead_bind.stage,
                "allowed_lead_stages": sorted(INVOICE_DRAFT_ALLOWED_LEAD_STAGES),
            },
        )

    quote_approval, quote_fingerprint = _resolve_quote_authority(
        quote_authority_ref=quote_authority_ref,
        material=material,
    )
    normalized_idempotency_key, invoice_digest, invoice_id, invoice_approval_id = (
        _invoice_identity(
            quote_fingerprint=quote_fingerprint,
            idempotency_key=body.idempotency_key,
        )
    )
    invoice_action_id = f"invoice:{invoice_digest}"

    invoice_approval_request = ApprovalRequest(
        approval_id=invoice_approval_id,
        object_type="invoice_draft",
        object_id=invoice_id,
        action_type="invoice_draft",
        action_mode="approval_required",
        channel="finance_manual",
        summary_ar=(
            "مسودة فاتورة من عرض عميل مخصص معتمد ببصمة ثابتة؛ "
            "تحتاج موافقة مستقلة قبل أي إرسال أو طلب دفع."
        ),
        summary_en=(
            "Invoice draft from an approved customer-specific quote fingerprint; "
            "independent approval is required before any send or payment request."
        ),
        risk_level="high",
        proof_impact=f"invoice_draft:{invoice_id}",
        action_id=invoice_action_id,
        lead_id=lead_id,
        audit_ref=quote_authority_ref,
        proof_target=f"payment_evidence:{invoice_id}",
    )
    invoice_approval, approval_created = _ensure_approval_request(
        invoice_approval_request
    )

    approved_amount = float(Decimal(material["approved_amount_sar"]))
    inv = InvoiceDraftRecord(
        id=invoice_id,
        lead_id=lead_id,
        tier="customer_specific_quote",
        amount_sar=approved_amount,
        line_items_ar=[
            "Revenue Command Pilot — نطاق ومدة ومعايير قبول خاصة بالعميل ومعتمدة",
            "المبلغ مربوط ببصمة Approval Center للعرض؛ مسودة الفاتورة ليست دفعًا.",
        ],
        status="approval_required",
        governance_note_ar=(
            "مسودة فقط: لا إرسال، لا رابط دفع، ولا تحصيل تلقائي. "
            "تتطلب موافقة مستقلة وإثبات دفع مستقل."
        ),
        qualified_discovery_ref=material["qualified_discovery_ref"],
        customer_specific_scope_ref=material["customer_specific_scope_ref"],
        quote_authority_ref=quote_authority_ref,
        quote_fingerprint=quote_fingerprint,
        idempotency_key=normalized_idempotency_key,
        approval_id=invoice_approval.approval_id,
        quote_authority_state="verified_approval_center_fingerprint",
    )
    evidence = EvidenceEvent(
        id=f"ev_invoice_{invoice_digest[:32]}",
        event_type="invoice_draft_created_from_verified_quote_fingerprint",
        entity_type="invoice_draft",
        entity_id=invoice_id,
        summary=(
            f"id={invoice_id} lead_id={lead_id} "
            f"qualified_discovery_ref={material['qualified_discovery_ref']} "
            f"customer_specific_scope_ref={material['customer_specific_scope_ref']} "
            f"quote_authority_ref={quote_authority_ref} "
            f"quote_fingerprint={quote_fingerprint} "
            f"invoice_approval_id={invoice_approval.approval_id} "
            f"approved_amount_sar={material['approved_amount_sar']} "
            "payment_verified=false"
        ),
        approval_id=invoice_approval.approval_id,
    )

    try:
        stored, created = store.create_invoice_draft_idempotent(
            inv,
            evidence=evidence,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail={"reason": "invoice_idempotency_conflict"},
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"reason": "invoice_store_unavailable"},
        ) from exc

    return {
        "item": stored.model_dump(mode="json"),
        "authority": {
            "qualified_discovery_ref": material["qualified_discovery_ref"],
            "customer_specific_scope_ref": material["customer_specific_scope_ref"],
            "quote_authority_ref": quote_authority_ref,
            "quote_fingerprint": quote_fingerprint,
            "quote_approval_status": ApprovalStatus(quote_approval.status).value,
            "amount_source": "approved_customer_specific_quote_fingerprint",
            "invoice_approval_id": invoice_approval.approval_id,
            "invoice_approval_status": ApprovalStatus(invoice_approval.status).value,
            "approval_idempotent_replay": not approval_created,
            "idempotent_replay": not created,
            "payment_verified": False,
        },
    }
