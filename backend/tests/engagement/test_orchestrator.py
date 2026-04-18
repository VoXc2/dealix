"""
Tests for EngagementOrchestrator — playbook loading, step execution, sequencing.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from app.engagement.base import (
    AgentContext,
    ChannelType,
    DeliveryReceipt,
    DeliveryStatus,
    EngagementSettings,
    LeadStage,
)
from app.engagement.orchestrator import (
    EngagementOrchestrator,
    Lead,
    Playbook,
    PlaybookStep,
)

_PLAYBOOKS_DIR = (
    Path(__file__).parents[2] / "app" / "engagement" / "playbooks"
)


# ─────────────────────────────────────────────────────────────
# Playbook loading
# ─────────────────────────────────────────────────────────────

def test_load_ecommerce_playbook():
    """ecommerce_outbound.yaml loads correctly."""
    pb = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")
    assert pb.name == "ecommerce_outbound"
    assert pb.target_sector == "ecommerce"
    assert len(pb.steps) >= 3
    assert pb.steps[0].channel == ChannelType.WHATSAPP
    assert pb.steps[0].delay_days == 0


def test_load_agency_playbook():
    """agency_outbound.yaml loads with LinkedIn as first channel."""
    pb = Playbook.from_yaml(_PLAYBOOKS_DIR / "agency_outbound.yaml")
    assert pb.name == "agency_outbound"
    assert pb.steps[0].channel == ChannelType.LINKEDIN


def test_load_real_estate_playbook():
    """real_estate_outbound.yaml loads with multiple steps."""
    pb = Playbook.from_yaml(_PLAYBOOKS_DIR / "real_estate_outbound.yaml")
    assert pb.name == "real_estate_outbound"
    assert len(pb.steps) >= 5


def test_load_all_playbooks():
    """All YAML files in playbooks/ directory load without error."""
    playbooks = Playbook.from_dir(_PLAYBOOKS_DIR)
    assert len(playbooks) == 3
    names = [p.name for p in playbooks]
    assert "ecommerce_outbound" in names
    assert "agency_outbound" in names
    assert "real_estate_outbound" in names


# ─────────────────────────────────────────────────────────────
# Lead model
# ─────────────────────────────────────────────────────────────

def test_lead_preferred_address():
    """Lead.preferred_address returns the correct contact for each channel."""
    lead = Lead(
        id="l1",
        name="Ahmed",
        phone="+966512345678",
        email="ahmed@test.com",
        linkedin_urn="urn:li:fs_salesProfile:ACoAA",
    )
    assert lead.preferred_address(ChannelType.WHATSAPP) == "+966512345678"
    assert lead.preferred_address(ChannelType.EMAIL) == "ahmed@test.com"
    assert lead.preferred_address(ChannelType.LINKEDIN) == "urn:li:fs_salesProfile:ACoAA"
    assert lead.preferred_address(ChannelType.SMS) == "+966512345678"
    assert lead.preferred_address(ChannelType.VOICE) == "+966512345678"


def test_lead_to_context():
    """Lead.to_context() maps fields correctly to AgentContext."""
    lead = Lead(
        id="l2",
        name="Fatima",
        company="شركة الريادة",
        sector="real_estate",
        city="Riyadh",
        phone="+966500000000",
        opt_in=True,
    )
    ctx = lead.to_context()
    assert ctx.lead_id == "l2"
    assert ctx.lead_name == "Fatima"
    assert ctx.company_name == "شركة الريادة"
    assert ctx.opt_in is True


# ─────────────────────────────────────────────────────────────
# Orchestrator — step execution
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def orchestrator(settings, memory, llm):
    return EngagementOrchestrator(settings=settings, memory=memory, llm=llm)


@pytest.mark.asyncio
async def test_run_step_success(orchestrator, wa_agent):
    """run_step() sends via the correct agent and returns success."""
    # Mock the agent's send_with_guards to return success
    mock_receipt = DeliveryReceipt(
        channel=ChannelType.WHATSAPP,
        to="+966512345678",
        status=DeliveryStatus.SENT,
    )
    wa_agent.send_with_guards = AsyncMock(return_value=mock_receipt)
    orchestrator.register_agent(ChannelType.WHATSAPP, wa_agent)

    # Mock LLM so compose_message doesn't need real API
    orchestrator.llm.chat = AsyncMock(return_value="رسالة تسويقية")

    lead = Lead(id="l1", name="Ahmed", company="Test Co", phone="+966512345678")
    playbook = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")

    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)

    assert result.success is True
    assert result.channel == ChannelType.WHATSAPP
    assert result.receipt is not None
    assert result.receipt.status == DeliveryStatus.SENT


@pytest.mark.asyncio
async def test_run_step_no_agent_registered(orchestrator):
    """run_step() returns failure when no agent is registered for the channel."""
    lead = Lead(id="l2", name="Ahmed", phone="+966512345678")
    playbook = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")

    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)

    assert result.success is False
    # Either no agent or no channel found
    assert result.error is not None


@pytest.mark.asyncio
async def test_run_step_no_address(orchestrator, wa_agent):
    """run_step() returns failure when lead has no address for the channel."""
    orchestrator.register_agent(ChannelType.WHATSAPP, wa_agent)

    # Lead with no phone number
    lead = Lead(id="l3", name="Ahmed", email="ahmed@test.com")
    playbook = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")

    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)

    assert result.success is False


@pytest.mark.asyncio
async def test_run_step_out_of_range(orchestrator, wa_agent):
    """run_step() returns error when step_index exceeds playbook length."""
    orchestrator.register_agent(ChannelType.WHATSAPP, wa_agent)
    lead = Lead(id="l4", name="Ahmed", phone="+966512345678")
    playbook = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")

    result = await orchestrator.run_step(
        lead=lead, playbook=playbook, step_index=999
    )

    assert result.success is False
    assert "out of range" in result.error.lower()


@pytest.mark.asyncio
async def test_run_step_schedules_next(orchestrator, wa_agent):
    """run_step() calculates next_step_at based on delay_days."""
    mock_receipt = DeliveryReceipt(
        channel=ChannelType.WHATSAPP,
        to="+966512345678",
        status=DeliveryStatus.SENT,
    )
    wa_agent.send_with_guards = AsyncMock(return_value=mock_receipt)
    orchestrator.register_agent(ChannelType.WHATSAPP, wa_agent)
    orchestrator.llm.chat = AsyncMock(return_value="رسالة")

    lead = Lead(id="l5", name="Ahmed", phone="+966512345678")
    playbook = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")

    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)

    # Step 1 (index 0) is WhatsApp Day 0
    # Step 2 (index 1) is WhatsApp Day 3 → next_step_at should be ~3 days from now
    assert result.next_step_at is not None
    expected = datetime.now(timezone.utc) + timedelta(days=3)
    diff = abs((result.next_step_at - expected).total_seconds())
    assert diff < 10  # within 10 seconds


@pytest.mark.asyncio
async def test_channel_priority_fallback(orchestrator, email_agent):
    """Orchestrator falls back to email when WhatsApp agent is not registered."""
    # Only register email, not WhatsApp
    orchestrator.register_agent(ChannelType.EMAIL, email_agent)
    orchestrator.llm.chat = AsyncMock(return_value="Email message")

    mock_receipt = DeliveryReceipt(
        channel=ChannelType.EMAIL,
        to="test@test.com",
        status=DeliveryStatus.SENT,
    )
    email_agent.send_with_guards = AsyncMock(return_value=mock_receipt)

    # Lead has both phone and email
    lead = Lead(
        id="l6", name="Ahmed",
        phone="+966512345678",
        email="ahmed@test.com",
    )
    playbook = Playbook.from_yaml(_PLAYBOOKS_DIR / "ecommerce_outbound.yaml")

    result = await orchestrator.run_step(lead=lead, playbook=playbook, step_index=0)

    # Should fall back to email since WhatsApp agent is not registered
    assert result.channel == ChannelType.EMAIL
    assert result.success is True


# ─────────────────────────────────────────────────────────────
# Message composition
# ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_compose_message_with_template(orchestrator):
    """_compose_message uses static template when provided."""
    step = PlaybookStep(
        channel=ChannelType.WHATSAPP,
        delay_days=0,
        prompt_key="whatsapp_outbound_ar",
        message_template="مرحباً {name} من {company}",
    )
    lead = Lead(id="l7", name="أحمد", company="شركة النجاح")
    message = await orchestrator._compose_message(lead, step)
    assert "أحمد" in message
    assert "شركة النجاح" in message


@pytest.mark.asyncio
async def test_compose_message_via_llm(orchestrator):
    """_compose_message calls LLM when no template is provided."""
    orchestrator.llm.chat = AsyncMock(return_value="رسالة من الـ LLM")

    step = PlaybookStep(
        channel=ChannelType.WHATSAPP,
        delay_days=0,
        prompt_key="whatsapp_outbound_ar",
    )
    lead = Lead(id="l8", name="Fatima", company="مؤسسة التميز")
    message = await orchestrator._compose_message(lead, step)

    assert message == "رسالة من الـ LLM"
    orchestrator.llm.chat.assert_called_once()
