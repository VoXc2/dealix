from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LLMCall:
    call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider: str = ""
    model: str = ""
    prompt: str = ""
    response: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    latency_ms: float = 0.0
    status: str = "success"
    error: str | None = None
    agent_id: str | None = None
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AgentAction:
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    action_type: str = ""
    input: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    status: str = "success"
    error: str | None = None
    trace_id: str | None = None
    parent_action_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CostReport:
    period_days: int = 30
    total_cost: float = 0.0
    by_provider: dict[str, float] = field(default_factory=dict)
    by_model: dict[str, float] = field(default_factory=dict)
    by_agent: dict[str, float] = field(default_factory=dict)
    daily_costs: list[dict[str, Any]] = field(default_factory=list)
    total_calls: int = 0
    avg_cost_per_call: float = 0.0


class LangfuseTracker:
    def __init__(
        self,
        public_key: str | None = None,
        secret_key: str | None = None,
        host: str = "https://cloud.langfuse.com",
        enabled: bool = True,
    ):
        self._public_key = public_key
        self._secret_key = secret_key
        self._host = host
        self._enabled = enabled
        self._calls: list[LLMCall] = []
        self._actions: list[AgentAction] = []
        self._traces: dict[str, dict[str, Any]] = {}

        if enabled:
            logger.info("Langfuse initialized (host: %s)", host)

    async def trace_llm_call(self, call: LLMCall) -> str:
        trace_id = call.call_id
        self._calls.append(call)

        if not self._enabled:
            return trace_id

        await self._send_to_langfuse({
            "id": trace_id,
            "type": "llm_call",
            "provider": call.provider,
            "model": call.model,
            "input": call.prompt[:1000],
            "output": call.response[:1000],
            "usage": {
                "prompt_tokens": call.prompt_tokens,
                "completion_tokens": call.completion_tokens,
                "total_tokens": call.total_tokens,
            },
            "cost": call.cost,
            "latency_ms": call.latency_ms,
            "status": call.status,
            "error": call.error,
            "agent_id": call.agent_id,
            "session_id": call.session_id,
            "metadata": call.metadata,
            "timestamp": call.timestamp.isoformat(),
        })

        if trace_id not in self._traces:
            self._traces[trace_id] = {"calls": [], "actions": [], "started_at": call.timestamp}
        self._traces[trace_id]["calls"].append(call.call_id)

        return trace_id

    async def trace_agent_action(self, action: AgentAction) -> str:
        trace_id = action.action_id
        self._actions.append(action)

        if not self._enabled:
            return trace_id

        await self._send_to_langfuse({
            "id": trace_id,
            "type": "agent_action",
            "agent_id": action.agent_id,
            "action_type": action.action_type,
            "input": action.input,
            "output": action.output,
            "duration_ms": action.duration_ms,
            "status": action.status,
            "error": action.error,
            "trace_id": action.trace_id,
            "parent_action_id": action.parent_action_id,
            "metadata": action.metadata,
            "timestamp": action.timestamp.isoformat(),
        })

        parent_trace = action.trace_id or trace_id
        if parent_trace not in self._traces:
            self._traces[parent_trace] = {"calls": [], "actions": [], "started_at": action.timestamp}
        self._traces[parent_trace]["actions"].append(action.action_id)

        return trace_id

    async def create_trace(
        self,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        trace_id = str(uuid.uuid4())
        self._traces[trace_id] = {
            "name": name,
            "calls": [],
            "actions": [],
            "metadata": metadata or {},
            "started_at": datetime.utcnow(),
        }

        if self._enabled:
            await self._send_to_langfuse({
                "id": trace_id,
                "type": "trace",
                "name": name,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat(),
            })

        return trace_id

    async def get_cost_report(self, days: int = 30) -> CostReport:
        cutoff = datetime.utcnow() - timedelta(days=days)
        calls = [c for c in self._calls if c.timestamp >= cutoff]

        report = CostReport(period_days=days, total_calls=len(calls))

        daily: dict[str, float] = {}
        for call in calls:
            report.total_cost += call.cost
            report.by_provider[call.provider] = (
                report.by_provider.get(call.provider, 0) + call.cost
            )
            report.by_model[call.model] = (
                report.by_model.get(call.model, 0) + call.cost
            )
            if call.agent_id:
                report.by_agent[call.agent_id] = (
                    report.by_agent.get(call.agent_id, 0) + call.cost
                )

            day_key = call.timestamp.strftime("%Y-%m-%d")
            daily[day_key] = daily.get(day_key, 0) + call.cost

        report.daily_costs = [
            {"date": date, "cost": round(cost, 4)}
            for date, cost in sorted(daily.items())
        ]
        report.avg_cost_per_call = (
            round(report.total_cost / len(calls), 6) if calls else 0.0
        )

        return report

    async def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        return self._traces.get(trace_id)

    async def get_llm_calls(
        self,
        limit: int = 100,
        agent_id: str | None = None,
        model: str | None = None,
    ) -> list[LLMCall]:
        calls = list(self._calls)
        if agent_id:
            calls = [c for c in calls if c.agent_id == agent_id]
        if model:
            calls = [c for c in calls if c.model == model]
        return sorted(calls, key=lambda c: c.timestamp, reverse=True)[:limit]

    async def get_agent_actions(
        self,
        agent_id: str | None = None,
        limit: int = 100,
    ) -> list[AgentAction]:
        actions = list(self._actions)
        if agent_id:
            actions = [a for a in actions if a.agent_id == agent_id]
        return sorted(actions, key=lambda a: a.timestamp, reverse=True)[:limit]

    async def _send_to_langfuse(self, data: dict[str, Any]) -> None:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                }
                if self._public_key and self._secret_key:
                    import base64
                    auth = base64.b64encode(
                        f"{self._public_key}:{self._secret_key}".encode()
                    ).decode()
                    headers["Authorization"] = f"Basic {auth}"
                async with session.post(
                    f"{self._host}/api/public/observations",
                    json=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status not in (200, 201):
                        logger.warning("Langfuse API returned %d", resp.status)
        except ImportError:
            logger.debug("aiohttp not available, skipping Langfuse send")
        except Exception as e:
            logger.debug("Failed to send to Langfuse: %s", e)
