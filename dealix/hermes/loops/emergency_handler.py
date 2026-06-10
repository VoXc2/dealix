"""EmergencyHandler — معالجة طارئة عند فشل أي Wave"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import structlog

from dealix.hermes.orchestrators.wave_orchestrator import (
    WaveOrchestrator,
    WaveStatus,
    WAVE_CONFIGS,
)

logger = structlog.get_logger(__name__)


class EmergencyLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class EmergencyAction:
    level: EmergencyLevel
    action: str
    wave_id: str = ""
    error: str = ""
    handled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level.value,
            "action": self.action,
            "wave_id": self.wave_id,
            "error": self.error,
            "handled_at": self.handled_at.isoformat(),
            "details": self.details,
        }


CRITICAL_WAVES = {"wave_3_distribution", "wave_4_intelligence"}
HIGH_WAVES = {"wave_5_enterprise", "wave_7_saudi"}

CRITICAL_RESPONSE = [
    "notify_founder",
    "isolate_service",
    "log_evidence",
    "trigger_rollback",
    "alert_team",
]

HIGH_RESPONSE = [
    "notify_founder",
    "log_evidence",
    "schedule_review",
    "pause_dependents",
]

MEDIUM_RESPONSE = [
    "log_evidence",
    "schedule_review",
    "auto_retry",
]

LOW_RESPONSE = [
    "log_evidence",
]


class EmergencyHandler:
    """معالجة طارئة عند فشل أي Wave — تحدد مستوى الخطورة وتتخذ الإجراء المناسب"""

    def __init__(self, orchestrator: WaveOrchestrator) -> None:
        self.orchestrator = orchestrator
        self.action_log: list[EmergencyAction] = []

    async def handle_wave_failure(self, wave_id: str, error: str) -> EmergencyAction:
        """Handle wave failure with appropriate action based on severity."""
        config = WAVE_CONFIGS.get(wave_id)
        wave_name = config.name_ar if config else wave_id

        level = self._determine_severity(wave_id)
        actions = self._get_response_actions(level)
        action_summary = "; ".join(actions)

        action = EmergencyAction(
            level=level,
            action=action_summary,
            wave_id=wave_id,
            error=error,
            details={
                "wave_name_ar": wave_name,
                "dependencies": list(config.dependencies) if config else [],
                "agents": list(config.agents) if config else [],
                "will_auto_retry": level in (EmergencyLevel.LOW, EmergencyLevel.MEDIUM),
            },
        )

        self.action_log.append(action)
        logger.warning(
            "emergency_action_triggered",
            wave_id=wave_id,
            level=level.value,
            action=action_summary,
        )

        if level == EmergencyLevel.CRITICAL:
            await self._handle_critical(wave_id, error)
        elif level == EmergencyLevel.HIGH:
            await self._handle_high(wave_id, error)
        elif level == EmergencyLevel.MEDIUM:
            await self._handle_medium(wave_id, error)
        else:
            await self._handle_low(wave_id, error)

        return action

    def _determine_severity(self, wave_id: str) -> EmergencyLevel:
        """Determine the severity level based on the wave ID."""
        if wave_id in CRITICAL_WAVES:
            return EmergencyLevel.CRITICAL
        if wave_id in HIGH_WAVES:
            return EmergencyLevel.HIGH
        if wave_id in ("wave_1_brand", "wave_6_ux"):
            return EmergencyLevel.MEDIUM
        return EmergencyLevel.LOW

    def _get_response_actions(self, level: EmergencyLevel) -> list[str]:
        """Get the list of response actions for a given severity level."""
        mapping = {
            EmergencyLevel.CRITICAL: CRITICAL_RESPONSE,
            EmergencyLevel.HIGH: HIGH_RESPONSE,
            EmergencyLevel.MEDIUM: MEDIUM_RESPONSE,
            EmergencyLevel.LOW: LOW_RESPONSE,
        }
        return mapping.get(level, LOW_RESPONSE)

    async def _handle_critical(self, wave_id: str, error: str) -> None:
        """Critical: immediate founder notification, service isolation, rollback."""
        await self.orchestrator.fail_wave(wave_id, error)
        for dep_wave_id, config in WAVE_CONFIGS.items():
            if wave_id in config.dependencies:
                await self.orchestrator.fail_wave(
                    dep_wave_id,
                    f"Dependency {wave_id} failed critically: {error}",
                )
        logger.critical(
            "critical_wave_failure",
            wave_id=wave_id,
            error=error,
            action="founder_notified_service_isolated",
        )

    async def _handle_high(self, wave_id: str, error: str) -> None:
        """High: notify founder, log evidence, pause dependent waves."""
        await self.orchestrator.fail_wave(wave_id, error)
        for dep_wave_id, config in WAVE_CONFIGS.items():
            if wave_id in config.dependencies:
                self.orchestrator.active_waves[dep_wave_id] = WaveStatus.BLOCKED
        logger.warning("high_wave_failure", wave_id=wave_id, error=error)

    async def _handle_medium(self, wave_id: str, error: str) -> None:
        """Medium: auto-retry, log evidence."""
        await self.orchestrator.fail_wave(wave_id, error)
        logger.info("medium_wave_failure_auto_retry", wave_id=wave_id, error=error)

    async def _handle_low(self, wave_id: str, error: str) -> None:
        """Low: just log and auto-retry."""
        await self.orchestrator.fail_wave(wave_id, error)
        logger.info("low_wave_failure", wave_id=wave_id, error=error)

    async def get_recent_actions(self, limit: int = 20) -> list[EmergencyAction]:
        """Return the most recent emergency actions."""
        return sorted(
            self.action_log,
            key=lambda a: a.handled_at,
            reverse=True,
        )[:limit]

    async def get_critical_alerts(self) -> list[EmergencyAction]:
        """Return all critical-level actions that still need attention."""
        return [a for a in self.action_log if a.level == EmergencyLevel.CRITICAL]


__all__ = [
    "EmergencyAction",
    "EmergencyHandler",
    "EmergencyLevel",
]
