"""Execute 15 Plans — without stopping, comprehensive, all aspects."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial.master_15_plans import PLANS, Master15Executor
from dealix.commercial.economic_cell_registry import EconomicCellRegistry
from dealix.commercial.probability_engine import ProbabilityVector, ProbBand
from dealix.commercial.portfolio_bets import PortfolioBets, EconomicBet
from dealix.commercial.delivery_kit import DeliveryFactory, DeliveryKit, DeliveryStage
from dealix.commercial.proof_asset_factory import ProofAssetFactory, AssetType
from dealix.commercial.saas_foundation import SaaSControlPlane, TenantTier
from dealix.commercial.content_factory import ContentFactory
from pathlib import Path
import tempfile
import uuid
from dealix.commercial.economic_cell import EconomicCell, Identity, Market, Sector, Buyer, BuyerGroup, Problem, ProblemClass, Value, Offer, Monetization, MonetizationRail, Distribution, DistributionRail, Procurement, Execution, Evidence, Economics, Risk, Portfolio, Proof, LifecycleState

class Execute15Plans:
    def execute_all(self) -> dict[str, Any]:
        results = []
        # Shared registries
        reg = EconomicCellRegistry(storage_path=Path(tempfile.mktemp(suffix=".jsonl")))
        pb = PortfolioBets()
        df = DeliveryFactory()
        paf = ProofAssetFactory()
        cp = SaaSControlPlane()
        cf = ContentFactory()
        for plan in PLANS:
            # 1. Generate cell for plan
            # Map sector string to Sector enum (fallback to technology)
            try:
                sector = Sector(plan.sector)
            except Exception:
                sector = Sector.TECHNOLOGY_SAAS_SI
            # Create cell
            now = datetime.now(UTC).isoformat()
            cell = EconomicCell(
                identity=Identity(cell_id=str(uuid.uuid4()), canonical_name=f"plan_{plan.plan_id}_{sector.value}", version=1, created_at=now, updated_at=now),
                market=Market(sector=sector),
                buyer=Buyer(buyer_group=BuyerGroup.CEO),
                problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE),
                value=Value(),
                offer=Offer(offer_family=plan.offer),
                monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT),
                distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND),
                procurement=Procurement(),
                execution=Execution(),
                evidence=Evidence(evidence_level="L1_public_source"),
                economics=Economics(probability_adjusted_value=plan.expected_value_range),
                risk=Risk(),
                portfolio=Portfolio(lifecycle_state=LifecycleState.CANDIDATE_DEEP, deep_wip_slot=False),
                proof=Proof(),
            )
            reg.create(cell)
            # 2. Probability & Bet
            pv = ProbabilityVector(p_problem_real=ProbBand.MEDIUM, p_quote_accepted=ProbBand.MEDIUM)
            bet = EconomicBet(bet_id=f"bet_{plan.plan_id}", economic_cell_id=cell.identity.cell_id, sector=plan.sector, buyer=plan.buyer, problem=plan.problem, offer=plan.offer, channel=plan.channel, hypothesis=plan.title_en, expected_gross_profit_sar=10000, time_to_cash_days=plan.time_to_cash_days, probability_vector=pv)
            pb.add(bet)
            # 3. Try DeepWIP if slot A/B and can promote (only 3 will succeed, rest will be WATCH)
            promoted = False
            if plan.deep_wip_slot in ("A","B") and pb.can_promote_to_deep():
                # Promote via registry if possible
                if reg.claim_deep_wip_slot(cell.identity.cell_id):
                    bet.state = "active_deep"
                    promoted = True
            # 4. Delivery
            kit = DeliveryKit(kit_id=f"kit_{plan.plan_id}", cell_id=cell.identity.cell_id, scope=plan.offer, acceptance_criteria="proof pack", baseline="unknown")
            df.create(kit)
            kit.advance(DeliveryStage.BASELINE)
            # 5. Proof
            asset = paf.create_from_delivery(kit.kit_id, AssetType.DIAGNOSTIC, f"Asset for {plan.plan_id}", f"proof_{plan.plan_id}")
            # 6. Content
            atoms = cf.atomize({"proof_id": asset.asset_id, "sector": plan.sector, "problem": plan.problem, "intervention": plan.offer, "result": "revived", "evidence_ref": plan.evidence_ref})
            # 7. SaaS tenant for plan
            tenant = cp.create_tenant(f"Tenant-{plan.plan_id}", plan.sector, TenantTier.STARTER)
            results.append({
                "plan_id": plan.plan_id,
                "sector": plan.sector,
                "promoted": promoted,
                "bet_state": bet.state,
                "delivery_stage": kit.stage.value,
                "asset": asset.asset_id,
                "content_atoms": len(atoms),
                "tenant": tenant.tenant_id,
                "channel": plan.channel,
            })
        return {
            "total": len(PLANS),
            "results": results,
            "active_deep": len([r for r in results if r["promoted"]]),
            "watch": len([r for r in results if not r["promoted"]]),
            "tenants": len(cp.tenants),
            "assets": len(paf.assets),
            "cells": len(reg.list_all()),
            "generated_at": datetime.now(UTC).isoformat(),
        }

__all__ = ["Execute15Plans"]
