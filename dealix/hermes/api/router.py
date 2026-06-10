"""Hermes FastAPI router — exposes all Hermes agents, pipelines, and loops."""

from __future__ import annotations

import time
import uuid
from typing import Any

import structlog
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from dealix.hermes.config import get_hermes_config
from dealix.hermes.memory import HermesMemory
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)

hermes_router = APIRouter(prefix="/api/v1/hermes", tags=["hermes"])

# ---------------------------------------------------------------------------
# Shared singletons — created once at import time
# ---------------------------------------------------------------------------

_registry: HermesRegistry | None = None
_memory: HermesMemory | None = None
_orchestrator: HermesOrchestrator | None = None


def _get_registry() -> HermesRegistry:
    global _registry
    if _registry is None:
        _registry = HermesRegistry.instance()
    return _registry


def _get_memory() -> HermesMemory:
    global _memory
    if _memory is None:
        _memory = HermesMemory()
    return _memory


def _get_orchestrator() -> HermesOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = HermesOrchestrator(
            registry=_get_registry(),
            memory=_get_memory(),
            config=get_hermes_config(),
        )
    return _orchestrator


# ---------------------------------------------------------------------------
# In-memory usage tracker — keyed by agent name
# ---------------------------------------------------------------------------
import collections

_usage_store: dict[str, dict] = collections.defaultdict(lambda: {
    "total_calls": 0,
    "total_tokens": 0,
    "total_duration_ms": 0.0,
})


def _record_usage(agent: str, tokens: int, duration_ms: float) -> None:
    _usage_store[agent]["total_calls"] += 1
    _usage_store[agent]["total_tokens"] += tokens
    _usage_store[agent]["total_duration_ms"] += duration_ms


# ---------------------------------------------------------------------------
# Response model
# ---------------------------------------------------------------------------


