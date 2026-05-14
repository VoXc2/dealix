"""Source Passport — minimum declared fields before AI use."""

from __future__ import annotations

SOURCE_PASSPORT_REQUIRED_KEYS: frozenset[str] = frozenset(
    {
        "source_id",
        "source_type",
        "owner",
        "allowed_use",
        "contains_pii",
        "sensitivity",
        "relationship_status",
        "retention_policy",
        "ai_access_allowed",
        "external_use_allowed",
    },
)


def source_passport_keys_present(keys_declared: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = sorted(SOURCE_PASSPORT_REQUIRED_KEYS - keys_declared)
    return not missing, tuple(missing)
