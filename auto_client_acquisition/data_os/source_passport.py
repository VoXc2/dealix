"""Source Passport — the contract for ANY data entering Dealix.

No passport → no AI use. Unknown source → no outreach. PII + external use
→ approval required. These rules are enforced in
governance_os.runtime_decision.decide().
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

ALLOWED_SOURCE_TYPES = frozenset({
    "client_upload",
    "crm_export",
    "manual_entry",
    "partner_data",
    "licensed_dataset",
})
ALLOWED_OWNERS = frozenset({"client", "dealix", "partner"})
ALLOWED_USES = frozenset({
    "internal_analysis",
    "draft_only",
    "reporting",
    "scoring",
})
ALLOWED_SENSITIVITY = frozenset({"low", "medium", "high"})
ALLOWED_RETENTION = frozenset({
    "project_duration",
    "retainer_duration",
    "anonymize_after_close",
    "delete_after_close",
})


@dataclass(frozen=True)
class SourcePassport:
    source_id: str
    source_type: str
    owner: str
    allowed_use: tuple[str, ...]
    contains_pii: bool
    sensitivity: str
    ai_access_allowed: bool
    external_use_allowed: bool
    retention_policy: str


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    missing: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()


def _bad(field_name: str, value: object, allowed: Iterable[str]) -> str:
    return f"{field_name}={value!r} not in {sorted(allowed)}"


def validate(passport: SourcePassport | None) -> ValidationResult:
    """A passport is valid iff every required field is set + within the
    canonical enum. None / missing source_id → invalid."""
    if passport is None:
        return ValidationResult(is_valid=False, missing=("passport",), reasons=("no_passport",))
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
        reasons.append(_bad("retention_policy", passport.retention_policy, ALLOWED_RETENTION))
    return ValidationResult(
        is_valid=not missing and not reasons,
        missing=tuple(missing),
        reasons=tuple(reasons),
    )


def requires_approval(passport: SourcePassport, intended_use: str) -> bool:
    """True iff the intended use, given this passport, demands human
    approval before proceeding.

    Cases:
    - intended_use not in passport.allowed_use → True (out-of-scope use)
    - contains_pii AND external_use_allowed → True (external PII)
    - sensitivity == "high" → True (always reviewed)
    - retention_policy == "delete_after_close" AND intended_use == "reporting" → True
    """
    if intended_use not in passport.allowed_use:
        return True
    if passport.contains_pii and passport.external_use_allowed:
        return True
    if passport.sensitivity == "high":
        return True
    if (
        passport.retention_policy == "delete_after_close"
        and intended_use == "reporting"
    ):
        return True
    return False


__all__ = [
    "ALLOWED_OWNERS",
    "ALLOWED_RETENTION",
    "ALLOWED_SENSITIVITY",
    "ALLOWED_SOURCE_TYPES",
    "ALLOWED_USES",
    "SourcePassport",
    "ValidationResult",
    "requires_approval",
    "validate",
]
