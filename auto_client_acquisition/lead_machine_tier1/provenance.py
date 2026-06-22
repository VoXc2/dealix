from __future__ import annotations

from .schemas import ProvenanceRecord
from .source_registry import get_source_definition


def validate_provenance(record: ProvenanceRecord) -> list[str]:
    source = get_source_definition(record.source_name)
    issues: list[str] = []
    if source.allowed_use == "blocked":
        issues.append("blocked_source")
    if source.provenance_required and not record.source_type:
        issues.append("missing_source_type")
    if record.confidence < 0.35:
        issues.append("low_provenance_confidence")
    if record.refresh_needed:
        issues.append("refresh_needed")
    return issues