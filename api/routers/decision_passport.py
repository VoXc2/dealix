"""Decision Passport + Golden Chain + Evidence catalog (Revenue OS).

Wave 12 §32.3.4 (Engine 4 hardening) adds POST /api/v1/decision-passport/create
which validates an inbound passport against the 4 hard rules:
- No Decision Passport = No Action (caller builds first)
- No Proof Target = No Action (proof_target non-empty)
- No Owner = Not Operational (owner non-empty + Literal-valid)
- No Safe Channel = Blocked (best_channel must be in allowed_channels when supplied)
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from auto_client_acquisition.decision_passport import (
    DecisionPassport,
    PassportPersistenceError,
    ValidationFailure,
    get_default_passport_store,
    validate_passport,
)
from auto_client_acquisition.proof_engine.evidence import (
    EVIDENCE_LEVEL_DESCRIPTIONS_AR,
    EVIDENCE_LEVEL_DESCRIPTIONS_EN,
    EvidenceLevel,
)

router = APIRouter(prefix="/api/v1/decision-passport", tags=["Decision Passport"])


# Wave 12 hard-gates surface for parity with other Wave 4+ routers.
_HARD_GATES = {
    "no_decision_passport_no_action": True,
    "no_proof_target_no_action": True,
    "no_owner_not_operational": True,
    "no_safe_channel_blocked": True,
    "approval_required_for_external_actions": True,
}


GOLDEN_CHAIN_AR = (
    "إشارة السوق → عميل محتمل → جواز قرار → إجراء معتمد → تسليم → إثبات → توسعة → تعلّم"
)
GOLDEN_CHAIN_EN = (
    "Market signal → Lead → Decision Passport → Approved action → Delivery → "
    "Proof → Expansion → Learning"
)


@router.get("/golden-chain")
async def golden_chain() -> dict[str, Any]:
    """السلسلة الذهبية — مرجع منتج ثابت."""
    return {
        "chain_ar": GOLDEN_CHAIN_AR,
        "chain_en": GOLDEN_CHAIN_EN,
        "rule": "No Decision Passport = No Action",
        "rule_ar": "بدون جواز قرار لا يُنفَّذ إجراء خارجي",
    }


@router.get("/evidence-levels")
async def evidence_levels() -> dict[str, Any]:
    """مستويات أدلة الـ Proof — L0–L5."""
    return {
        "levels": [
            {
                "level": int(lev),
                "name": lev.name,
                "description_ar": EVIDENCE_LEVEL_DESCRIPTIONS_AR.get(int(lev), ""),
                "description_en": EVIDENCE_LEVEL_DESCRIPTIONS_EN.get(int(lev), ""),
            }
            for lev in EvidenceLevel
        ],
    }


@router.get("/status")
async def status() -> dict[str, Any]:
    """Layer status + hard gates (Wave 12 §32.3.4 parity with other routers)."""
    return {
        "service": "decision_passport",
        "schema_version": "1.1",
        "hard_gates": _HARD_GATES,
        "rules": [
            "No Decision Passport = No Action",
            "No Proof Target = No Action",
            "No Owner = Not Operational",
            "No Safe Channel = Blocked",
        ],
    }


@router.post("/create")
async def create_passport(
    passport: DecisionPassport,
    allowed_channels: str | None = Query(
        default=None,
        description=(
            "Optional comma-separated list of channels the customer permits "
            "(from CompanyBrainV6.allowed_channels). When supplied, "
            "best_channel must be in this list or 422 is returned."
        ),
    ),
) -> dict[str, Any]:
    """Validate + echo a Decision Passport (Wave 12 §32.3.4).

    The caller is expected to build the passport upstream (via
    ``build_from_pipeline_result()`` or equivalent) — this endpoint
    runs the 4 hard-rule guards and either echoes the validated
    passport or returns 422 with structured detail.

    Args:
        passport: A v1.1 DecisionPassport instance.
        allowed_channels: Comma-separated channel allowlist (optional).

    Returns:
        ``{...passport fields..., "validated": True}`` on success.

    Raises:
        HTTPException(422): with detail ``{rule, field, message}`` on
            any hard-rule violation.
    """
    parsed_allowed: list[str] | None = None
    if allowed_channels:
        parsed_allowed = [c.strip() for c in allowed_channels.split(",") if c.strip()]
    try:
        validate_passport(passport, allowed_channels=parsed_allowed)
    except ValidationFailure as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "rule": exc.rule,
                "field": exc.field,
                "message": str(exc),
            },
        ) from exc
    body = passport.model_dump(mode="json")
    body["validated"] = True
    return body


# ── Governed Revenue — append-only passport store ─────────────────


@router.post("/store")
async def store_passport(
    passport: DecisionPassport,
    tenant_id: str | None = Query(default=None, description="Optional tenant scope."),
) -> dict[str, Any]:
    """Validate + persist a Decision Passport into the append-only store.

    The store re-runs ``validate_passport()`` and requires an explicit
    ``source`` + ``approval``. Append-only — there is no update/delete.
    """
    try:
        passport_id = get_default_passport_store().add(passport, tenant_id=tenant_id)
    except PassportPersistenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "stored": True,
        "passport_id": passport_id,
        "governance_decision": "allow",
    }


@router.get("/store")
async def list_stored_passports(
    tenant_id: str | None = Query(default=None),
    lead_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
) -> dict[str, Any]:
    """List stored Decision Passports, newest first."""
    rows = get_default_passport_store().list(
        tenant_id=tenant_id, lead_id=lead_id, limit=limit
    )
    return {
        "count": len(rows),
        "passports": [r.model_dump(mode="json") for r in rows],
        "governance_decision": "allow",
    }


@router.get("/store/{passport_id}")
async def get_stored_passport(passport_id: str) -> dict[str, Any]:
    """Fetch one stored Decision Passport by id."""
    passport = get_default_passport_store().get(passport_id)
    if passport is None:
        raise HTTPException(status_code=404, detail=f"passport {passport_id!r} not found")
    body = passport.model_dump(mode="json")
    body["governance_decision"] = "allow"
    return body
