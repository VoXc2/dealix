"""Audit and explainability ledger."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuditRecord:
    event_id: str
    action_name: str
    decision: str
    actor: str
    reasons: tuple[str, ...]
    timestamp_epoch: int
    trace_id: str = ''


_AUDIT_LOG: list[AuditRecord] = []


def record_audit_event(record: AuditRecord) -> None:
    _AUDIT_LOG.append(record)


def list_audit_events() -> tuple[AuditRecord, ...]:
    return tuple(_AUDIT_LOG)


def explain_action(event_id: str) -> str:
    for record in _AUDIT_LOG:
        if record.event_id == event_id:
            reasons = '; '.join(record.reasons)
            return f'{record.action_name} => {record.decision} ({reasons})'
    return 'event_not_found'


def clear_audit_log_for_tests() -> None:
    _AUDIT_LOG.clear()


__all__ = [
    'AuditRecord',
    'clear_audit_log_for_tests',
    'explain_action',
    'list_audit_events',
    'record_audit_event',
]
