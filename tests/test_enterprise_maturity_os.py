"""Tests for enterprise_maturity_os scoring model."""

from __future__ import annotations

import pytest

from auto_client_acquisition.enterprise_maturity_os import (
    CAPABILITY_KEYS,
    compute_domain_capability_score,
    evaluate_enterprise_maturity,
    validate_capability_scores,
)


def _all_scores(value: float) -> dict[str, float]:
    return {key: value for key in CAPABILITY_KEYS}


def test_validate_capability_scores_rejects_out_of_range() -> None:
    scores = _all_scores(50.0)
    scores["safe_evolution"] = 101.0
    with pytest.raises(ValueError):
        validate_capability_scores(scores)


def test_compute_domain_capability_score_foundation() -> None:
    scores = _all_scores(80.0)
    assert compute_domain_capability_score("foundation_maturity", scores) == 80.0


def test_evaluate_enterprise_maturity_not_ready_with_low_artifacts() -> None:
    scores = _all_scores(90.0)
    artifacts = {
        "foundation_maturity": 0.0,
        "agentic_runtime_maturity": 0.0,
        "workflow_orchestration_maturity": 0.0,
        "organizational_memory_maturity": 0.0,
        "governance_maturity": 0.0,
        "evaluation_maturity": 0.0,
        "continuous_evolution_maturity": 0.0,
    }
    report = evaluate_enterprise_maturity(scores, artifacts)
    assert report.transformation_ready is False
    assert report.overall_score == 63.0


def test_evaluate_enterprise_maturity_ready_when_domains_all_high() -> None:
    scores = _all_scores(88.0)
    artifacts = {
        "foundation_maturity": 90.0,
        "agentic_runtime_maturity": 90.0,
        "workflow_orchestration_maturity": 90.0,
        "organizational_memory_maturity": 90.0,
        "governance_maturity": 90.0,
        "evaluation_maturity": 90.0,
        "continuous_evolution_maturity": 90.0,
    }
    report = evaluate_enterprise_maturity(scores, artifacts)
    assert report.transformation_ready is True
    assert report.overall_score >= 88.0
