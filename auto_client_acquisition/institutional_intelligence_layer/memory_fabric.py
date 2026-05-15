"""Institutional memory fabric and lineage checks (System 59)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionMemoryRecord:
    decision_id: str
    timestamp_iso: str
    actor_id: str
    policy_version: str
    data_refs: tuple[str, ...]
    rationale: str
    workflow_id: str


def decision_lineage_complete(record: DecisionMemoryRecord) -> bool:
    """A decision lineage is complete if all provenance fields exist."""
    return bool(
        record.decision_id.strip()
        and record.timestamp_iso.strip()
        and record.actor_id.strip()
        and record.policy_version.strip()
        and record.workflow_id.strip()
        and record.rationale.strip()
        and record.data_refs
    )


def build_decision_trace(records: tuple[DecisionMemoryRecord, ...]) -> dict[str, dict[str, object]]:
    """Build immutable-style decision traces keyed by decision id."""
    traces: dict[str, dict[str, object]] = {}
    for rec in sorted(records, key=lambda x: x.timestamp_iso):
        traces[rec.decision_id] = {
            "workflow_id": rec.workflow_id,
            "timestamp_iso": rec.timestamp_iso,
            "actor_id": rec.actor_id,
            "policy_version": rec.policy_version,
            "data_refs": rec.data_refs,
            "rationale": rec.rationale,
            "lineage_complete": decision_lineage_complete(rec),
        }
    return traces


def memory_fabric_dependency(
    records: tuple[DecisionMemoryRecord, ...],
    *,
    min_records: int = 1,
) -> bool:
    """Institutional dependency requires complete and queryable memory."""
    if len(records) < min_records:
        return False
    return all(decision_lineage_complete(r) for r in records)
