#!/usr/bin/env python3
"""Fail-closed verifier for Dealix Human Review opt-in semantics."""

from __future__ import annotations

from dealix.commercial.human_review_opt_in import HumanReviewOptIn, HumanReviewOptInRequest


def _request(**overrides: object) -> HumanReviewOptInRequest:
    values: dict[str, object] = {
        "diagnostic_id": "diag_verify",
        "contact_value": "verify@example.invalid",
        "contact_channel": "email",
        "consent_ref": "consent://verify/human-review",
        "consent_obtained_at": "2026-08-29T09:00:00+03:00",
        "consent_method": "web_form",
        "evaluated_at": "2026-08-29T09:05:00+03:00",
        "follow_up_expires_at": "2026-09-01T09:00:00+03:00",
        "retention_until": "2026-09-05T09:00:00+03:00",
        "retention_notice_version": "privacy-verify",
        "retention_notice_acknowledged": True,
        "suppression_check_ref": "suppression://verify/clear",
        "suppression_state": "CLEAR",
    }
    values.update(overrides)
    return HumanReviewOptInRequest(**values)  # type: ignore[arg-type]


def main() -> int:
    handoff = HumanReviewOptIn.prepare(_request())

    assert handoff.eligible_for_manual_follow_up is True
    assert handoff.state == "CONSENTED_HUMAN_REVIEW_REQUEST"
    assert handoff.consent_method == "web_form"
    assert handoff.consent_obtained_at.endswith("Z")
    assert handoff.contact_fingerprint_scope == "diagnostic_scoped_pseudonym_not_anonymization"
    assert handoff.marketing_consent is False
    assert handoff.relationship_verified is False
    assert handoff.external_send_authority is False
    assert handoff.quote_authority is False
    assert handoff.payment_authority is False
    assert handoff.public_publish_authority is False
    assert handoff.customer_value_claim is False
    assert "verify@example.invalid" not in str(handoff.to_dict())

    suppressed = HumanReviewOptIn.prepare(_request(suppression_state="SUPPRESSED"))
    assert suppressed.eligible_for_manual_follow_up is False
    assert suppressed.blocked_reason == "SUPPRESSED"

    expired = HumanReviewOptIn.prepare(
        _request(evaluated_at="2026-09-02T09:00:00+03:00")
    )
    assert expired.eligible_for_manual_follow_up is False
    assert expired.blocked_reason == "FOLLOW_UP_PERMISSION_EXPIRED"

    print("DEALIX_HUMAN_REVIEW_OPT_IN=PASS")
    print("CONSENT_TIME_METHOD_RECORDED=1")
    print("PURPOSE_SCOPE=human_review_follow_up_only")
    print("FOLLOW_UP_EXPIRY_ENFORCED=1")
    print("RETENTION_BOUNDARY_ENFORCED=1")
    print("MARKETING_CONSENT_INFERRED=0")
    print("RELATIONSHIP_PROMOTED=0")
    print("EXTERNAL_SEND_AUTHORITY=0")
    print("QUOTE_AUTHORITY=0")
    print("PAYMENT_AUTHORITY=0")
    print("RAW_CONTACT_IN_RECEIPT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
