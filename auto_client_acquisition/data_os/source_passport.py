"""Data OS bridge to Source Passport (sovereignty gate before AI use)."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from auto_client_acquisition.compliance_trust_os.source_passport_v2 import SourcePassportV2
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    SourcePassport,
    source_passport_allows_task,
    source_passport_valid_for_ai,
)

ALLOWED_SOURCE_TYPES = frozenset(
    {"client_upload", "crm_export", "manual_entry", "partner_data", "licensed_dataset"}
)
ALLOWED_OWNERS = frozenset({"client", "dealix", "partner"})
ALLOWED_USES = frozenset({"internal_analysis", "draft_only", "reporting", "scoring"})
ALLOWED_SENSITIVITY = frozenset({"low", "medium", "high"})
ALLOWED_RETENTION = frozenset(
    {"project_duration", "retainer_duration", "anonymize_after_close", "delete_after_close"}
)


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating a Source Passport against the canonical enums."""

    is_valid: bool
    missing: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()


def _bad(field_name: str, value: object, allowed: Iterable[str]) -> str:
    return f"{field_name}={value!r} not in {sorted(allowed)}"


def validate(passport: SourcePassport | None) -> ValidationResult:
    """A passport is valid iff every required field is set and within the
    canonical enum. A missing passport or empty ``source_id`` is invalid."""
    if passport is None:
        return ValidationResult(
            is_valid=False, missing=("passport",), reasons=("no_passport",)
        )
    missing: list[str] = []
    reasons: list[str] = []
    if not passport.source_id:
        missing.append("source_id")
    if passport.source_type not in ALLOWED_SOURCE_TYPES:
        reasons.append(_bad("source_type", passport.source_type, ALLOWED_SOURCE_TYPES))
    if passport.owner not in ALLOWED_OWNERS:
        reasons.append(_bad("owner", passport.owner, ALLOWED_OWNERS))
    if not passport.allowed_use:
        missing.append("allowed_use")
    else:
        for use in passport.allowed_use:
            if use not in ALLOWED_USES:
                reasons.append(_bad("allowed_use[]", use, ALLOWED_USES))
                break
    if passport.sensitivity not in ALLOWED_SENSITIVITY:
        reasons.append(_bad("sensitivity", passport.sensitivity, ALLOWED_SENSITIVITY))
    if passport.retention_policy not in ALLOWED_RETENTION:
        reasons.append(
            _bad("retention_policy", passport.retention_policy, ALLOWED_RETENTION)
        )
    return ValidationResult(
        is_valid=not missing and not reasons,
        missing=tuple(missing),
        reasons=tuple(reasons),
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


__all__ = [
    "SourcePassport",
    "ValidationResult",
    "governance_decision_hints_for_passport_gate",
    "source_passport_allows_task",
    "source_passport_from_v2",
    "source_passport_valid_for_ai",
    "validate",
]
