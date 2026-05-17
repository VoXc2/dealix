"""Playbooks store — persisted vertical playbook records.

Endpoints under /api/v1/playbooks/:
    GET    /status            — module health
    POST   /                  — create one playbook
    GET    /                  — list playbooks
    GET    /{id}              — fetch one playbook
    PATCH  /{id}/status       — update playbook status
    DELETE /{id}              — soft-delete a playbook
    POST   /seed              — seed the store from the 5-vertical catalog
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.vertical_playbooks.playbook_store import (
    get_default_playbook_store,
)

router = APIRouter(prefix="/api/v1/playbooks", tags=["playbooks"])


@router.get("/status")
async def status() -> dict[str, Any]:
    """Module health."""
    return {
        "module": "playbook_store",
        "guardrails": {"tenant_scoped": True, "soft_delete": True},
        "governance_decision": "allow",
    }


@router.post("")
async def create_playbook(payload: dict = Body(...)) -> dict[str, Any]:
    """Create one playbook record."""
    name = payload.get("name")
    vertical = payload.get("vertical")
    if not name or not vertical:
        raise HTTPException(status_code=422, detail="name + vertical required")
    try:
        row = get_default_playbook_store().add(
            name=str(name),
            vertical=str(vertical),
            tenant_id=payload.get("tenant_id"),
            version=int(payload.get("version", 1)),
            stage=str(payload.get("stage", "")),
            steps=payload.get("steps"),
            entry_criteria=payload.get("entry_criteria"),
            exit_criteria=payload.get("exit_criteria"),
            owner=str(payload.get("owner", "")),
            status=str(payload.get("status", "draft")),
            meta_json=payload.get("meta_json"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"playbook": row, "governance_decision": "allow"}


@router.get("")
async def list_playbooks(
    tenant_id: str | None = None,
    vertical: str | None = None,
    status: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """List active playbook records, newest first."""
    rows = get_default_playbook_store().list(
        tenant_id=tenant_id,
        vertical=vertical,
        status=status,
        limit=max(1, min(int(limit), 1000)),
    )
    return {"count": len(rows), "playbooks": rows, "governance_decision": "allow"}


@router.get("/{playbook_id}")
async def get_playbook(playbook_id: str) -> dict[str, Any]:
    """Fetch one playbook record by id."""
    row = get_default_playbook_store().get(playbook_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"playbook {playbook_id!r} not found")
    return {"playbook": row, "governance_decision": "allow"}


@router.patch("/{playbook_id}/status")
async def update_playbook_status(
    playbook_id: str, payload: dict = Body(...)
) -> dict[str, Any]:
    """Update a playbook's status."""
    new_status = payload.get("status")
    if not new_status:
        raise HTTPException(status_code=422, detail="status required")
    row = get_default_playbook_store().update_status(playbook_id, str(new_status))
    if row is None:
        raise HTTPException(status_code=404, detail=f"playbook {playbook_id!r} not found")
    return {"playbook": row, "governance_decision": "allow"}


@router.delete("/{playbook_id}")
async def delete_playbook(playbook_id: str) -> dict[str, Any]:
    """Soft-delete a playbook record."""
    found = get_default_playbook_store().soft_delete(playbook_id)
    if not found:
        raise HTTPException(status_code=404, detail=f"playbook {playbook_id!r} not found")
    return {"deleted": True, "playbook_id": playbook_id, "governance_decision": "allow"}


@router.post("/seed")
async def seed_playbooks(payload: dict = Body(default_factory=dict)) -> dict[str, Any]:
    """Seed the store from the hand-curated 5-vertical catalog."""
    rows = get_default_playbook_store().seed_from_catalog(
        tenant_id=payload.get("tenant_id")
    )
    return {"seeded": len(rows), "playbooks": rows, "governance_decision": "allow"}
