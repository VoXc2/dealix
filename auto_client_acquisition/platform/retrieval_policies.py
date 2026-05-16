"""Permission-aware retrieval policy enforcement."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.freshness import compute_freshness_score
from auto_client_acquisition.platform.memory_governance import MemoryRecord, MemorySensitivity


@dataclass(frozen=True, slots=True)
class RetrievalRequest:
    tenant_id: str
    actor_permissions: tuple[str, ...]
    max_sensitivity: MemorySensitivity
    now_epoch: int
    min_freshness: float = 0.3


_SENSITIVITY_ORDER: dict[MemorySensitivity, int] = {
    MemorySensitivity.PUBLIC: 0,
    MemorySensitivity.INTERNAL: 1,
    MemorySensitivity.CONFIDENTIAL: 2,
    MemorySensitivity.RESTRICTED: 3,
}


def _sensitivity_allowed(record: MemoryRecord, request: RetrievalRequest) -> bool:
    return _SENSITIVITY_ORDER[record.sensitivity] <= _SENSITIVITY_ORDER[request.max_sensitivity]


def permission_aware_retrieval(records: tuple[MemoryRecord, ...], request: RetrievalRequest) -> tuple[MemoryRecord, ...]:
    allowed: list[MemoryRecord] = []
    for record in records:
        if record.tenant_id != request.tenant_id:
            continue
        if not _sensitivity_allowed(record, request):
            continue
        if not set(record.permissions).issubset(set(request.actor_permissions)):
            continue
        freshness = compute_freshness_score(
            now_epoch=request.now_epoch,
            created_at_epoch=record.created_at_epoch,
            ttl_seconds=90 * 24 * 3600,
        )
        if freshness < request.min_freshness:
            continue
        allowed.append(record)
    return tuple(allowed)


__all__ = ['RetrievalRequest', 'permission_aware_retrieval']
