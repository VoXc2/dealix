"""Deliverables in-memory + JSONL store.

Persistence: append-only JSONL at data/wave13/deliverables.jsonl.
Index: in-memory dict keyed by deliverable_id.

Article 11: minimum viable persistence — when first paid customer signs,
swap to Postgres ORM following proof_ledger/postgres_backend.py.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import UTC, datetime, timezone

from auto_client_acquisition.deliverables.schemas import (
    Deliverable,
    DeliverableType,
)

_JSONL_PATH = os.path.join("data", "wave13", "deliverables.jsonl")
_INDEX: dict[str, Deliverable] = {}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(rec: Deliverable) -> None:
    _ensure_dir()
    _INDEX[rec.deliverable_id] = rec
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(rec.model_dump_json() + "\n")


def create_deliverable(
    *,
    session_id: str,
    customer_handle: str,
    type: DeliverableType,
    title_ar: str,
    title_en: str,
    customer_visible: bool = True,
    approval_required: bool = True,
    proof_related: bool = False,
    proof_event_id: str | None = None,
    artifact_uri: str | None = None,
    persist: bool = True,
) -> Deliverable:
    """Create a Deliverable in 'draft' status and (optionally) persist."""
    rec = Deliverable(
        deliverable_id=f"deliv_{uuid.uuid4().hex[:10]}",
        session_id=session_id,
        customer_handle=customer_handle,
        type=type,
        title_ar=title_ar,
        title_en=title_en,
        status="draft",
        version=1,
        customer_visible=customer_visible,
        approval_required=approval_required,
        proof_related=proof_related,
        proof_event_id=proof_event_id,
        artifact_uri=artifact_uri,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    if persist:
        _persist(rec)
    else:
        _INDEX[rec.deliverable_id] = rec
    return rec


def get_deliverable(deliverable_id: str) -> Deliverable | None:
    return _INDEX.get(deliverable_id)


def list_by_session(session_id: str, *, customer_visible_only: bool = False) -> list[Deliverable]:
    """List all deliverables for a session.

    `customer_visible_only=True` filters to customer_visible=True (portal use).
    """
    items = [d for d in _INDEX.values() if d.session_id == session_id]
    if customer_visible_only:
        items = [d for d in items if d.customer_visible]
    items.sort(key=lambda d: d.created_at)
    return items


def reset_for_test() -> None:
    """Test-only helper to clear the in-memory index."""
    _INDEX.clear()
