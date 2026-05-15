"""Dealix Source Passport — data sovereignty gate before AI use."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourcePassport:
    source_id: str
    source_type: str
    owner: str
    allowed_use: frozenset[str]
    contains_pii: bool
    sensitivity: str
    retention_policy: str
    ai_access_allowed: bool
    external_use_allowed: bool


def source_passport_valid_for_ai(passport: SourcePassport) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not passport.source_id.strip():
        errors.append("source_id_required")
    if not passport.allowed_use:
        errors.append("allowed_use_required")
    if not passport.ai_access_allowed:
        errors.append("ai_access_denied")
    # PII without clear basis still needs human path — flag if external use requested
    if passport.contains_pii and passport.external_use_allowed:
        errors.append("pii_external_use_requires_approval_workflow")
    return not errors, tuple(errors)


def source_passport_allows_task(passport: SourcePassport, task_use: str) -> bool:
    return task_use in passport.allowed_use and passport.ai_access_allowed
