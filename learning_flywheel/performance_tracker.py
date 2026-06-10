from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DataPoint:
    timestamp: datetime
    value: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TrendData:
    metric: str
    agent_id: str
    data_points: list[DataPoint] = field(default_factory=list)
    current_value: float = 0.0
    previous_value: float = 0.0
    change_percent: float = 0.0
    trend_direction: str = "stable"
    moving_avg_7d: float = 0.0
    moving_avg_30d: float = 0.0
    volatility: float = 0.0


@dataclass
class ComparisonData:
    metric: str
    agent_comparisons: dict[str, dict[str, float]] = field(default_factory=dict)
    best_agent: str | None = None
    worst_agent: str | None = None
    average_value: float = 0.0
    median_value: float = 0.0
    std_deviation: float = 0.0


class PerformanceTracker:
    METRICS = [
        "conversion_rate",
        "response_rate",
        "reply_rate",
        "meeting_rate",
        "close_rate",
    ]

    def __init__(self):
        self._data: dict[str, dict[str, list[DataPoint]]] = {}
        self._aggregates: dict[str, dict[str, dict[str, float]]] = {}

    async def track(
        self,
        metric: str,
        agent_id: str,
        value: float,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if metric not in self.METRICS:
            logger.warning("Unknown metric '%s'. Known: %s", metric, self.METRICS)

        if metric not in self._data:
            self._data[metric] = {}
        if agent_id not in self._data[metric]:
            self._data[metric][agent_id] = []

        point = DataPoint(
            timestamp=datetime.utcnow(),
            value=value,
            metadata=metadata or {},
        )
        self._data[metric][agent_id].append(point)
        logger.debug("Tracked %s=%.4f for agent %s", metric, value, agent_id)

    async def get_trend(
        self,
        metric: str,
        agent_id: str,
        days: int = 30,
    ) -> TrendData:
        cutoff = datetime.utcnow() - timedelta(days=days)
        points = self._data.get(metric, {}).get(agent_id, [])
        filtered = [p for p in points if p.timestamp >= cutoff]

        if not filtered:
            return TrendData(metric=metric, agent_id=agent_id)

        values = [p.value for p in filtered]
        current = values[-1]
        previous = values[0] if len(values) > 1 else current
        change = ((current - previous) / previous * 100) if previous != 0 else 0

        direction = "stable"
        if change > 5:
            direction = "up"
        elif change < -5:
            direction = "down"

        n = len(values)
        ma7 = sum(values[-7:]) / min(7, n) if n >= 1 else current
        ma30 = sum(values) / n

        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        volatility = variance ** 0.5

        return TrendData(
            metric=metric,
            agent_id=agent_id,
            data_points=filtered,
            current_value=current,
            previous_value=previous,
            change_percent=round(change, 2),
            trend_direction=direction,
            moving_avg_7d=round(ma7, 4),
            moving_avg_30d=round(ma30, 4),
            volatility=round(volatility, 4),
        )

    async def compare(
        self,
        metric: str,
        agent_ids: list[str],
        days: int = 30,
    ) -> ComparisonData:
        comparisons: dict[str, dict[str, float]] = {}

        for agent_id in agent_ids:
            trend = await self.get_trend(metric, agent_id, days)
            comparisons[agent_id] = {
                "current": trend.current_value,
                "avg_7d": trend.moving_avg_7d,
                "avg_30d": trend.moving_avg_30d,
                "change": trend.change_percent,
                "volatility": trend.volatility,
            }

        current_values = [c["current"] for c in comparisons.values()]
        if not current_values:
            return ComparisonData(metric=metric)

        avg = sum(current_values) / len(current_values)
        sorted_vals = sorted(current_values)
        n = len(sorted_vals)
        median = sorted_vals[n // 2] if n % 2 == 1 else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
        variance = sum((v - avg) ** 2 for v in current_values) / n
        std_dev = variance ** 0.5

        best_agent = max(comparisons, key=lambda a: comparisons[a]["current"])
        worst_agent = min(comparisons, key=lambda a: comparisons[a]["current"])

        return ComparisonData(
            metric=metric,
            agent_comparisons=comparisons,
            best_agent=best_agent,
            worst_agent=worst_agent,
            average_value=round(avg, 4),
            median_value=round(median, 4),
            std_deviation=round(std_dev, 4),
        )

    async def get_metrics_summary(
        self,
        agent_id: str,
        days: int = 7,
    ) -> dict[str, float]:
        summary = {}
        for metric in self.METRICS:
            try:
                trend = await self.get_trend(metric, agent_id, days)
                summary[metric] = trend.current_value
            except Exception:
                summary[metric] = 0.0
        return summary

    async def get_top_performers(
        self,
        metric: str,
        top_n: int = 5,
        days: int = 30,
    ) -> list[dict[str, Any]]:
        all_agents = set()
        if metric in self._data:
            all_agents = set(self._data[metric].keys())

        performers = []
        for agent_id in all_agents:
            trend = await self.get_trend(metric, agent_id, days)
            performers.append({
                "agent_id": agent_id,
                "value": trend.current_value,
                "trend": trend.trend_direction,
                "change": trend.change_percent,
            })

        performers.sort(key=lambda p: p["value"], reverse=True)
        return performers[:top_n]

    async def get_metric_history(
        self,
        metric: str,
        agent_id: str,
        start: datetime,
        end: datetime | None = None,
    ) -> list[DataPoint]:
        end = end or datetime.utcnow()
        points = self._data.get(metric, {}).get(agent_id, [])
        return [p for p in points if start <= p.timestamp <= end]
