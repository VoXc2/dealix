"""Experiment System — run at most 3 disciplined experiments per week.

Every experiment is: a hypothesis, one metric that proves it, a 7-day
timebox, and a keep / kill / iterate decision. More than 3 a week is
chaos, not discipline — registration is hard-capped.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4

MAX_EXPERIMENTS_PER_WEEK = 3
_DEFAULT_PATH = "data/revenue_assurance/experiments.jsonl"
_lock = threading.Lock()


class ExperimentDecision(StrEnum):
    PENDING = "pending"
    KEEP = "keep"
    KILL = "kill"
    ITERATE = "iterate"


class ExperimentLimitError(RuntimeError):
    """Raised when a 4th experiment is registered within one ISO week."""


@dataclass(frozen=True, slots=True)
class Experiment:
    experiment_id: str
    hypothesis: str
    metric: str
    timebox_days: int
    week_label: str
    decision: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    raw = os.environ.get("DEALIX_EXPERIMENTS_PATH", _DEFAULT_PATH)
    path = Path(raw)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[2] / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _week_label(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    iso = now.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _read_all() -> list[Experiment]:
    path = _path()
    if not path.exists():
        return []
    out: list[Experiment] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(Experiment(**json.loads(line)))
            except Exception:  # noqa: BLE001
                continue
    return out


def _write_all(experiments: list[Experiment]) -> None:
    path = _path()
    with path.open("w", encoding="utf-8") as handle:
        for exp in experiments:
            handle.write(json.dumps(exp.to_dict(), ensure_ascii=False))
            handle.write("\n")


def register_experiment(
    *,
    hypothesis: str,
    metric: str,
    timebox_days: int = 7,
    week_label: str | None = None,
) -> Experiment:
    """Register a new experiment for the current ISO week.

    Raises :class:`ExperimentLimitError` if the week already holds
    ``MAX_EXPERIMENTS_PER_WEEK`` experiments.
    """
    if not hypothesis.strip():
        raise ValueError("hypothesis is required")
    if not metric.strip():
        raise ValueError("metric is required")
    label = week_label or _week_label()
    with _lock:
        existing = _read_all()
        this_week = [e for e in existing if e.week_label == label]
        if len(this_week) >= MAX_EXPERIMENTS_PER_WEEK:
            raise ExperimentLimitError(
                f"week {label} already has {MAX_EXPERIMENTS_PER_WEEK} experiments"
            )
        experiment = Experiment(
            experiment_id=f"exp_{uuid4().hex[:20]}",
            hypothesis=hypothesis.strip(),
            metric=metric.strip(),
            timebox_days=max(1, int(timebox_days)),
            week_label=label,
            decision=ExperimentDecision.PENDING.value,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        existing.append(experiment)
        _write_all(existing)
        return experiment


def decide_experiment(experiment_id: str, decision: ExperimentDecision | str) -> Experiment:
    """Record a keep / kill / iterate decision for an experiment."""
    decision_value = decision.value if isinstance(decision, ExperimentDecision) else str(decision)
    if decision_value not in {d.value for d in ExperimentDecision}:
        raise ValueError(f"invalid decision: {decision_value!r}")
    with _lock:
        experiments = _read_all()
        updated: Experiment | None = None
        for idx, exp in enumerate(experiments):
            if exp.experiment_id == experiment_id:
                updated = Experiment(
                    experiment_id=exp.experiment_id,
                    hypothesis=exp.hypothesis,
                    metric=exp.metric,
                    timebox_days=exp.timebox_days,
                    week_label=exp.week_label,
                    decision=decision_value,
                    created_at=exp.created_at,
                )
                experiments[idx] = updated
                break
        if updated is None:
            raise KeyError(f"experiment not found: {experiment_id!r}")
        _write_all(experiments)
        return updated


def list_experiments(*, week_label: str | None = None) -> list[Experiment]:
    """List experiments, optionally filtered to one ISO week."""
    experiments = _read_all()
    if week_label:
        experiments = [e for e in experiments if e.week_label == week_label]
    experiments.sort(key=lambda e: e.created_at, reverse=True)
    return experiments


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        path.unlink()


__all__ = [
    "MAX_EXPERIMENTS_PER_WEEK",
    "Experiment",
    "ExperimentDecision",
    "ExperimentLimitError",
    "clear_for_test",
    "decide_experiment",
    "list_experiments",
    "register_experiment",
]