class HermesResponse(BaseModel):
    """Standard response envelope for all Hermes endpoints."""

    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    agent: str = ""
    duration_ms: float = 0.0
    tokens_used: int = 0


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class AgentRunRequest(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
    customer_id: str = ""


class PipelineRunRequest(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
    session_id: str = ""
    customer_id: str = ""


class OrchestrateRequest(BaseModel):
    goal: str
    available_agents: list[str] = Field(default_factory=list)
    max_iterations: int = Field(default=10, ge=1, le=20)
    customer_id: str = ""


class RevenueLoopStartRequest(BaseModel):
    tenant_id: str
    customer_id: str = ""


class LeadBatchRequest(BaseModel):
    leads: list[dict[str, Any]]
    customer_id: str = ""


class SprintStartRequest(BaseModel):
    client_data: dict[str, Any]
    sprint_id: str = ""
    customer_id: str = ""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@hermes_router.post("/agents/{agent_name}/run", response_model=HermesResponse)
async def run_agent(agent_name: str, body: AgentRunRequest) -> HermesResponse:
    """Run a specific Hermes agent by name."""
    registry = _get_registry()
    t0 = time.perf_counter()

    try:
        agent = registry.get(agent_name)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent_name!r} not found. Available: {registry.list_agents()}",
        )

    input_data = body.input_data
    if body.customer_id:
        input_data = {**input_data, "customer_id": body.customer_id}

    try:
        result = await agent.run(input_data)
    except Exception as exc:
        logger.error("hermes_agent_run_error", agent=agent_name, error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    duration_ms = (time.perf_counter() - t0) * 1000
    tokens = result.get("usage", {}).get("total_tokens", 0)

    _record_usage(agent_name, tokens, duration_ms)

    logger.info("hermes_agent_run_complete", agent=agent_name, duration_ms=round(duration_ms, 1))
    return HermesResponse(
        success=True,
        data=result,
        agent=agent_name,
        duration_ms=round(duration_ms, 1),
        tokens_used=tokens,
    )


@hermes_router.post("/pipeline/{pipeline_name}", response_model=HermesResponse)
async def run_pipeline(pipeline_name: str, body: PipelineRunRequest) -> HermesResponse:
    """Run a predefined multi-agent pipeline."""
    orchestrator = _get_orchestrator()
    t0 = time.perf_counter()

    input_data = body.input_data
    if body.customer_id:
        input_data = {**input_data, "customer_id": body.customer_id}

    session_id = body.session_id or str(uuid.uuid4())

    try:
        result = await orchestrator.run_pipeline(pipeline_name, input_data, session_id)
    except Exception as exc:
        logger.error("hermes_pipeline_error", pipeline=pipeline_name, error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if "error" in result and "available_pipelines" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    duration_ms = (time.perf_counter() - t0) * 1000
    return HermesResponse(
        success=True,
        data=result,
        agent="orchestrator",
        duration_ms=round(duration_ms, 1),
        tokens_used=0,
    )


@hermes_router.post("/orchestrate", response_model=HermesResponse)
async def orchestrate(body: OrchestrateRequest) -> HermesResponse:
    """Run a goal-driven supervisor loop over a set of agents."""
    orchestrator = _get_orchestrator()
    t0 = time.perf_counter()

    available = body.available_agents or _get_registry().list_agents()

    try:
        result = await orchestrator.run_supervisor_loop(
            goal=body.goal,
            available_agents=available,
            max_iterations=body.max_iterations,
        )
    except Exception as exc:
        logger.error("hermes_orchestrate_error", goal=body.goal, error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    duration_ms = (time.perf_counter() - t0) * 1000
    tokens = result.get("total_tokens", 0)
    return HermesResponse(
        success=True,
        data=result,
        agent="supervisor",
        duration_ms=round(duration_ms, 1),
        tokens_used=tokens,
    )


@hermes_router.get("/agents")
async def list_agents() -> dict[str, Any]:
    """List all registered Hermes agents with metadata."""
    registry = _get_registry()
    return {
        "agents": registry.all_info(),
        "count": len(registry.list_agents()),
        "governance_decision": "approved",
    }


@hermes_router.get("/agents/{agent_name}")
async def get_agent_info(agent_name: str) -> dict[str, Any]:
    """Get metadata for a specific agent."""
    registry = _get_registry()
    try:
        info = registry.info(agent_name)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent_name!r} not found.",
        )
    return {"agent": info, "governance_decision": "approved"}


@hermes_router.post("/loops/revenue/start")
async def start_revenue_loop(
    body: RevenueLoopStartRequest,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Start the revenue intelligence loop as a background task."""
    from dealix.hermes.loops.revenue_loop import RevenueLoop

    orchestrator = _get_orchestrator()
    loop = RevenueLoop(orchestrator=orchestrator, config=get_hermes_config())

    background_tasks.add_task(loop.run_forever, body.tenant_id)
    logger.info("revenue_loop_background_started", tenant_id=body.tenant_id)
    return {
        "started": True,
        "tenant_id": body.tenant_id,
        "mode": "background",
        "governance_decision": "approved",
    }


@hermes_router.post("/loops/lead/batch", response_model=HermesResponse)
async def process_lead_batch(body: LeadBatchRequest) -> HermesResponse:
    """Process a batch of leads through the LeadIntelligenceAgent."""
    from dealix.hermes.loops.lead_loop import LeadLoop

    t0 = time.perf_counter()
    loop = LeadLoop(registry=_get_registry(), config=get_hermes_config())

    try:
        result = await loop.run_once(body.leads)
    except Exception as exc:
        logger.error("lead_batch_error", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    duration_ms = (time.perf_counter() - t0) * 1000
    return HermesResponse(
        success=True,
        data=result,
        agent="lead_intelligence",
        duration_ms=round(duration_ms, 1),
        tokens_used=result.get("usage", {}).get("total_tokens", 0),
    )


@hermes_router.post("/sprint/start", response_model=HermesResponse)
async def start_sprint(body: SprintStartRequest) -> HermesResponse:
    """Start a new 7-day Revenue Intelligence Sprint."""
    from dealix.hermes.loops.sprint_loop import SprintLoop

    t0 = time.perf_counter()
    sprint_id = body.sprint_id or f"SPRINT-{str(uuid.uuid4())[:8].upper()}"
    loop = SprintLoop(
        registry=_get_registry(),
        memory=_get_memory(),
        config=get_hermes_config(),
    )

    client_data = body.client_data
    if body.customer_id:
        client_data = {**client_data, "customer_id": body.customer_id}

    try:
        result = await loop.run_sprint(client_data=client_data, sprint_id=sprint_id)
    except Exception as exc:
        logger.error("sprint_start_error", sprint_id=sprint_id, error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    duration_ms = (time.perf_counter() - t0) * 1000
    return HermesResponse(
        success=True,
        data=result,
        agent="sprint_orchestrator",
        duration_ms=round(duration_ms, 1),
        tokens_used=0,
    )


@hermes_router.get("/health")
async def hermes_health() -> dict[str, Any]:
    """Hermes system health check."""
    from dealix.hermes.loops.watchdog_loop import WatchdogLoop

    watchdog = WatchdogLoop(registry=_get_registry(), config=get_hermes_config())
    health = await watchdog.run_once()

    http_status = 200 if health["status"] == "healthy" else (503 if health["status"] == "critical" else 200)
    if http_status == 503:
        raise HTTPException(status_code=503, detail=health)

    return {**health, "governance_decision": "approved"}


@hermes_router.get("/usage")
async def get_usage() -> dict[str, Any]:
    """Return token and call usage aggregated by agent."""
    config = get_hermes_config()
    return {
        "usage_by_agent": dict(_usage_store),
        "cost_per_million_tokens_usd": 15.0,  # Opus 4 approximate rate
        "budget_usd": config.hermes_cost_budget_usd,
        "governance_decision": "approved",
    }


# ---------------------------------------------------------------------------
# Outreach queue models
# ---------------------------------------------------------------------------


class ApproveOutreachRequest(BaseModel):
    approved_by: str = "founder"


class RejectOutreachRequest(BaseModel):
    reason: str = ""


class DailyOutreachRequest(BaseModel):
    leads: list[dict[str, Any]] = Field(default_factory=list)
    customer_id: str = ""


# ---------------------------------------------------------------------------
# Outreach queue endpoints
# ---------------------------------------------------------------------------


@hermes_router.get("/outreach/queue")
async def get_outreach_queue() -> dict[str, Any]:
    """List all pending outreach drafts awaiting founder approval."""
    from dealix.hermes.outreach_queue import OutreachQueue

    q = OutreachQueue.instance()
    return {
        "pending": [d.to_dict() for d in q.pending()],
        "stats": q.stats(),
        "governance_decision": "approved",
    }


@hermes_router.post("/outreach/{draft_id}/approve")
async def approve_outreach(draft_id: str, body: ApproveOutreachRequest) -> dict[str, Any]:
    """Approve an outreach draft (founder action). Does not send automatically."""
    from dealix.hermes.outreach_queue import OutreachQueue

    try:
        draft = OutreachQueue.instance().approve(draft_id, approved_by=body.approved_by)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Draft {draft_id!r} not found")
    return {"approved": True, "draft": draft.to_dict(), "governance_decision": "approved"}


@hermes_router.post("/outreach/{draft_id}/reject")
async def reject_outreach(draft_id: str, body: RejectOutreachRequest) -> dict[str, Any]:
    """Reject an outreach draft."""
    from dealix.hermes.outreach_queue import OutreachQueue

    try:
        draft = OutreachQueue.instance().reject(draft_id, reason=body.reason)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Draft {draft_id!r} not found")
    return {"rejected": True, "draft": draft.to_dict(), "governance_decision": "approved"}


@hermes_router.post("/outreach/run-daily", response_model=HermesResponse)
async def run_daily_outreach(
    body: DailyOutreachRequest,
    background_tasks: BackgroundTasks,
) -> HermesResponse:
    """Trigger the daily customer acquisition cycle (queues drafts for approval)."""
    from dealix.hermes.loops.daily_outreach_loop import DailyOutreachLoop

    t0 = time.perf_counter()
    loop = DailyOutreachLoop(registry=_get_registry(), config=get_hermes_config())
    result = await loop.run_once(leads=body.leads)
    duration_ms = (time.perf_counter() - t0) * 1000
    return HermesResponse(
        success=True,
        data=result,
        agent="customer_acquisition",
        duration_ms=round(duration_ms, 1),
        tokens_used=result.get("usage", {}).get("total_tokens", 0),
    )


__all__ = ["HermesResponse", "hermes_router"]
