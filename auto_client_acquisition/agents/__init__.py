"""Phase 8 agents package."""
from auto_client_acquisition.agents.intake import IntakeAgent, Lead, LeadSource, LeadStatus
from auto_client_acquisition.agents.icp_matcher import ICPMatcherAgent, FitScore, ICP
from auto_client_acquisition.agents.pain_extractor import PainExtractorAgent, ExtractionResult, PainPoint
from auto_client_acquisition.agents.qualification import QualificationAgent
from auto_client_acquisition.agents.booking import BookingAgent
from auto_client_acquisition.agents.crm import CRMAgent
from auto_client_acquisition.agents.proposal import ProposalAgent
from auto_client_acquisition.agents.outreach import OutreachAgent
from auto_client_acquisition.agents.followup import FollowUpAgent

__all__ = [
    "IntakeAgent",
    "Lead",
    "LeadSource",
    "LeadStatus",
    "ICPMatcherAgent",
    "FitScore",
    "ICP",
    "PainExtractorAgent",
    "ExtractionResult",
    "PainPoint",
    "QualificationAgent",
    "BookingAgent",
    "CRMAgent",
    "ProposalAgent",
    "OutreachAgent",
    "FollowUpAgent",
]
