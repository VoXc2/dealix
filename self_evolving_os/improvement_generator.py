from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


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
    score: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    source: str = "automated_scan"


class ImprovementGenerator:
    def __init__(self):
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
        logger.info("Scan generated %d improvement proposals", len(prioritized))
        return prioritized

    async def generate_proposal(
        self,
        signal: ImprovementSignal,
    ) -> ImprovementProposal:
        category = self._signal_to_category(signal)
        risk = self._assess_risk(signal)
        config_changes = self._generate_config(signal)
        title = f"Improve {signal.metric}: {signal.current_value:.2f} -> {signal.expected_value:.2f}"
        description = (
            f"Detected gap of {signal.gap:.2%} in '{signal.metric}'. "
            f"Current: {signal.current_value:.4f}, Expected: {signal.expected_value:.4f}. "
            f"Source: {signal.source}"
        )

        return ImprovementProposal(
            title=title,
            description=description,
            category=category,
            risk_level=risk,
            expected_impact=signal.gap,
            auto_appliable=risk in (RiskLevel.LOW,),
            config_changes=config_changes,
            rollback_plan=f"Revert config changes for {signal.metric}",
            signals=[signal],
            score=self._calculate_score(signal, risk),
        )

    async def prioritize(
        self,
        proposals: list[ImprovementProposal],
    ) -> list[ImprovementProposal]:
        scored = sorted(proposals, key=lambda p: p.score, reverse=True)
        for i, p in enumerate(scored):
            p.score = max(0.0, p.score - (i * 0.05))
        return sorted(scored, key=lambda p: p.score, reverse=True)

    async def get_proposals(
        self,
        category: ImprovementCategory | None = None,
        risk_level: RiskLevel | None = None,
        limit: int = 50,
    ) -> list[ImprovementProposal]:
        results = list(self._generated_proposals)
        if category:
            results = [p for p in results if p.category == category]
        if risk_level:
            results = [p for p in results if p.risk_level == risk_level]
        return sorted(results, key=lambda p: p.score, reverse=True)[:limit]

    async def get_proposal(self, proposal_id: str) -> ImprovementProposal | None:
        for p in self._generated_proposals:
            if p.proposal_id == proposal_id:
                return p
        return None

    async def _run_scanner(
        self,
        scanner: dict[str, Any],
    ) -> ImprovementSignal | None:
        current_value = await self._get_metric_value(scanner["metric"])
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
            threshold * 0.8 if scanner["metric"] in ("error_rate", "avg_latency_ms", "cost_per_call")
            else min(1.0, threshold * 1.15)
        )

        return ImprovementSignal(
            source=scanner["name"],
            metric=scanner["metric"],
            current_value=current_value,
            expected_value=expected,
            gap=gap,
            context={"threshold": threshold, "scanner": scanner["name"]},
        )

    async def _get_metric_value(self, metric: str) -> float:
        simulated = {
            "avg_latency_ms": 1500.0,
            "error_rate": 0.05,
            "cost_per_call": 0.02,
            "success_rate": 0.92,
        }
        return simulated.get(metric, 0.0)

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
        if len(proposals) >= 3:
            categories = [p.category for p in proposals]
            freq = {}
            for cat in categories:
                freq[cat] = freq.get(cat, 0) + 1
            for cat, count in freq.items():
                if count >= 2:
                    recurring = [p for p in proposals if p.category == cat]
                    combined = ImprovementProposal(
                        title=f"Multiple {cat.value} improvements detected",
                        description=f"Found {count} related improvement signals in {cat.value}",
                        category=cat,
                        risk_level=RiskLevel.MEDIUM,
                        expected_impact=sum(p.expected_impact for p in recurring) / len(recurring),
                        auto_appliable=False,
                        config_changes={"pattern_detected": True, "count": count},
                        source="pattern_detection",
                    )
                    proposals.append(combined)
