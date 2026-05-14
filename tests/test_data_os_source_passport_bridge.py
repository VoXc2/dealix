"""Bridge tests: Data OS ↔ Source Passport v2."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.source_passport_v2 import SourcePassportV2
from auto_client_acquisition.data_os.source_passport import (
    source_passport_from_v2,
    source_passport_valid_for_ai,
)


def test_source_passport_from_v2_maps_to_institutional_shape() -> None:
    v2 = SourcePassportV2(
        source_id="SRC-001",
        source_type="client_upload",
        owner="client",
        collection_context="crm_export",
        allowed_use=("internal_analysis", "draft_only"),
        contains_pii=True,
        sensitivity="medium",
        relationship_status="contracted",
        ai_access_allowed=True,
        external_use_allowed=False,
        retention_policy="project_duration",
        deletion_required_after="project_end+30d",
    )
    p = source_passport_from_v2(v2)
    ok, err = source_passport_valid_for_ai(p)
    assert ok
    assert err == ()


def test_governance_hint_pii_external_path() -> None:
    from auto_client_acquisition.data_os.source_passport import governance_decision_hints_for_passport_gate

    ok, key = governance_decision_hints_for_passport_gate(
        False,
        ("pii_external_use_requires_approval_workflow",),
    )
    assert not ok
    assert key == "pii_external_requires_approval"
