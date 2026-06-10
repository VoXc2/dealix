from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Variant:
    variant_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    traffic_percentage: float = 0.5
    conversions: int = 0
    impressions: int = 0
    is_control: bool = False


@dataclass
class ExperimentConfig:
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    metric: str = "conversion_rate"
    min_sample_size: int = 100
    confidence_level: float = 0.95
    max_duration_hours: int = 168
    variants: list[Variant] = field(default_factory=lambda: [
        Variant(name="control", is_control=True, traffic_percentage=0.5),
        Variant(name="treatment", traffic_percentage=0.5),
    ])


@dataclass
class Experiment:
    experiment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    config: ExperimentConfig = field(default_factory=ExperimentConfig)
    status: ExperimentStatus = ExperimentStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class ExperimentResults:
    experiment_id: str
    experiment_name: str
    status: ExperimentStatus
    variants: list[Variant]
    winner_id: str | None = None
    confidence: float = 0.0
    lift: float = 0.0
    is_significant: bool = False
    sample_size_reached: bool = False
    duration_hours: float = 0.0
    error: str | None = None


class ABTestingFramework:
    def __init__(self):
        self._experiments: dict[str, Experiment] = {}
        self._assignments: dict[str, dict[str, str]] = {}
        self._conversion_log: list[dict[str, Any]] = []

    async def create_experiment(self, config: ExperimentConfig) -> Experiment:
        experiment = Experiment(
            config=config,
            status=ExperimentStatus.DRAFT,
        )
        total_traffic = sum(v.traffic_percentage for v in config.variants)
        if abs(total_traffic - 1.0) > 0.001:
            for v in config.variants:
                v.traffic_percentage = v.traffic_percentage / total_traffic
        self._experiments[experiment.experiment_id] = experiment
        logger.info(
            "Created experiment '%s' with %d variants",
            config.name, len(config.variants),
        )
        return experiment

    async def start_experiment(self, experiment_id: str) -> Experiment:
        experiment = self._experiments.get(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.utcnow()
        logger.info("Started experiment '%s'", experiment.config.name)
        return experiment

    async def assign_variant(
        self,
        experiment_id: str,
        unit_id: str,
    ) -> str:
        experiment = self._experiments.get(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
        if experiment.status != ExperimentStatus.RUNNING:
            raise ValueError(f"Experiment {experiment_id} is not running")

        if experiment_id in self._assignments and unit_id in self._assignments[experiment_id]:
            return self._assignments[experiment_id][unit_id]

        import hashlib
        hash_input = f"{experiment_id}:{unit_id}"
        hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        normalized = (hash_val % 10000) / 10000

        cumulative = 0.0
        chosen_variant = experiment.config.variants[0]
        for variant in experiment.config.variants:
            cumulative += variant.traffic_percentage
            if normalized <= cumulative:
                chosen_variant = variant
                break

        chosen_variant.impressions += 1

        if experiment_id not in self._assignments:
            self._assignments[experiment_id] = {}
        self._assignments[experiment_id][unit_id] = chosen_variant.variant_id

        return chosen_variant.variant_id

    async def track_conversion(
        self,
        experiment_id: str,
        unit_id: str,
        event: str = "conversion",
    ) -> None:
        experiment = self._experiments.get(experiment_id)
        if not experiment:
            return

        variant_id = self._assignments.get(experiment_id, {}).get(unit_id)
        if not variant_id:
            return

        for variant in experiment.config.variants:
            if variant.variant_id == variant_id:
                variant.conversions += 1
                break

        self._conversion_log.append({
            "experiment_id": experiment_id,
            "unit_id": unit_id,
            "variant_id": variant_id,
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def get_experiment(self, experiment_id: str) -> Experiment | None:
        return self._experiments.get(experiment_id)

    async def get_results(self, experiment_id: str) -> ExperimentResults:
        experiment = self._experiments.get(experiment_id)
        if not experiment:
            return ExperimentResults(
                experiment_id=experiment_id,
                experiment_name="unknown",
                status=ExperimentStatus.CANCELLED,
                variants=[],
                error="Experiment not found",
            )

        variants = experiment.config.variants
        control = next((v for v in variants if v.is_control), variants[0])
        treatment = next((v for v in variants if not v.is_control), None)

        control_rate = control.conversions / control.impressions if control.impressions > 0 else 0
        treatment_rate = treatment.conversions / treatment.impressions if (treatment and treatment.impressions > 0) else 0
        lift = treatment_rate - control_rate if treatment else 0

        min_impr = min(
            v.impressions for v in variants if v.impressions > 0
        ) if variants else 0
        sample_size_reached = min_impr >= experiment.config.min_sample_size if variants else False

        significance = self._calculate_significance(
            control.conversions, control.impressions,
            treatment.conversions, treatment.impressions if treatment else 0,
        ) if treatment else 0

        is_significant = significance >= experiment.config.confidence_level and sample_size_reached

        duration = (
            (experiment.completed_at - experiment.started_at).total_seconds() / 3600
            if experiment.completed_at and experiment.started_at
            else 0
        )

        winner = None
        if is_significant and lift > 0 and treatment:
            winner = treatment.variant_id
        elif is_significant and lift < 0:
            winner = control.variant_id

        return ExperimentResults(
            experiment_id=experiment_id,
            experiment_name=experiment.config.name,
            status=experiment.status,
            variants=variants,
            winner_id=winner,
            confidence=significance,
            lift=lift,
            is_significant=is_significant,
            sample_size_reached=sample_size_reached,
            duration_hours=duration,
        )

    async def declare_winner(self, experiment_id: str) -> str | None:
        results = await self.get_results(experiment_id)
        if results.winner_id:
            experiment = self._experiments[experiment_id]
            experiment.status = ExperimentStatus.COMPLETED
            experiment.completed_at = datetime.utcnow()
            logger.info(
                "Experiment '%s' completed. Winner: %s (lift: %.2f%%, confidence: %.1f%%)",
                results.experiment_name, results.winner_id,
                results.lift * 100, results.confidence * 100,
            )
        return results.winner_id

    async def pause_experiment(self, experiment_id: str) -> None:
        experiment = self._experiments.get(experiment_id)
        if experiment:
            experiment.status = ExperimentStatus.PAUSED

    async def resume_experiment(self, experiment_id: str) -> None:
        experiment = self._experiments.get(experiment_id)
        if experiment:
            experiment.status = ExperimentStatus.RUNNING

    async def cancel_experiment(self, experiment_id: str) -> None:
        experiment = self._experiments.get(experiment_id)
        if experiment:
            experiment.status = ExperimentStatus.CANCELLED

    async def list_experiments(
        self,
        status: ExperimentStatus | None = None,
    ) -> list[Experiment]:
        if status:
            return [e for e in self._experiments.values() if e.status == status]
        return list(self._experiments.values())

    def _calculate_significance(
        self,
        control_conv: int,
        control_total: int,
        treatment_conv: int,
        treatment_total: int,
    ) -> float:
        if control_total == 0 or treatment_total == 0:
            return 0.0
        import math
        p1 = control_conv / control_total
        p2 = treatment_conv / treatment_total
        p_pool = (control_conv + treatment_conv) / (control_total + treatment_total)
        se = math.sqrt(p_pool * (1 - p_pool) * (1 / control_total + 1 / treatment_total))
        if se == 0:
            return 0.0
        z = abs(p2 - p1) / se
        return self._z_to_p(z)

    def _z_to_p(self, z: float) -> float:
        import math
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))
