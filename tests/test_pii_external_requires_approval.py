"""Contract: PII + external_use_allowed must fail static AI-valid check (approval workflow)."""

from __future__ import annotations

from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    SourcePassport,
    source_passport_valid_for_ai,
)


def test_pii_external_requires_approval_workflow() -> None:
    passport = SourcePassport(
        source_id="SRC-PII-1",
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"internal_analysis"}),
        contains_pii=True,
        sensitivity="high",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=True,
    )
    ok, errors = source_passport_valid_for_ai(passport)
    assert not ok
    assert "pii_external_use_requires_approval_workflow" in errors
