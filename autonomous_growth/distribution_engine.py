"""
Autonomous Distribution Engine — orchestrates lead scoring, product routing,
proposal generation, and sector campaign distribution.

محرك التوزيع المستقل — ينسق تقييم العملاء وتوجيه المنتجات وإنشاء العروض
وتوزيع الحملات القطاعية.
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
from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier
from core.logging import get_logger
from core.utils import generate_id, utcnow

log = get_logger(__name__)

# Minimum confidence for auto-selection (without founder approval)
_AUTO_SELECT_CONFIDENCE = 0.6


@dataclass
class DistributionEngineResult:
    """Full result of processing one lead through the distribution engine."""

    lead_id: str
    product_route: ProductRouteDecision | None = None
    proposal_draft: ProposalDraft | None = None
    content_scheduled: bool = False
    sector_campaign_url: str | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lead_id": self.lead_id,
            "product_route": self.product_route.to_dict() if self.product_route else None,
            "proposal_draft": self.proposal_draft.to_dict() if self.proposal_draft else None,
            "content_scheduled": self.content_scheduled,
            "sector_campaign_url": self.sector_campaign_url,
            "warnings": self.warnings,
        }


class AutonomousDistributionEngine:
    """
    Coordinates: lead ICP scoring → product routing → proposal drafting →
    content distribution queuing.

    Every proposal starts as 'pending_approval'. Founder must explicitly
    approve before any outbound communication occurs.

    ينسق: تقييم ICP → توجيه المنتج → مسوّدة العرض → جدولة المحتوى.
    كل عرض يبدأ بحالة 'pending_approval'. يجب على المؤسس الموافقة صراحةً
    قبل أي تواصل خارجي.
    """

    def __init__(self) -> None:
        self.router_agent = ProductRouterAgent()
        self.proposal_agent = ProposalSenderAgent()
        self.distribution_agent = DistributionAgent()
        self.log = log.bind(component="distribution_engine")

    # ── Primary entry point ────────────────────────────────────────

    async def process_lead(self, payload: dict[str, Any]) -> DistributionEngineResult:
        """
        Full pipeline for a single inbound lead.

        Steps:
          1. Extract / default ICP score
          2. Route to product via ProductRouterAgent
          3. Auto-select product if confidence >= threshold and no approval required
          4. Generate bilingual proposal draft (always pending_approval)
          5. Queue content distribution for the lead's sector

        Parameters
        ----------
        payload:
            Must contain at least one of: ``name``, ``company``. Optional keys:
            ``icp_score`` (float), ``sector`` (str), ``company_size`` (str),
            ``budget_signal`` (str), ``lead_id`` (str), ``locale`` (str).
        """
        lead_id = payload.get("lead_id") or generate_id("lead")
        result = DistributionEngineResult(lead_id=lead_id)

        # Step 1: ICP score
        icp_score: float = float(payload.get("icp_score", 0.4))
        sector: str = payload.get("sector", "general")
        company_size: str = payload.get("company_size", "medium")
        budget_signal: str | None = payload.get("budget_signal")
        locale: str = payload.get("locale", "ar")

        # Step 2: Product routing
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

        # Step 3: Confidence check
        if route.confidence < _AUTO_SELECT_CONFIDENCE:
            result.warnings.append(
                f"low_confidence_route: confidence={route.confidence:.2f} — "
                "manual review recommended before sending proposal"
            )

        if route.requires_founder_approval:
            result.warnings.append(
                f"founder_approval_required for tier={route.recommended_tier.value}"
            )

        # Step 4: Generate proposal draft (always pending_approval)
        try:
            draft = await self.proposal_agent.run(
                product=route.product,
                lead_profile=payload,
                locale=locale,
            )
            result.proposal_draft = draft
        except Exception as exc:
            self.log.warning("proposal_generation_failed", error=str(exc), lead_id=lead_id)
            result.warnings.append(f"proposal_generation_failed: {exc}")

        # Step 5: Queue content distribution for the sector
        try:
            from autonomous_growth.agents.content import ContentPiece
            # Create a lightweight synthetic content reference for scheduling purposes
            placeholder_content = ContentPiece(
                id=generate_id("cnt"),
                content_type="linkedin_post",
                channel="linkedin",
                locale=locale,
                topic=f"Dealix {route.product.name_en} — {sector} sector",
                title=f"Dealix {route.product.name_en}",
                body_markdown="",
                word_count=0,
            )
            await self.distribution_agent.run(
                content=placeholder_content,
                channels=["linkedin", "email"],
            )
            result.content_scheduled = True
        except Exception as exc:
            self.log.warning("content_distribution_failed", error=str(exc), lead_id=lead_id)
            result.warnings.append(f"content_distribution_queuing_failed: {exc}")

        self.log.info(
            "lead_processed",
            lead_id=lead_id,
            tier=route.recommended_tier.value,
            confidence=route.confidence,
            proposal_id=result.proposal_draft.id if result.proposal_draft else None,
            warnings=len(result.warnings),
        )
        return result

    # ── Sector campaigns ───────────────────────────────────────────

    async def run_sector_distribution(
        self,
        sector: str,
        channels: list[str],
    ) -> list[DistributionEngineResult]:
        """
        Run a sector-wide campaign and route each identified prospect to the
        right product tier.

        In practice this creates synthetic prospect placeholders for the sector;
        a real integration would pull from the lead inbox or CRM.

        Parameters
        ----------
        sector:
            Saudi sector name (e.g. "healthcare", "retail", "logistics").
        channels:
            Distribution channels to schedule content on.
        """
        self.log.info("sector_campaign_start", sector=sector, channels=channels)

        # Generate representative prospect profiles for the sector
        prospects = self._generate_sector_prospects(sector)

        tasks = [self.process_lead(prospect) for prospect in prospects]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        results: list[DistributionEngineResult] = []
        for r in raw_results:
            if isinstance(r, Exception):
                err_result = DistributionEngineResult(
                    lead_id=generate_id("err"),
                    warnings=[f"sector_prospect_failed: {r}"],
                )
                results.append(err_result)
            else:
                results.append(r)  # type: ignore[arg-type]

        self.log.info(
            "sector_campaign_complete",
            sector=sector,
            prospects=len(prospects),
            results=len(results),
        )
        return results

    # ── Approval queue helpers ─────────────────────────────────────

    async def get_pending_approvals(self) -> list[ProposalDraft]:
        """Return all drafts with status 'pending_approval' from the queue."""
        all_drafts = _read_queue()
        return [d for d in all_drafts if d.status == "pending_approval"]

    async def approve_proposal(self, proposal_id: str) -> bool:
        """
        Update the status of a draft to 'approved' in the JSONL queue.

        Returns True if the draft was found and updated, False otherwise.
        """
        all_drafts = _read_queue()
        updated = False
        for draft in all_drafts:
            if draft.id == proposal_id and draft.status == "pending_approval":
                draft.status = "approved"
                updated = True
                break

        if updated:
            _rewrite_queue(all_drafts)
            self.log.info("proposal_approved", proposal_id=proposal_id)
        else:
            self.log.warning(
                "proposal_approve_not_found",
                proposal_id=proposal_id,
            )
        return updated

    # ── Stats ──────────────────────────────────────────────────────

    def get_stats(self) -> dict[str, Any]:
        """Return aggregate stats from the proposal queue."""
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
        }

    # ── Private helpers ────────────────────────────────────────────

    @staticmethod
    def _generate_sector_prospects(sector: str) -> list[dict[str, Any]]:
        """
        Create a small set of representative prospect payloads for a sector.
        In production these would come from lead-inbox / CRM queries.
        """
        base_profiles: list[dict[str, Any]] = [
            {
                "lead_id": generate_id("sect"),
                "name": f"مدير العمليات — قطاع {sector}",
                "company": f"شركة {sector} السعودية",
                "sector": sector,
                "company_size": "medium",
                "icp_score": 0.45,
                "locale": "ar",
            },
            {
                "lead_id": generate_id("sect"),
                "name": f"Head of Sales — {sector} sector",
                "company": f"{sector.title()} Corp",
                "sector": sector,
                "company_size": "large",
                "icp_score": 0.72,
                "locale": "en",
            },
        ]
        return base_profiles
