"""Correctness tests for the deterministic layer validation engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.layer_validation import validation_engine as ve


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the engine at an isolated temp repo root."""
    monkeypatch.setattr(ve, "REPO", tmp_path)
    return tmp_path


def test_check_modules_flags_missing_and_empty(repo: Path) -> None:
    (repo / "real_pkg").mkdir()
    (repo / "real_pkg" / "code.py").write_text("x = 1\n")
    (repo / "empty_pkg").mkdir()  # exists but no code

    layer = {
        "modules": [
            {"path": "real_pkg"},
            {"path": "empty_pkg"},
            {"path": "ghost_pkg"},
        ]
    }
    gate = ve.check_modules(layer)
    assert gate["passed"] is False
    assert "module_no_code:empty_pkg" in gate["blockers"]
    assert "module_missing:ghost_pkg" in gate["blockers"]
    assert not any(b.startswith("module") and "real_pkg" in b for b in gate["blockers"])


def test_check_modules_accepts_yaml_only_directory(repo: Path) -> None:
    (repo / "evals").mkdir()
    (repo / "evals" / "pack.yaml").write_text("name: pack\n")
    gate = ve.check_modules({"modules": [{"path": "evals"}]})
    assert gate["passed"] is True


def test_check_required_tests_flags_missing(repo: Path) -> None:
    (repo / "tests").mkdir()
    (repo / "tests" / "test_present.py").write_text("def test_x():\n    pass\n")
    layer = {"required_tests": ["tests/test_present.py", "tests/test_absent.py"]}
    gate = ve.check_required_tests(layer)
    assert gate["passed"] is False
    assert gate["blockers"] == ["test_missing:tests/test_absent.py"]


def test_check_checklist_downgrades_unverified_claim(repo: Path) -> None:
    (repo / "tests").mkdir()
    (repo / "tests" / "test_real.py").write_text("def test_x():\n    pass\n")
    layer = {
        "checklist": [
            {"id": "verified", "evidence_test": "tests/test_real.py", "done": True},
            {"id": "fake_claim", "evidence_test": "tests/test_ghost.py", "done": True},
            {"id": "honest_todo", "done": False},
        ]
    }
    gate = ve.check_checklist(layer)
    assert "checklist_unverified:fake_claim" in gate["blockers"]
    assert "checklist_incomplete:honest_todo" in gate["blockers"]
    assert "checklist_unverified:verified" not in gate["blockers"]
    assert len(gate["blockers"]) == 2


def test_score_redistributes_when_tests_not_run() -> None:
    layer = {
        "modules": [{"path": "a"}, {"path": "b"}],
        "required_tests": ["t1", "t2"],
        "checklist": [{"id": "c1", "done": True}, {"id": "c2", "done": True}],
    }
    gates = [
        {"gate": "modules", "passed": True, "blockers": []},
        {"gate": "required_tests", "passed": True, "blockers": []},
        {"gate": "checklist", "passed": True, "blockers": []},
    ]
    assert ve._score_layer(layer, gates, run_tests=False) == 100


def test_score_drops_with_blockers() -> None:
    layer = {
        "modules": [{"path": "a"}, {"path": "b"}],
        "required_tests": ["t1", "t2"],
        "checklist": [{"id": "c1", "done": True}, {"id": "c2", "done": True}],
    }
    gates = [
        {"gate": "modules", "passed": True, "blockers": []},
        {"gate": "required_tests", "passed": True, "blockers": []},
        {"gate": "checklist", "passed": False, "blockers": ["checklist_incomplete:c1"]},
    ]
    # checklist sub-score = 0.5 -> weighted (35 + 25 + 30*0.5)/90 = 83
    assert ve._score_layer(layer, gates, run_tests=False) == 83


@pytest.mark.parametrize(
    ("score", "expected"),
    [(100, ve.READY), (85, ve.READY), (84, ve.PARTIAL), (40, ve.PARTIAL), (39, ve.MISSING)],
)
def test_status_thresholds(score: int, expected: str) -> None:
    assert ve._status_from_score(score) == expected
