"""IncidentDetector — كشف تلقائي للحوادث في جميع الأنظمة"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class IncidentSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Incident:
    incident_id: str
    title: str
    description: str
    severity: IncidentSeverity
    source: str
    detected_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    pattern_matched: str = ""
    metric_value: float = 0.0
    threshold: float = 0.0
    context: dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
    resolved: bool = False
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "source": self.source,
            "detected_at": self.detected_at.isoformat(),
            "pattern_matched": self.pattern_matched,
            "metric_value": self.metric_value,
            "threshold": self.threshold,
            "context": self.context,
            "acknowledged": self.acknowledged,
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


PATTERN_RULES: list[dict[str, Any]] = [
    {
        "name": "high_error_rate",
        "pattern": "error_rate > 0.05",
        "severity": IncidentSeverity.CRITICAL,
        "description": "معدل الأخطاء تجاوز 5% — قد يشير إلى خلل في النظام",
        "description_en": "Error rate exceeds 5% — may indicate system malfunction",
        "metric": "error_rate",
        "threshold": 0.05,
    },
    {
        "name": "high_api_latency",
        "pattern": "api_latency > 5000",
        "severity": IncidentSeverity.HIGH,
        "description": "زمن استجابة API تجاوز 5 ثوانٍ",
        "description_en": "API latency exceeds 5 seconds",
        "metric": "api_latency_ms",
        "threshold": 5000,
    },
    {
        "name": "payment_failure",
        "pattern": "payment_failure_rate > 0.1",
        "severity": IncidentSeverity.CRITICAL,
        "description": "معدل فشل المدفوعات تجاوز 10%",
        "description_en": "Payment failure rate exceeds 10%",
        "metric": "payment_failure_rate",
        "threshold": 0.1,
    },
    {
        "name": "auth_failure",
        "pattern": "auth_failure_rate > 0.2",
        "severity": IncidentSeverity.HIGH,
        "description": "معدل فشل المصادقة تجاوز 20% — هجوم محتمل",
        "description_en": "Auth failure rate exceeds 20% — potential attack",
        "metric": "auth_failure_rate",
        "threshold": 0.2,
    },
    {
        "name": "low_disk_space",
        "pattern": "disk_usage > 0.90",
        "severity": IncidentSeverity.MEDIUM,
        "description": "استخدام القرص تجاوز 90%",
        "description_en": "Disk usage exceeds 90%",
        "metric": "disk_usage_pct",
        "threshold": 0.90,
    },
    {
        "name": "high_memory_usage",
        "pattern": "memory_usage > 0.85",
        "severity": IncidentSeverity.MEDIUM,
        "description": "استخدام الذاكرة تجاوز 85%",
        "description_en": "Memory usage exceeds 85%",
        "metric": "memory_usage_pct",
        "threshold": 0.85,
    },
    {
        "name": "agent_downtime",
        "pattern": "agent_uptime < 0.99",
        "severity": IncidentSeverity.CRITICAL,
        "description": "وقت تشغيل الوكيل أقل من 99%",
        "description_en": "Agent uptime below 99%",
        "metric": "agent_uptime_pct",
        "threshold": 0.99,
    },
    {
        "name": "queue_backlog",
        "pattern": "queue_depth > 100",
        "severity": IncidentSeverity.HIGH,
        "description": "عمق قائمة الانتظار تجاوز 100 — تراكم المهام",
        "description_en": "Queue depth exceeds 100 — task backlog",
        "metric": "queue_depth",
        "threshold": 100,
    },
]


class IncidentDetector:
    """يكتشف الحوادث تلقائياً بمسح جميع الأنظمة بشكل دوري"""

    def __init__(self) -> None:
        self.patterns: list[dict[str, Any]] = PATTERN_RULES
        self._detected_incidents: list[Incident] = []
        self._incident_counter: int = 0

    async def scan(self) -> list[Incident]:
        """Scan for incidents across all systems.

        Collects metrics from all monitored sources and checks against
        all defined patterns. Returns newly detected incidents.
        """
        metrics = await self._collect_metrics()
        new_incidents: list[Incident] = []

        for pattern in self.patterns:
            metric_name = pattern["metric"]
            metric_value = metrics.get(metric_name, 0.0)
            threshold = pattern["threshold"]

            if metric_value > threshold:
                incident = self._create_incident(pattern, metric_value)
                self._detected_incidents.append(incident)
                new_incidents.append(incident)
                logger.warning(
                    "incident_detected",
                    pattern=pattern["name"],
                    metric=metric_name,
                    value=metric_value,
                    threshold=threshold,
                )

        return new_incidents

    async def _collect_metrics(self) -> dict[str, float]:
        """Collect metrics from all monitored systems.

        Returns a dict of metric_name -> current value.
        In production, this queries APM, logs, databases, and agents.
        """
        return {
            "error_rate": 0.0,
            "api_latency_ms": 0.0,
            "payment_failure_rate": 0.0,
            "auth_failure_rate": 0.0,
            "disk_usage_pct": 0.0,
            "memory_usage_pct": 0.0,
            "agent_uptime_pct": 100.0,
            "queue_depth": 0,
        }

    def _create_incident(self, pattern: dict[str, Any], metric_value: float) -> Incident:
        """Create an Incident from a matched pattern."""
        self._incident_counter += 1
        return Incident(
            incident_id=f"inc_{self._incident_counter:04d}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            title=pattern.get("description", pattern["name"]),
            description=pattern.get("description_en", pattern["name"]),
            severity=pattern["severity"],
            source="incident_detector",
            pattern_matched=pattern["name"],
            metric_value=metric_value,
            threshold=pattern["threshold"],
        )

    async def get_active_incidents(self) -> list[Incident]:
        """Return all currently active (not resolved) incidents."""
        return [i for i in self._detected_incidents if not i.resolved]

    async def get_incident_history(self, limit: int = 100) -> list[Incident]:
        """Return recent incident history."""
        sorted_incidents = sorted(
            self._detected_incidents,
            key=lambda i: i.detected_at,
            reverse=True,
        )
        return sorted_incidents[:limit]

    async def acknowledge_incident(self, incident_id: str) -> bool:
        """Mark an incident as acknowledged."""
        for inc in self._detected_incidents:
            if inc.incident_id == incident_id:
                inc.acknowledged = True
                logger.info("incident_acknowledged", incident_id=incident_id)
                return True
        return False

    async def resolve_incident(self, incident_id: str) -> bool:
        """Mark an incident as resolved."""
        for inc in self._detected_incidents:
            if inc.incident_id == incident_id:
                inc.resolved = True
                inc.resolved_at = datetime.now(UTC)
                logger.info("incident_resolved", incident_id=incident_id)
                return True
        return False


__all__ = [
    "Incident",
    "IncidentDetector",
    "IncidentSeverity",
    "PATTERN_RULES",
]
