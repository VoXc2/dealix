"""Strategic risk, compliance & resilience — deterministic operating gates."""

from __future__ import annotations

from auto_client_acquisition.risk_resilience_os.channel_policy import (
    FORBIDDEN_CHANNEL_AUTOMATIONS,
    channel_automation_forbidden,
    whatsapp_client_use_allowed,
)
from auto_client_acquisition.risk_resilience_os.claim_safety import (
    CLAIM_CLASSES,
    claim_class_valid,
    claim_may_appear_in_case_study,
)
from auto_client_acquisition.risk_resilience_os.client_risk_score import (
    ClientRiskSignals,
    client_risk_tier,
)
from auto_client_acquisition.risk_resilience_os.incident_response import (
    CLIENT_INCIDENT_PHASES,
    incident_response_phases_complete,
)
from auto_client_acquisition.risk_resilience_os.partner_risk import (
    PartnerCovenantSignals,
    partner_referral_only_weak_qa,
    partner_should_suspend,
)
from auto_client_acquisition.risk_resilience_os.resilience_playbooks import (
    RESILIENCE_SHOCK_TYPES,
    governance_failure_playbook_steps,
    resilience_shock_valid,
)
from auto_client_acquisition.risk_resilience_os.risk_register import (
    RISK_REGISTER_METADATA_FIELDS,
    RISK_TAXONOMY_CATEGORIES,
    risk_register_metadata_complete,
    risk_taxonomy_category_valid,
)
from auto_client_acquisition.risk_resilience_os.risk_score import (
    ai_output_qa_band,
    autonomy_level_allowed_in_mvp,
)
from auto_client_acquisition.risk_resilience_os.strategic_drift import (
    STRATEGIC_DRIFT_WARNING_SIGNALS,
    drift_freeze_new_features_recommended,
    drift_warning_signal_valid,
)

__all__ = (
    "CLAIM_CLASSES",
    "CLIENT_INCIDENT_PHASES",
    "FORBIDDEN_CHANNEL_AUTOMATIONS",
    "RESILIENCE_SHOCK_TYPES",
    "RISK_REGISTER_METADATA_FIELDS",
    "RISK_TAXONOMY_CATEGORIES",
    "STRATEGIC_DRIFT_WARNING_SIGNALS",
    "ClientRiskSignals",
    "PartnerCovenantSignals",
    "ai_output_qa_band",
    "autonomy_level_allowed_in_mvp",
    "channel_automation_forbidden",
    "claim_class_valid",
    "claim_may_appear_in_case_study",
    "client_risk_tier",
    "drift_freeze_new_features_recommended",
    "drift_warning_signal_valid",
    "governance_failure_playbook_steps",
    "incident_response_phases_complete",
    "partner_referral_only_weak_qa",
    "partner_should_suspend",
    "resilience_shock_valid",
    "risk_register_metadata_complete",
    "risk_taxonomy_category_valid",
    "whatsapp_client_use_allowed",
)
