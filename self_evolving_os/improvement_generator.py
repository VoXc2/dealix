from __future__ import annotations

import inspect
import logging
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImprovementCategory(str, Enum):
    PERFORMANCE = "performance"
    COST = "cost"
    RELIABILITY = "reliability"
    SECURITY = "security"
    USER_EXPERIENCE = "user_experience"
    CODE_QUALITY = "code_quality"
    COMPLIANCE = "compliance"
    SCALABILITY = "scalability"


@dataclass(frozen=True)
class MetricObservation:
    """A measured input that can admit an improvement proposal.

    The legacy package no longer invents measurements. A provider must supply a
    real value plus at least one evidence reference. Synthetic observations are
    allowed for tests/fixtures but cannot enter the real proposal queue.
    """

    value: float
    evidence_refs: tuple[str, ...] = ()
    source: str = ""
    observed_at: datetime | None = None
    synthetic: bool = False

    @property
    def evidence_backed(self) -> bool:
        return bool(tuple(ref.strip() for ref in self.evidence_refs if ref.strip())) and not self.synthetic


MetricProvider = Callable[
    [str],
    MetricObservation | None | Awaitable[MetricObservation | None],
]


@dataclass
class ImprovementSignal:
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    metric: str = ""
    current_value: float = 0.0
    expected_value: float = 0.0
    gap: float = 0.0
    context: dict[str, Any] = field(default_factory=dict)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    evidence_refs: list[str] = field(default_factory=list)
    evidence_state: str = UNKNOWN
    synthetic: bool = False


@dataclass
class ImprovementProposal:
    proposal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    category: ImprovementCategory = ImprovementCategory.PERFORMANCE
    risk_level: RiskLevel = RiskLevel.LOW
    expected_impact: float = 0.0
    implementation_effort: str = "low"
    auto_appliable: bool = False
    config_changes: dict[str, Any] = field(default_factory=dict)
    rollback_plan: str = ""
    signals: list[ImprovementSignal] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    authority_class: str = "APPROVAL_REQUIRED"
    score: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    source: str = "automated_scan"


