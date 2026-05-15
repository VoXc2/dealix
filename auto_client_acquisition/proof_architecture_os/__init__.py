"""Enterprise Proof & Value Architecture — deterministic proof economics."""

from __future__ import annotations

from auto_client_acquisition.proof_architecture_os.case_safe_summary import (
    case_safe_public_summary_ok,
)
from auto_client_acquisition.proof_architecture_os.proof_dashboard import (
    PROOF_DASHBOARD_SIGNALS,
    proof_dashboard_coverage_score,
)
from auto_client_acquisition.proof_architecture_os.proof_levels import (
    PROOF_LEVELS,
    proof_level_opens_retainer_path,
    proof_level_valid,
)
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.proof_architecture_os.proof_score import (
    EnterpriseProofDimensions,
    enterprise_proof_score,
    proof_allows_case_study,
    proof_allows_retainer_pitch,
    proof_allows_sales_asset,
    proof_score_band,
)
from auto_client_acquisition.proof_architecture_os.proof_to_retainer import (
    RetainerGateInput,
    RetainerPath,
    VentureFactoryGateV2Input,
    retainer_gate_passes,
    retainer_path_recommendation,
    venture_factory_gate_v2_passes,
)
from auto_client_acquisition.proof_architecture_os.roi_discipline import (
    RoiConfidence,
    roi_must_label_distinct,
    roi_observed_ok_for_internal_report,
    roi_safe_for_public_case,
)
from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)
from auto_client_acquisition.proof_architecture_os.value_metrics_by_offer import (
    OFFER_AI_GOVERNANCE_REVIEW,
    OFFER_AI_QUICK_WIN_SPRINT,
    OFFER_COMPANY_BRAIN_SPRINT,
    OFFER_EXECUTIVE_REPORTING_AUTOMATION,
    OFFER_REVENUE_INTELLIGENCE_SPRINT,
    VALUE_METRICS_BY_OFFER,
    value_metrics_for_offer,
)

__all__ = (
    "OFFER_AI_GOVERNANCE_REVIEW",
    "OFFER_AI_QUICK_WIN_SPRINT",
    "OFFER_COMPANY_BRAIN_SPRINT",
    "OFFER_EXECUTIVE_REPORTING_AUTOMATION",
    "OFFER_REVENUE_INTELLIGENCE_SPRINT",
    "PROOF_DASHBOARD_SIGNALS",
    "PROOF_LEVELS",
    "PROOF_PACK_V2_SECTIONS",
    "VALUE_METRICS_BY_OFFER",
    "EnterpriseProofDimensions",
    "RetainerGateInput",
    "RetainerPath",
    "RoiConfidence",
    "ValueLedgerEvent",
    "VentureFactoryGateV2Input",
    "case_safe_public_summary_ok",
    "enterprise_proof_score",
    "proof_allows_case_study",
    "proof_allows_retainer_pitch",
    "proof_allows_sales_asset",
    "proof_dashboard_coverage_score",
    "proof_level_opens_retainer_path",
    "proof_level_valid",
    "proof_pack_v2_sections_complete",
    "proof_score_band",
    "retainer_gate_passes",
    "retainer_path_recommendation",
    "roi_must_label_distinct",
    "roi_observed_ok_for_internal_report",
    "roi_safe_for_public_case",
    "value_ledger_event_valid",
    "value_metrics_for_offer",
    "venture_factory_gate_v2_passes",
)
