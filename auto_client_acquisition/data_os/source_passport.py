"""Data OS bridge to Source Passport (sovereignty gate before AI use)."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.compliance_trust_os.source_passport_v2 import SourcePassportV2
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    SourcePassport,
    source_passport_allows_task,
    source_passport_valid_for_ai,
)


def source_passport_from_v2(p: SourcePassportV2) -> SourcePassport:
    """Map extended v2 record to the core institutional passport shape."""
    return SourcePassport(
        source_id=p.source_id,
        source_type=p.source_type,
        owner=p.owner,
        allowed_use=frozenset(p.allowed_use),
        contains_pii=p.contains_pii,
        sensitivity=p.sensitivity,
        retention_policy=p.retention_policy,
        ai_access_allowed=p.ai_access_allowed,
        external_use_allowed=p.external_use_allowed,
    )


def governance_decision_hints_for_passport_gate(
    ok: bool,
    errors: tuple[str, ...],
) -> tuple[bool, str]:
    """
    Interpret ``source_passport_valid_for_ai`` result for routing hints.

    Returns (ai_allowed_hint, reason_key) where reason_key is machine-stable.
    """
    if ok:
        return True, "allow"
    if errors == ("pii_external_use_requires_approval_workflow",):
        return False, "pii_external_requires_approval"
    return False, "blocked"


@dataclass(frozen=True, slots=True)
class SourcePassportValidation:
    is_valid: bool
    reasons: tuple[str, ...]
    missing: tuple[str, ...]


def validate(passport: SourcePassport) -> SourcePassportValidation:
    ok, errors = source_passport_valid_for_ai(passport)
    missing = tuple(err for err in errors if err.endswith("_required"))
    return SourcePassportValidation(is_valid=ok, reasons=errors, missing=missing)


__all__ = [
    "SourcePassport",
    "SourcePassportValidation",
    "governance_decision_hints_for_passport_gate",
    "source_passport_allows_task",
    "source_passport_from_v2",
    "source_passport_valid_for_ai",
    "validate",
]
