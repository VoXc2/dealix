"""Compliance-by-design & trust operations — runtime gates and artifacts."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.allowed_use_checker import (
    allowed_use_internal_analysis_only,
    allowed_use_permits_ai,
)
from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
    governance_decision_for_pii_external,
)
from auto_client_acquisition.compliance_trust_os.audit_trail import (
    AUDIT_EVENT_REQUIRED_FIELDS,
    audit_event_metadata_complete,
)
from auto_client_acquisition.compliance_trust_os.channel_policy import (
    COMPLIANCE_CHANNEL_POLICIES,
    compliance_channel_policy_valid,
    external_channel_action_requires_approval,
)
from auto_client_acquisition.compliance_trust_os.claim_compliance import (
    CLAIM_STATUSES,
    claim_allowed_in_case_safe_summary,
    claim_allowed_in_client_output,
    claim_status_valid,
)
from auto_client_acquisition.compliance_trust_os.claim_safety import (
    FORBIDDEN_CLAIM_PATTERNS,
    claim_estimated_requires_caveat,
    forbidden_claim_pattern_listed,
)
from auto_client_acquisition.compliance_trust_os.compliance_dashboard import (
    COMPLIANCE_DASHBOARD_METRICS,
    compliance_dashboard_coverage_score,
)
from auto_client_acquisition.compliance_trust_os.compliance_report import (
    COMPLIANCE_REPORT_SECTIONS,
    compliance_report_sections_complete,
)
from auto_client_acquisition.compliance_trust_os.incident_response import (
    COMPLIANCE_INCIDENT_FLOW,
    COMPLIANCE_INCIDENT_TYPES,
    compliance_incident_type_valid,
    incident_closure_requires_artifact,
)
from auto_client_acquisition.compliance_trust_os.pii_classifier import (
    PII_SENSITIVITY_LEVELS,
    external_blocked_without_passport_permission,
    pii_plus_external_requires_approval,
    pii_sensitivity_valid,
)
from auto_client_acquisition.compliance_trust_os.policy_registry import (
    KNOWN_RUNTIME_POLICY_RULES,
    policy_rule_known,
)
from auto_client_acquisition.compliance_trust_os.source_passport_v2 import (
    REQUIRED_SOURCE_PASSPORT_V2_FIELDS,
    SourcePassportV2,
    ai_use_requires_passport,
    source_passport_v2_valid,
)

__all__ = (
    "AUDIT_EVENT_REQUIRED_FIELDS",
    "CLAIM_STATUSES",
    "COMPLIANCE_CHANNEL_POLICIES",
    "COMPLIANCE_DASHBOARD_METRICS",
    "COMPLIANCE_INCIDENT_FLOW",
    "COMPLIANCE_INCIDENT_TYPES",
    "COMPLIANCE_REPORT_SECTIONS",
    "FORBIDDEN_CLAIM_PATTERNS",
    "KNOWN_RUNTIME_POLICY_RULES",
    "PII_SENSITIVITY_LEVELS",
    "REQUIRED_SOURCE_PASSPORT_V2_FIELDS",
    "GovernanceDecision",
    "SourcePassportV2",
    "ai_use_requires_passport",
    "allowed_use_internal_analysis_only",
    "allowed_use_permits_ai",
    "audit_event_metadata_complete",
    "claim_allowed_in_case_safe_summary",
    "claim_allowed_in_client_output",
    "claim_estimated_requires_caveat",
    "claim_status_valid",
    "compliance_channel_policy_valid",
    "compliance_dashboard_coverage_score",
    "compliance_incident_type_valid",
    "compliance_report_sections_complete",
    "external_blocked_without_passport_permission",
    "external_channel_action_requires_approval",
    "forbidden_claim_pattern_listed",
    "governance_decision_for_pii_external",
    "incident_closure_requires_artifact",
    "pii_plus_external_requires_approval",
    "pii_sensitivity_valid",
    "policy_rule_known",
    "source_passport_v2_valid",
)
