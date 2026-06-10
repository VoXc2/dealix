from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class LearningEventType(str, Enum):
    PERFORMANCE_DROP = "performance_drop"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    USER_FEEDBACK = "user_feedback"
    ERROR_SPIKE = "error_spike"
    LATENCY_INCREASE = "latency_increase"
    COST_INCREASE = "cost_increase"
    AB_TEST_WINNER = "ab_test_winner"
    NEW_PATTERN = "new_pattern"


class AdaptationType(str, Enum):
    PROMPT_TWEAK = "prompt_tweak"
    MODEL_DOWNGRADE = "model_downgrade"
    MODEL_UPGRADE = "model_upgrade"
    TEMPERATURE_ADJUST = "temperature_adjust"
    ROUTING_CHANGE = "routing_change"
    TIMEOUT_ADJUST = "timeout_adjust"
    RETRY_CONFIG = "retry_config"
    BEHAVIOR_OVERRIDE = "behavior_override"


class AdaptationScope(str, Enum):
    AGENT = "agent"
    CUSTOMER = "customer"
    GLOBAL = "global"
    TASK_TYPE = "task_type"


@dataclass
class LearningEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: LearningEventType = LearningEventType.PERFORMANCE_DROP
    agent_id: str = ""
    metric: str = ""
    old_value: float = 0.0
    new_value: float = 0.0
    threshold: float = 0.0
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BehaviorChange:
    change_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    adaptation_type: AdaptationType = AdaptationType.PROMPT_TWEAK
    scope: AdaptationScope = AdaptationScope.AGENT
    target_id: str = ""
    config_changes: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    confidence: float = 0.0
    auto_appliable: bool = False
    risk_level: str = "low"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Adaptation:
    adaptation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    change: BehaviorChange | None = None
    applied_at: datetime | None = None
    active: bool = True
    metrics_before: dict[str, float] = field(default_factory=dict)
    metrics_after: dict[str, float] = field(default_factory=dict)
    rollback_at: datetime | None = None


@dataclass
class AdaptationResult:
    adaptation_id: str
    success: bool
    message: str
    applied_changes: dict[str, Any] = field(default_factory=dict)


class BehaviorAdapter:
    def __init__(self):
        self._adaptations: dict[str, Adaptation] = {}
        self._event_log: list[LearningEvent] = []
        self._rules: list[dict[str, Any]] = [
            {
                "event_type": LearningEventType.PERFORMANCE_DROP,
                "adaptation_type": AdaptationType.PROMPT_TWEAK,
                "confidence": 0.6,
                "risk": "low",
            },
            {
                "event_type": LearningEventType.ERROR_SPIKE,
                "adaptation_type": AdaptationType.MODEL_DOWNGRADE,
                "confidence": 0.7,
                "risk": "medium",
            },
            {
                "event_type": LearningEventType.COST_INCREASE,
                "adaptation_type": AdaptationType.MODEL_DOWNGRADE,
                "confidence": 0.8,
                "risk": "low",
            },
            {
                "event_type": LearningEventType.AB_TEST_WINNER,
                "adaptation_type": AdaptationType.ROUTING_CHANGE,
                "confidence": 0.9,
                "risk": "low",
            },
        ]

    async def process_event(self, event: LearningEvent) -> BehaviorChange | None:
        self._event_log.append(event)
        change = self._match_rule(event)
        if change:
            logger.info(
                "Event %s matched rule -> %s for agent %s",
                event.event_type.value, change.adaptation_type.value, event.agent_id,
            )
        return change

    async def adapt_agent(
        self,
        agent_id: str,
        change: BehaviorChange,
    ) -> AdaptationResult:
        adaptation = Adaptation(
            change=change,
            applied_at=datetime.utcnow(),
            metrics_before={},
        )
        self._adaptations[adaptation.adaptation_id] = adaptation

        if change.scope == AdaptationScope.AGENT:
            adaptation.metrics_before = await self._capture_metrics(agent_id)
            logger.info(
                "Adaptation %s applied to agent %s: %s",
                adaptation.adaptation_id, agent_id, change.config_changes,
            )
        elif change.scope == AdaptationScope.GLOBAL:
            logger.info(
                "Global adaptation %s applied: %s",
                adaptation.adaptation_id, change.config_changes,
            )

        return AdaptationResult(
            adaptation_id=adaptation.adaptation_id,
            success=True,
            message=f"Applied {change.adaptation_type.value} to {change.scope.value} '{change.target_id}'",
            applied_changes=change.config_changes,
        )

    async def get_active_adaptations(self) -> list[Adaptation]:
        return [
            a for a in self._adaptations.values()
            if a.active and a.rollback_at is None
        ]

    async def get_adaptation(self, adaptation_id: str) -> Adaptation | None:
        return self._adaptations.get(adaptation_id)

    async def get_adaptations_for_agent(self, agent_id: str) -> list[Adaptation]:
        return [
            a for a in self._adaptations.values()
            if a.change and a.change.target_id == agent_id
        ]

    async def _capture_metrics(self, agent_id: str) -> dict[str, float]:
        return {
            "latency_ms": 0.0,
            "success_rate": 1.0,
            "avg_tokens": 0,
        }

    def _match_rule(self, event: LearningEvent) -> BehaviorChange | None:
        for rule in self._rules:
            if rule["event_type"] != event.event_type:
                continue
            return BehaviorChange(
                adaptation_type=rule["adaptation_type"],
                target_id=event.agent_id,
                config_changes=self._generate_config(event, rule),
                reason=f"Automated response to {event.event_type.value}: "
                       f"{event.metric} changed from {event.old_value} to {event.new_value}",
                confidence=rule["confidence"],
                auto_appliable=rule["risk"] == "low",
                risk_level=rule["risk"],
            )
        return None

    def _generate_config(
        self,
        event: LearningEvent,
        rule: dict[str, Any],
    ) -> dict[str, Any]:
        base = {"trigger_metric": event.metric, "trigger_event": event.event_type.value}
        if rule["adaptation_type"] == AdaptationType.TEMPERATURE_ADJUST:
            base["temperature"] = max(0.0, min(2.0, event.new_value - 0.1))
        elif rule["adaptation_type"] == AdaptationType.TIMEOUT_ADJUST:
            base["timeout_ms"] = int(max(5000, event.new_value * 1.5))
        elif rule["adaptation_type"] == AdaptationType.MODEL_DOWNGRADE:
            base["model_downgrade"] = True
            base["reason"] = "Cost/error optimization"
        return base
