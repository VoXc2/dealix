"""Deep WIP Enforcer — hard constraint ACTIVE_DEEP ≤ 3.

Enforced at:
- Application/service layer
- Scheduler
- President Command
- Workflow runner
- Tests
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.commercial.economic_cell import (
    EconomicCell,
    LifecycleState,
)
from dealix.commercial.economic_cell_registry import EconomicCellRegistry


DEEP_WIP_MAX = 3


@dataclass
class WipSlot:
    cell_id: str
    claimed_at: str
    claimed_by: str
    expected_release: str | None = None


class DeepWipEnforcer:
    """Enforces the ACTIVE_DEEP ≤ 3 invariant."""

    def __init__(self, registry: EconomicCellRegistry) -> None:
        self.registry = registry
        self._slots: dict[str, WipSlot] = {}  # cell_id -> WipSlot
        self._sync_from_registry()

    def _sync_from_registry(self) -> None:
        active = self.registry.list_active_deep()
        for cell in active:
            if cell.identity.cell_id not in self._slots:
                self._slots[cell.identity.cell_id] = WipSlot(
                    cell_id=cell.identity.cell_id,
                    claimed_at=cell.identity.updated_at,
                    claimed_by="registry_sync",
                )

    def current_count(self) -> int:
        return len(self._slots)

    def available_slots(self) -> int:
        return max(0, DEEP_WIP_MAX - self.current_count())

    def is_full(self) -> bool:
        return self.current_count() >= DEEP_WIP_MAX

    def claim_slot(self, cell_id: str, claimed_by: str = "system") -> bool:
        """Attempt to claim a deep WIP slot for a cell."""
        if self.is_full():
            return False

        cell = self.registry.get(cell_id)
        if not cell:
            return False

        if cell.portfolio.lifecycle_state != LifecycleState.CANDIDATE_DEEP:
            return False

        # Claim in registry
        success = self.registry.claim_deep_wip_slot(cell_id)
        if success:
            self._slots[cell_id] = WipSlot(
                cell_id=cell_id,
                claimed_at=datetime.now(UTC).isoformat(),
                claimed_by=claimed_by,
            )
        return success

    def release_slot(self, cell_id: str) -> bool:
        """Release a deep WIP slot."""
        if cell_id not in self._slots:
            return False

        success = self.registry.release_deep_wip_slot(cell_id)
        if success:
            del self._slots[cell_id]
        return success

    def force_release_slot(self, cell_id: str) -> bool:
        """Force release (e.g., for kill/demote)."""
        if cell_id in self._slots:
            self.registry.release_deep_wip_slot(cell_id)
            del self._slots[cell_id]
            return True
        return False

    def get_occupants(self) -> list[WipSlot]:
        return list(self._slots.values())

    def can_promote_to_deep(self) -> bool:
        return self.available_slots() > 0

    def demote_lowest_priority(self, ranked_cells: list[EconomicCell]) -> EconomicCell | None:
        """Demote the lowest priority ACTIVE_DEEP cell to make room."""
        active = self.registry.list_active_deep()
        if not active:
            return None

        # Find lowest priority among active deep
        active_ids = {c.identity.cell_id for c in active}
        ranked_active = [c for c in ranked_cells if c.identity.cell_id in active_ids]

        if not ranked_active:
            return None

        # Demote the last one (lowest priority)
        victim = ranked_active[-1]
        return self.registry.transition(
            victim,
            LifecycleState.CANDIDATE_DEEP,
            notes="Demoted to make room for higher priority deep work",
        )

    def status(self) -> dict[str, Any]:
        return {
            "max_slots": DEEP_WIP_MAX,
            "current_count": self.current_count(),
            "available_slots": self.available_slots(),
            "is_full": self.is_full(),
            "occupants": [
                {
                    "cell_id": slot.cell_id,
                    "claimed_at": slot.claimed_at,
                    "claimed_by": slot.claimed_by,
                }
                for slot in self.get_occupants()
            ],
        }


# ─── Integration with President Command ────────────────────────────────


@dataclass
class DeepWipPolicy:
    """Policy for deep WIP management."""

    max_slots: int = DEEP_WIP_MAX
    auto_demote_on_full: bool = True
    require_explicit_approval_for_4th: bool = True
    stop_loss_on_blocked: bool = True


class PresidentWipController:
    """President Command integration for deep WIP control."""

    def __init__(self, enforcer: DeepWipEnforcer, policy: DeepWipPolicy | None = None) -> None:
        self.enforcer = enforcer
        self.policy = policy or DeepWipPolicy()

    def evaluate_promotion_request(
        self,
        cell: EconomicCell,
        dispatcher_ranked: list[EconomicCell],
    ) -> dict[str, Any]:
        """Evaluate if a cell can be promoted to ACTIVE_DEEP."""
        if cell.portfolio.lifecycle_state != LifecycleState.CANDIDATE_DEEP:
            return {
                "allowed": False,
                "reason": f"Cell not in CANDIDATE_DEEP state: {cell.portfolio.lifecycle_state}",
            }

        if self.enforcer.can_promote_to_deep():
            return {
                "allowed": True,
                "reason": "Slot available",
                "slot_number": self.enforcer.current_count() + 1,
            }

        if not self.policy.auto_demote_on_full:
            return {
                "allowed": False,
                "reason": f"All {DEEP_WIP_MAX} deep WIP slots occupied. Auto-demote disabled.",
                "requires_explicit_approval": True,
            }

        # Find demotion candidate
        victim = self.enforcer.demote_lowest_priority(dispatcher_ranked)
        if victim:
            return {
                "allowed": True,
                "reason": f"Will demote {victim.identity.cell_id} to make room",
                "demotion_candidate": victim.identity.cell_id,
                "requires_approval": self.policy.require_explicit_approval_for_4th,
            }

        return {
            "allowed": False,
            "reason": "No suitable demotion candidate found",
        }

    def execute_promotion(
        self,
        cell: EconomicCell,
        dispatcher_ranked: list[EconomicCell],
        approved_by: str = "president",
    ) -> tuple[bool, EconomicCell | None, str]:
        """Execute promotion with demotion if needed."""
        eval_result = self.evaluate_promotion_request(cell, dispatcher_ranked)

        if not eval_result["allowed"]:
            return False, None, eval_result["reason"]

        # Check if demotion needed
        if eval_result.get("demotion_candidate"):
            victim_id = eval_result["demotion_candidate"]
            victim = self.registry.get(victim_id)
            if victim:
                self.enforcer.force_release_slot(victim_id)
                # Demote victim
                from dealix.commercial.portfolio_state_machine import TransitionReason
                victim = self.registry.transition(
                    victim,
                    LifecycleState.CANDIDATE_DEEP,
                    notes=f"Demoted for {cell.identity.cell_id}",
                )
                # Update registry (assuming registry has update method)
                # This would need registry.update(victim)

        # Claim slot for new cell
        claimed = self.enforcer.claim_slot(cell.identity.cell_id, approved_by)
        if not claimed:
            return False, None, "Failed to claim slot"

        # Promote cell
        from dealix.commercial.portfolio_state_machine import TransitionReason
        updated = self.registry.transition(
            cell,
            LifecycleState.ACTIVE_DEEP,
            reason=TransitionReason.WIP_SLOT_CLAIMED,
            notes=f"Promoted by {approved_by}",
        )

        return True, updated, "Promoted to ACTIVE_DEEP"


# ─── Singleton ────────────────────────────────────────────────────────

_DEFAULT_ENFORCER: DeepWipEnforcer | None = None


def get_enforcer(registry: EconomicCellRegistry | None = None) -> DeepWipEnforcer:
    global _DEFAULT_ENFORCER
    if _DEFAULT_ENFORCER is None:
        if registry is None:
            from dealix.commercial.economic_cell_registry import get_default_registry
            registry = get_default_registry()
        _DEFAULT_ENFORCER = DeepWipEnforcer(registry)
    return _DEFAULT_ENFORCER


def reset_enforcer_for_tests(enforcer: DeepWipEnforcer | None = None) -> DeepWipEnforcer | None:
    global _DEFAULT_ENFORCER
    _DEFAULT_ENFORCER = enforcer
    return _DEFAULT_ENFORCER


__all__ = [
    "DEEP_WIP_MAX",
    "WipSlot",
    "DeepWipEnforcer",
    "DeepWipPolicy",
    "PresidentWipController",
    "get_enforcer",
    "reset_enforcer_for_tests",
]
