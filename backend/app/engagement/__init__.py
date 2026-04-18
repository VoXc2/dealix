"""
Dealix — Omnichannel Engagement Agents
=======================================
Unified framework for all outreach channels.

Package structure:
  base.py        — BaseEngagementAgent (ABC)
  memory.py      — ConversationMemory (aiosqlite)
  llm.py         — LLMGateway (Groq primary / OpenAI fallback)
  orchestrator.py — EngagementOrchestrator
  channels/
    whatsapp.py  — WhatsAppAgent (Twilio)
    email.py     — EmailAgent (SendGrid + Gmail API)
    linkedin.py  — LinkedInAgent (Unipile)
    sms.py       — SMSAgent (Twilio SMS)
    voice.py     — VoiceAgent (Retell/Vapi stub)
    social.py    — SocialListener (X + Instagram)
  prompts/       — Arabic system prompts (.md files)
  playbooks/     — Sequence definitions (.yaml files)
"""

from .base import (
    BaseEngagementAgent,
    AgentContext,
    IncomingMessage,
    DeliveryReceipt,
    ChannelType,
    MessageDirection,
    LeadStage,
)
from .memory import ConversationMemory
from .llm import LLMGateway
from .orchestrator import EngagementOrchestrator

__all__ = [
    "BaseEngagementAgent",
    "AgentContext",
    "IncomingMessage",
    "DeliveryReceipt",
    "ChannelType",
    "MessageDirection",
    "LeadStage",
    "ConversationMemory",
    "LLMGateway",
    "EngagementOrchestrator",
]
