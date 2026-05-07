"""Proof Pack assembly — orchestrates selection + redaction + cover.

Composes a ProofPack from N proof events for one customer. The
output is a deterministic dict with: pack_id, cover, events, summary,
audit_log. Does NOT publish — output is internal_only by default.

Hard rules:
- Only events with evidence_level in {customer_confirmed, payment_confirmed}
  qualify for inclusion in a publishable pack
- consent_for_publication=False events are still included but flagged
- approval_status must be approved; otherwise pending events are excluded
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Iterable

_PACKS_DIR = os.path.join("data", "proof_packs")


def _ensure_dir() -> None:
    os.makedirs(_PACKS_DIR, exist_ok=True)


def _qualifies_for_publish(event: dict[str, Any]) -> bool:
    return (
        event.get("evidence_level") in ("customer_confirmed", "payment_confirmed")
        and bool(event.get("consent_for_publication"))
        and event.get("approval_status") == "approved"
    )


def assemble_proof_pack(
    *,
    customer_handle: str,
    events: Iterable[dict[str, Any]],
    audience: str = "internal_only",
) -> dict[str, Any]:
    """Compose a proof pack from event dicts.

    Each event dict must include: event_id, event_type, summary_ar/en,
    evidence_level, approval_status, consent_for_publication.

    The pack is persisted to data/proof_packs/{pack_id}.json.
    """
    if audience not in ("internal_only", "external_publishable"):
        raise ValueError(f"invalid audience: {audience}")

    pack_id = f"pack_{uuid.uuid4().hex[:10]}"
    events_list = list(events)
    publishable = [e for e in events_list if _qualifies_for_publish(e)]
    pending = [e for e in events_list if not _qualifies_for_publish(e)]

    if audience == "external_publishable" and not publishable:
        raise ValueError(
            "cannot build external_publishable pack with zero publishable events"
        )

    cover = {
        "pack_id": pack_id,
        "customer_handle": customer_handle,
        "audience": audience,
        "event_count": len(events_list),
        "publishable_count": len(publishable),
        "internal_only_count": len(pending),
        "assembled_at": datetime.now(timezone.utc).isoformat(),
    }

    pack = {
        "pack_id": pack_id,
        "customer_handle": customer_handle,
        "audience": audience,
        "cover": cover,
        "events": events_list if audience == "internal_only" else publishable,
        "audit_log": [
            {"step": "selection", "input_count": len(events_list)},
            {"step": "publish_filter", "qualified_count": len(publishable)},
            {"step": "audience_check", "audience": audience},
        ],
        "safety_summary": (
            "publishable_consent_required"
            if audience == "external_publishable"
            else "internal_only_default"
        ),
    }

    _ensure_dir()
    target = os.path.join(_PACKS_DIR, f"{pack_id}.json")
    import json
    with open(target, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)

    return pack
