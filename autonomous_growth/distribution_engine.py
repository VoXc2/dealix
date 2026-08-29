"""Legacy autonomous distribution compatibility engine.

This engine may create internal research/draft artifacts only. It does not create
relationships, consent, customer-specific quote authority, send authority,
publish authority, payment authority, or revenue truth.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from autonomous_growth.agents.distribution import DistributionAgent
from autonomous_growth.agents.product_router import ProductRouteDecision, ProductRouterAgent
from autonomous_growth.agents.proposal_sender import (
    ProposalDraft,
    ProposalSenderAgent,
    _read_queue,
    _rewrite_queue,
)
from core.logging import get_logger
from core.utils import generate_id, utcnow

log = get_logger(__name__)
_AUTO_SELECT_CONFIDENCE = 0.6


@dataclass
class DistributionEngineResult:
    lead_id: str
    product_route: ProductRouteDecision | None = None
    proposal_draft: ProposalDraft | None = None
    content_scheduled: bool = False
    sector_campaign_url: str | None = None
    warnings: list[str] = field(default_factory=list)
    commercial_truth_state: str = "UNVERIFIED_RESEARCH_OR_DRAFT"
    synthetic: bool = False
    external_sends_executed: int = 0
    public_publishes_executed: int = 0
    payments_or_spend_executed: int = 0
    execution_authority_issued: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "lead_id": self.lead_id,
            "product_route": self.product_route.to_dict() if self.product_route else None,
            "proposal_draft": self.proposal_draft.to_dict() if self.proposal_draft else None,
            "content_scheduled": self.content_scheduled,
            "sector_campaign_url": self.sector_campaign_url,
            "warnings": self.warnings,
            "commercial_truth_state": self.commercial_truth_state,
            "synthetic": self.synthetic,
            "external_sends_executed": self.external_sends_executed,
            "public_publishes_executed": self.public_publishes_executed,
            "payments_or_spend_executed": self.payments_or_spend_executed,
            "execution_authority_issued": self.execution_authority_issued,
        }


class AutonomousDistributionEngine:
    """Compatibility orchestration for internal research/drafts only."""

    def __init__(self) -> None:
        self.router_agent = ProductRouterAgent()
        self.proposal_agent = ProposalSenderAgent()
        self.distribution_agent = DistributionAgent()
        self.log = log.bind(component="distribution_engine")

    async def process_lead(self, payload: dict[str, Any]) -> DistributionEngineResult:
        lead_id = payload.get("lead_id") or generate_id("lead")
        is_synthetic = bool(payload.get("synthetic")) or payload.get("commercial_truth_state") == "SYNTHETIC_RESEARCH_ONLY"
        result = DistributionEngineResult(
            lead_id=lead_id,
            synthetic=is_synthetic,
            commercial_truth_state=(
                "SYNTHETIC_RESEARCH_ONLY" if is_synthetic else payload.get("commercial_truth_state", "UNVERIFIED_RESEARCH_OR_DRAFT")
            ),
        )

        if is_synthetic:
            result.warnings.extend(
                [
                    "SYNTHETIC_RESEARCH_ONLY",
                    "synthetic_not_relationship",
                    "synthetic_not_proposal_candidate",
                    "external_execution_blocked",
                ]
            )
            return result

        icp_score: float = float(payload.get("icp_score", 0.0))
        sector: str = payload.get("sector", "general")
        company_size: str = payload.get("company_size", "medium")
        budget_signal: str | None = payload.get("budget_signal")
        locale: str = payload.get("locale", "ar")

        try:
            route = await self.router_agent.run(
                lead_profile=payload,
                icp_score=icp_score,
                sector=sector,
                company_size=company_size,
                budget_signal=budget_signal,
            )
            result.product_route = route
        except Exception as exc:
            self.log.warning("product_routing_failed", error=str(exc), lead_id=lead_id)
            result.warnings.append(f"product_routing_failed: {exc}")
            return result

        if route.confidence < _AUTO_SELECT_CONFIDENCE:
            result.warnings.append(f"low_confidence_capability_hypothesis: confidence={route.confidence:.2f}")
        if route.recommended_tier.value != "free_diagnostic":
            result.warnings.append("legacy_paid_tier_is_capability_hypothesis_only")
        if route.requires_founder_approval:
            result.warnings.append(f"founder_review_required_for_capability_hypothesis={route.recommended_tier.value}")
            result.warnings.append(f"founder_approval_required for tier={route.recommended_tier.value}; internal_review_only")

        try:
            draft = await self.proposal_agent.run(product=route.product, lead_profile=payload, locale=locale)
            result.proposal_draft = draft
        except Exception as exc:
            self.log.warning("proposal_generation_failed", error=str(exc), lead_id=lead_id)
            result.warnings.append(f"proposal_generation_failed: {exc}")

        try:
            from autonomous_growth.agents.content import ContentPiece

            placeholder_content = ContentPiece(
                id=generate_id("cnt"),
                content_type="linkedin_post",
                channel="linkedin",
                locale=locale,
                topic=f"Dealix evidence-first diagnostic — {sector} sector",
                title="Dealix evidence-first diagnostic",
                body_markdown="",
                word_count=0,
            )
            await self.distribution_agent.run(content=placeholder_content, channels=["linkedin", "email"])
            result.content_scheduled = True
            result.warnings.append("distribution_plan_internal_only_no_publish_authority")
        except Exception as exc:
            self.log.warning("content_distribution_failed", error=str(exc), lead_id=lead_id)
            result.warnings.append(f"content_distribution_queuing_failed: {exc}")

        self.log.info(
            "lead_processed_internal_only",
            lead_id=lead_id,
            tier=route.recommended_tier.value,
            confidence=route.confidence,
            proposal_id=result.proposal_draft.id if result.proposal_draft else None,
            external_sends_executed=0,
            public_publishes_executed=0,
            payments_or_spend_executed=0,
            execution_authority_issued=0,
        )
        return result

    async def run_sector_distribution(self, sector: str, channels: list[str]) -> list[DistributionEngineResult]:
        """Generate synthetic research fixtures only; never commercial pipeline rows."""
        self.log.info("sector_research_start", sector=sector, channels=channels)
        prospects = self._generate_sector_prospects(sector)
        tasks = [self.process_lead(prospect) for prospect in prospects]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        results: list[DistributionEngineResult] = []
        for item in raw_results:
            if isinstance(item, Exception):
                results.append(
                    DistributionEngineResult(
                        lead_id=generate_id("err"),
                        warnings=[f"sector_research_fixture_failed: {item}"],
                        commercial_truth_state="SYNTHETIC_RESEARCH_ONLY",
                        synthetic=True,
                    )
                )
            else:
                results.append(item)  # type: ignore[arg-type]
        return results

    async def get_pending_approvals(self) -> list[ProposalDraft]:
        return [draft for draft in _read_queue() if draft.status == "pending_approval"]

    async def approve_proposal(self, proposal_id: str) -> bool:
        """Mark internal review complete without granting external authority."""
        all_drafts = _read_queue()
        updated = False
        for draft in all_drafts:
            if draft.id == proposal_id and draft.status == "pending_approval":
                draft.status = "approved"
                draft.commercial_authority = False
                draft.quote_authority = False
                draft.send_authority = False
                draft.execution_authority = False
                draft.external_effect = False
                updated = True
                break
        if updated:
            _rewrite_queue(all_drafts)
            self.log.info("proposal_reviewed_internal_only", proposal_id=proposal_id, send_authority=False, execution_authority=False)
        else:
            self.log.warning("proposal_approve_not_found", proposal_id=proposal_id)
        return updated

    def get_stats(self) -> dict[str, Any]:
        all_drafts = _read_queue()
        counts: dict[str, int] = {"pending_approval": 0, "approved": 0, "sent": 0}
        for draft in all_drafts:
            if draft.status in counts:
                counts[draft.status] += 1
        return {
            "total_processed": len(all_drafts),
            "pending": counts["pending_approval"],
            "approved": counts["approved"],
            "sent": counts["sent"],
            "as_of": utcnow().isoformat(),
            "approval_semantics": "INTERNAL_REVIEW_ONLY_NOT_SEND_AUTHORITY",
        }

    @staticmethod
    def _generate_sector_prospects(sector: str) -> list[dict[str, Any]]:
        return [
            {
                "lead_id": generate_id("sect"),
                "name": f"Synthetic operator persona — {sector}",
                "company": f"Synthetic {sector} research fixture",
                "sector": sector,
                "company_size": "medium",
                "icp_score": 0.45,
                "locale": "ar",
                "synthetic": True,
                "commercial_truth_state": "SYNTHETIC_RESEARCH_ONLY",
            },
            {
                "lead_id": generate_id("sect"),
                "name": f"Synthetic commercial persona — {sector}",
                "company": f"Synthetic {sector} research fixture",
                "sector": sector,
                "company_size": "large",
                "icp_score": 0.72,
                "locale": "en",
                "synthetic": True,
                "commercial_truth_state": "SYNTHETIC_RESEARCH_ONLY",
            },
        ]
