"""Per-object-type data minimization contract."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DataMinimizationContract:
    """Which fields are PII / what to keep / what to drop on export."""

    object_type: str
    pii_fields: tuple[str, ...]
    safe_to_export: tuple[str, ...]
    drop_on_audit_export: tuple[str, ...] = field(default=())
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_type": self.object_type,
            "pii_fields": list(self.pii_fields),
            "safe_to_export": list(self.safe_to_export),
            "drop_on_audit_export": list(self.drop_on_audit_export),
            "notes": self.notes,
        }


# Static contracts for the core object types we currently track.
_CONTRACTS: dict[str, DataMinimizationContract] = {
    "lead": DataMinimizationContract(
        object_type="lead",
        pii_fields=("contact_email", "contact_phone", "contact_name"),
        safe_to_export=(
            "id", "company_name", "sector", "region", "fit_score",
            "urgency_score", "status", "created_at",
        ),
        drop_on_audit_export=("contact_email", "contact_phone", "contact_name"),
        notes="Contact PII never appears in audit exports; aggregate counts only.",
    ),
    "consent_record": DataMinimizationContract(
        object_type="consent_record",
        pii_fields=("contact_id",),
        safe_to_export=(
            "id", "channel", "consent_status", "consent_source",
            "consent_timestamp", "withdrawal_timestamp", "allowed_purposes",
        ),
        drop_on_audit_export=("contact_id",),
        notes="contact_id replaced with a per-contact opaque hash on export.",
    ),
    "proof_event": DataMinimizationContract(
        object_type="proof_event",
        pii_fields=("payload",),
        safe_to_export=(
            "id", "event_type", "service_id", "redacted_summary_ar",
            "redacted_summary_en", "evidence_source", "confidence",
            "consent_for_publication", "approval_status", "risk_level",
            "created_at",
        ),
        drop_on_audit_export=("payload",),
        notes="payload may contain raw context; never exported. Public summary uses redacted_* fields.",
    ),
    "draft_message": DataMinimizationContract(
        object_type="draft_message",
        pii_fields=("recipient_email", "recipient_phone"),
        safe_to_export=(
            "id", "channel", "service_id", "status",
            "approval_status", "created_at",
        ),
        drop_on_audit_export=("recipient_email", "recipient_phone"),
        notes="Draft body is internal; only metadata exposed to audits.",
    ),
}


def list_known_object_types() -> list[str]:
    return sorted(_CONTRACTS.keys())


def data_minimization_for(object_type: str) -> DataMinimizationContract:
    if object_type not in _CONTRACTS:
        raise KeyError(f"unknown object_type: {object_type}")
    return _CONTRACTS[object_type]
