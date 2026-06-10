from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class SLAStatus(str, Enum):
    COMPLIANT = "compliant"
    WARNING = "warning"
    BREACHED = "breached"
    CRITICAL = "critical"


class SLAMetric(str, Enum):
    UPTIME = "uptime"
    LATENCY_P99 = "latency_p99"
    ERROR_RATE = "error_rate"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    AVAILABILITY = "availability"


@dataclass
class SLAContract:
    contract_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str = ""
    customer_name: str = ""
    metrics: dict[SLAMetric, float] = field(default_factory=lambda: {
        SLAMetric.UPTIME: 99.9,
        SLAMetric.LATENCY_P99: 5000,
        SLAMetric.ERROR_RATE: 0.01,
        SLAMetric.AVAILABILITY: 99.9,
    })
    warning_threshold: float = 0.9
    critical_threshold: float = 1.25
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: datetime | None = None
    active: bool = True


@dataclass
class SLABreach:
    breach_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    contract_id: str = ""
    customer_id: str = ""
    metric: SLAMetric = SLAMetric.LATENCY_P99
    expected_value: float = 0.0
    actual_value: float = 0.0
    deviation: float = 0.0
    detected_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: datetime | None = None
    severity: str = "warning"
    details: str = ""


@dataclass
class SLACheckpoint:
    timestamp: datetime
    metric: SLAMetric
    value: float
    compliant: bool


