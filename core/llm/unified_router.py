from __future__ import annotations

import logging
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TaskType(str, Enum):
    REFACTORING = "refactoring"
    CLASSIFICATION = "classification"
    NEW_FEATURES = "new_features"
    AGENT_CODE = "agent_code"
    SYSTEM_DESIGN = "system_design"
    COMPLIANCE = "compliance"
    EXECUTIVE = "executive"
    STRATEGY = "strategy"
    ANALYSIS = "analysis"
    SUMMARIZATION = "summarization"
    EXTRACTION = "extraction"
    GENERATION = "generation"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: TaskType | str = TaskType.ANALYSIS
    content: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    max_cost: float | None = None
    required_provider: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class RouterDecision:
    task_id: str
    provider: str
    model: str
    gear: str
    estimated_cost: float
    max_tokens: int
    temperature: float
    fallback_chain: list[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class CostEstimate:
    task_id: str
    estimated_input_tokens: int
    estimated_output_tokens: int
    cost_per_1m_input: float
    cost_per_1m_output: float
    estimated_total_cost: float
    gear: str


@dataclass
class UsageSummary:
    total_calls: int = 0
    total_cost: float = 0.0
    by_gear: dict[str, int] = field(default_factory=dict)
    by_provider: dict[str, int] = field(default_factory=dict)
    by_model: dict[str, int] = field(default_factory=dict)
    failures: int = 0
    since: datetime = field(default_factory=datetime.utcnow)


class DealixRouter:
    GEARS = {
        "daily": {
            "provider": "deepseek",
            "model": "deepseek-chat",
            "cost_per_1m_input": 0.02,
            "cost_per_1m_output": 0.02,
            "for": ["refactoring", "classification"],
            "max_tokens": 8192,
        },
        "power": {
            "provider": "minimax",
            "model": "minimax_m2.5",
            "cost_per_1m_input": 0.15,
            "cost_per_1m_output": 0.15,
            "for": ["new_features", "agent_code"],
            "max_tokens": 16384,
        },
        "architect": {
            "provider": "minimax",
            "model": "minimax_m2.7",
            "cost_per_1m_input": 0.279,
            "cost_per_1m_output": 0.279,
            "for": ["system_design", "compliance"],
            "max_tokens": 32768,
        },
        "strategic": {
            "provider": "anthropic",
            "model": "claude-opus-4",
            "cost_per_1m_input": 15.00,
            "cost_per_1m_output": 75.00,
            "for": ["executive", "strategy"],
            "max_tokens": 65536,
        },
    }

    TASK_TO_GEAR = {
        TaskType.REFACTORING: "daily",
        TaskType.CLASSIFICATION: "daily",
        TaskType.NEW_FEATURES: "power",
        TaskType.AGENT_CODE: "power",
        TaskType.SYSTEM_DESIGN: "architect",
        TaskType.COMPLIANCE: "architect",
        TaskType.EXECUTIVE: "strategic",
        TaskType.STRATEGY: "strategic",
        TaskType.ANALYSIS: "power",
        TaskType.SUMMARIZATION: "daily",
        TaskType.EXTRACTION: "daily",
        TaskType.GENERATION: "power",
    }

    FAILOVER_ORDER = ["daily", "power", "architect", "strategic"]

    def __init__(self):
        self._usage: dict[str, Any] = defaultdict(lambda: {"calls": 0, "cost": 0.0, "failures": 0})
        self._total_calls = 0
        self._total_cost = 0.0
        self._session_start = datetime.utcnow()
        self._call_log: list[dict[str, Any]] = []

    async def route(self, task: Task) -> RouterDecision:
        gear_name = self._select_gear(task)
        gear = self.GEARS[gear_name]

        if task.required_provider and gear["provider"] != task.required_provider:
            for fallback_gear in self.FAILOVER_ORDER:
                if self.GEARS[fallback_gear]["provider"] == task.required_provider:
                    gear_name = fallback_gear
                    gear = self.GEARS[fallback_gear]
                    break

        estimated_cost = self._estimate_call_cost(task, gear)
        if task.max_cost is not None and estimated_cost > task.max_cost:
            for cheaper in self.FAILOVER_ORDER:
                cheaper_gear = self.GEARS[cheaper]
                cheaper_cost = self._estimate_call_cost(task, cheaper_gear)
                if cheaper_cost <= task.max_cost:
                    gear_name = cheaper
                    gear = cheaper_gear
                    estimated_cost = cheaper_cost
                    break

        fallback_chain = self._build_fallback_chain(gear_name)
        temp = self._select_temperature(task, gear)

        return RouterDecision(
            task_id=task.id,
            provider=gear["provider"],
            model=gear["model"],
            gear=gear_name,
            estimated_cost=estimated_cost,
            max_tokens=min(task.max_tokens, gear["max_tokens"]),
            temperature=temp,
            fallback_chain=fallback_chain,
            confidence=self._calculate_confidence(task, gear_name),
        )

    async def route_with_fallback(self, task: Task) -> RouterDecision:
        primary = await self.route(task)
        if primary.fallback_chain:
            logger.info(
                "Task %s routed to %s with fallback chain: %s",
                task.id, primary.gear, primary.fallback_chain,
            )
        self._log_call(task, primary)
        return primary

    def estimate_cost(self, task: Task) -> CostEstimate:
        gear_name = self._select_gear(task)
        gear = self.GEARS[gear_name]

        input_tokens = len(task.content.split()) * 1.3
        output_tokens = task.max_tokens // 2

        estimated = (
            (input_tokens / 1_000_000) * gear["cost_per_1m_input"]
            + (output_tokens / 1_000_000) * gear["cost_per_1m_output"]
        )

        return CostEstimate(
            task_id=task.id,
            estimated_input_tokens=int(input_tokens),
            estimated_output_tokens=output_tokens,
            cost_per_1m_input=gear["cost_per_1m_input"],
            cost_per_1m_output=gear["cost_per_1m_output"],
            estimated_total_cost=round(estimated, 6),
            gear=gear_name,
        )

    def get_usage_summary(self) -> UsageSummary:
        summary = UsageSummary(since=self._session_start)
        for gear_name, gear in self.GEARS.items():
            data = self._usage[gear_name]
            summary.total_calls += data["calls"]
            summary.total_cost += data["cost"]
            summary.failures += data["failures"]
            summary.by_gear[gear_name] = data["calls"]
            summary.by_provider[gear["provider"]] = (
                summary.by_provider.get(gear["provider"], 0) + data["calls"]
            )
            summary.by_model[gear["model"]] = (
                summary.by_model.get(gear["model"], 0) + data["calls"]
            )
        return summary

    def get_call_log(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        return self._call_log[offset : offset + limit]

    def record_failure(self, task_id: str) -> None:
        for gear_name in self._usage:
            if gear_name in task_id:
                self._usage[gear_name]["failures"] += 1
                self._usage[gear_name]["calls"] += 1
                break

    def reset_usage(self) -> None:
        self._usage.clear()
        self._total_calls = 0
        self._total_cost = 0.0

    def _select_gear(self, task: Task) -> str:
        task_type = task.type if isinstance(task.type, TaskType) else TaskType(task.type)
        return self.TASK_TO_GEAR.get(task_type, "power")

    def _estimate_call_cost(self, task: Task, gear: dict) -> float:
        input_chars = len(task.content)
        input_tokens = input_chars / 4
        output_tokens = task.max_tokens
        cost = (
            (input_tokens / 1_000_000) * gear["cost_per_1m_input"]
            + (output_tokens / 1_000_000) * gear["cost_per_1m_output"]
        )
        return round(cost, 6)

    def _build_fallback_chain(self, gear_name: str) -> list[str]:
        idx = self.FAILOVER_ORDER.index(gear_name)
        return self.FAILOVER_ORDER[idx + 1 :]

    def _select_temperature(self, task: Task, gear: dict) -> float:
        if task.temperature != 0.7:
            return task.temperature
        creative_types = {TaskType.NEW_FEATURES, TaskType.GENERATION, TaskType.STRATEGY}
        if isinstance(task.type, TaskType) and task.type in creative_types:
            return 0.8
        precise_types = {TaskType.CLASSIFICATION, TaskType.EXTRACTION, TaskType.COMPLIANCE}
        if isinstance(task.type, TaskType) and task.type in precise_types:
            return 0.1
        return 0.3

    def _calculate_confidence(self, task: Task, gear_name: str) -> float:
        base = 0.95
        task_type = task.type if isinstance(task.type, TaskType) else TaskType(task.type)
        gear = self.GEARS[gear_name]
        if task_type.value in gear["for"]:
            base += 0.04
        usage = self._usage[gear_name]
        if usage["failures"] > 10 and usage["calls"] > 0:
            failure_rate = usage["failures"] / usage["calls"]
            base -= failure_rate * 0.5
        return max(0.5, min(1.0, base))

    def _log_call(self, task: Task, decision: RouterDecision) -> None:
        self._usage[decision.gear]["calls"] += 1
        self._usage[decision.gear]["cost"] += decision.estimated_cost
        self._total_calls += 1
        self._total_cost += decision.estimated_cost

        self._call_log.append({
            "task_id": task.id,
            "task_type": task.type.value if isinstance(task.type, TaskType) else task.type,
            "gear": decision.gear,
            "provider": decision.provider,
            "model": decision.model,
            "estimated_cost": decision.estimated_cost,
            "confidence": decision.confidence,
            "timestamp": datetime.utcnow().isoformat(),
        })

        if len(self._call_log) > 10000:
            self._call_log = self._call_log[-5000:]
