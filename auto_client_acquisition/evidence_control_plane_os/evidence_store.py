"""Append-only, tenant-scoped evidence ledger.

``evidence_object.py`` defines the *shape* of an auditable artifact;
this module gives it a *store*. Every governance decision, approval,
runtime-safety event, and value record can be appended here, and the
events for one workflow run can be read back as an ordered trace.

In-memory / process-scoped — the same dev stopgap the rest of the
control plane uses. Reads are tenant-scoped: a caller only ever sees
its own tenant's evidence.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import uuid4

from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
    EvidenceObject,
    evidence_object_valid,
)

_LOCK = threading.Lock()
_LEDGER: list[EvidenceObject] = []


def record_evidence(obj: EvidenceObject) -> EvidenceObject:
    """Append one evidence object. Raises ``ValueError`` if invalid."""
    ok, errors = evidence_object_valid(obj)
    if not ok:
        raise ValueError(f"invalid_evidence_object:{','.join(errors)}")
    with _LOCK:
        _LEDGER.append(obj)
    return obj


def record(
    *,
    tenant_id: str,
    evidence_type: str,
    client_id: str,
    summary: str,
    actor_type: str = "system",
    actor_id: str = "control_plane",
    human_owner: str = "",
    project_id: str = "",
    run_id: str = "",
    source_ids: tuple[str, ...] = (),
    linked_artifacts: tuple[str, ...] = (),
    confidence: str = "medium",
) -> EvidenceObject:
    """Construct and append an evidence object in one call."""
    obj = EvidenceObject(
        evidence_id=f"ev_{uuid4().hex[:12]}",
        evidence_type=evidence_type,
        client_id=client_id,
        project_id=project_id,
        actor_type=actor_type,
        actor_id=actor_id,
        human_owner=human_owner,
        source_ids=source_ids,
        linked_artifacts=linked_artifacts,
        summary=summary,
        confidence=confidence,
        timestamp_iso=datetime.now(UTC).isoformat(),
        tenant_id=tenant_id,
        run_id=run_id,
    )
    return record_evidence(obj)


def list_evidence(
    *,
    tenant_id: str,
    run_id: str | None = None,
    client_id: str | None = None,
) -> list[EvidenceObject]:
    """Tenant-scoped evidence, oldest first. Optionally filter by run/client."""
    with _LOCK:
        rows = [e for e in _LEDGER if e.tenant_id == tenant_id]
    if run_id is not None:
        rows = [e for e in rows if e.run_id == run_id]
    if client_id is not None:
        rows = [e for e in rows if e.client_id == client_id]
    return rows


def run_trace(*, tenant_id: str, run_id: str) -> list[EvidenceObject]:
    """Ordered evidence trace for a single workflow run."""
    return list_evidence(tenant_id=tenant_id, run_id=run_id)


def clear_evidence_store_for_tests() -> None:
    with _LOCK:
        _LEDGER.clear()


__all__ = [
    "clear_evidence_store_for_tests",
    "list_evidence",
    "record",
    "record_evidence",
    "run_trace",
]