class SLAMonitor:
    def __init__(self):
        self._contracts: dict[str, SLAContract] = {}
        self._breaches: list[SLABreach] = []
        self._checkpoints: list[SLACheckpoint] = []
        self._metrics_log: dict[str, list[dict[str, Any]]] = {}

    async def register_contract(self, contract: SLAContract) -> str:
        self._contracts[contract.contract_id] = contract
        logger.info(
            "Registered SLA contract %s for customer %s",
            contract.contract_id, contract.customer_name,
        )
        return contract.contract_id

    async def check_sla(self, contract: SLAContract) -> SLAStatus:
        violations = 0
        total_metrics = len(contract.metrics)

        for metric, target in contract.metrics.items():
            current_value = await self._get_current_metric(metric)
            is_compliant = await self._check_compliance(metric, current_value, target)

            self._checkpoints.append(SLACheckpoint(
                timestamp=datetime.utcnow(),
                metric=metric,
                value=current_value,
                compliant=is_compliant,
            ))

            if not is_compliant:
                violations += 1
                ratio = current_value / target if target > 0 else float("inf")
                severity = "critical" if ratio > contract.critical_threshold else "warning"
                if severity == "critical":
                    breach = SLABreach(
                        contract_id=contract.contract_id,
                        customer_id=contract.customer_id,
                        metric=metric,
                        expected_value=target,
                        actual_value=current_value,
                        deviation=abs(current_value - target) / target if target > 0 else 0,
                        severity=severity,
                        details=f"Metric {metric.value}: {current_value:.4f} (target: {target:.4f})",
                    )
                    self._breaches.append(breach)
                    logger.warning("SLA breach: %s", breach.details)

        if violations == 0:
            return SLAStatus.COMPLIANT
        violation_rate = violations / total_metrics
        if violation_rate >= 0.5:
            return SLAStatus.CRITICAL
        if violation_rate >= 0.25:
            return SLAStatus.BREACHED
        return SLAStatus.WARNING

    async def get_compliance_rate(
        self,
        customer_id: str,
        days: int = 30,
    ) -> float:
        cutoff = datetime.utcnow() - timedelta(days=days)
        relevant = [
            cp for cp in self._checkpoints
            if cp.timestamp >= cutoff
        ]
        if not relevant:
            return 1.0
        compliant = sum(1 for cp in relevant if cp.compliant)
        return compliant / len(relevant)

    async def get_breaches(
        self,
        customer_id: str,
        resolved: bool | None = None,
    ) -> list[SLABreach]:
        results = [b for b in self._breaches if b.customer_id == customer_id]
        if resolved is not None:
            if resolved:
                results = [b for b in results if b.resolved_at is not None]
            else:
                results = [b for b in results if b.resolved_at is None]
        return results

    async def resolve_breach(self, breach_id: str) -> bool:
        for breach in self._breaches:
            if breach.breach_id == breach_id and breach.resolved_at is None:
                breach.resolved_at = datetime.utcnow()
                logger.info("Resolved SLA breach %s", breach_id)
                return True
        return False

    async def get_contract(self, contract_id: str) -> SLAContract | None:
        return self._contracts.get(contract_id)

    async def get_contracts_for_customer(
        self,
        customer_id: str,
    ) -> list[SLAContract]:
        return [
            c for c in self._contracts.values()
            if c.customer_id == customer_id and c.active
        ]

    async def record_metric(
        self,
        metric: SLAMetric,
        value: float,
        customer_id: str | None = None,
    ) -> None:
        entry = {
            "metric": metric.value,
            "value": value,
            "customer_id": customer_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        if customer_id not in self._metrics_log:
            self._metrics_log[customer_id] = []
        self._metrics_log[customer_id].append(entry)

        for contract in self._contracts.values():
            if customer_id and contract.customer_id != customer_id:
                continue
            if metric in contract.metrics:
                target = contract.metrics[metric]
                is_ok = await self._check_compliance(metric, value, target)
                if not is_ok and self._is_new_breach(contract, metric, value):
                    ratio = value / target if target > 0 else float("inf")
                    breach = SLABreach(
                        contract_id=contract.contract_id,
                        customer_id=contract.customer_id,
                        metric=metric,
                        expected_value=target,
                        actual_value=value,
                        deviation=abs(value - target) / target if target > 0 else 0,
                        severity="critical" if ratio > contract.critical_threshold else "warning",
                        details=f"Metric {metric.value}: {value:.4f} (target: {target:.4f})",
                    )
                    self._breaches.append(breach)

    async def get_sla_summary(self, customer_id: str) -> dict[str, Any]:
        contracts = await self.get_contracts_for_customer(customer_id)
        compliance = await self.get_compliance_rate(customer_id)
        breaches = await self.get_breaches(customer_id, resolved=False)
        return {
            "customer_id": customer_id,
            "active_contracts": len(contracts),
            "compliance_rate": round(compliance, 4),
            "open_breaches": len(breaches),
            "status": SLAStatus.COMPLIANT.value if compliance > 0.99 else SLAStatus.WARNING.value,
        }

    async def _get_current_metric(self, metric: SLAMetric) -> float:
        simulated = {
            SLAMetric.UPTIME: 99.95,
            SLAMetric.LATENCY_P99: 1200.0,
            SLAMetric.ERROR_RATE: 0.005,
            SLAMetric.RESPONSE_TIME: 800.0,
            SLAMetric.THROUGHPUT: 150.0,
            SLAMetric.AVAILABILITY: 99.9,
        }
        return simulated.get(metric, 1.0)

    async def _check_compliance(
        self,
        metric: SLAMetric,
        current: float,
        target: float,
    ) -> bool:
        lower_is_better = {
            SLAMetric.LATENCY_P99,
            SLAMetric.ERROR_RATE,
            SLAMetric.RESPONSE_TIME,
        }
        if metric in lower_is_better:
            return current <= target
        return current >= target

    def _is_new_breach(
        self,
        contract: SLAContract,
        metric: SLAMetric,
        value: float,
    ) -> bool:
        recent = [
            b for b in self._breaches
            if b.contract_id == contract.contract_id
            and b.metric == metric
            and b.resolved_at is None
        ]
        if recent:
            return False
        cutoff = datetime.utcnow() - timedelta(hours=1)
        recent_log = [
            cp for cp in self._checkpoints
            if cp.metric == metric
            and cp.timestamp >= cutoff
            and not cp.compliant
        ]
        return len(recent_log) <= 1
