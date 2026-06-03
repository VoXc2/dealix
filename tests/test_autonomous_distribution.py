"""
Unit tests for the autonomous product distribution engine.
اختبارات وحدة لمحرك التوزيع المستقل.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

# ---------------------------------------------------------------------------
# Module-level fixtures / helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_queue_path(tmp_path: Path) -> str:
    """Return a temporary JSONL path and set the env-var override."""
    p = str(tmp_path / "proposal_queue.jsonl")
    os.environ["DEALIX_PROPOSAL_QUEUE_PATH"] = p
    yield p
    os.environ.pop("DEALIX_PROPOSAL_QUEUE_PATH", None)


# ---------------------------------------------------------------------------
# 1. Product catalog completeness
# ---------------------------------------------------------------------------


def test_product_catalog_has_all_five_tiers() -> None:
    """All five product tiers must be present in PRODUCT_CATALOG."""
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    for tier in ProductTier:
        assert tier in PRODUCT_CATALOG, f"Missing tier in catalog: {tier.value}"


def test_product_catalog_fields_populated() -> None:
    """Every product must have non-empty required fields."""
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    for tier, product in PRODUCT_CATALOG.items():
        assert product.id, f"product.id is empty for tier {tier.value}"
        assert product.name_ar, f"product.name_ar is empty for tier {tier.value}"
        assert product.name_en, f"product.name_en is empty for tier {tier.value}"
        assert product.tier == tier, f"product.tier mismatch for {tier.value}"
        assert product.delivery_days > 0, f"delivery_days must be > 0 for {tier.value}"
        assert isinstance(product.key_outcomes, list)


def test_product_catalog_price_ladder() -> None:
    """Prices must be non-decreasing up the ladder."""
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    ladder = [
        ProductTier.FREE_DIAGNOSTIC,
        ProductTier.SPRINT,
        ProductTier.DATA_PACK,
        ProductTier.MANAGED_OPS,
        ProductTier.CUSTOM_AI,
    ]
    prev_price = -1
    for tier in ladder:
        price = PRODUCT_CATALOG[tier].price_sar
        assert price >= prev_price, (
            f"Price for {tier.value} ({price}) is less than previous tier ({prev_price})"
        )
        prev_price = price


def test_product_to_dict_roundtrip() -> None:
    """to_dict must include all required keys."""
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    product = PRODUCT_CATALOG[ProductTier.SPRINT]
    d = product.to_dict()
    required_keys = {
        "id", "name_ar", "name_en", "tier", "price_sar", "price_max_sar",
        "description_ar", "description_en", "target_company_size",
        "target_sectors", "min_icp_score", "delivery_days", "key_outcomes",
    }
    assert required_keys.issubset(d.keys())


# ---------------------------------------------------------------------------
# 2. ProductRouterAgent — scoring thresholds
# ---------------------------------------------------------------------------

# We mock the BaseAgent LLM router so no network calls are made.
# core.memory imports sqlalchemy which is unavailable in the test environment,
# so we inject a fake module via sys.modules before any agent is instantiated.
@pytest.fixture
def mock_router_agent(mock_llm_response: Any) -> Any:  # noqa: ANN401
    import sys
    from unittest.mock import MagicMock

    # Stub out the heavy memory stack before agents are instantiated
    fake_revenue_memory_module = MagicMock()
    fake_memory_module = MagicMock()
    fake_embedding_module = MagicMock()

    injected: dict[str, Any] = {}
    for mod_path, fake in [
        ("core.memory", fake_memory_module),
        ("core.memory.revenue_memory", fake_revenue_memory_module),
        ("core.memory.embedding_service", fake_embedding_module),
    ]:
        if mod_path not in sys.modules:
            sys.modules[mod_path] = fake
            injected[mod_path] = fake

    # Also patch the LLM router
    with patch("core.agents.base.get_router") as m1:
        router_instance = AsyncMock()
        router_instance.run.return_value = mock_llm_response
        m1.return_value = router_instance
        yield router_instance

    # Clean up only what we injected
    for mod_path in injected:
        sys.modules.pop(mod_path, None)


@pytest.mark.asyncio
async def test_router_low_icp_returns_free_diagnostic(mock_router_agent: Any) -> None:
    """ICP score below 0.3 must route to FREE_DIAGNOSTIC."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Test Lead"},
        icp_score=0.1,
        sector="retail",
        company_size="small",
        budget_signal=None,
    )
    assert decision.recommended_tier == ProductTier.FREE_DIAGNOSTIC
    assert decision.requires_founder_approval is False


