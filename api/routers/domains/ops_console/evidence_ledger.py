"""Ops Console — Evidence Ledger.

سجل الأدلة.

GET /api/v1/ops/evidence         — proof + value event stream, sources.
GET /api/v1/ops/evidence/levels  — the L0–L5 evidence-level catalog.

Read-only; admin-key gated. Proof events are surfaced from their REDACTED
summaries only — raw summaries are never exposed (doctrine: no raw PII).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/evidence",
    tags=["Ops Console — Evidence Ledger"],
    dependencies=[Depends(require_admin_key)],
)


def _proof_events() -> list[dict[str, Any]]:
    from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger

    events: list[dict[str, Any]] = []
    for e in get_default_ledger().list_events(limit=100):
        events.append(
            {
                "id": getattr(e, "id", ""),
                "event_type": str(getattr(e, "event_type", "")),
                "customer_handle": getattr(e, "customer_handle", ""),
                "evidence_source": getattr(e, "evidence_source", ""),
                "confidence": getattr(e, "confidence", None),
                "approval_status": getattr(e, "approval_status", ""),
                "risk_level": getattr(e, "risk_level", ""),
                # Redacted summaries only — never the raw summary fields.
                "summary_ar": getattr(e, "redacted_summary_ar", ""),
                "summary_en": getattr(e, "redacted_summary_en", ""),
                "created_at": str(getattr(e, "created_at", "")),
            }
        )
    return events


def _value_events() -> list[dict[str, Any]]:
    from auto_client_acquisition.value_os.value_ledger import list_events

    out: list[dict[str, Any]] = []
    for e in list_events(limit=100):
        rec = e.to_dict() if hasattr(e, "to_dict") else {}
        out.append(
            {
                "event_id": rec.get("event_id", ""),
                "kind": rec.get("kind", ""),
                "amount": rec.get("amount", 0),
                "tier": rec.get("tier", ""),
                "source_ref": rec.get("source_ref", ""),
                "occurred_at": rec.get("occurred_at", ""),
            }
        )
    return out


@router.get("/levels")
async def evidence_levels() -> dict[str, Any]:
    """The L0–L5 evidence-level catalog (bilingual)."""
    try:
        from auto_client_acquisition.proof_engine.evidence import (
            EVIDENCE_LEVEL_DESCRIPTIONS_AR,
            EVIDENCE_LEVEL_DESCRIPTIONS_EN,
        )

        levels = [
            {
                "level": i,
                "description_ar": EVIDENCE_LEVEL_DESCRIPTIONS_AR.get(i, ""),
                "description_en": EVIDENCE_LEVEL_DESCRIPTIONS_EN.get(i, ""),
            }
            for i in range(6)
        ]
    except Exception:  # noqa: BLE001
        return governed({"levels": [], "note": "evidence_levels_unavailable"})
    return governed({"levels": levels})


@router.get("")
async def evidence_ledger() -> dict[str, Any]:
    """Proof + value event stream and the distinct evidence sources."""
    try:
        proof = _proof_events()
        proof_note: str | None = None
    except Exception:  # noqa: BLE001
        proof, proof_note = [], "proof_ledger_unavailable"

    try:
        value = _value_events()
        value_note: str | None = None
    except Exception:  # noqa: BLE001
        value, value_note = [], "value_ledger_unavailable"

    sources = sorted({e["evidence_source"] for e in proof if e.get("evidence_source")})
    return governed(
        {
            "proof_events": {"count": len(proof), "items": proof, "note": proof_note},
            "value_events": {"count": len(value), "items": value, "note": value_note},
            "sources": sources,
        }
    )
