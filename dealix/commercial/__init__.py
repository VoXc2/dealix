"""dealix.commercial — Commercial chain engine.

Diagnostic → Warm Intro → Pilot Delivery → Proof Pack → Upsell.
All modules enforce constitutional guardrails:
  NO_LIVE_SEND, NO_LIVE_CHARGE, NO_FAKE_PROOF, NO_UNAPPROVED_TESTIMONIAL.
"""

from dealix.commercial.case_study_generator import (
    CaseStudyDocument,
    CaseStudyGenerator,
    CaseStudyRequest,
)
from dealix.commercial.diagnostic_engine import (
    DiagnosticEngine,
    DiagnosticReport,
    DiagnosticRequest,
)
from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotPlan, PilotStartRequest
from dealix.commercial.proof_builder import ProofBuilder, ProofBuildRequest, ProofPackDocument
from dealix.commercial.upsell_engine import UpsellCheckResult, UpsellEngine
from dealix.commercial.warm_intro_generator import (
    OutreachDraftBundle,
    WarmIntroGenerator,
    WarmIntroRequest,
)

__all__ = [
    "CaseStudyDocument",
    "CaseStudyGenerator",
    "CaseStudyRequest",
    "DiagnosticEngine",
    "DiagnosticReport",
    "DiagnosticRequest",
    "OutreachDraftBundle",
    "PilotDeliveryKit",
    "PilotPlan",
    "PilotStartRequest",
    "ProofBuildRequest",
    "ProofBuilder",
    "ProofPackDocument",
    "UpsellCheckResult",
    "UpsellEngine",
    "WarmIntroGenerator",
    "WarmIntroRequest",
]
