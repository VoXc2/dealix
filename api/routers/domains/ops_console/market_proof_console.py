"""Ops Console — Market Proof Console.

غرفة إثبات السوق.

GET /api/v1/ops/market-proof
  The client-risk scoring model, sample (assembled) proof packs from the
  proof ledger, market-signal status, and target accounts. Read-only;
  admin-key gated. Market signals are caller-supplied only — no scraping.
  Target accounts return company/sector only — no contact PII.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/market-proof",
    tags=["Ops Console — Market Proof"],
    dependencies=[Depends(require_admin_key)],
)

_RISK_SIGNALS = (
    "wants_scraping_or_spam",
    "wants_guaranteed_sales",
    "unclear_pain",
    "no_owner",
    "data_not_ready",
    "budget_unknown",
)


def _risk_model() -> list[dict[str, Any]]:
    """Derive each signal's point weight by scoring it in isolation."""
    from auto_client_acquisition.sales_os import ClientRiskSignals, client_risk_score

    model: list[dict[str, Any]] = []
    for sig in _RISK_SIGNALS:
        flags = {name: (name == sig) for name in _RISK_SIGNALS}
        points = client_risk_score(ClientRiskSignals(**flags))
        model.append({"signal": sig, "points": points})
    return model


def _sample_proof_packs() -> list[dict[str, Any]]:
    from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger

    packs: list[dict[str, Any]] = []
    for e in get_default_ledger().list_events(limit=200):
        event_type = str(getattr(e, "event_type", ""))
        if "PROOF_PACK" not in event_type.upper():
            continue
        packs.append(
            {
                "id": getattr(e, "id", ""),
                "event_type": event_type,
                "customer_handle": getattr(e, "customer_handle", ""),
                "confidence": getattr(e, "confidence", None),
                "approval_status": getattr(e, "approval_status", ""),
                "created_at": str(getattr(e, "created_at", "")),
            }
        )
    return packs[:20]


async def _target_accounts() -> list[dict[str, Any]]:
    from sqlalchemy import select

    from db.models import AccountRecord
    from db.session import async_session_factory

    async with async_session_factory()() as session:
        stmt = (
            select(AccountRecord)
            .where(AccountRecord.deleted_at.is_(None))
            .order_by(AccountRecord.created_at.desc())
            .limit(25)
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [
            {
                "id": r.id,
                "company_name": r.company_name,
                "sector": r.sector,
                "city": r.city,
                "country": r.country,
                "status": r.status,
                "risk_level": r.risk_level,
                "data_quality_score": r.data_quality_score,
            }
            for r in rows
        ]


@router.get("")
async def market_proof() -> dict[str, Any]:
    """Risk model, sample proof packs, market-signal status, target accounts."""
    try:
        risk_model = _risk_model()
    except Exception:  # noqa: BLE001
        risk_model = []

    try:
        packs = _sample_proof_packs()
        packs_note: str | None = None
    except Exception:  # noqa: BLE001
        packs, packs_note = [], "proof_ledger_unavailable"

    try:
        accounts = await _target_accounts()
        accounts_note: str | None = None
    except Exception:  # noqa: BLE001
        accounts, accounts_note = [], "database_unavailable"

    return governed(
        {
            "risk_score": {
                "model": risk_model,
                "max": 100,
                "note": "higher score = higher client risk",
            },
            "sample_proof_packs": {
                "count": len(packs),
                "items": packs,
                "note": packs_note,
            },
            "market_signals": {
                "count": 0,
                "note": "signals are caller-supplied via the orchestrator — no scraping",
            },
            "target_accounts": {
                "count": len(accounts),
                "items": accounts,
                "note": accounts_note,
            },
        }
    )
