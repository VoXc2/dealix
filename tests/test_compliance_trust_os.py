"""Tests for compliance_trust_os."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os import (
    COMPLIANCE_DASHBOARD_METRICS,
    COMPLIANCE_REPORT_SECTIONS,
    GovernanceDecision,
    KNOWN_RUNTIME_POLICY_RULES,
    SourcePassportV2,
    ai_use_requires_passport,
    allowed_use_permits_ai,
    audit_event_metadata_complete,
    claim_allowed_in_client_output,
    compliance_dashboard_coverage_score,
    compliance_report_sections_complete,
    external_blocked_without_passport_permission,
    governance_decision_for_pii_external,
    incident_closure_requires_artifact,
    pii_plus_external_requires_approval,
    policy_rule_known,
    source_passport_v2_valid,
)


def _sample_passport() -> SourcePassportV2:
    return SourcePassportV2(
        source_id="SRC-001",
        source_type="client_upload",
        owner="client",
        collection_context="revenue_analysis",
        allowed_use=("internal_analysis", "draft_only"),
        contains_pii=True,
        sensitivity="medium",
        relationship_status="existing_relationship",
        ai_access_allowed=True,
        external_use_allowed=False,
        retention_policy="project_duration",
        deletion_required_after="contract_end",
    )


def test_source_passport_v2() -> None:
    p = _sample_passport()
    assert source_passport_v2_valid(p)
    assert ai_use_requires_passport(True)
    assert allowed_use_permits_ai(allowed_use=p.allowed_use)


def test_governance_decision_router() -> None:
    assert (
        governance_decision_for_pii_external(
            contains_pii=True,
            external_action_requested=False,
            passport_external_allowed=False,
        )
        == GovernanceDecision.DRAFT_ONLY
    )
    assert (
        governance_decision_for_pii_external(
            contains_pii=False,
            external_action_requested=True,
            passport_external_allowed=True,
        )
        == GovernanceDecision.REQUIRE_APPROVAL
    )
    assert (
        governance_decision_for_pii_external(
            contains_pii=False,
            external_action_requested=True,
            passport_external_allowed=False,
        )
        == GovernanceDecision.BLOCK
    )


def test_pii_external_approval_flag() -> None:
    assert pii_plus_external_requires_approval(contains_pii=True, external_action_requested=True)
    assert external_blocked_without_passport_permission(passport_external_allowed=False)


def test_claim_compliance() -> None:
    assert not claim_allowed_in_client_output("UNSUPPORTED")
    assert claim_allowed_in_client_output("ESTIMATED")


def test_audit_and_report() -> None:
    ok, _ = audit_event_metadata_complete(frozenset())
    assert not ok
    ok2, _ = compliance_report_sections_complete(frozenset(COMPLIANCE_REPORT_SECTIONS))
    assert ok2


def test_incident_closure() -> None:
    assert not incident_closure_requires_artifact(rule_added=False, test_added=False, checklist_updated=False)
    assert incident_closure_requires_artifact(rule_added=True, test_added=False, checklist_updated=False)


def test_dashboard_coverage() -> None:
    assert compliance_dashboard_coverage_score(frozenset(COMPLIANCE_DASHBOARD_METRICS)) == 100


def test_policy_registry() -> None:
    assert policy_rule_known("no_source_no_ai")
    assert len(KNOWN_RUNTIME_POLICY_RULES) >= 3


def test_channel_and_claim_safety() -> None:
    from auto_client_acquisition.compliance_trust_os import (
        COMPLIANCE_CHANNEL_POLICIES,
        claim_estimated_requires_caveat,
        compliance_channel_policy_valid,
        external_channel_action_requires_approval,
        forbidden_claim_pattern_listed,
    )

    assert compliance_channel_policy_valid(COMPLIANCE_CHANNEL_POLICIES[0])
    assert external_channel_action_requires_approval("email")
    assert forbidden_claim_pattern_listed("guaranteed_sales")
    assert claim_estimated_requires_caveat("ESTIMATED")
    assert not claim_estimated_requires_caveat("VERIFIED")
