"""Memory governance contracts and confidence scoring."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MemorySensitivity(StrEnum):
    PUBLIC = 'public'
    INTERNAL = 'internal'
    CONFIDENTIAL = 'confidential'
    RESTRICTED = 'restricted'


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    tenant_id: str
    source: str
    created_at_epoch: int
    sensitivity: MemorySensitivity
    permissions: tuple[str, ...]
    lineage_id: str
    confidence: float


def validate_memory_record(record: MemoryRecord) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not record.memory_id.strip() or not record.tenant_id.strip():
        errors.append('memory_identity_missing')
    if not record.source.strip():
        errors.append('memory_source_missing')
    if not record.lineage_id.strip():
        errors.append('memory_lineage_missing')
    if not (0.0 <= record.confidence <= 1.0):
        errors.append('memory_confidence_out_of_range')
    return len(errors) == 0, tuple(errors)


def memory_confidence_score(*, source_reliability: float, freshness_score: float, lineage_score: float) -> float:
    score = (0.5 * source_reliability) + (0.3 * freshness_score) + (0.2 * lineage_score)
    return round(max(0.0, min(1.0, score)), 4)


__all__ = [
    'MemoryRecord',
    'MemorySensitivity',
    'memory_confidence_score',
    'validate_memory_record',
]
