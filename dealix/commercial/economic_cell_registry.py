"""Economic Cell Registry — sparse materialization of 500+ addressable cells.

Uses templates, canonical dimensions, and evidence-driven activation.
No 500 projects, no 500 agents. Just addressable economic movements.
"""

from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import hashlib

from dealix.commercial.economic_cell import (
    BuyerGroup,
    CellTemplate,
    DEFAULT_TEMPLATES,
    DistributionRail,
    EconomicCell,
    EvidenceLevel,
    KillTrigger,
    LifecycleState,
    MonetizationRail,
    ProblemClass,
    PromotionGate,
    Sector,
    UNKNOWN,
)


class EconomicCellRegistry:
    """Thread-safe registry with sparse materialization and template expansion."""

    def __init__(self, storage_path: Path | None = None) -> None:
        self._lock = threading.RLock()
        self._cells: dict[str, EconomicCell] = {}
        self._templates: dict[str, CellTemplate] = {t.template_id: t for t in DEFAULT_TEMPLATES}
        self._storage_path = storage_path or Path("data/economic_cells.jsonl")
        self._load()

    # ─── Core CRUD ──────────────────────────────────────────────────────

    def create(self, cell: EconomicCell) -> EconomicCell:
        with self._lock:
            if cell.identity.cell_id in self._cells:
                raise ValueError(f"cell_id already exists: {cell.identity.cell_id}")
            self._cells[cell.identity.cell_id] = cell
            self._persist_cell(cell)
        return cell

    def get(self, cell_id: str) -> EconomicCell | None:
        with self._lock:
            return self._cells.get(cell_id)

    def update(self, cell: EconomicCell) -> EconomicCell:
        with self._lock:
            if cell.identity.cell_id not in self._cells:
                raise ValueError(f"cell not found: {cell.identity.cell_id}")
            # Increment version
            new_identity = cell.identity.model_copy(update={
                "version": cell.identity.version + 1,
                "updated_at": datetime.now(UTC).isoformat(),
            })
            updated = cell.model_copy(update={"identity": new_identity})
            self._cells[cell.identity.cell_id] = updated
            self._persist_cell(updated)
        return updated

    def delete(self, cell_id: str) -> bool:
        with self._lock:
            if cell_id in self._cells:
                del self._cells[cell_id]
                return True
            return False

    def list_all(self) -> list[EconomicCell]:
        with self._lock:
            return list(self._cells.values())

    def list_by_state(self, state: LifecycleState) -> list[EconomicCell]:
        with self._lock:
            return [c for c in self._cells.values() if c.portfolio.lifecycle_state == state]

    def list_active_deep(self) -> list[EconomicCell]:
        return self.list_by_state(LifecycleState.ACTIVE_DEEP)

    def count_active_deep(self) -> int:
        return len(self.list_active_deep())

    # ─── Template-based Generation ──────────────────────────────────────

    def register_template(self, template: CellTemplate) -> None:
        with self._lock:
            self._templates[template.template_id] = template

    def generate_from_template(
        self,
        template_id: str,
        *,
        canonical_name: str,
        overrides: dict[str, Any] | None = None,
    ) -> EconomicCell:
        with self._lock:
            template = self._templates.get(template_id)
            if not template:
                raise ValueError(f"template not found: {template_id}")

            base = self._template_to_cell(template, canonical_name)
            if overrides:
                base = self._apply_overrides(base, overrides)
            return self.create(base)

    def _template_to_cell(self, template: CellTemplate, canonical_name: str) -> EconomicCell:
        from dealix.commercial.economic_cell import (
            Buyer,
            Distribution,
            Economics,
            Evidence,
            Execution,
            Identity,
            Market,
            Monetization,
            Offer,
            Portfolio,
            Problem,
            Procurement,
            Proof,
            Risk,
            Value,
        )

        now = datetime.now(UTC).isoformat()
        cell_id = f"cell_{template.template_id}_{hashlib.md5(canonical_name.encode()).hexdigest()[:8]}"

        return EconomicCell(
            identity=Identity(cell_id=cell_id, canonical_name=canonical_name, version=1, created_at=now, updated_at=now),
            market=Market(sector=template.sector),
            buyer=Buyer(buyer_group=template.buyer_group),
            problem=Problem(problem_class=template.problem_class),
            value=Value(),
            offer=Offer(offer_family=template.name),
            monetization=Monetization(monetization_rail=template.monetization_rail),
            distribution=Distribution(distribution_rail=template.distribution_rail),
            procurement=Procurement(procurement_rail=template.procurement_rail),
            execution=Execution(
                capability_dependencies=list(template.capability_tags),
                reusable_factory_dependencies=list(template.factory_dependencies),
            ),
            evidence=Evidence(evidence_level=template.default_evidence_level),
            economics=Economics(),
            risk=Risk(),
            portfolio=Portfolio(lifecycle_state=template.default_lifecycle),
            proof=Proof(),
        )

    def _apply_overrides(self, cell: EconomicCell, overrides: dict[str, Any]) -> EconomicCell:
        dump = cell.model_dump(mode="json")
        self._deep_merge(dump, overrides)
        return EconomicCell(**dump)

    @staticmethod
    def _deep_merge(base: dict[str, Any], updates: dict[str, Any]) -> None:
        for k, v in updates.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                EconomicCellRegistry._deep_merge(base[k], v)
            else:
                base[k] = v

    # ─── Bulk Generation (Sector × Buyer × Problem × Rail) ─────────────

    def generate_addressable_universe(
        self,
        sectors: list[Sector] | None = None,
        buyer_groups: list[str] | None = None,
        problem_classes: list[str] | None = None,
        monetization_rails: list[str] | None = None,
        distribution_rails: list[str] | None = None,
        max_cells: int = 500,
    ) -> list[EconomicCell]:
        """Generate candidate cells from dimension cross-product (sparse, evidence-first)."""
        sectors = sectors or list(Sector)
        buyer_groups = buyer_groups or [g.value for g in BuyerGroup]
        problem_classes = problem_classes or [p.value for p in ProblemClass]
        monetization_rails = monetization_rails or [m.value for m in MonetizationRail]
        distribution_rails = distribution_rails or [d.value for d in DistributionRail]

        generated: list[EconomicCell] = []
        for sector in sectors:
            for buyer in buyer_groups:
                for problem in problem_classes:
                    for monetization in monetization_rails:
                        for distribution in distribution_rails:
                            if len(generated) >= max_cells:
                                return generated
                            try:
                                cell = self._generate_candidate(
                                    sector, buyer, problem, monetization, distribution
                                )
                                if cell.identity.cell_id not in self._cells:
                                    generated.append(cell)
                            except Exception:
                                continue
        return generated

    def _generate_candidate(
        self,
        sector: Sector,
        buyer: str,
        problem: str,
        monetization: str,
        distribution: str,
    ) -> EconomicCell:
        from dealix.commercial.economic_cell import (
            Buyer,
            Distribution,
            Economics,
            Evidence,
            Execution,
            Identity,
            Market,
            Monetization,
            Offer,
            Portfolio,
            Problem,
            Procurement,
            Proof,
            Risk,
            Value,
            BuyerGroup,
            MonetizationRail,
            DistributionRail,
        )

        key = f"{sector.value}|{buyer}|{problem}|{monetization}|{distribution}"
        cell_id = f"cell_{hashlib.sha256(key.encode()).hexdigest()[:12]}"
        name = f"{sector.value}:{buyer}:{problem}:{monetization}:{distribution}"

        return EconomicCell(
            identity=Identity(
                cell_id=cell_id,
                canonical_name=name,
                version=1,
                created_at=datetime.now(UTC).isoformat(),
                updated_at=datetime.now(UTC).isoformat(),
            ),
            market=Market(sector=sector),
            buyer=Buyer(buyer_group=BuyerGroup(buyer)),
            problem=Problem(problem_class=ProblemClass(problem)),
            value=Value(),
            offer=Offer(offer_family=f"{sector.value}_{problem}"),
            monetization=Monetization(monetization_rail=MonetizationRail(monetization)),
            distribution=Distribution(distribution_rail=DistributionRail(distribution)),
            procurement=Procurement(),
            execution=Execution(),
            evidence=Evidence(),
            economics=Economics(),
            risk=Risk(),
            portfolio=Portfolio(),
            proof=Proof(),
        )

    # ─── Evidence-Driven Activation ────────────────────────────────────

    def activate_with_evidence(
        self,
        cell_id: str,
        evidence_refs: list[str],
        evidence_level: EvidenceLevel,
        next_action: str,
        assigned_agent: str,
    ) -> EconomicCell:
        cell = self.get(cell_id)
        if not cell:
            raise ValueError(f"cell not found: {cell_id}")

        updated = cell.model_copy(update={
            "evidence": cell.evidence.model_copy(update={
                "evidence_level": evidence_level,
                "evidence_sources": list(set(cell.evidence.evidence_sources + evidence_refs)),
            }),
            "portfolio": cell.portfolio.model_copy(update={
                "lifecycle_state": LifecycleState.VALIDATE,
                "next_action": next_action,
                "assigned_agent": assigned_agent,
            }),
        })
        return self.update(updated)

    # ─── Promotion/Kill Gates ──────────────────────────────────────────

    def evaluate_promotion(self, cell_id: str, gate: PromotionGate, evidence: dict[str, Any]) -> bool:
        """Check if a promotion gate is satisfied. Returns True if gate passes."""
        cell = self.get(cell_id)
        if not cell:
            return False

        checks = {
            PromotionGate.GATE_1_REAL_SIGNAL: lambda: bool(evidence.get("problem_evidence")),
            PromotionGate.GATE_2_BUYER: lambda: bool(cell.buyer.economic_buyer or cell.buyer.champion_role),
            PromotionGate.GATE_3_ECONOMIC_PAIN: lambda: cell.problem.measurable_loss_type != UNKNOWN,
            PromotionGate.GATE_4_ACCESS: lambda: cell.distribution.relationship_requirement or evidence.get("warm_path"),
            PromotionGate.GATE_5_PROCUREMENT: lambda: cell.procurement.procurement_rail != ProcurementRail.GOVERNMENT_PROCUREMENT or evidence.get("vendor_registered"),
            PromotionGate.GATE_6_DELIVERY: lambda: bool(cell.execution.capability_dependencies),
            PromotionGate.GATE_7_ECONOMICS: lambda: cell.economics.probability_adjusted_value != UNKNOWN,
            PromotionGate.GATE_8_PROOF: lambda: cell.proof.proof_strength != UNKNOWN,
            PromotionGate.GATE_9_REPEATABILITY: lambda: bool(cell.execution.reusable_factory_dependencies),
            PromotionGate.GATE_10_RISK: lambda: cell.risk.regulatory_risk != "high" and cell.risk.cybersecurity_risk != "high",
        }
        return checks.get(gate, lambda: False)()

    def promote(self, cell_id: str, new_state: LifecycleState, gate: PromotionGate, evidence: dict[str, Any]) -> EconomicCell:
        if not self.evaluate_promotion(cell_id, gate, evidence):
            raise ValueError(f"promotion gate {gate} not satisfied for {cell_id}")

        cell = self.get(cell_id)
        if not cell:
            raise ValueError(f"cell not found: {cell_id}")

        next_gate = self._next_gate(gate)
        updated = cell.model_copy(update={
            "portfolio": cell.portfolio.model_copy(update={
                "lifecycle_state": new_state,
                "promotion_gate": next_gate,
            }),
        })
        return self.update(updated)

    def kill(self, cell_id: str, trigger: KillTrigger, reason: str) -> EconomicCell:
        cell = self.get(cell_id)
        if not cell:
            raise ValueError(f"cell not found: {cell_id}")

        updated = cell.model_copy(update={
            "portfolio": cell.portfolio.model_copy(update={
                "lifecycle_state": LifecycleState.KILLED,
                "kill_gate": trigger,
                "stop_loss": reason,
            }),
        })
        return self.update(updated)

    def _next_gate(self, current: PromotionGate) -> PromotionGate | None:
        gates = list(PromotionGate)
        idx = gates.index(current)
        return gates[idx + 1] if idx + 1 < len(gates) else None

    # ─── Deep WIP Enforcement ──────────────────────────────────────────

    def claim_deep_wip_slot(self, cell_id: str) -> bool:
        """Attempt to claim a deep WIP slot. Returns True if successful."""
        with self._lock:
            active_deep = self.list_active_deep()
            if len(active_deep) >= 3:
                return False
            cell = self._cells.get(cell_id)
            if not cell:
                return False
            if cell.portfolio.lifecycle_state != LifecycleState.CANDIDATE_DEEP:
                return False
            updated = cell.model_copy(update={
                "portfolio": cell.portfolio.model_copy(update={
                    "lifecycle_state": LifecycleState.ACTIVE_DEEP,
                    "deep_wip_slot": True,
                }),
            })
            self._cells[cell_id] = updated
            self._persist_cell(updated)
            return True

    def release_deep_wip_slot(self, cell_id: str) -> bool:
        with self._lock:
            cell = self._cells.get(cell_id)
            if not cell or not cell.portfolio.deep_wip_slot:
                return False
            updated = cell.model_copy(update={
                "portfolio": cell.portfolio.model_copy(update={
                    "deep_wip_slot": False,
                }),
            })
            self._cells[cell_id] = updated
            self._persist_cell(updated)
            return True

    # ─── Persistence ────────────────────────────────────────────────────

    def _persist_cell(self, cell: EconomicCell) -> None:
        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            line = cell.model_dump_json() + "\n"
            with self._storage_path.open("a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass  # Best effort

    def _load(self) -> None:
        if not self._storage_path.exists():
            return
        try:
            with self._storage_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cell = EconomicCell.model_validate_json(line)
                        self._cells[cell.identity.cell_id] = cell
                    except Exception:
                        continue
        except Exception:
            pass

    # ─── Export / Reporting ────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_cells": len(self._cells),
                "active_deep": self.count_active_deep(),
                "by_state": {
                    state.value: len(self.list_by_state(state))
                    for state in LifecycleState
                },
                "cells": [c.model_dump(mode="json") for c in self._cells.values()],
            }


# ─── Singleton Access ──────────────────────────────────────────────────

_DEFAULT_REGISTRY: EconomicCellRegistry | None = None
_REGISTRY_LOCK = threading.Lock()


def get_default_registry() -> EconomicCellRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        with _REGISTRY_LOCK:
            if _DEFAULT_REGISTRY is None:
                _DEFAULT_REGISTRY = EconomicCellRegistry()
    return _DEFAULT_REGISTRY


def reset_registry_for_tests(registry: EconomicCellRegistry | None = None) -> EconomicCellRegistry | None:
    global _DEFAULT_REGISTRY
    with _REGISTRY_LOCK:
        _DEFAULT_REGISTRY = registry
    return _DEFAULT_REGISTRY


__all__ = [
    "EconomicCellRegistry",
    "get_default_registry",
    "reset_registry_for_tests",
]
