"""PostMortemGenerator — تقرير ما بعد الحادث التلقائي"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Optional

import structlog

from auto_client_acquisition.runtime_safety_os.incident_detection import Incident

logger = structlog.get_logger(__name__)


@dataclass
class TimelineEvent:
    timestamp: str
    event: str
    detail: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"timestamp": self.timestamp, "event": self.event, "detail": self.detail}


@dataclass
class RootCauseAnalysis:
    root_cause: str
    contributing_factors: list[str] = field(default_factory=list)
    why_chain: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_cause": self.root_cause,
            "contributing_factors": self.contributing_factors,
            "why_chain": self.why_chain,
            "evidence": self.evidence,
        }


@dataclass
class ActionItem:
    description: str
    owner: str = "unassigned"
    priority: str = "medium"
    deadline: Optional[str] = None
    status: str = "open"

    def to_dict(self) -> dict[str, Optional[str]]:
        return {
            "description": self.description,
            "owner": self.owner,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
        }


@dataclass
class PostMortem:
    title: str
    incident_id: str
    severity: str
    summary: str
    timeline: list[TimelineEvent] = field(default_factory=list)
    impact: str = ""
    root_cause_analysis: RootCauseAnalysis = field(default_factory=RootCauseAnalysis)
    action_items: list[ActionItem] = field(default_factory=list)
    lessons_learned: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    author: str = "auto_generated"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "incident_id": self.incident_id,
            "severity": self.severity,
            "summary": self.summary,
            "timeline": [t.to_dict() for t in self.timeline],
            "impact": self.impact,
            "root_cause_analysis": self.root_cause_analysis.to_dict(),
            "action_items": [a.to_dict() for a in self.action_items],
            "lessons_learned": self.lessons_learned,
            "generated_at": self.generated_at,
            "author": self.author,
        }


class PostMortemGenerator:
    """يُولد تقارير ما بعد الحادث تلقائياً — تحليل السبب الجذري + توصيات"""

    def __init__(self) -> None:
        self._generated: list[PostMortem] = []

    async def generate(self, incident: Incident) -> PostMortem:
        """Generate a comprehensive post-mortem for an incident.

        Performs automated root cause analysis, builds a timeline,
        and generates action items with lessons learned.
        """
        logger.info("generating_post_mortem", incident_id=incident.incident_id)

        timeline = self._build_timeline(incident)
        root_cause = self._analyze_root_cause(incident)
        impact = self._assess_impact(incident)
        action_items = self._generate_action_items(incident, root_cause)
        lessons = self._extract_lessons(incident, root_cause)

        post_mortem = PostMortem(
            title=f"Post-Mortem: {incident.title}",
            incident_id=incident.incident_id,
            severity=incident.severity.value,
            summary=self._generate_summary(incident, root_cause),
            timeline=timeline,
            impact=impact,
            root_cause_analysis=root_cause,
            action_items=action_items,
            lessons_learned=lessons,
        )

        self._generated.append(post_mortem)
        logger.info("post_mortem_generated", incident_id=incident.incident_id)

        return post_mortem

    def _build_timeline(self, incident: Incident) -> list[TimelineEvent]:
        """Build a timeline of events leading up to and following the incident."""
        events: list[TimelineEvent] = []

        events.append(
            TimelineEvent(
                timestamp=incident.detected_at.isoformat(),
                event="incident_detected",
                detail=f"Pattern '{incident.pattern_matched}' triggered: "
                f"{incident.metric_value} > {incident.threshold}",
            )
        )

        if incident.context:
            for key, value in incident.context.items():
                events.append(
                    TimelineEvent(
                        timestamp=incident.detected_at.isoformat(),
                        event=f"context_{key}",
                        detail=str(value),
                    )
                )

        return events

    def _analyze_root_cause(self, incident: Incident) -> RootCauseAnalysis:
        """Analyze the root cause of the incident."""
        cause_map: dict[str, tuple[str, list[str], list[str]]] = {
            "high_error_rate": (
                "System error rate exceeded threshold due to software defect or resource exhaustion",
                [
                    "Insufficient error handling in critical path",
                    "Missing circuit breakers between services",
                    "Inadequate load testing coverage",
                ],
                [
                    "Why did error rate exceed 5%? → Defect in recently deployed code",
                    "Why was the defect not caught? → Insufficient test coverage",
                    "Why was test coverage inadequate? → Release deadline pressure",
                    "Why was there deadline pressure? → Poor estimation",
                ],
            ),
            "high_api_latency": (
                "API response time degraded due to resource contention or inefficient query patterns",
                [
                    "Missing database query optimization",
                    "Insufficient connection pooling",
                    "No caching layer for frequent queries",
                ],
                [
                    "Why did latency exceed 5s? → Database query slowdown",
                    "Why did queries slow down? → Missing indexes on new tables",
                    "Why were indexes missing? → Schema migration without review",
                ],
            ),
            "payment_failure": (
                "Payment processing failures due to integration or provider issues",
                [
                    "Inadequate payment provider error handling",
                    "Missing retry logic for transient failures",
                    "No payment gateway failover",
                ],
                [
                    "Why did payment failure rate exceed 10%? → Provider timeout",
                    "Why was there no failover? → Single provider dependency",
                    "Why no failover? → MVP timeline constraint",
                ],
            ),
            "auth_failure": (
                "Authentication failures detected — potential security incident or configuration issue",
                [
                    "Expired API tokens or certificates",
                    "Misconfigured identity provider",
                    "Brute force attack attempt",
                ],
                [
                    "Why did auth failure rate exceed 20%? → Expired service account token",
                    "Why was the token not rotated? → No automated rotation policy",
                    "Why no rotation policy? → Not implemented in initial security setup",
                ],
            ),
        }

        cause_data = cause_map.get(incident.pattern_matched)
        if cause_data:
            return RootCauseAnalysis(
                root_cause=cause_data[0],
                contributing_factors=cause_data[1],
                why_chain=cause_data[2],
                evidence=[
                    f"Metric: {incident.metric_value} (threshold: {incident.threshold})",
                    f"Pattern: {incident.pattern_matched}",
                    f"Source: {incident.source}",
                ],
            )

        return RootCauseAnalysis(
            root_cause=f"Unknown root cause for pattern: {incident.pattern_matched}",
            contributing_factors=["Manual investigation required"],
            why_chain=["Automated analysis inconclusive — manual RCA needed"],
            evidence=[f"Detected via pattern: {incident.pattern_matched}"],
        )

    def _assess_impact(self, incident: Incident) -> str:
        """Assess the business and technical impact of the incident."""
        impact_map: dict[str, str] = {
            "high_error_rate": "User-facing errors, potential data inconsistency, degraded experience",
            "high_api_latency": "Slow page loads, timeout errors, poor user experience",
            "payment_failure": "Revenue loss, customer frustration, support tickets",
            "auth_failure": "Legitimate users blocked, potential data exposure risk",
            "low_disk_space": "Potential service outage if disk fills completely",
            "high_memory_usage": "Service crashes, OOM kills, degraded performance",
            "agent_downtime": "Automated operations paused, manual intervention required",
            "queue_backlog": "Delayed processing, SLA breaches, customer impact",
        }

        return impact_map.get(incident.pattern_matched, "Impact assessment requires manual review")

    def _generate_action_items(
        self, incident: Incident, root_cause: RootCauseAnalysis
    ) -> list[ActionItem]:
        """Generate actionable remediation items."""
        action_map: dict[str, list[ActionItem]] = {
            "high_error_rate": [
                ActionItem("Add circuit breakers to all service calls", priority="high"),
                ActionItem("Improve error handling in critical paths", priority="high"),
                ActionItem("Add integration tests for error scenarios", priority="medium"),
            ],
            "high_api_latency": [
                ActionItem("Add database query performance monitoring", priority="high"),
                ActionItem("Implement caching layer for frequent queries", priority="high"),
                ActionItem("Review and optimize N+1 query patterns", priority="medium"),
            ],
            "payment_failure": [
                ActionItem("Implement payment provider failover", priority="critical"),
                ActionItem("Add retry logic with exponential backoff", priority="high"),
                ActionItem("Set up payment monitoring and alerting", priority="high"),
            ],
            "auth_failure": [
                ActionItem("Implement automated certificate rotation", priority="critical"),
                ActionItem("Audit all service account permissions", priority="high"),
                ActionItem("Add rate limiting for auth endpoints", priority="high"),
            ],
        }

        items = action_map.get(incident.pattern_matched, [
            ActionItem(
                "Investigate and document root cause manually",
                priority="high",
                deadline="48h",
            ),
            ActionItem(
                "Implement monitoring for similar patterns",
                priority="medium",
            ),
        ])

        return items

    def _extract_lessons(
        self, incident: Incident, root_cause: RootCauseAnalysis
    ) -> list[str]:
        """Extract lessons learned from the incident."""
        base_lessons = [
            "Automated detection should trigger immediate logging",
            "Post-mortem generation should be immediate and automatic",
            "Action items must have owners and deadlines",
        ]

        specific_lessons: dict[str, list[str]] = {
            "high_error_rate": [
                "Error budgets help balance velocity and reliability",
                "Canary deployments catch errors before full rollout",
            ],
            "payment_failure": [
                "Payment integrations need thorough failure testing",
                "Multiple payment providers reduce single-point-of-failure risk",
            ],
            "auth_failure": [
                "Service account tokens should auto-rotate",
                "Auth monitoring detects attacks early",
            ],
        }

        lessons = base_lessons + specific_lessons.get(incident.pattern_matched, [])
        return lessons

    def _generate_summary(self, incident: Incident, root_cause: RootCauseAnalysis) -> str:
        """Generate an executive summary of the incident."""
        return (
            f"Incident '{incident.title}' detected via pattern '{incident.pattern_matched}' "
            f"with severity {incident.severity.value}. "
            f"Root cause: {root_cause.root_cause}. "
            f"{len(root_cause.contributing_factors)} contributing factors identified. "
            f"Post-mortem generated automatically."
        )

    async def get_post_mortem(self, incident_id: str) -> Optional[PostMortem]:
        """Retrieve a generated post-mortem by incident ID."""
        for pm in self._generated:
            if pm.incident_id == incident_id:
                return pm
        return None

    async def list_recent(self, limit: int = 20) -> list[PostMortem]:
        """List recently generated post-mortems."""
        return sorted(self._generated, key=lambda p: p.generated_at, reverse=True)[:limit]


__all__ = [
    "ActionItem",
    "PostMortem",
    "PostMortemGenerator",
    "RootCauseAnalysis",
    "TimelineEvent",
]
