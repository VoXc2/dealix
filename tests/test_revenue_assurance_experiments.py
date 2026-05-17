"""Experiment System — at most 3 disciplined experiments per ISO week."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_assurance_os.experiment_system import (
    ExperimentDecision,
    ExperimentLimitError,
    decide_experiment,
    list_experiments,
    register_experiment,
)


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_EXPERIMENTS_PATH", str(tmp_path / "experiments.jsonl"))


def test_three_experiments_allowed_fourth_rejected() -> None:
    for i in range(3):
        register_experiment(
            hypothesis=f"hypothesis {i}", metric="reply_rate", week_label="2026-W20"
        )
    with pytest.raises(ExperimentLimitError):
        register_experiment(hypothesis="one too many", metric="reply_rate", week_label="2026-W20")


def test_limit_is_per_week() -> None:
    for i in range(3):
        register_experiment(hypothesis=f"h{i}", metric="m", week_label="2026-W20")
    # A different week is unaffected.
    exp = register_experiment(hypothesis="next week", metric="m", week_label="2026-W21")
    assert exp.week_label == "2026-W21"


def test_decision_is_recorded() -> None:
    exp = register_experiment(hypothesis="h", metric="m", week_label="2026-W20")
    decided = decide_experiment(exp.experiment_id, ExperimentDecision.KILL)
    assert decided.decision == "kill"
    assert list_experiments(week_label="2026-W20")[0].decision == "kill"