class ImprovementGenerator:
    """Legacy compatibility scanner with fail-closed evidence semantics.

    Real self-improvement authority belongs to the canonical Development
    Factory. This package may prepare evidence-backed proposals only; it may not
    fabricate telemetry or create apply/commit/merge authority.
    """

    def __init__(self, metric_provider: MetricProvider | None = None):
        self._metric_provider = metric_provider
        self._scan_history: list[datetime] = []
        self._generated_proposals: list[ImprovementProposal] = []
        self._scanners: list[dict[str, Any]] = [
            {
                "name": "latency_scanner",
                "category": ImprovementCategory.PERFORMANCE,
                "metric": "avg_latency_ms",
                "threshold": 2000,
                "risk": RiskLevel.LOW,
            },
            {
                "name": "error_rate_scanner",
                "category": ImprovementCategory.RELIABILITY,
                "metric": "error_rate",
                "threshold": 0.1,
                "risk": RiskLevel.MEDIUM,
            },
            {
                "name": "cost_scanner",
                "category": ImprovementCategory.COST,
                "metric": "cost_per_call",
                "threshold": 0.05,
                "risk": RiskLevel.LOW,
            },
            {
                "name": "success_rate_scanner",
                "category": ImprovementCategory.RELIABILITY,
                "metric": "success_rate",
                "threshold": 0.85,
                "risk": RiskLevel.HIGH,
            },
        ]

    async def scan_for_improvements(self) -> list[ImprovementProposal]:
        self._scan_history.append(datetime.utcnow())
        proposals: list[ImprovementProposal] = []

        for scanner in self._scanners:
            signal = await self._run_scanner(scanner)
            if signal and signal.gap > 0:
                proposal = await self.generate_proposal(signal)
                proposals.append(proposal)

        await self._detect_patterns(proposals)
        prioritized = await self.prioritize(proposals)

        self._generated_proposals.extend(prioritized)
        logger.info("Scan generated %d evidence-backed improvement proposals", len(prioritized))
        return prioritized

    async def generate_proposal(
        self,
        signal: ImprovementSignal,
    ) -> ImprovementProposal:
        if signal.synthetic or not any(ref.strip() for ref in signal.evidence_refs):
            raise ValueError("EVIDENCE_REQUIRED: simulated or source-less signals cannot create real improvements")

        category = self._signal_to_category(signal)
        risk = self._assess_risk(signal)
        config_changes = self._generate_config(signal)
        title = f"Improve {signal.metric}: {signal.current_value:.2f} -> {signal.expected_value:.2f}"
        description = (
            f"Detected evidence-backed gap of {signal.gap:.2%} in '{signal.metric}'. "
            f"Current: {signal.current_value:.4f}, Expected: {signal.expected_value:.4f}. "
            f"Source: {signal.source}"
        )

        refs = sorted({ref.strip() for ref in signal.evidence_refs if ref.strip()})
        return ImprovementProposal(
            title=title,
            description=description,
            category=category,
            risk_level=risk,
            expected_impact=signal.gap,
            auto_appliable=False,
            config_changes=config_changes,
            rollback_plan=f"Revert bounded change for {signal.metric}",
            signals=[signal],
            evidence_refs=refs,
            authority_class="APPROVAL_REQUIRED",
            score=self._calculate_score(signal, risk),
        )

    async def prioritize(
        self,
        proposals: list[ImprovementProposal],
    ) -> list[ImprovementProposal]:
        scored = sorted(proposals, key=lambda p: p.score, reverse=True)
        for i, proposal in enumerate(scored):
            proposal.score = max(0.0, proposal.score - (i * 0.05))
        return sorted(scored, key=lambda proposal: proposal.score, reverse=True)

    async def get_proposals(
        self,
        category: ImprovementCategory | None = None,
        risk_level: RiskLevel | None = None,
        limit: int = 50,
    ) -> list[ImprovementProposal]:
        results = list(self._generated_proposals)
        if category:
            results = [proposal for proposal in results if proposal.category == category]
        if risk_level:
            results = [proposal for proposal in results if proposal.risk_level == risk_level]
        return sorted(results, key=lambda proposal: proposal.score, reverse=True)[:limit]

    async def get_proposal(self, proposal_id: str) -> ImprovementProposal | None:
        for proposal in self._generated_proposals:
            if proposal.proposal_id == proposal_id:
                return proposal
        return None

    async def _run_scanner(
        self,
        scanner: dict[str, Any],
    ) -> ImprovementSignal | None:
        observation = await self._get_metric_observation(scanner["metric"])
        if observation is None:
            logger.debug("Metric %s remains %s", scanner["metric"], UNKNOWN)
            return None
        if not observation.evidence_backed:
            logger.info("Ignoring synthetic or source-less observation for %s", scanner["metric"])
            return None

        current_value = observation.value
        threshold = scanner["threshold"]
        gap = 0.0

        if scanner["metric"] in ("error_rate", "avg_latency_ms", "cost_per_call"):
            if current_value > threshold:
                gap = (current_value - threshold) / threshold
        elif scanner["metric"] == "success_rate":
            if current_value < threshold:
                gap = (threshold - current_value) / threshold

        if gap <= 0:
            return None

        expected = (
            threshold * 0.8
            if scanner["metric"] in ("error_rate", "avg_latency_ms", "cost_per_call")
            else min(1.0, threshold * 1.15)
        )
        refs = sorted({ref.strip() for ref in observation.evidence_refs if ref.strip()})
        return ImprovementSignal(
            source=observation.source or scanner["name"],
            metric=scanner["metric"],
            current_value=current_value,
            expected_value=expected,
            gap=gap,
            context={
                "threshold": threshold,
                "scanner": scanner["name"],
                "observed_at": observation.observed_at.isoformat() if observation.observed_at else UNKNOWN,
            },
            evidence_refs=refs,
            evidence_state="EVIDENCE_BACKED",
            synthetic=False,
        )

    async def _get_metric_observation(self, metric: str) -> MetricObservation | None:
        if self._metric_provider is None:
            return None
        result = self._metric_provider(metric)
        if inspect.isawaitable(result):
            result = await result
        if result is not None and not isinstance(result, MetricObservation):
            raise TypeError("metric_provider must return MetricObservation or None")
        return result

    async def _get_metric_value(self, metric: str) -> float | None:
        """Compatibility helper. Missing evidence remains unknown, never simulated."""
        observation = await self._get_metric_observation(metric)
        return observation.value if observation and observation.evidence_backed else None

    def _signal_to_category(self, signal: ImprovementSignal) -> ImprovementCategory:
        mapping = {
            "avg_latency_ms": ImprovementCategory.PERFORMANCE,
            "error_rate": ImprovementCategory.RELIABILITY,
            "cost_per_call": ImprovementCategory.COST,
            "success_rate": ImprovementCategory.RELIABILITY,
        }
        return mapping.get(signal.metric, ImprovementCategory.PERFORMANCE)

    def _assess_risk(self, signal: ImprovementSignal) -> RiskLevel:
        if signal.metric == "success_rate" and signal.gap > 0.2:
            return RiskLevel.HIGH
        if signal.metric == "error_rate" and signal.gap > 0.5:
            return RiskLevel.MEDIUM
        if signal.gap > 0.3:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _generate_config(self, signal: ImprovementSignal) -> dict[str, Any]:
        config = {"metric": signal.metric, "target": signal.expected_value}
        if signal.metric == "avg_latency_ms":
            config["timeout_ms"] = int(signal.expected_value * 0.8)
            config["max_retries"] = 2
        elif signal.metric == "error_rate":
            config["retry_backoff"] = "exponential"
            config["max_retries"] = 3
        elif signal.metric == "cost_per_call":
            config["preferred_model"] = "cheaper"
            config["cost_limit"] = signal.expected_value
        elif signal.metric == "success_rate":
            config["fallback_enabled"] = True
            config["num_fallbacks"] = 2
        return config

    def _calculate_score(self, signal: ImprovementSignal, risk: RiskLevel) -> float:
        impact_score = min(1.0, signal.gap * 2)
        risk_score = {
            RiskLevel.LOW: 0.9,
            RiskLevel.MEDIUM: 0.6,
            RiskLevel.HIGH: 0.3,
            RiskLevel.CRITICAL: 0.1,
        }.get(risk, 0.5)
        return round(impact_score * risk_score, 4)

    async def _detect_patterns(
        self,
        proposals: list[ImprovementProposal],
    ) -> None:
        if len(proposals) < 3:
            return
        categories = [proposal.category for proposal in proposals]
        frequency: dict[ImprovementCategory, int] = {}
        for category in categories:
            frequency[category] = frequency.get(category, 0) + 1
        for category, count in frequency.items():
            if count < 2:
                continue
            recurring = [proposal for proposal in proposals if proposal.category == category]
            refs = sorted({ref for proposal in recurring for ref in proposal.evidence_refs})
            proposals.append(
                ImprovementProposal(
                    title=f"Multiple {category.value} improvements detected",
                    description=f"Found {count} evidence-backed signals in {category.value}",
                    category=category,
                    risk_level=RiskLevel.MEDIUM,
                    expected_impact=sum(proposal.expected_impact for proposal in recurring) / len(recurring),
                    auto_appliable=False,
                    config_changes={"pattern_detected": True, "count": count},
                    rollback_plan="No automatic application; route through canonical Development Factory",
                    evidence_refs=refs,
                    authority_class="APPROVAL_REQUIRED",
                    source="pattern_detection",
                )
            )
