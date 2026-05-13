"""Institutional Source Passport enforcement.

Wraps ``global_grade_os.enterprise_trust.SourcePassport`` with the
doctrine enforcement rules from
``docs/institutional_control/SOURCE_PASSPORT_STANDARD.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.global_grade_os.enterprise_trust import (
    AllowedUse,
    SourcePassport,
)


@dataclass(frozen=True)
class SourcePassportEnforcement:
    allow: bool
    reason: str
    requires_redaction: bool = False
    requires_approval: bool = False


def enforce_source_passport_use(
    passport: SourcePassport | None,
    *,
    requested_use: AllowedUse,
    is_external_action: bool,
    is_outreach: bool,
) -> SourcePassportEnforcement:
    """Apply the five doctrine rules.

    * No passport → no AI use.
    * No allowed use → internal analysis only.
    * PII + unclear basis → redact or block.
    * External action → approval required.
    * Unknown source → no outreach.
    """

    if passport is None:
        return SourcePassportEnforcement(
            allow=False, reason="no_passport_no_ai_use"
        )

    if not passport.allowed_use:
        if requested_use is AllowedUse.INTERNAL_ANALYSIS:
            return SourcePassportEnforcement(
                allow=True, reason="fallback_to_internal_analysis_only"
            )
        return SourcePassportEnforcement(
            allow=False, reason="no_allowed_use_internal_only"
        )

    if passport.contains_pii and not passport.ai_access_allowed:
        return SourcePassportEnforcement(
            allow=False, reason="pii_without_ai_access", requires_redaction=True
        )

    if not passport.permits(requested_use):
        return SourcePassportEnforcement(
            allow=False, reason="requested_use_not_in_allowed_use"
        )

    if is_outreach and passport.source_type == "unknown":
        return SourcePassportEnforcement(
            allow=False, reason="unknown_source_no_outreach"
        )

    if is_external_action:
        if not passport.external_use_allowed:
            return SourcePassportEnforcement(
                allow=False,
                reason="external_use_not_permitted",
                requires_approval=True,
            )
        return SourcePassportEnforcement(
            allow=True, reason="external_action_allowed_with_approval",
            requires_approval=True,
        )

    return SourcePassportEnforcement(
        allow=True,
        reason="all_preconditions_met",
        requires_redaction=passport.contains_pii,
    )
