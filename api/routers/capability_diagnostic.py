"""Capability Diagnostic — HTTP surface for the Dealix paid entry.

POST /api/v1/diagnostic/intent — score 6 capability axes (0..5), get the
recommended Sprint + retainer + transformation gap, and create a Moyasar
invoice for the Diagnostic offer. The invoice is **not** revenue until
``/api/v1/payment-ops/{id}/confirm`` runs with an evidence reference.

GET /api/v1/diagnostic/{diagnostic_id}/report — read back the diagnostic
record (scores, recommended sprint, expected proof, retainer path).

Doctrine bindings:
  * ``endgame_os.capability_diagnostic`` — scoring + sprint recommendation.
  * ``payment_ops`` — Moyasar invoice creation with hard gates.
  * ``operating_manual_os.non_negotiables`` — pre-flight checks.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.endgame_os.capability_diagnostic import (
    RECOMMENDED_SPRINT_BY_AXIS,
    RETAINER_BY_SPRINT,
    CapabilityAxis,
    CapabilityScore,
    recommend_sprint,
)
from auto_client_acquisition.operating_manual_os.non_negotiables import (
    NonNegotiableCheck,
    check_action_against_non_negotiables,
)
from auto_client_acquisition.payment_ops import create_invoice_intent

router = APIRouter(prefix="/api/v1/diagnostic", tags=["capability-diagnostic"])

# Default Diagnostic price. Fixed for Phase 1; overridable via env.
_DEFAULT_DIAGNOSTIC_PRICE_SAR: float = float(
    os.getenv("DEALIX_DIAGNOSTIC_PRICE_SAR", "4500")
)
_DEFAULT_PAYMENT_METHOD: str = os.getenv(
    "DEALIX_DIAGNOSTIC_DEFAULT_METHOD", "bank_transfer"
)

# Append-only diagnostic store. Same pattern as lead_inbox.
_DIAGNOSTIC_STORE_PATH = Path(
    os.getenv("DEALIX_DIAGNOSTIC_STORE", "var/diagnostics.jsonl")
)


def _persist(record: dict[str, Any]) -> None:
    _DIAGNOSTIC_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _DIAGNOSTIC_STORE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _load(diagnostic_id: str) -> dict[str, Any] | None:
    if not _DIAGNOSTIC_STORE_PATH.exists():
        return None
    with _DIAGNOSTIC_STORE_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("diagnostic_id") == diagnostic_id:
                return rec
    return None


def _parse_axes(raw: dict[str, int]) -> tuple[CapabilityScore, ...]:
    """Validate and convert the score dict to typed CapabilityScore tuple."""

    allowed = {axis.value for axis in CapabilityAxis}
    unknown = set(raw) - allowed
    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"unknown_axes: {sorted(unknown)}",
        )
    missing = allowed - set(raw)
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"missing_axes: {sorted(missing)}",
        )
    scores: list[CapabilityScore] = []
    for axis in CapabilityAxis:
        value = raw[axis.value]
        if not isinstance(value, int) or not 0 <= value <= 5:
            raise HTTPException(
                status_code=422,
                detail=f"axis {axis.value}: score must be int in 0..5",
            )
        scores.append(CapabilityScore(axis=axis, score=value))
    return tuple(scores)


def _feasibility_from_data_readiness(data_score: int) -> str:
    """Mirror the doctrine DTG feasibility tiers without coupling to DCI types."""

    if data_score >= 4:
        return "high"
    if data_score >= 2:
        return "medium"
    return "low"


def _dtg_decision(gap: int, feasibility: str) -> str:
    """Apply the DTG decision matrix from
    ``docs/global_grade/TRANSFORMATION_GAP.md``.

    | Gap | Feasibility | Decision |
    | --- | --- | --- |
    | High | High | sprint_now |
    | High | Low/Medium | diagnostic_first |
    | Low | High | quick_win |
    | Low | Low/Medium | deprioritize |
    """

    high_gap = gap >= 2
    high_feasibility = feasibility == "high"
    if high_gap and high_feasibility:
        return "sprint_now"
    if high_gap and not high_feasibility:
        return "diagnostic_first"
    if (not high_gap) and high_feasibility:
        return "quick_win"
    return "deprioritize"


def _composite(scores: tuple[CapabilityScore, ...]) -> float:
    return sum(s.score for s in scores) / len(scores)


def _expected_proof(weakest_axis: CapabilityAxis) -> tuple[str, ...]:
    """Phase 1 doctrine: what the Sprint will produce as proof."""

    mapping: dict[CapabilityAxis, tuple[str, ...]] = {
        CapabilityAxis.REVENUE: (
            "50 accounts scored",
            "duplicate rate identified",
            "top 10 opportunities",
            "draft pack created",
            "unsafe actions blocked",
        ),
        CapabilityAxis.DATA: (
            "Source Passport produced",
            "data quality score",
            "PII flags",
            "allowed-use registry",
        ),
        CapabilityAxis.GOVERNANCE: (
            "policy rules created",
            "approval matrix",
            "AI run ledger sample",
            "audit coverage plan",
        ),
        CapabilityAxis.KNOWLEDGE: (
            "source registry",
            "citation coverage report",
            "insufficient-evidence rate",
            "knowledge gap list",
        ),
        CapabilityAxis.OPERATIONS: (
            "workflow map",
            "approval path defined",
            "SOP draft",
            "time-saved estimate",
        ),
        CapabilityAxis.PROOF: (
            "Proof Pack template",
            "evidence-level audit",
            "case-safe summary",
        ),
    }
    return mapping[weakest_axis]


@router.post("/intent")
async def diagnostic_intent(
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Create a Diagnostic intent and the matching Moyasar invoice intent.

    Required body:
      * ``customer_handle`` — internal handle for the prospect.
      * ``company`` — display name (legal/brand).
      * ``scores`` — dict mapping each of the 6 axes to an int 0..5.

    Optional:
      * ``sector`` — Saudi sector taxonomy hint.
      * ``city`` — Saudi city.
      * ``amount_sar`` — overrides the default Diagnostic price.
      * ``method`` — payment method (must be in payment_ops allowed list).
      * ``contact_email`` — prospect email (audit only).
    """

    customer_handle = payload.get("customer_handle")
    company = payload.get("company")
    scores_raw = payload.get("scores")
    if not customer_handle or not company:
        raise HTTPException(
            status_code=422,
            detail="customer_handle + company required",
        )
    if not isinstance(scores_raw, dict):
        raise HTTPException(
            status_code=422,
            detail="scores object required (axis_name -> int 0..5)",
        )

    # Doctrine pre-flight — verify the action does not violate non-negotiables.
    pre_flight = check_action_against_non_negotiables(
        NonNegotiableCheck(action="diagnostic_intent")
    )
    if not pre_flight.allowed:
        raise HTTPException(
            status_code=403,
            detail={"non_negotiables_violated": [v.value for v in pre_flight.violations]},
        )

    scores = _parse_axes(scores_raw)
    sprint, retainer = recommend_sprint(scores)
    weakest = min(scores, key=lambda s: s.score)
    target = min(max(weakest.score + 2, 3), 5)
    data_score = next(s.score for s in scores if s.axis is CapabilityAxis.DATA)
    feasibility = _feasibility_from_data_readiness(data_score)
    gap = target - weakest.score
    dtg_recommendation = _dtg_decision(gap=gap, feasibility=feasibility)
    composite = round(_composite(scores), 2)
    expected_proof = _expected_proof(weakest.axis)

    amount_sar = float(payload.get("amount_sar", _DEFAULT_DIAGNOSTIC_PRICE_SAR))
    method = payload.get("method", _DEFAULT_PAYMENT_METHOD)
    try:
        invoice = create_invoice_intent(
            customer_handle=customer_handle,
            amount_sar=amount_sar,
            method=method,
            service_session_id=None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    diagnostic_id = f"DIAG-{uuid4().hex[:12].upper()}"
    record = {
        "diagnostic_id": diagnostic_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "customer_handle": customer_handle,
        "company": company,
        "sector": payload.get("sector"),
        "city": payload.get("city"),
        "contact_email": payload.get("contact_email"),
        "scores": {axis.value: next(s.score for s in scores if s.axis is axis) for axis in CapabilityAxis},
        "composite_score": composite,
        "weakest_axis": weakest.axis.value,
        "transformation_target": target,
        "transformation_gap": gap,
        "data_readiness_feasibility": feasibility,
        "dtg_recommendation": dtg_recommendation,
        "recommended_sprint": sprint,
        "retainer_path": retainer,
        "expected_proof": list(expected_proof),
        "payment_id": invoice.payment_id,
        "invoice_state": invoice.status,
        "amount_sar": amount_sar,
    }
    _persist(record)

    return {
        "diagnostic": record,
        "payment": invoice.model_dump(mode="json"),
        "warning_invoice_not_revenue": "invoice_intent != revenue",
        "next_step": (
            "Submit manual evidence via /api/v1/payment-ops/manual-evidence, "
            "then confirm via /api/v1/payment-ops/confirm."
        ),
    }


@router.get("/{diagnostic_id}/report")
async def diagnostic_report(diagnostic_id: str) -> dict[str, Any]:
    rec = _load(diagnostic_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    return {
        "diagnostic": rec,
        "narrative": {
            "headline": (
                f"Capability composite {rec['composite_score']}/5 — "
                f"weakest axis: {rec['weakest_axis']} "
                f"(transformation gap {rec['transformation_gap']})."
            ),
            "recommendation": (
                f"Recommended sprint: {rec['recommended_sprint']}. "
                f"Retainer path: {rec['retainer_path']}."
            ),
            "expected_proof": rec["expected_proof"],
            "dtg_decision": rec["dtg_recommendation"],
        },
    }


@router.get("/recommendation-table")
async def recommendation_table() -> dict[str, Any]:
    """Public table of which sprint is recommended for each weakest axis."""

    return {
        "by_axis": {axis.value: sprint for axis, sprint in RECOMMENDED_SPRINT_BY_AXIS.items()},
        "by_sprint": RETAINER_BY_SPRINT,
    }
