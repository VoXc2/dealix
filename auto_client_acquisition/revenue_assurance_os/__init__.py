"""Revenue Assurance OS — the Operating Assurance Layer above every machine.

Dealix does not need more machines; it needs a layer that proves, weekly,
that the machines produce revenue, serve the customer, prevent risk, record
evidence, and tell the founder what to double / kill / not build.

This package is a *layer*: it reads from existing systems (full_ops_radar,
value_os, auditability_os, approval_center, governance_os, sales_os,
proof_os) and never mutates them. It performs no live-send.

Components:
  - assurance_score      : 7-category Revenue Assurance Score (0-100)
  - scale_gate           : the 7 hard thresholds gating expansion
  - truth_report         : weekly truth-from-facts report
  - funnel_scoreboard    : the 10 funnel numbers that matter
  - stage_exit           : per-stage exit criteria
  - definition_of_done   : per-machine Definition of Done
  - acceptance_tests     : Red-Team failure-mode suite
  - gates                : deterministic failure-mode guards
  - evidence_audit       : weekly Evidence Ledger integrity audit
  - agent_observability  : redacted agent-run log
  - experiment_system    : <= 3 disciplined experiments per week
  - ceo_review           : weekly CEO Review scaffold
  - board_pack           : monthly Board Pack
  - no_build_gate        : the No-Build Gate
  - root_cause           : funnel Root Cause Matrix
  - control_rules        : scale / keep / kill channel verdict
  - renderers            : bilingual markdown renderers
"""

from auto_client_acquisition.revenue_assurance_os.acceptance_tests import (
    AcceptanceResult,
    acceptance_suite_passed,
    run_acceptance_suite,
)
from auto_client_acquisition.revenue_assurance_os.agent_observability import (
    AgentRunRecord,
    list_runs,
    record_run,
)
from auto_client_acquisition.revenue_assurance_os.assurance_score import (
    CATEGORY_WEIGHTS,
    compute_assurance_score,
    readiness_label,
)
from auto_client_acquisition.revenue_assurance_os.board_pack import (
    BoardPack,
    build_board_pack,
)
from auto_client_acquisition.revenue_assurance_os.ceo_review import (
    CeoReview,
    build_ceo_review,
)
from auto_client_acquisition.revenue_assurance_os.control_rules import (
    ChannelVerdict,
    channel_verdict,
)
from auto_client_acquisition.revenue_assurance_os.definition_of_done import (
    MACHINE_DOD,
    dod_status,
)
from auto_client_acquisition.revenue_assurance_os.evidence_audit import (
    EvidenceAuditResult,
    audit_evidence,
)
from auto_client_acquisition.revenue_assurance_os.experiment_system import (
    Experiment,
    ExperimentDecision,
    register_experiment,
)
from auto_client_acquisition.revenue_assurance_os.funnel_scoreboard import (
    FunnelScoreboard,
    FunnelStage,
    build_scoreboard,
    worst_bottleneck,
)
from auto_client_acquisition.revenue_assurance_os.no_build_gate import (
    NoBuildDecision,
    no_build_decision,
)
from auto_client_acquisition.revenue_assurance_os.root_cause import (
    RootCauseDiagnosis,
    diagnose,
)
from auto_client_acquisition.revenue_assurance_os.scale_gate import (
    ScaleGateResult,
    can_scale,
)
from auto_client_acquisition.revenue_assurance_os.stage_exit import (
    PipelineStage,
    stage_exit_check,
)
from auto_client_acquisition.revenue_assurance_os.truth_report import (
    TruthReport,
    build_truth_report,
)

__all__ = [
    "CATEGORY_WEIGHTS",
    "MACHINE_DOD",
    "AcceptanceResult",
    "AgentRunRecord",
    "BoardPack",
    "CeoReview",
    "ChannelVerdict",
    "EvidenceAuditResult",
    "Experiment",
    "ExperimentDecision",
    "FunnelScoreboard",
    "FunnelStage",
    "NoBuildDecision",
    "PipelineStage",
    "RootCauseDiagnosis",
    "ScaleGateResult",
    "TruthReport",
    "acceptance_suite_passed",
    "audit_evidence",
    "build_board_pack",
    "build_ceo_review",
    "build_scoreboard",
    "build_truth_report",
    "can_scale",
    "channel_verdict",
    "compute_assurance_score",
    "diagnose",
    "dod_status",
    "list_runs",
    "no_build_decision",
    "readiness_label",
    "record_run",
    "register_experiment",
    "run_acceptance_suite",
    "stage_exit_check",
    "worst_bottleneck",
]
