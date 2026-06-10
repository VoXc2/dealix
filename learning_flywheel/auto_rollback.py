from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class RollbackStatus(str, Enum):
    MONITORING = "monitoring"
    TRIGGERED = "triggered"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class RollbackDecision:
    adaptation_id: str
    should_rollback: bool
    degradation: float
    threshold: float
    reason: str
    status: RollbackStatus = RollbackStatus.MONITORING
    current_metrics: dict[str, float] = field(default_factory=dict)
    baseline_metrics: dict[str, float] = field(default_factory=dict)


@dataclass
class RollbackResult:
    adaptation_id: str
    success: bool
    status: RollbackStatus
    previous_config: dict[str, Any] = field(default_factory=dict)
    restored_config: dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


class AutoRollback:
    THRESHOLD = 0.15

    def __init__(self):
        self._rollbacks: dict[str, RollbackDecision] = {}
        self._history: dict[str, list[RollbackResult]] = {}
        self._baselines: dict[str, dict[str, float]] = {}

    async def monitor(self, adaptation_id: str) -> RollbackDecision:
        current_metrics = await self._collect_current_metrics(adaptation_id)
        baseline = self._baselines.get(adaptation_id, self._default_baseline())
        degradation = self._calculate_degradation(current_metrics, baseline)

        logger.debug(
            "Monitoring adaptation %s: degradation=%.2f%% (threshold=%.0f%%)",
            adaptation_id, degradation * 100, self.THRESHOLD * 100,
        )

        decision = RollbackDecision(
            adaptation_id=adaptation_id,
            should_rollback=degradation > self.THRESHOLD,
            degradation=degradation,
            threshold=self.THRESHOLD,
            reason=self._build_reason(degradation, current_metrics, baseline),
            status=RollbackStatus.TRIGGERED if degradation > self.THRESHOLD else RollbackStatus.MONITORING,
            current_metrics=current_metrics,
            baseline_metrics=baseline,
        )

        self._rollbacks[adaptation_id] = decision
        return decision

    async def rollback(self, adaptation_id: str) -> RollbackResult:
        import time
        start = time.time()

        decision = self._rollbacks.get(adaptation_id)
        if not decision:
            return RollbackResult(
                adaptation_id=adaptation_id,
                success=False,
                status=RollbackStatus.FAILED,
                error="No monitoring data found",
            )

        if not decision.should_rollback:
            return RollbackResult(
                adaptation_id=adaptation_id,
                success=True,
                status=RollbackStatus.SKIPPED,
                error="Degradation below threshold, rollback not needed",
            )

        try:
            decision.status = RollbackStatus.IN_PROGRESS
            previous = {"adaptation_id": adaptation_id}
            restored = await self._perform_rollback(adaptation_id)

            duration = time.time() - start
            result = RollbackResult(
                adaptation_id=adaptation_id,
                success=True,
                status=RollbackStatus.COMPLETED,
                previous_config=previous,
                restored_config=restored,
                duration_seconds=round(duration, 3),
            )

            decision.status = RollbackStatus.COMPLETED
            logger.info(
                "Rollback completed for adaptation %s in %.2fs",
                adaptation_id, duration,
            )

        except Exception as e:
            logger.exception("Rollback failed for adaptation %s", adaptation_id)
            result = RollbackResult(
                adaptation_id=adaptation_id,
                success=False,
                status=RollbackStatus.FAILED,
                error=str(e),
            )
            decision.status = RollbackStatus.FAILED

        if adaptation_id not in self._history:
            self._history[adaptation_id] = []
        self._history[adaptation_id].append(result)

        return result

    async def set_baseline(
        self,
        adaptation_id: str,
        metrics: dict[str, float],
    ) -> None:
        self._baselines[adaptation_id] = metrics
        logger.debug("Set baseline for adaptation %s: %s", adaptation_id, metrics)

    async def get_rollback_history(
        self,
        adaptation_id: str,
    ) -> list[RollbackResult]:
        return self._history.get(adaptation_id, [])

    async def get_decision(self, adaptation_id: str) -> RollbackDecision | None:
        return self._rollbacks.get(adaptation_id)

    async def _collect_current_metrics(
        self,
        adaptation_id: str,
    ) -> dict[str, float]:
        return {
            "latency_ms": 0.0,
            "success_rate": 1.0,
            "error_rate": 0.0,
            "avg_tokens": 0.0,
            "cost_per_call": 0.0,
        }

    def _calculate_degradation(
        self,
        current: dict[str, float],
        baseline: dict[str, float],
    ) -> float:
        degradations = []
        for key in baseline:
            if key not in current or baseline[key] == 0:
                continue
            if key == "success_rate":
                if current[key] < baseline[key]:
                    degradations.append((baseline[key] - current[key]) / baseline[key])
            elif key == "error_rate":
                if current[key] > baseline[key]:
                    degradations.append((current[key] - baseline[key]) / max(baseline[key], 0.01))
            elif current[key] > baseline[key] * 1.1:
                degradations.append((current[key] - baseline[key]) / baseline[key])
        return max(degradations) if degradations else 0.0

    def _build_reason(
        self,
        degradation: float,
        current: dict[str, float],
        baseline: dict[str, float],
    ) -> str:
        parts = [f"Overall degradation: {degradation:.1%}"]
        for key in baseline:
            if key in current and key == "success_rate":
                change = current[key] - baseline[key]
                if change < -0.05:
                    parts.append(f"{key}: {baseline[key]:.2f} -> {current[key]:.2f}")
            elif key in current:
                change = (current[key] - baseline[key]) / baseline[key] if baseline[key] else 0
                if abs(change) > 0.1:
                    parts.append(f"{key}: {baseline[key]:.2f} -> {current[key]:.2f}")
        return "; ".join(parts)

    def _default_baseline(self) -> dict[str, float]:
        return {
            "latency_ms": 1000.0,
            "success_rate": 0.95,
            "error_rate": 0.05,
            "avg_tokens": 2000,
            "cost_per_call": 0.01,
        }
