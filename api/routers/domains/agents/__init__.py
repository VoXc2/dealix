"""
Agents domain — LLM gateway, AI workforce, observability, safety, delivery.
مجال الوكلاء — بوابة LLM، القوى العاملة بالذكاء الاصطناعي، المراقبة، السلامة، التسليم.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    agent_governance,
    agentic_enterprise,
    agents,
    ai_workforce,
    automation,
    delivery_factory,
    delivery_os,
    knowledge_v10,
    llm_gateway_v10,
    observability_v10,
    safety_v10,
    workflow_os_v10,
)
from api.routers import (
    agent_observability as agent_observability_router,
)
from api.routers import (
    tool_guardrail_gateway as tool_guardrail_gateway_router,
)

# api.routers.autonomous remains deliberately unregistered while #1070 is open.
# That legacy mixed-generation router still contains public/global surfaces that
# can create tenant-less records or assert sent/paid/customer states without the
# canonical Approval/Outcome/Proof chain. The bounded schema and test work in
# #1094 may continue, but production registration must fail closed until every
# retained endpoint has explicit authentication, tenant, policy, and evidence
# contracts. Do not re-add it here merely because revision 020 exists.

_ROUTERS = [
    agentic_enterprise.router,
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
    knowledge_v10.router,
]


def get_routers() -> list[APIRouter]:
    """Return all production-registered agents-domain routers."""
    return _ROUTERS
