"""
Legacy acquisition pipeline compatibility orchestrator.

Flow:
  raw payload → Intake → ICP/Pain analysis → Qualification questions
              → truth-gated CRM mirror → truth-gated booking/proposal/distribution

IMPORTANT:
Dealix Revenue Mesh / Company OS owns commercial truth. This compatibility
pipeline may analyze unverified input, but it must not promote research or a
fit score into a CRM relationship, deal, booking, proposal, or distribution
candidate without evidence-backed authority metadata.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.agents.booking import BookingAgent, BookingResult
from auto_client_acquisition.agents.crm import CRMAgent, CRMSyncResult
from auto_client_acquisition.agents.icp_matcher import FitScore, ICPMatcherAgent
from auto_client_acquisition.agents.intake import IntakeAgent, Lead, LeadSource, LeadStatus
from auto_client_acquisition.agents.pain_extractor import ExtractionResult, PainExtractorAgent
from auto_client_acquisition.agents.proposal import Proposal, ProposalAgent
from auto_client_acquisition.agents.qualification import QualificationAgent, QualificationResult
from auto_client_acquisition.revenue_os.crm_mirror_policy import evaluate_hubspot_mirror
from autonomous_growth.distribution_engine import (
    AutonomousDistributionEngine,
    DistributionEngineResult,
)
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PipelineResult:
    lead: Lead
    extraction: ExtractionResult | None = None
    fit_score: FitScore | None = None
    qualification: QualificationResult | None = None
    crm_sync: CRMSyncResult | None = None
    booking: BookingResult | None = None
    proposal: Proposal | None = None
    distribution: DistributionEngineResult | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lead": self.lead.to_dict(),
            "extraction": self.extraction.to_dict() if self.extraction else None,
            "fit_score": self.fit_score.to_dict() if self.fit_score else None,
            "qualification": self.qualification.to_dict() if self.qualification else None,
            "crm_sync": self.crm_sync.to_dict() if self.crm_sync else None,
            "booking": self.booking.to_dict() if self.booking else None,
            "proposal": self.proposal.to_dict() if self.proposal else None,
            "distribution": self.distribution.to_dict() if self.distribution else None,
            "warnings": self.warnings,
        }


class AcquisitionPipeline:
    """Compatibility orchestrator with fail-closed commercial side effects."""

    def __init__(self) -> None:
        self.intake = IntakeAgent()
        self.icp_matcher = ICPMatcherAgent()
        self.pain_extractor = PainExtractorAgent()
        self.qualification = QualificationAgent()
        self.crm = CRMAgent()
        self.booking = BookingAgent()
        self.proposal = ProposalAgent()
        self.distribution_engine = AutonomousDistributionEngine()
        self.log = logger.bind(component="acquisition_pipeline")

    async def run(
        self,
        payload: dict[str, Any],
        *,
        source: LeadSource | str = LeadSource.WEBSITE,
        use_llm_pain: bool = True,
        auto_book: bool = False,
        auto_proposal: bool = False,
    ) -> PipelineResult:
        """Run analysis for one payload; commercial writes fail closed."""
        result = PipelineResult(lead=Lead(id="pending", source=LeadSource.MANUAL))

        # Step 1 — Intake. Intake normalizes input but does NOT verify commercial
        # authority. Trusted adapters must stamp evidence metadata separately.
        lead = await self.intake.run(payload=payload, source=source)
        result.lead = lead

        # Preserve only an explicit trusted-adapter envelope. Browser/user fields
        # alone are never authority. Internal adapters can pass this object after
        # they have verified it against the canonical evidence plane.
        trusted = payload.get("_dealix_verified")
        if isinstance(trusted, dict) and trusted.get("authority_verified") is True:
            allowed_keys = {
                "authority_verified",
                "truth_class",
                "relationship_state",
                "evidence_id",
                "opportunity_id",
                "consent_state",
                "self_test",
                "synthetic",
                "suppressed",
                "opted_out",
                "quote_evidence_id",
                "approved_quote_amount_sar",
                "payment_verified",
                "payment_evidence_id",
            }
            lead.metadata.update({k: trusted[k] for k in allowed_keys if k in trusted})

        # Step 2 — Pain extraction (analysis only)
        if lead.message:
            try:
                extraction = await self.pain_extractor.run(
                    message=lead.message,
                    locale=lead.locale,
                    use_llm=use_llm_pain,
                )
                result.extraction = extraction
                lead.pain_points = [p.text for p in extraction.pain_points]
                lead.urgency_score = extraction.urgency_score
            except Exception as e:
                self.log.warning("pain_extraction_skipped", error=str(e))
                result.warnings.append(f"pain_extraction_failed: {e}")

        # Step 3 — ICP match (analysis only; fit != relationship)
        try:
            fit = await self.icp_matcher.run(lead=lead)
            result.fit_score = fit
            lead.fit_score = fit.overall_score
        except Exception as e:
            self.log.warning("icp_match_failed", error=str(e))
            result.warnings.append(f"icp_match_failed: {e}")

        # Step 4 — Qualification question set. A model/status result does not by
        # itself authorize CRM/deal/contact promotion.
        try:
            qual = await self.qualification.run(lead=lead, fit_score=result.fit_score)
            result.qualification = qual
            lead.status = qual.new_status
        except Exception as e:
            self.log.warning("qualification_failed", error=str(e))
            result.warnings.append(f"qualification_failed: {e}")

        mirror = evaluate_hubspot_mirror(lead)

        # Step 5 — CRM mirror (best-effort, contact-only by default). The adapter
        # independently re-evaluates the same truth policy.
        if mirror.allow_contact:
            try:
                sync = await self.crm.run(
                    lead=lead,
                    fit_score=result.fit_score,
                    create_deal=False,
                )
                result.crm_sync = sync
            except Exception as e:
                self.log.warning("crm_sync_failed", error=str(e))
                result.warnings.append(f"crm_sync_failed: {e}")
        else:
            result.warnings.append("crm_mirror_blocked: " + ",".join(mirror.reasons))

        # Step 6 — Booking requires evidence-backed relationship authority in
        # addition to fit. Fit score alone can never schedule a buyer.
        if auto_book and mirror.allow_contact and result.fit_score and result.fit_score.overall_score >= 0.5:
            try:
                booking = await self.booking.run(lead=lead)
                result.booking = booking
            except Exception as e:
                self.log.warning("booking_failed", error=str(e))
                result.warnings.append(f"booking_failed: {e}")

        # Step 7 — Proposal remains internal/draft and requires the same verified
        # relationship boundary plus qualified status.
        if (
            auto_proposal
            and mirror.allow_contact
            and result.fit_score
            and result.fit_score.overall_score >= 0.7
            and lead.status in (LeadStatus.QUALIFIED, LeadStatus.DISCOVERY, LeadStatus.PROPOSAL)
        ):
            try:
                proposal = await self.proposal.run(lead=lead, fit_score=result.fit_score)
                result.proposal = proposal
            except Exception as e:
                self.log.warning("proposal_failed", error=str(e))
                result.warnings.append(f"proposal_failed: {e}")

        # Step 8 — Legacy distribution is blocked for unverified research. The
        # canonical Revenue Mesh remains the authority for offer/channel routing.
        if mirror.allow_contact:
            try:
                dist_payload = {
                    "lead_id": lead.id,
                    "icp_score": result.fit_score.overall_score if result.fit_score else 0.4,
                    "sector": getattr(lead, "sector", ""),
                    "company_name": lead.company_name if hasattr(lead, "company_name") else "",
                    "company_size": getattr(lead, "company_size", "medium"),
                    "budget_signal": None,
                    "locale": lead.locale,
                }
                result.distribution = await self.distribution_engine.process_lead(dist_payload)
            except Exception as e:
                self.log.warning("distribution_engine_skipped", error=str(e))
                result.warnings.append(f"distribution_engine_failed: {e}")
        else:
            result.warnings.append("distribution_blocked_unverified_relationship")

        self.log.info(
            "pipeline_complete",
            lead_id=lead.id,
            tier=result.fit_score.tier if result.fit_score else "?",
            status=lead.status.value,
            commercial_authority=mirror.allow_contact,
            distribution_tier=(
                result.distribution.product_route.recommended_tier.value
                if result.distribution and result.distribution.product_route
                else "blocked_or_none"
            ),
            warnings=len(result.warnings),
        )
        return result

    BATCH_MIN_SIZE = 5
    BATCH_MAX_CONCURRENCY = 8

    async def run_batch(
        self,
        payloads: list[dict[str, Any]],
        *,
        source: LeadSource | str = LeadSource.WEBSITE,
        use_llm_pain: bool = True,
        auto_book: bool = False,
        auto_proposal: bool = False,
        concurrency: int | None = None,
    ) -> list[PipelineResult]:
        """Run a bounded batch; every item keeps its own truth gate."""
        if not payloads:
            return []

        limit = concurrency or self.BATCH_MAX_CONCURRENCY
        sem = asyncio.Semaphore(limit)

        async def _one(p: dict[str, Any]) -> PipelineResult:
            async with sem:
                return await self.run(
                    payload=p,
                    source=source,
                    use_llm_pain=use_llm_pain,
                    auto_book=auto_book,
                    auto_proposal=auto_proposal,
                )

        self.log.info(
            "batch_start",
            size=len(payloads),
            concurrency=limit,
            use_batch_llm=len(payloads) >= self.BATCH_MIN_SIZE,
        )

        results = await asyncio.gather(*[_one(p) for p in payloads], return_exceptions=True)
        final: list[PipelineResult] = []
        errors = 0
        for r in results:
            if isinstance(r, Exception):
                errors += 1
                final.append(
                    PipelineResult(
                        lead=Lead(id="error", source=LeadSource.MANUAL),
                        warnings=[f"batch_error: {r}"],
                    )
                )
            else:
                final.append(r)  # type: ignore[arg-type]

        self.log.info("batch_complete", processed=len(final), errors=errors)
        return final
