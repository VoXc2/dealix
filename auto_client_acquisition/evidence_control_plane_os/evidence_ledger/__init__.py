"""Append-only Evidence Events ledger.

An Evidence Event is one immutable record that an action, observation or
proof artifact occurred. The ledger is append-only by construction —
there are no update or delete code paths.

Public API:
    from auto_client_acquisition.evidence_control_plane_os.evidence_ledger import (
        EvidenceEvent,
        FileEvidenceLedger,
        PostgresEvidenceLedger,
        get_default_evidence_ledger,
        reset_default_evidence_ledger,
    )
"""
from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.factory import (
    EvidenceLedger,
    get_default_evidence_ledger,
    reset_default_evidence_ledger,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.file_backend import (
    FileEvidenceLedger,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.postgres_backend import (
    EvidenceEventORM,
    EvidenceLedgerBase,
    PostgresEvidenceLedger,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.schemas import (
    EvidenceEvent,
)

__all__ = [
    "EvidenceEvent",
    "EvidenceEventORM",
    "EvidenceLedger",
    "EvidenceLedgerBase",
    "FileEvidenceLedger",
    "PostgresEvidenceLedger",
    "get_default_evidence_ledger",
    "reset_default_evidence_ledger",
]
