"""Sovereign scale OS — gates, partners, pricing, hiring, SaaS readiness."""

from __future__ import annotations

from auto_client_acquisition.scale_os.hiring_trigger import (
    HiringRole,
    HiringSignals,
    recommend_hires,
)
from auto_client_acquisition.scale_os.partner_score import (
    PartnerReadinessInputs,
    compute_partner_readiness_score,
)
from auto_client_acquisition.scale_os.pricing_stage import (
    PricingEvolutionStage,
    PricingSignals,
    infer_pricing_stage,
)
from auto_client_acquisition.scale_os.saas_transition_score import (
    SaasReadinessBand,
    SaasTransitionSignals,
    compute_saas_transition_score,
    saas_readiness_band,
)
from auto_client_acquisition.scale_os.scale_gates import (
    Gate1FounderToProductized,
    Gate2ProductizedToTool,
    Gate3ToolToTeam,
    Gate4TeamToPartner,
    Gate5PartnerToPlatform,
    Gate6PlatformToAcademy,
    Gate7AcademyToVenture,
    LeverageTier,
    ScaleLadderStep,
    evaluate_gate1,
    evaluate_gate2,
    evaluate_gate3,
    evaluate_gate4,
    evaluate_gate5,
    evaluate_gate6,
    evaluate_gate7,
)
from auto_client_acquisition.scale_os.scale_readiness import (
    FINAL_SCALE_TEST,
    SCALE_SYSTEMS,
    FinalScaleCheck,
    ScaleReadinessReport,
    ScaleSystem,
    ScaleSystemResult,
    compute_scale_readiness,
    evaluate_final_scale_test,
    evaluate_scale_system,
)

__all__ = [
    "FINAL_SCALE_TEST",
    "SCALE_SYSTEMS",
    "FinalScaleCheck",
    "Gate1FounderToProductized",
    "Gate2ProductizedToTool",
    "Gate3ToolToTeam",
    "Gate4TeamToPartner",
    "Gate5PartnerToPlatform",
    "Gate6PlatformToAcademy",
    "Gate7AcademyToVenture",
    "HiringRole",
    "HiringSignals",
    "LeverageTier",
    "PartnerReadinessInputs",
    "PricingEvolutionStage",
    "PricingSignals",
    "SaasReadinessBand",
    "SaasTransitionSignals",
    "ScaleLadderStep",
    "ScaleReadinessReport",
    "ScaleSystem",
    "ScaleSystemResult",
    "compute_partner_readiness_score",
    "compute_saas_transition_score",
    "compute_scale_readiness",
    "evaluate_final_scale_test",
    "evaluate_gate1",
    "evaluate_gate2",
    "evaluate_gate3",
    "evaluate_gate4",
    "evaluate_gate5",
    "evaluate_gate6",
    "evaluate_gate7",
    "evaluate_scale_system",
    "infer_pricing_stage",
    "recommend_hires",
    "saas_readiness_band",
]
