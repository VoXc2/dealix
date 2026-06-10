"""Diagnostic Workflow — v6 Phase 4 founder happy-path orchestrator.

Wires intake -> diagnostic build -> service recommendation -> pilot
offer -> delivery plan -> proof plan into a single module the founder
calls when a warm intro lands.

Pure local composition. No LLM, no live send, no charge. The pilot
price is FIXED at 499 SAR (Literal[499] in the schema).

Public API:
    from auto_client_acquisition.diagnostic_workflow import (
        IntakeRequest, IntakeRecord, DiagnosticBundle,
        PilotOffer, ProofPlan,
        parse_intake, build_diagnostic, recommend_service,
        build_pilot_offer, build_delivery_plan_for_recommendation,
        build_proof_plan,
    )
"""
from auto_client_acquisition.diagnostic_workflow.delivery_plan_connector import (
    build_delivery_plan_for_recommendation,
)
from auto_client_acquisition.diagnostic_workflow.diagnostic_builder import (
    build_diagnostic,
)
from auto_client_acquisition.diagnostic_workflow.intake_parser import parse_intake
from auto_client_acquisition.diagnostic_workflow.pilot_offer_builder import (
    build_pilot_offer,
)
from auto_client_acquisition.diagnostic_workflow.proof_pack_connector import (
    build_proof_plan,
)
from auto_client_acquisition.diagnostic_workflow.schemas import (
    DiagnosticBundle,
    IntakeRecord,
    IntakeRequest,
    PilotOffer,
    ProofPlan,
)
from auto_client_acquisition.diagnostic_workflow.service_recommender import (
    recommend_service,
)

__all__ = [
    "DiagnosticBundle",
    "IntakeRecord",
    "IntakeRequest",
    "PilotOffer",
    "ProofPlan",
    "build_delivery_plan_for_recommendation",
    "build_diagnostic",
    "build_pilot_offer",
    "build_proof_plan",
    "parse_intake",
    "recommend_service",
]
