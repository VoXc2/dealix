"""CI gate for AI quality — runs the deterministic eval harness.

Governance is the product moat: any governance probe failure fails the
build. The overall pass rate must stay at or above the harness threshold.
"""
from __future__ import annotations

from evals.runner import run_evals


def test_eval_harness_passes() -> None:
    report = run_evals()
    assert report.total > 0, "no probes loaded"
    assert report.ok(), report.to_markdown()


def test_no_governance_violations() -> None:
    report = run_evals()
    assert report.governance_violations == 0, report.to_markdown()


def test_every_category_covered() -> None:
    report = run_evals()
    categories = set(report.by_category())
    for required in ("governance", "value_discipline", "arabic_quality"):
        assert required in categories, f"eval category not covered: {required}"
