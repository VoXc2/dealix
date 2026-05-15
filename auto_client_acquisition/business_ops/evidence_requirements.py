"""
Wave 9 - Evidence Requirements per Journey Stage
Defines what evidence is required to advance through each stage.
"""
from dataclasses import dataclass, field

from .stage_definitions import JourneyStage


@dataclass
class EvidenceRequirement:
    stage: JourneyStage
    required_fields: list[str]
    optional_fields: list[str] = field(default_factory=list)
    proof_level: int = 0   # L0-L5
    notes: str = ""


EVIDENCE_REQUIREMENTS: dict[JourneyStage, EvidenceRequirement] = {
    JourneyStage.TARGET_IDENTIFIED: EvidenceRequirement(
        stage=JourneyStage.TARGET_IDENTIFIED,
        required_fields=["company_name", "sector", "city"],
        optional_fields=["website", "linkedin_url", "employee_count"],
        proof_level=0,
        notes="Manually entered by founder. No scraping.",
    ),
    JourneyStage.ICP_QUALIFIED: EvidenceRequirement(
        stage=JourneyStage.ICP_QUALIFIED,
        required_fields=["icp_score", "sector_match", "size_match"],
        optional_fields=["revenue_range", "pain_hypothesis"],
        proof_level=0,
        notes="ICP score >= 60 to advance.",
    ),
    JourneyStage.WARM_INTRO_DRAFTED: EvidenceRequirement(
        stage=JourneyStage.WARM_INTRO_DRAFTED,
        required_fields=["draft_message_text", "channel"],
        optional_fields=["referral_name"],
        proof_level=0,
        notes="Draft only. Not sent. channel must not be cold_whatsapp.",
    ),
    JourneyStage.OUTREACH_APPROVED: EvidenceRequirement(
        stage=JourneyStage.OUTREACH_APPROVED,
        required_fields=["founder_approval_timestamp", "approved_by"],
        proof_level=0,
        notes="Explicit founder approval required.",
    ),
    JourneyStage.OUTREACH_SENT: EvidenceRequirement(
        stage=JourneyStage.OUTREACH_SENT,
        required_fields=["sent_timestamp", "channel", "message_ref"],
        proof_level=1,
        notes="Manual send confirmation. No automation.",
    ),
    JourneyStage.RESPONSE_RECEIVED: EvidenceRequirement(
        stage=JourneyStage.RESPONSE_RECEIVED,
        required_fields=["response_text", "response_timestamp", "sentiment"],
        proof_level=1,
    ),
    JourneyStage.DISCOVERY_SCHEDULED: EvidenceRequirement(
        stage=JourneyStage.DISCOVERY_SCHEDULED,
        required_fields=["meeting_datetime", "meeting_channel"],
        proof_level=1,
    ),
    JourneyStage.DISCOVERY_COMPLETED: EvidenceRequirement(
        stage=JourneyStage.DISCOVERY_COMPLETED,
        required_fields=["pain_points", "current_state", "desired_state", "budget_signal"],
        optional_fields=["notes", "recording_consent"],
        proof_level=1,
    ),
    JourneyStage.FIT_SCORED: EvidenceRequirement(
        stage=JourneyStage.FIT_SCORED,
        required_fields=["fit_score", "recommended_offer_id", "scoring_breakdown"],
        proof_level=1,
    ),
    JourneyStage.OFFER_PRESENTED: EvidenceRequirement(
        stage=JourneyStage.OFFER_PRESENTED,
        required_fields=["offer_id", "price_presented", "presented_at"],
        proof_level=1,
        notes="No guaranteed outcome claims.",
    ),
    JourneyStage.PROPOSAL_SENT: EvidenceRequirement(
        stage=JourneyStage.PROPOSAL_SENT,
        required_fields=["proposal_doc_ref", "sent_at"],
        proof_level=1,
    ),
    JourneyStage.NEGOTIATION: EvidenceRequirement(
        stage=JourneyStage.NEGOTIATION,
        required_fields=["negotiation_notes"],
        proof_level=1,
    ),
    JourneyStage.VERBAL_AGREEMENT: EvidenceRequirement(
        stage=JourneyStage.VERBAL_AGREEMENT,
        required_fields=["verbal_yes_note", "agreed_offer_id", "agreed_price"],
        proof_level=2,
    ),
    JourneyStage.CONTRACT_SENT: EvidenceRequirement(
        stage=JourneyStage.CONTRACT_SENT,
        required_fields=["contract_doc_ref", "sent_at"],
        proof_level=2,
    ),
    JourneyStage.CONTRACT_SIGNED: EvidenceRequirement(
        stage=JourneyStage.CONTRACT_SIGNED,
        required_fields=["signed_contract_ref", "signed_at", "client_name"],
        proof_level=3,
    ),
    JourneyStage.INVOICE_ISSUED: EvidenceRequirement(
        stage=JourneyStage.INVOICE_ISSUED,
        required_fields=["invoice_number", "amount_sar", "zatca_compliant"],
        proof_level=3,
        notes="ZATCA compliance required for KSA invoicing.",
    ),
    JourneyStage.PAYMENT_CONFIRMED: EvidenceRequirement(
        stage=JourneyStage.PAYMENT_CONFIRMED,
        required_fields=["payment_reference", "amount_received_sar", "payment_method", "confirmed_at"],
        proof_level=4,
        notes="HARD GATE: No delivery without payment_confirmed.",
    ),
    JourneyStage.ONBOARDING_STARTED: EvidenceRequirement(
        stage=JourneyStage.ONBOARDING_STARTED,
        required_fields=["onboarding_checklist_id", "started_at"],
        proof_level=3,
    ),
    JourneyStage.DELIVERY_IN_PROGRESS: EvidenceRequirement(
        stage=JourneyStage.DELIVERY_IN_PROGRESS,
        required_fields=["delivery_milestones", "kickoff_date"],
        proof_level=3,
    ),
    JourneyStage.DELIVERY_COMPLETED: EvidenceRequirement(
        stage=JourneyStage.DELIVERY_COMPLETED,
        required_fields=["deliverables_accepted", "completion_date", "client_sign_off"],
        proof_level=4,
    ),
    JourneyStage.RESULT_DOCUMENTED: EvidenceRequirement(
        stage=JourneyStage.RESULT_DOCUMENTED,
        required_fields=["measured_outcome", "baseline", "result_delta"],
        optional_fields=["client_quote_with_permission"],
        proof_level=4,
        notes="Real data only. No fabricated metrics.",
    ),
    JourneyStage.CASE_STUDY_CANDIDATE: EvidenceRequirement(
        stage=JourneyStage.CASE_STUDY_CANDIDATE,
        required_fields=["client_permission_doc", "client_permission_granted_at", "result_summary"],
        proof_level=5,
        notes="Explicit client permission required before any public use.",
    ),
}


def get_evidence_requirements(stage: JourneyStage) -> EvidenceRequirement | None:
    return EVIDENCE_REQUIREMENTS.get(stage)


def validate_evidence(stage: JourneyStage, evidence: dict) -> dict:
    """Returns {"valid": bool, "missing": [...], "warnings": [...]}"""
    req = get_evidence_requirements(stage)
    if not req:
        return {"valid": False, "missing": ["unknown_stage"], "warnings": []}
    missing = [f for f in req.required_fields if not evidence.get(f)]
    warnings = []
    if stage == JourneyStage.WARM_INTRO_DRAFTED:
        channel = evidence.get("channel", "")
        if "whatsapp" in str(channel).lower() and evidence.get("is_cold", True):
            warnings.append("BLOCKED: cold WhatsApp outreach is not permitted")
    if stage == JourneyStage.PAYMENT_CONFIRMED:
        if not evidence.get("payment_reference"):
            warnings.append("HARD GATE: delivery cannot start without payment_reference")
    return {
        "valid": len(missing) == 0,
        "missing": missing,
        "warnings": warnings,
        "proof_level": req.proof_level,
    }