@pytest.mark.asyncio
async def test_router_mid_low_icp_returns_sprint(mock_router_agent: Any) -> None:
    """ICP score in [0.3, 0.5) must route to SPRINT."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Mid Lead"},
        icp_score=0.4,
        sector="logistics",
        company_size="small",
        budget_signal=None,
    )
    assert decision.recommended_tier == ProductTier.SPRINT
    assert decision.requires_founder_approval is False


@pytest.mark.asyncio
async def test_router_mid_icp_returns_data_pack(mock_router_agent: Any) -> None:
    """ICP score in [0.5, 0.7) without high budget signal must route to DATA_PACK."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Warm Lead"},
        icp_score=0.6,
        sector="healthcare",
        company_size="medium",
        budget_signal=None,
    )
    assert decision.recommended_tier == ProductTier.DATA_PACK
    assert decision.requires_founder_approval is False


@pytest.mark.asyncio
async def test_router_mid_icp_high_budget_returns_managed_ops(mock_router_agent: Any) -> None:
    """ICP score in [0.5, 0.7) with high budget signal must route to MANAGED_OPS."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Budget Lead"},
        icp_score=0.62,
        sector="finance",
        company_size="large",
        budget_signal="high",
    )
    assert decision.recommended_tier == ProductTier.MANAGED_OPS
    assert decision.requires_founder_approval is True


@pytest.mark.asyncio
async def test_router_high_icp_medium_company_returns_managed_ops(
    mock_router_agent: Any,
) -> None:
    """ICP score >= 0.7 with non-enterprise company must route to MANAGED_OPS."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Hot Lead"},
        icp_score=0.75,
        sector="retail",
        company_size="medium",
        budget_signal=None,
    )
    assert decision.recommended_tier == ProductTier.MANAGED_OPS
    assert decision.requires_founder_approval is True


@pytest.mark.asyncio
async def test_router_high_icp_enterprise_returns_custom_ai(mock_router_agent: Any) -> None:
    """ICP score >= 0.7 with enterprise/large company must route to CUSTOM_AI."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Enterprise Lead"},
        icp_score=0.85,
        sector="energy",
        company_size="enterprise",
        budget_signal=None,
    )
    assert decision.recommended_tier == ProductTier.CUSTOM_AI
    assert decision.requires_founder_approval is True


@pytest.mark.asyncio
async def test_router_decision_has_upsell(mock_router_agent: Any) -> None:
    """Every decision below the top tier should have an upsell_tier."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Sprint Lead"},
        icp_score=0.35,
        sector="education",
        company_size="small",
        budget_signal=None,
    )
    assert decision.upsell_tier is not None
    assert decision.upsell_tier != decision.recommended_tier


@pytest.mark.asyncio
async def test_router_top_tier_no_upsell(mock_router_agent: Any) -> None:
    """CUSTOM_AI has no upsell tier."""
    from autonomous_growth.agents.product_router import ProductRouterAgent
    from autonomous_growth.product_catalog import ProductTier

    agent = ProductRouterAgent()
    decision = await agent.run(
        lead_profile={"name": "Enterprise Lead"},
        icp_score=0.95,
        sector="telecom",
        company_size="enterprise",
        budget_signal="high",
    )
    assert decision.recommended_tier == ProductTier.CUSTOM_AI
    assert decision.upsell_tier is None


