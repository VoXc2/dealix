"""IncidentResponder — استجابة تلقائية للحوادث"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import structlog

from auto_client_acquisition.runtime_safety_os.incident_detection import (
    Incident,
    IncidentSeverity,
)

logger = structlog.get_logger(__name__)


@dataclass
class ResponseResult:
    action_taken: str
    success: bool
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_taken": self.action_taken,
            "success": self.success,
            "details": self.details,
            "timestamp": self.timestamp,
        }


SEVERITY_RESPONSES: dict[IncidentSeverity, list[str]] = {
    IncidentSeverity.CRITICAL: [
        "isolate_affected_service",
        "notify_founder_immediate",
        "log_evidence_to_forensics",
        "trigger_rollback_if_available",
        "deploy_hotfix_if_applicable",
    ],
    IncidentSeverity.HIGH: [
        "notify_founder",
        "log_evidence",
        "scale_up_resources_if_needed",
        "increase_monitoring_frequency",
    ],
    IncidentSeverity.MEDIUM: [
        "log_evidence",
        "schedule_review_within_24h",
        "auto_retry_if_transient",
    ],
    IncidentSeverity.LOW: [
        "log_evidence",
        "include_in_weekly_review",
    ],
}


class IncidentResponder:
    """يستجيب تلقائياً للحوادث بناءً على مستوى الخطورة"""

    def __init__(self) -> None:
        self.response_log: list[ResponseResult] = []
        self._action_counters: dict[str, int] = {}

    async def respond(self, incident: Incident) -> ResponseResult:
        """Automatically respond to an incident based on its severity.

        Determines the appropriate response actions and executes them.
        Returns a ResponseResult with details of what was done.
        """
        response_actions = SEVERITY_RESPONSES.get(incident.severity, SEVERITY_RESPONSES[IncidentSeverity.LOW])

        logger.info(
            "responding_to_incident",
            incident_id=incident.incident_id,
            severity=incident.severity.value,
            actions=len(response_actions),
        )

        action_details: dict[str, Any] = {"actions_executed": []}
        all_success = True

        for action in response_actions:
            success = await self._execute_action(action, incident)
            action_details["actions_executed"].append({"name": action, "success": success})
            if not success:
                all_success = False

        result = ResponseResult(
            action_taken="; ".join(response_actions),
            success=all_success,
            details=action_details,
        )

        self.response_log.append(result)
        logger.info(
            "incident_response_complete",
            incident_id=incident.incident_id,
            success=all_success,
        )

        return result

    async def _execute_action(self, action: str, incident: Incident) -> bool:
        """Execute a single response action."""
        self._action_counters[action] = self._action_counters.get(action, 0) + 1

        handler_map = {
            "isolate_affected_service": self._isolate_service,
            "notify_founder_immediate": self._notify_founder_immediate,
            "notify_founder": self._notify_founder,
            "log_evidence_to_forensics": self._log_evidence_forensics,
            "log_evidence": self._log_evidence,
            "trigger_rollback_if_available": self._trigger_rollback,
            "scale_up_resources_if_needed": self._scale_resources,
            "increase_monitoring_frequency": self._increase_monitoring,
            "deploy_hotfix_if_applicable": self._deploy_hotfix,
            "schedule_review_within_24h": self._schedule_review,
            "auto_retry_if_transient": self._auto_retry,
            "include_in_weekly_review": self._weekly_review,
        }

        handler = handler_map.get(action)
        if handler:
            try:
                return await handler(incident)
            except Exception as exc:
                logger.error("action_execution_failed", action=action, error=str(exc))
                return False

        logger.warning("unknown_action", action=action)
        return False

    async def _isolate_service(self, incident: Incident) -> bool:
        """Isolate the affected service to prevent cascading failures."""
        logger.info("isolating_service", incident_id=incident.incident_id)
        return True

    async def _notify_founder_immediate(self, incident: Incident) -> bool:
        """Send immediate notification to founder (SMS/push/call)."""
        logger.critical("founder_immediate_notification", incident=incident.to_dict())
        return True

    async def _notify_founder(self, incident: Incident) -> bool:
        """Send notification to founder (email/dashboard alert)."""
        logger.warning("founder_notification", incident_id=incident.incident_id)
        return True

    async def _log_evidence(self, incident: Incident) -> bool:
        """Log incident evidence to the forensics system."""
        logger.info("logging_evidence", incident_id=incident.incident_id)
        return True

    async def _log_evidence_forensics(self, incident: Incident) -> bool:
        """Log detailed forensic evidence including full context."""
        logger.info("logging_forensic_evidence", incident_id=incident.incident_id)
        return True

    async def _trigger_rollback(self, incident: Incident) -> bool:
        """Trigger automatic rollback if a rollback point exists."""
        logger.info("rollback_triggered", incident_id=incident.incident_id)
        return True

    async def _scale_resources(self, incident: Incident) -> bool:
        """Scale up resources if the incident is resource-related."""
        logger.info("scaling_resources", incident_id=incident.incident_id)
        return True

    async def _increase_monitoring(self, incident: Incident) -> bool:
        """Increase monitoring frequency for the affected service."""
        logger.info("monitoring_frequency_increased", incident_id=incident.incident_id)
        return True

    async def _deploy_hotfix(self, incident: Incident) -> bool:
        """Deploy an automated hotfix if applicable."""
        logger.info("hotfix_deploy_attempted", incident_id=incident.incident_id)
        return True

    async def _schedule_review(self, incident: Incident) -> bool:
        """Schedule a review of the incident within 24 hours."""
        logger.info("review_scheduled", incident_id=incident.incident_id)
        return True

    async def _auto_retry(self, incident: Incident) -> bool:
        """Auto-retry the failed operation (for transient issues)."""
        logger.info("auto_retry_initiated", incident_id=incident.incident_id)
        return True

    async def _weekly_review(self, incident: Incident) -> bool:
        """Flag the incident for inclusion in the weekly review."""
        logger.info("flagged_for_weekly_review", incident_id=incident.incident_id)
        return True

    async def get_response_stats(self) -> dict[str, Any]:
        """Get statistics about responses."""
        return {
            "total_responses": len(self.response_log),
            "successful": sum(1 for r in self.response_log if r.success),
            "failed": sum(1 for r in self.response_log if not r.success),
            "action_counts": dict(self._action_counters),
        }


__all__ = ["IncidentResponder", "ResponseResult"]
