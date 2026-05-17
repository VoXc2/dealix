"""
Agents domain — LLM gateway, AI workforce, observability, safety, delivery.
مجال الوكلاء — بوابة LLM، القوى العاملة بالذكاء الاصطناعي، المراقبة، السلامة، التسليم.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    agent_governance,
    agent_observability as agent_observability_router,
    agents,
    ai_workforce,
    automation,
    autonomous,
    delivery_factory,
    delivery_os,
    knowledge,
    knowledge_v10,
    llm_gateway_v10,
    observability_v10,
    safety_v10,
    tool_guardrail_gateway as tool_guardrail_gateway_router,
    workflow_os_v10,
)

_ROUTERS = [
    agents.router,
    ai_workforce.router,
    llm_gateway_v10.router,
    agent_governance.router,
    agent_observability_router.router,
    tool_guardrail_gateway_router.router,
    safety_v10.router,
    observability_v10.router,
    workflow_os_v10.router,
    delivery_factory.router,
    delivery_os.router,
    automation.router,
    autonomous.router,
    knowledge_v10.router,
    knowledge.router,
]


def get_routers() -> list[APIRouter]:
    """Return all agents-domain routers."""
    return _ROUTERS