@pytest.mark.asyncio
async def test_router_confidence_in_range(mock_router_agent: Any) -> None:
    """Confidence must always be in [0, 1]."""
    from autonomous_growth.agents.product_router import ProductRouterAgent

    agent = ProductRouterAgent()
    for score in [0.0, 0.29, 0.31, 0.55, 0.71, 1.0]:
        decision = await agent.run(
            lead_profile={"name": "Lead"},
            icp_score=score,
            sector="general",
            company_size="medium",
            budget_signal=None,
        )
        assert 0.0 <= decision.confidence <= 1.0, (
            f"Confidence out of range for icp_score={score}: {decision.confidence}"
        )


# ---------------------------------------------------------------------------
# 3. ProposalSenderAgent — draft creation and queue I/O
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_proposal_sender_creates_draft(tmp_queue_path: str, mock_router_agent: Any) -> None:
    """ProposalSenderAgent.run must create a draft with status pending_approval."""
    from autonomous_growth.agents.proposal_sender import ProposalSenderAgent
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    agent = ProposalSenderAgent()
    product = PRODUCT_CATALOG[ProductTier.SPRINT]
    draft = await agent.run(
        product=product,
        lead_profile={"name": "Ahmad Al-Rashid", "company": "Tech Corp"},
        locale="ar",
    )

    assert draft.status == "pending_approval"
    assert draft.product_tier == ProductTier.SPRINT
    assert draft.id.startswith("prop_")
    assert draft.subject_ar
    assert draft.subject_en
    assert draft.body_ar
    assert draft.body_en


