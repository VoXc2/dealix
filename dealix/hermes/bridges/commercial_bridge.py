"""CommercialBridge — connects Hermes agents to dealix/commercial/ business logic.

Each method tries to call the real commercial module first. If unavailable
(missing env var, import error, or empty input), it falls back gracefully
so Hermes agents stay operational in mock/offline mode.
"""

from __future__ import annotations

from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class CommercialBridge:
    """Singleton bridge to dealix/commercial/ modules."""

    _instance: CommercialBridge | None = None

    @classmethod
    def instance(cls) -> CommercialBridge:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Diagnostic Engine
    # ------------------------------------------------------------------

    async def run_diagnostic(
        self,
        company_name: str,
        sector: str = "b2b_services",
        pain_points: list[str] | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        """Run the commercial DiagnosticEngine and return structured report dict."""
        try:
            from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

            req = DiagnosticRequest(
                company_name=company_name,
                sector=sector,
                pain_points=pain_points or [],
                notes=notes,
            )
            engine = DiagnosticEngine()
            report = engine.generate(req)
            logger.info("commercial_bridge_diagnostic", company=company_name, sector=sector)
            return {
                "source": "commercial_diagnostic_engine",
                "company_name": company_name,
                "sector": sector,
                "report": report.to_dict(),
                "markdown": report.markdown if hasattr(report, "markdown") else "",
            }
        except Exception as exc:
            logger.warning("commercial_bridge_diagnostic_fallback", error=str(exc))
            return {
                "source": "mock_fallback",
                "company_name": company_name,
                "sector": sector,
                "error": str(exc),
                "gaps": [
                    f"Data quality gap detected for {company_name}",
                    "Lead scoring not implemented",
                    "Revenue attribution missing",
                ],
                "quick_wins": [
                    "Implement CRM data quality score",
                    "Add ICP scoring to top 20 accounts",
                    "Set up revenue tracking dashboard",
                ],
                "recommended_offer": "Revenue Intelligence Sprint (499 SAR)",
                "roi_estimate_sar": 50000,
            }

    # ------------------------------------------------------------------
    # Sprint Orchestrator
    # ------------------------------------------------------------------

    async def run_sprint(
        self,
        engagement_id: str,
        customer_id: str,
        customer_name: str = "",
        sector: str = "b2b_services",
        sources: list[dict[str, Any]] | None = None,
        rows: list[dict[str, Any]] | None = None,
        pain_summary: str = "",
        founder_approved: bool = False,
    ) -> dict[str, Any]:
        """Run all 7 days of the commercial SprintOrchestrator."""
        try:
            from dealix.commercial.sprint_orchestrator import SprintContext, SprintOrchestrator

            ctx = SprintContext(
                engagement_id=engagement_id,
                customer_id=customer_id,
                customer_name=customer_name,
                sector=sector,
                sources=sources or [],
                rows=rows or [],
                pain_summary=pain_summary,
                founder_approved=founder_approved,
            )
            orchestrator = SprintOrchestrator()
            day_results = orchestrator.run_all(ctx)
            logger.info(
                "commercial_bridge_sprint",
                engagement_id=engagement_id,
                customer=customer_name,
                days=len(day_results),
            )
            return {
                "source": "commercial_sprint_orchestrator",
                "engagement_id": engagement_id,
                "customer_name": customer_name,
                "days_completed": len(day_results),
                "day_results": [r.to_dict() if hasattr(r, "to_dict") else vars(r) for r in day_results],
            }
        except Exception as exc:
            logger.warning("commercial_bridge_sprint_fallback", error=str(exc))
            return {
                "source": "mock_fallback",
                "engagement_id": engagement_id,
                "customer_name": customer_name,
                "error": str(exc),
                "days_completed": 7,
                "day_results": [
                    {"day": i, "status": "mock", "summary": f"Day {i} completed (mock mode)"}
                    for i in range(1, 8)
                ],
            }

    # ------------------------------------------------------------------
    # Proof Pack Builder
    # ------------------------------------------------------------------

    async def build_proof_pack(
        self,
        account_id: str,
        company_name: str,
        events: list[dict[str, Any]] | None = None,
        approved_by_founder: bool = False,
        customer_consent: bool = False,
    ) -> dict[str, Any]:
        """Build a proof pack using the commercial ProofPackBuilder."""
        try:
            from dealix.commercial.proof_builder import (
                ProofBuildRequest,
                ProofEvent,
                ProofPackBuilder,
            )

            proof_events = [ProofEvent(**e) for e in (events or [])]
            req = ProofBuildRequest(
                account_id=account_id,
                company_name=company_name,
                events=proof_events,
                approved_by_founder=approved_by_founder,
                customer_consent=customer_consent,
            )
            builder = ProofPackBuilder()
            doc = builder.build(req)
            logger.info("commercial_bridge_proof", account_id=account_id, company=company_name)
            return {
                "source": "commercial_proof_builder",
                "account_id": account_id,
                "company_name": company_name,
                "proof_pack": doc.model_dump() if hasattr(doc, "model_dump") else vars(doc),
            }
        except Exception as exc:
            logger.warning("commercial_bridge_proof_fallback", error=str(exc))
            return {
                "source": "mock_fallback",
                "account_id": account_id,
                "company_name": company_name,
                "error": str(exc),
                "proof_pack": {
                    "pack_id": f"PROOF-{account_id[:8].upper()}",
                    "level": "L0",
                    "score": 0.0,
                    "note": "No proof events provided — collect evidence first",
                },
            }

    # ------------------------------------------------------------------
    # Upsell Engine
    # ------------------------------------------------------------------

    async def check_upsell_eligibility(
        self,
        account_id: str,
        company_name: str,
        proof_event_count: int = 0,
        current_tier: str = "",
    ) -> dict[str, Any]:
        """Check upsell eligibility using the commercial UpsellEngine."""
        try:
            from dealix.commercial.upsell_engine import UpsellEngine

            engine = UpsellEngine()
            result = engine.check(
                account_id=account_id,
                company_name=company_name,
                proof_event_count=proof_event_count,
            )
            logger.info(
                "commercial_bridge_upsell",
                account_id=account_id,
                eligible=result.is_eligible,
                tier=result.recommended_tier,
            )
            return {
                "source": "commercial_upsell_engine",
                "account_id": account_id,
                "company_name": company_name,
                "is_eligible": result.is_eligible,
                "recommended_tier": result.recommended_tier,
                "reason_ar": result.reason_ar,
                "reason_en": result.reason_en,
                "proposal_draft_ar": result.proposal_draft_ar,
                "proposal_draft_en": result.proposal_draft_en,
                "approval_status": result.approval_status,
            }
        except Exception as exc:
            logger.warning("commercial_bridge_upsell_fallback", error=str(exc))
            eligible = proof_event_count >= 3
            return {
                "source": "mock_fallback",
                "account_id": account_id,
                "company_name": company_name,
                "error": str(exc),
                "is_eligible": eligible,
                "recommended_tier": "managed_ops_2999" if eligible else "",
                "reason_en": f"{'Eligible' if eligible else 'Not yet eligible'} based on {proof_event_count} proof events",
                "approval_status": "approval_required",
            }

    # ------------------------------------------------------------------
    # Market Intelligence
    # ------------------------------------------------------------------

    async def get_market_intelligence(
        self,
        sector: str,
        city: str = "Riyadh",
    ) -> dict[str, Any]:
        """Get Saudi market intelligence from the existing market intel module."""
        try:
            from dealix.commercial.market_intelligence import (
                MarketIntelligenceEngine,  # type: ignore[import]
            )
            engine = MarketIntelligenceEngine()
            result = engine.get_sector_intel(sector=sector, city=city)
            logger.info("commercial_bridge_market_intel", sector=sector, city=city)
            return {"source": "commercial_market_intelligence", "sector": sector, "city": city, "data": result}
        except Exception as exc:
            logger.debug("commercial_bridge_market_intel_fallback", error=str(exc))
            return {
                "source": "mock_fallback",
                "sector": sector,
                "city": city,
                "saudi_market_size_sar": 5_000_000_000,
                "growth_rate_pct": 8.5,
                "vision_2030_alignment": "high",
                "key_opportunities": [
                    f"Vision 2030 digitalisation mandate in {sector}",
                    "SME growth programme (Monshaat) funding available",
                    "NEOM and giga-project supply chain opportunities",
                ],
            }


__all__ = ["CommercialBridge"]
