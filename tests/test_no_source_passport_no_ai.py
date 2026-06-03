"""Contract: no valid Source Passport path → no AI use (institutional rule)."""

from __future__ import annotations

from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    SourcePassport,
    source_passport_valid_for_ai,
)


def test_no_source_passport_no_ai_invalid_passport() -> None:
    passport = SourcePassport(
        source_id="",
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"internal_analysis"}),
        contains_pii=False,
        sensitivity="low",
        retention_policy="project_duration",
        ai_access_allowed=False,
        external_use_allowed=False,
    )
    ok, errors = source_passport_valid_for_ai(passport)
    assert not ok
    assert "source_id_required" in errors
    assert "ai_access_denied" in errors


def test_no_source_passport_no_ai_allowed_when_valid() -> None:
    passport = SourcePassport(
        source_id="SRC-001",
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"internal_analysis"}),
        contains_pii=True,
        sensitivity="medium",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )
    ok, errors = source_passport_valid_for_ai(passport)
    assert ok
    assert errors == ()
