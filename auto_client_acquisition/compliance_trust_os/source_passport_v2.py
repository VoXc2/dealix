"""Source Passport v2 — minimum fields for governed AI use."""

from __future__ import annotations

from dataclasses import dataclass

REQUIRED_SOURCE_PASSPORT_V2_FIELDS: tuple[str, ...] = (
    "source_id",
    "source_type",
    "owner",
    "collection_context",
    "allowed_use",
    "contains_pii",
    "sensitivity",
    "relationship_status",
    "ai_access_allowed",
    "external_use_allowed",
    "retention_policy",
    "deletion_required_after",
)


@dataclass(frozen=True, slots=True)
class SourcePassportV2:
    source_id: str
    source_type: str
    owner: str
    collection_context: str
    allowed_use: tuple[str, ...]
    contains_pii: bool
    sensitivity: str
    relationship_status: str
    ai_access_allowed: bool
    external_use_allowed: bool
    retention_policy: str
    deletion_required_after: str


def source_passport_v2_valid(p: SourcePassportV2) -> bool:
    if not p.source_id.strip() or not p.source_type.strip() or not p.owner.strip():
        return False
    if not p.collection_context.strip() or not p.allowed_use:
        return False
    if not p.sensitivity.strip() or not p.relationship_status.strip():
        return False
    return bool(p.retention_policy.strip() and p.deletion_required_after.strip())


def ai_use_requires_passport(passport_present: bool) -> bool:
    """No Source Passport → no AI use."""
    return passport_present
