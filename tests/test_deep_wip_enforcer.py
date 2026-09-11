"""Deep WIP invariant — DEEP_WIP_MAX = 3, release truly frees capacity."""

from __future__ import annotations

import pathlib
import tempfile
import uuid
from datetime import UTC, datetime

from dealix.commercial.deep_wip_enforcer import (
    DEEP_WIP_MAX,
    DeepWipEnforcer,
    DeepWipPolicy,
    PresidentWipController,
)
from dealix.commercial.economic_cell import (
    Buyer,
    BuyerGroup,
    Distribution,
    DistributionRail,
    EconomicCell,
    Economics,
    Evidence,
    Execution,
    Identity,
    LifecycleState,
    Market,
    Monetization,
    MonetizationRail,
    Offer,
    Portfolio,
    Problem,
    ProblemClass,
    Procurement,
    Proof,
    Risk,
    Sector,
    Value,
)
from dealix.commercial.economic_cell_registry import EconomicCellRegistry


def _make_cell(state: LifecycleState = LifecycleState.CANDIDATE_DEEP) -> EconomicCell:
    now = datetime.now(UTC).isoformat()
    return EconomicCell(
        identity=Identity(cell_id=str(uuid.uuid4()), canonical_name="test", version=1, created_at=now, updated_at=now),
        market=Market(sector=Sector.TECHNOLOGY_SAAS_SI),
        buyer=Buyer(buyer_group=BuyerGroup.CEO),
        problem=Problem(problem_class=ProblemClass.REVENUE_LEAKAGE),
        value=Value(),
        offer=Offer(offer_family="test"),
        monetization=Monetization(monetization_rail=MonetizationRail.PAID_SPRINT),
        distribution=Distribution(distribution_rail=DistributionRail.WEBSITE_INBOUND),
        procurement=Procurement(),
        execution=Execution(),
        evidence=Evidence(),
        economics=Economics(),
        risk=Risk(),
        portfolio=Portfolio(lifecycle_state=state),
        proof=Proof(),
    )


def _registry_with_cells(count: int = 4) -> EconomicCellRegistry:
    registry = EconomicCellRegistry(storage_path=pathlib.Path(tempfile.mktemp(suffix=".jsonl")))
    for _ in range(count):
        registry.create(_make_cell())
    return registry


def test_deep_wip_max_is_three() -> None:
    assert DEEP_WIP_MAX == 3


def test_registry_blocks_fourth_slot() -> None:
    registry = _registry_with_cells()
    cells = registry.list_by_state(LifecycleState.CANDIDATE_DEEP)
    for cell in cells[:DEEP_WIP_MAX]:
        assert registry.claim_deep_wip_slot(cell.identity.cell_id)
    assert registry.count_active_deep() == DEEP_WIP_MAX
    assert not registry.claim_deep_wip_slot(cells[3].identity.cell_id)


def test_enforcer_blocks_fourth_slot() -> None:
    registry = _registry_with_cells()
    enforcer = DeepWipEnforcer(registry)
    cells = registry.list_by_state(LifecycleState.CANDIDATE_DEEP)
    for cell in cells[:DEEP_WIP_MAX]:
        assert enforcer.claim_slot(cell.identity.cell_id, "test")
    assert enforcer.current_count() == DEEP_WIP_MAX
    assert enforcer.is_full()
    assert enforcer.available_slots() == 0
    assert not enforcer.claim_slot(cells[3].identity.cell_id, "test")


def test_release_truly_frees_capacity() -> None:
    registry = _registry_with_cells()
    enforcer = DeepWipEnforcer(registry)
    cells = registry.list_by_state(LifecycleState.CANDIDATE_DEEP)
    for cell in cells[:DEEP_WIP_MAX]:
        assert enforcer.claim_slot(cell.identity.cell_id, "test")

    assert enforcer.release_slot(cells[0].identity.cell_id)
    assert enforcer.current_count() == DEEP_WIP_MAX - 1
    assert registry.get(cells[0].identity.cell_id).portfolio.lifecycle_state == LifecycleState.CANDIDATE_DEEP
    assert enforcer.claim_slot(cells[3].identity.cell_id, "test")
    assert enforcer.current_count() == DEEP_WIP_MAX


def test_president_controller_requires_approval_when_full_without_auto_demote() -> None:
    registry = _registry_with_cells()
    enforcer = DeepWipEnforcer(registry)
    cells = registry.list_by_state(LifecycleState.CANDIDATE_DEEP)
    for cell in cells[:DEEP_WIP_MAX]:
        assert enforcer.claim_slot(cell.identity.cell_id, "test")

    controller = PresidentWipController(enforcer, DeepWipPolicy(auto_demote_on_full=False))
    result = controller.evaluate_promotion_request(cells[3], [])
    assert result["allowed"] is False
    assert result["requires_explicit_approval"] is True
