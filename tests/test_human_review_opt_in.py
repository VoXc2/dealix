from __future__ import annotations

import pytest

from dealix.commercial.human_review_opt_in import (
    UNKNOWN,
    HumanReviewOptIn,
    HumanReviewOptInRequest,
)


def _request(**overrides: object) -> HumanReviewOptInRequest:
    values: dict[str, object] = {
        "diagnostic_id": "diag_123",
        "contact_value": "buyer@example.com",
        "contact_channel": "email",
        "consent_ref": "consent://human-review/123",
        "consent_obtained_at": "2026-08-29T09:00:00+03:00",
        "consent_method": "web_form",
        "evaluated_at": "2026-08-29T09:05:00+03:00",
        "follow_up_expires_at": "2026-09-01T09:00:00+03:00",
        "retention_until": "2026-09-05T09:00:00+03:00",
        "retention_notice_version": "privacy-2026-08",
        "retention_notice_acknowledged": True,
        "suppression_check_ref": "suppression://check/123",
        "suppression_state": "CLEAR",
    }
    values.update(overrides)
    return HumanReviewOptInRequest(**values)  # type: ignore[arg-type]


def test_valid_opt_in_prepares_manual_handoff_without_external_authority() -> None:
    first = HumanReviewOptIn.prepare(_request())
    second = HumanReviewOptIn.prepare(_request())

    assert first == second
    assert first.handoff_id.startswith("hr_")
    assert first.state == "CONSENTED_HUMAN_REVIEW_REQUEST"
    assert first.eligible_for_manual_follow_up is True
    assert first.blocked_reason == ""
    assert first.consent_method == "web_form"
    assert first.consent_obtained_at.endswith("Z")
    assert first.marketing_consent is False
    assert first.relationship_verified is False
    assert first.external_send_authority is False
    assert first.quote_authority is False
    assert first.payment_authority is False
    assert first.public_publish_authority is False
    assert first.customer_value_claim is False
    assert first.contact_fingerprint_scope == "diagnostic_scoped_pseudonym_not_anonymization"
    assert "buyer@example.com" not in str(first.to_dict())


def test_contact_fingerprint_is_scoped_to_diagnostic() -> None:
    first = HumanReviewOptIn.prepare(_request(diagnostic_id="diag_1"))
    second = HumanReviewOptIn.prepare(_request(diagnostic_id="diag_2"))
    assert first.contact_fingerprint != second.contact_fingerprint


def test_suppressed_contact_fails_closed() -> None:
    handoff = HumanReviewOptIn.prepare(_request(suppression_state="SUPPRESSED"))
    assert handoff.state == "HUMAN_REVIEW_BLOCKED"
    assert handoff.eligible_for_manual_follow_up is False
    assert handoff.blocked_reason == "SUPPRESSED"
    assert handoff.external_send_authority is False


def test_unknown_suppression_state_fails_closed() -> None:
    handoff = HumanReviewOptIn.prepare(_request(suppression_state=UNKNOWN))
    assert handoff.eligible_for_manual_follow_up is False
    assert handoff.blocked_reason == "SUPPRESSION_STATE_UNKNOWN"


def test_retention_notice_must_be_acknowledged() -> None:
    handoff = HumanReviewOptIn.prepare(_request(retention_notice_acknowledged=False))
    assert handoff.eligible_for_manual_follow_up is False
    assert handoff.blocked_reason == "RETENTION_NOTICE_NOT_ACKNOWLEDGED"


def test_follow_up_permission_expires_fail_closed() -> None:
    handoff = HumanReviewOptIn.prepare(
        _request(evaluated_at="2026-09-02T09:00:00+03:00")
    )
    assert handoff.eligible_for_manual_follow_up is False
    assert handoff.blocked_reason == "FOLLOW_UP_PERMISSION_EXPIRED"


def test_retention_window_must_cover_follow_up_window() -> None:
    with pytest.raises(ValueError, match="retention_until cannot precede"):
        HumanReviewOptIn.prepare(
            _request(retention_until="2026-08-31T09:00:00+03:00")
        )


def test_evaluation_cannot_precede_consent() -> None:
    with pytest.raises(ValueError, match="cannot precede consent"):
        HumanReviewOptIn.prepare(
            _request(evaluated_at="2026-08-29T08:59:00+03:00")
        )


def test_consent_timestamps_require_timezone() -> None:
    with pytest.raises(ValueError, match="include a timezone"):
        HumanReviewOptIn.prepare(
            _request(consent_obtained_at="2026-08-29T09:00:00")
        )


def test_consent_method_must_be_documented_supported_method() -> None:
    with pytest.raises(ValueError, match="consent_method is not supported"):
        HumanReviewOptIn.prepare(_request(consent_method="inferred"))  # type: ignore[arg-type]


def test_human_review_opt_in_cannot_create_marketing_consent() -> None:
    with pytest.raises(ValueError, match="cannot create or infer marketing consent"):
        HumanReviewOptIn.prepare(_request(marketing_consent=True))


def test_scope_cannot_expand_beyond_human_review_follow_up() -> None:
    with pytest.raises(ValueError, match="limited to Human Review follow-up"):
        HumanReviewOptIn.prepare(_request(contact_permission_scope="marketing_and_sales"))


@pytest.mark.parametrize(
    "field,value",
    [
        ("diagnostic_id", ""),
        ("contact_value", ""),
        ("consent_ref", ""),
        ("consent_obtained_at", ""),
        ("retention_notice_version", ""),
        ("suppression_check_ref", ""),
    ],
)
def test_required_evidence_fields_fail_closed(field: str, value: str) -> None:
    with pytest.raises(ValueError):
        HumanReviewOptIn.prepare(_request(**{field: value}))
