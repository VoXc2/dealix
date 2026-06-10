from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from .unified_router import Task

logger = logging.getLogger(__name__)


class BudgetExceededError(Exception):
    def __init__(self, agent_id: str, budget: Budget, cost: float):
        self.agent_id = agent_id
        self.budget = budget
        self.cost = cost
        super().__init__(
            f"Budget exceeded for agent '{agent_id}': "
            f"available={budget.remaining:.4f}, requested={cost:.4f}"
        )


@dataclass
class Budget:
    daily_limit: float = 10.0
    weekly_limit: float = 50.0
    monthly_limit: float = 200.0
    per_call_limit: float = 5.0
    remaining: float = 200.0
    spent_today: float = 0.0
    spent_this_week: float = 0.0
    spent_this_month: float = 0.0
    currency: str = "USD"
    alert_threshold: float = 0.8

    def reset_periods(self) -> None:
        self.spent_today = 0.0
        self.spent_this_week = 0.0
        self.spent_this_month = 0.0
        self.remaining = self.monthly_limit


@dataclass
class UsageRecord:
    agent_id: str
    task_id: str
    cost: float
    provider: str
    model: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


class CostBudgetManager:
    def __init__(self, redis_client: Any | None = None):
        self._redis = redis_client
        self._budgets: dict[str, Budget] = {}
        self._usage_log: list[UsageRecord] = []
        self._lock = asyncio.Lock()

    async def check_budget(self, agent_id: str, task: Task) -> bool:
        budget = await self.get_budget(agent_id)
        estimated_cost = self._estimate_task_cost(task)

        if estimated_cost > budget.per_call_limit:
            logger.warning(
                "Task cost %.4f exceeds per-call limit %.4f for agent '%s'",
                estimated_cost, budget.per_call_limit, agent_id,
            )
            return False

        if estimated_cost > budget.remaining:
            logger.warning(
                "Insufficient remaining budget for agent '%s': "
                "need %.4f, have %.4f",
                agent_id, estimated_cost, budget.remaining,
            )
            return False

        if budget.spent_today + estimated_cost > budget.daily_limit:
            logger.warning(
                "Daily limit would be exceeded for agent '%s'",
                agent_id,
            )
            return False

        return True

    async def deduct(self, agent_id: str, cost: float) -> None:
        async with self._lock:
            budget = await self.get_budget(agent_id)
            budget.remaining -= cost
            budget.spent_today += cost
            budget.spent_this_week += cost
            budget.spent_this_month += cost

            self._budgets[agent_id] = budget

            if budget.remaining / budget.monthly_limit < budget.alert_threshold:
                logger.info(
                    "Agent '%s' has used %.0f%% of monthly budget "
                    "(remaining: %.2f)",
                    agent_id,
                    (1 - budget.remaining / budget.monthly_limit) * 100,
                    budget.remaining,
                )

    async def get_budget(self, agent_id: str) -> Budget:
        if agent_id in self._budgets:
            return self._budgets[agent_id]
        budget = Budget()
        self._budgets[agent_id] = budget
        return budget

    async def set_budget(self, agent_id: str, budget: Budget) -> None:
        async with self._lock:
            self._budgets[agent_id] = budget
        logger.info("Budget set for agent '%s': %s", agent_id, budget)

    async def log_usage(
        self,
        agent_id: str,
        task_id: str,
        cost: float,
        provider: str,
        model: str,
    ) -> None:
        record = UsageRecord(
            agent_id=agent_id,
            task_id=task_id,
            cost=cost,
            provider=provider,
            model=model,
        )
        self._usage_log.append(record)
        if len(self._usage_log) > 100000:
            self._usage_log = self._usage_log[-50000:]

    async def get_usage(
        self,
        agent_id: str,
        days: int = 7,
    ) -> list[UsageRecord]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            r for r in self._usage_log
            if r.agent_id == agent_id and r.timestamp >= cutoff
        ]

    async def get_total_spend(self, agent_id: str) -> float:
        budget = await self.get_budget(agent_id)
        return budget.monthly_limit - budget.remaining

    async def enforce_budget(self, agent_id: str, task: Task) -> None:
        allowed = await self.check_budget(agent_id, task)
        if not allowed:
            budget = await self.get_budget(agent_id)
            estimated_cost = self._estimate_task_cost(task)
            raise BudgetExceededError(agent_id, budget, estimated_cost)

    async def reset_budgets(self) -> None:
        async with self._lock:
            for agent_id in self._budgets:
                self._budgets[agent_id].reset_periods()
        logger.info("All budgets have been reset")

    def _estimate_task_cost(self, task: Task) -> float:
        input_tokens = len(task.content) / 4
        output_tokens = task.max_tokens
        return ((input_tokens + output_tokens) / 1_000_000) * 0.15
