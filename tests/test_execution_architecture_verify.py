"""Tests for enterprise execution architecture verifier."""

from __future__ import annotations

from pathlib import Path

import yaml

from scripts.verify_execution_architecture import run_verification


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_execution_architecture_manifest_passes() -> None:
    repo = _repo_root()
    manifest = repo / "readiness" / "execution_architecture_manifest.yaml"
    ok, results = run_verification(repo, manifest)
    assert ok is True
    assert results
    assert all(item.ok for item in results)


def test_execution_architecture_manifest_fails_when_content_rule_missing(
    tmp_path: Path,
) -> None:
    repo = _repo_root()
    manifest_path = tmp_path / "manifest.yaml"
    sample_target = tmp_path / "target.txt"
    sample_target.write_text("hello", encoding="utf-8")

    manifest_path.write_text(
        yaml.safe_dump(
            {
                "required_directories": [],
                "required_files": [],
                "content_rules": {"target.txt": ["hello", "missing-token"]},
            }
        ),
        encoding="utf-8",
    )

    ok, results = run_verification(tmp_path, manifest_path)
    assert ok is False
    assert len(results) == 1
    assert results[0].ok is False
    assert "missing-token" in results[0].detail
