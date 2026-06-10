from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ModelInfo:
    model_id: str
    provider: str
    name: str
    version: str
    cost_per_1m_input: float
    cost_per_1m_output: float
    context_window: int
    max_output_tokens: int
    capabilities: list[str] = field(default_factory=list)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelPerformance:
    model_id: str
    avg_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    success_rate: float = 1.0
    total_calls: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    avg_tokens_per_call: int = 0
    error_rate: float = 0.0
    last_evaluated: datetime = field(default_factory=datetime.utcnow)
    metrics: dict[str, float] = field(default_factory=dict)


@dataclass
class ComparisonReport:
    model_ids: list[str]
    best_latency: str | None = None
    best_cost_efficiency: str | None = None
    highest_success_rate: str | None = None
    recommendations: list[str] = field(default_factory=list)
    comparisons: dict[str, dict[str, Any]] = field(default_factory=dict)


class ModelRegistry:
    def __init__(self):
        self._models: dict[str, ModelInfo] = {}
        self._performance: dict[str, ModelPerformance] = {}
        self._call_history: list[dict[str, Any]] = []

    async def register(self, model: ModelInfo) -> None:
        self._models[model.model_id] = model
        if model.model_id not in self._performance:
            self._performance[model.model_id] = ModelPerformance(
                model_id=model.model_id,
            )
        logger.info("Registered model: %s (%s v%s)", model.name, model.provider, model.version)

    async def get_model(self, model_id: str) -> ModelInfo | None:
        return self._models.get(model_id)

    async def get_performance(self, model_id: str) -> ModelPerformance:
        if model_id not in self._performance:
            self._performance[model_id] = ModelPerformance(model_id=model_id)
        return self._performance[model_id]

    async def record_call(
        self,
        model_id: str,
        latency_ms: float,
        tokens_used: int,
        cost: float,
        success: bool,
        error: str | None = None,
    ) -> None:
        perf = await self.get_performance(model_id)
        prev_total = perf.total_calls
        perf.total_calls += 1
        perf.total_tokens += tokens_used
        perf.total_cost += cost
        perf.avg_latency_ms = (
            (perf.avg_latency_ms * prev_total + latency_ms) / perf.total_calls
            if perf.total_calls > 0
            else latency_ms
        )
        perf.avg_tokens_per_call = perf.total_tokens // perf.total_calls if perf.total_calls > 0 else 0
        perf.p99_latency_ms = max(perf.p99_latency_ms, latency_ms)
        perf.success_rate = (
            (perf.success_rate * prev_total + (1.0 if success else 0.0)) / perf.total_calls
            if perf.total_calls > 0
            else (1.0 if success else 0.0)
        )
        perf.error_rate = 1.0 - perf.success_rate
        perf.last_evaluated = datetime.utcnow()

        self._call_history.append({
            "model_id": model_id,
            "latency_ms": latency_ms,
            "tokens_used": tokens_used,
            "cost": cost,
            "success": success,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        })

        if len(self._call_history) > 100000:
            self._call_history = self._call_history[-50000:]

    async def compare_models(self, model_ids: list[str]) -> ComparisonReport:
        report = ComparisonReport(model_ids=model_ids)
        best_latency = float("inf")
        best_cost = float("inf")
        best_success = 0.0

        for mid in model_ids:
            model = self._models.get(mid)
            perf = await self.get_performance(mid)
            info = {
                "model_id": mid,
                "name": model.name if model else "unknown",
                "provider": model.provider if model else "unknown",
                "version": model.version if model else "unknown",
                "total_calls": perf.total_calls,
                "avg_latency_ms": perf.avg_latency_ms,
                "p99_latency_ms": perf.p99_latency_ms,
                "success_rate": perf.success_rate,
                "error_rate": perf.error_rate,
                "total_cost": perf.total_cost,
                "avg_cost_per_call": perf.total_cost / perf.total_calls if perf.total_calls > 0 else 0,
                "avg_tokens_per_call": perf.avg_tokens_per_call,
            }
            report.comparisons[mid] = info

            if perf.avg_latency_ms < best_latency and perf.total_calls > 0:
                best_latency = perf.avg_latency_ms
                report.best_latency = mid
            cost_per_call = perf.total_cost / perf.total_calls if perf.total_calls > 0 else float("inf")
            if cost_per_call < best_cost and perf.total_calls > 0:
                best_cost = cost_per_call
                report.best_cost_efficiency = mid
            if perf.success_rate > best_success and perf.total_calls > 0:
                best_success = perf.success_rate
                report.highest_success_rate = mid

        if report.best_cost_efficiency:
            report.recommendations.append(
                f"Most cost-efficient: {report.best_cost_efficiency}"
            )
        if report.best_latency:
            report.recommendations.append(
                f"Lowest latency: {report.best_latency}"
            )
        if report.highest_success_rate:
            report.recommendations.append(
                f"Highest success rate: {report.highest_success_rate}"
            )

        return report

    async def list_models(self) -> list[ModelInfo]:
        return list(self._models.values())

    async def get_models_by_provider(self, provider: str) -> list[ModelInfo]:
        return [m for m in self._models.values() if m.provider == provider]

    async def get_models_by_capability(self, capability: str) -> list[ModelInfo]:
        return [m for m in self._models.values() if capability in m.capabilities]
