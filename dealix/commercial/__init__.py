"""dealix.commercial — Commercial chain engine.

Diagnostic → Warm Intro → Pilot Delivery → Proof Pack → Upsell.
All modules enforce constitutional guardrails:
  NO_LIVE_SEND, NO_LIVE_CHARGE, NO_FAKE_PROOF, NO_UNAPPROVED_TESTIMONIAL.
"""

from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest, DiagnosticReport
from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest, OutreachDraftBundle
from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest, PilotPlan
from dealix.commercial.proof_builder import ProofBuilder, ProofBuildRequest, ProofPackDocument
from dealix.commercial.upsell_engine import UpsellEngine, UpsellCheckResult
from dealix.commercial.case_study_generator import CaseStudyGenerator, CaseStudyRequest, CaseStudyDocument

__all__ = [
    "DiagnosticEngine", "DiagnosticRequest", "DiagnosticReport",
    "WarmIntroGenerator", "WarmIntroRequest", "OutreachDraftBundle",
    "PilotDeliveryKit", "PilotStartRequest", "PilotPlan",
    "ProofBuilder", "ProofBuildRequest", "ProofPackDocument",
    "UpsellEngine", "UpsellCheckResult",
    "CaseStudyGenerator", "CaseStudyRequest", "CaseStudyDocument",
]
