"""Proof Ledger v5 — file-backed JSONL stopgap until Postgres ships.

When the Postgres ProofEvent table lands, only the storage backend
swaps; the public API (record_event, list_events, build_pack,
export_redacted) stays the same.

Hard guarantees:
  - PII never written without redaction (raw events allowed only
    inside in-process buffer; on-disk JSONL goes through redactor)
  - Customer name never on-disk unless ``consent_for_publication=True``
  - Every event has approval_status=approval_required by default
"""
from auto_client_acquisition.proof_ledger.schemas import (
    ProofEvent,
    ProofEventType,
    RevenueWorkUnit,
    RevenueWorkUnitType,
)
from auto_client_acquisition.proof_ledger.file_backend import (
    FileProofLedger,
)
from auto_client_acquisition.proof_ledger.postgres_backend import (
    PostgresProofLedger,
)
from auto_client_acquisition.proof_ledger.factory import (
    get_default_ledger,
    recent_events,
)
from auto_client_acquisition.proof_ledger.evidence_export import (
    export_redacted,
    export_for_audit,
)

__all__ = [
    "ProofEvent",
    "ProofEventType",
    "RevenueWorkUnit",
    "RevenueWorkUnitType",
    "FileProofLedger",
    "PostgresProofLedger",
    "get_default_ledger",
    "recent_events",
    "export_redacted",
    "export_for_audit",
]