@pytest.mark.asyncio
async def test_proposal_sender_writes_to_queue(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """Draft must be written to the JSONL queue file."""
    from autonomous_growth.agents.proposal_sender import ProposalSenderAgent, _read_queue
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    agent = ProposalSenderAgent()
    product = PRODUCT_CATALOG[ProductTier.DATA_PACK]
    await agent.run(
        product=product,
        lead_profile={"name": "Sara Al-Qahtani"},
        locale="en",
    )

    drafts = _read_queue()
    assert len(drafts) >= 1
    assert drafts[-1].product_tier == ProductTier.DATA_PACK


# ---------------------------------------------------------------------------
# 4. DistributionEngine — process_lead
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_engine_process_lead_returns_valid_result(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """process_lead must return a DistributionEngineResult with lead_id set."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine

    engine = AutonomousDistributionEngine()
    result = await engine.process_lead(
        {
            "lead_id": "test_lead_001",
            "name": "Khalid Al-Otaibi",
            "company": "Saudi Retail Co",
            "sector": "retail",
            "company_size": "medium",
            "icp_score": 0.55,
            "locale": "ar",
        }
    )

    assert result.lead_id == "test_lead_001"
    assert result.product_route is not None
    assert result.proposal_draft is not None
    assert result.proposal_draft.status == "pending_approval"


@pytest.mark.asyncio
async def test_engine_process_lead_auto_assigns_lead_id(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """If no lead_id in payload, engine must generate one."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine

    engine = AutonomousDistributionEngine()
    result = await engine.process_lead({"name": "Anonymous", "icp_score": 0.3})
    assert result.lead_id
    assert result.lead_id.startswith("lead_")


@pytest.mark.asyncio
async def test_engine_low_icp_no_approval_required(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """Low ICP lead routes to free diagnostic — no founder approval required."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine
    from autonomous_growth.product_catalog import ProductTier

    engine = AutonomousDistributionEngine()
    result = await engine.process_lead({"name": "New Lead", "icp_score": 0.15})
    assert result.product_route is not None
    assert result.product_route.recommended_tier == ProductTier.FREE_DIAGNOSTIC
    assert result.product_route.requires_founder_approval is False


@pytest.mark.asyncio
async def test_engine_high_icp_enterprise_requires_approval(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """High ICP enterprise lead → CUSTOM_AI → requires founder approval."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine
    from autonomous_growth.product_catalog import ProductTier

    engine = AutonomousDistributionEngine()
    result = await engine.process_lead(
        {
            "name": "CEO",
            "company": "ARAMCO Digital",
            "icp_score": 0.9,
            "company_size": "enterprise",
            "sector": "energy",
        }
    )
    assert result.product_route is not None
    assert result.product_route.recommended_tier == ProductTier.CUSTOM_AI
    assert result.product_route.requires_founder_approval is True
    # Warning about founder approval should be in warnings
    assert any("founder_approval_required" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# 5. Pending approvals queue
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pending_approvals_returns_list(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """get_pending_approvals must return a list (possibly empty)."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine

    engine = AutonomousDistributionEngine()
    pending = await engine.get_pending_approvals()
    assert isinstance(pending, list)


@pytest.mark.asyncio
async def test_approve_proposal_updates_status(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """Approving a proposal must change its status from pending_approval to approved."""
    from autonomous_growth.agents.proposal_sender import ProposalSenderAgent, _read_queue
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine
    from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

    # Create a draft
    sender = ProposalSenderAgent()
    draft = await sender.run(
        product=PRODUCT_CATALOG[ProductTier.SPRINT],
        lead_profile={"name": "Test"},
        locale="ar",
    )

    engine = AutonomousDistributionEngine()

    # Should be pending
    pending = await engine.get_pending_approvals()
    assert any(d.id == draft.id for d in pending)

    # Approve
    result = await engine.approve_proposal(draft.id)
    assert result is True

    # Must no longer be in pending
    pending_after = await engine.get_pending_approvals()
    assert not any(d.id == draft.id for d in pending_after)

    # Queue file must show approved status
    all_drafts = _read_queue()
    matching = [d for d in all_drafts if d.id == draft.id]
    assert len(matching) == 1
    assert matching[0].status == "approved"


@pytest.mark.asyncio
async def test_approve_nonexistent_proposal_returns_false(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """Approving a non-existent proposal must return False."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine

    engine = AutonomousDistributionEngine()
    result = await engine.approve_proposal("nonexistent_id_xyz")
    assert result is False


# ---------------------------------------------------------------------------
# 6. Stats
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_stats_returns_expected_keys(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """get_stats must return dict with required keys."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine

    engine = AutonomousDistributionEngine()
    stats = engine.get_stats()
    for key in ("total_processed", "pending", "approved", "sent", "as_of"):
        assert key in stats, f"Missing key in stats: {key}"


# ---------------------------------------------------------------------------
# 7. ProposalDraft serialisation
# ---------------------------------------------------------------------------


def test_proposal_draft_from_dict_roundtrip() -> None:
    """ProposalDraft.from_dict(to_dict()) must produce an equivalent object."""
    from autonomous_growth.agents.proposal_sender import ProposalDraft
    from autonomous_growth.product_catalog import ProductTier

    draft = ProposalDraft(
        id="prop_abc123",
        product_tier=ProductTier.DATA_PACK,
        lead_name="Fatimah",
        locale="ar",
        subject_ar="عرض حزمة البيانات",
        subject_en="Data Pack proposal",
        body_ar="نص عربي",
        body_en="English body",
        cta_url="https://dealix.ai/book",
    )
    restored = ProposalDraft.from_dict(draft.to_dict())
    assert restored.id == draft.id
    assert restored.product_tier == draft.product_tier
    assert restored.status == "pending_approval"


# ---------------------------------------------------------------------------
# 8. Sector campaign
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sector_campaign_returns_results(
    tmp_queue_path: str, mock_router_agent: Any
) -> None:
    """run_sector_distribution must return at least one result."""
    from autonomous_growth.distribution_engine import AutonomousDistributionEngine

    engine = AutonomousDistributionEngine()
    results = await engine.run_sector_distribution(
        sector="healthcare",
        channels=["linkedin", "email"],
    )
    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert r.lead_id
