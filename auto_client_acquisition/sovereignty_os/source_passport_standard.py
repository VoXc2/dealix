"""Source Passport Standard — validation against the canonical schema.

See ``docs/sovereignty/SOURCE_PASSPORT_STANDARD.md``. Wraps the
``global_grade_os.enterprise_trust.SourcePassport`` dataclass with
sovereignty-grade checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from auto_client_acquisition.global_grade_os.enterprise_trust import (
    AllowedUse,
    SensitivityLevel,
    SourcePassport,
)


class PassportStandardCheck(str, Enum):
    OWNER_PRESENT = "owner_present"
    ALLOWED_USE_PRESENT = "allowed_use_present"
    SENSITIVITY_DECLARED = "sensitivity_declared"
    AI_ACCESS_DECISION_PRESENT = "ai_access_decision_present"
    EXTERNAL_USE_DECISION_PRESENT = "external_use_decision_present"
    RESIDENCY_PRESENT = "residency_present"
    PII_FLAG_PRESENT = "pii_flag_present"
    INTERNAL_USE_ONLY_WHEN_ALLOWED_USE_EMPTY = "internal_use_only_when_allowed_use_empty"
    PII_NOT_PUBLISHABLE = "pii_not_publishable"


@dataclass(frozen=True)
class PassportValidation:
    valid: bool
    failed_checks: tuple[PassportStandardCheck, ...]
    warnings: tuple[str, ...] = ()


def validate_passport(passport: SourcePassport | None) -> PassportValidation:
    """Validate a passport against the sovereignty standard.

    A ``None`` passport always fails — sovereignty requires presence.
    """

    if passport is None:
        return PassportValidation(
            valid=False,
            failed_checks=(PassportStandardCheck.OWNER_PRESENT,),
            warnings=("passport_missing",),
        )

    failures: list[PassportStandardCheck] = []
    warnings: list[str] = []

    if not passport.owner:
        failures.append(PassportStandardCheck.OWNER_PRESENT)
    if not passport.allowed_use:
        failures.append(PassportStandardCheck.ALLOWED_USE_PRESENT)
    if not isinstance(passport.sensitivity, SensitivityLevel):
        failures.append(PassportStandardCheck.SENSITIVITY_DECLARED)
    # bool fields exist in the dataclass; the presence check is implicit.
    if not isinstance(passport.ai_access_allowed, bool):
        failures.append(PassportStandardCheck.AI_ACCESS_DECISION_PRESENT)
    if not isinstance(passport.external_use_allowed, bool):
        failures.append(PassportStandardCheck.EXTERNAL_USE_DECISION_PRESENT)
    if not passport.residency:
        failures.append(PassportStandardCheck.RESIDENCY_PRESENT)
    if not isinstance(passport.contains_pii, bool):
        failures.append(PassportStandardCheck.PII_FLAG_PRESENT)

    if (
        passport.contains_pii
        and AllowedUse.PUBLIC_PUBLICATION in passport.allowed_use
    ):
        failures.append(PassportStandardCheck.PII_NOT_PUBLISHABLE)

    if not passport.allowed_use:
        warnings.append("falling_back_to_internal_use_only")
    if passport.last_reviewed_at is None:
        warnings.append("passport_never_reviewed")

    return PassportValidation(
        valid=not failures,
        failed_checks=tuple(failures),
        warnings=tuple(warnings),
    )
