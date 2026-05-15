"""Deterministic enterprise layer readiness validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REQUIRED_LAYER_DOCS = (
    "architecture.md",
    "readiness.md",
    "tests.md",
    "risk_model.md",
    "observability.md",
    "rollback.md",
)


@dataclass(frozen=True)
class CheckResult:
    """Single checklist evaluation output."""

    check_id: str
    description: str
    passed: bool
    missing_paths: tuple[str, ...]


@dataclass(frozen=True)
class LayerReport:
    """Per-layer readiness report."""

    layer_id: str
    title: str
    owner: str
    kpis: tuple[str, ...]
    score: int
    status: str
    missing_docs: tuple[str, ...]
    missing_required_paths: tuple[str, ...]
    missing_test_paths: tuple[str, ...]
    checks: tuple[CheckResult, ...]


@dataclass(frozen=True)
class ValidationReport:
    """Full report including cross-layer signal."""

    layers: tuple[LayerReport, ...]
    cross_layer_score: int
    cross_layer_status: str
    cross_layer_checks: tuple[CheckResult, ...]
    total_layers: int
    ready_layers: int
    verdict: str


def _as_tuple_of_str(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    out: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    return tuple(out)


def _path_exists(repo_root: Path, rel_path: str) -> bool:
    return (repo_root / rel_path).exists()


def _missing_paths(repo_root: Path, paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(p for p in paths if not _path_exists(repo_root, p))


def _evaluate_check(repo_root: Path, raw_check: dict[str, Any]) -> CheckResult:
    check_id = str(raw_check.get("id") or "unknown_check")
    description = str(raw_check.get("description") or "")
    evidence_paths = _as_tuple_of_str(raw_check.get("evidence_paths"))
    missing = _missing_paths(repo_root, evidence_paths)
    return CheckResult(
        check_id=check_id,
        description=description,
        passed=not missing,
        missing_paths=missing,
    )


def _evaluate_layer_docs(repo_root: Path, layer_id: str) -> tuple[str, ...]:
    base = Path("readiness") / layer_id
    missing: list[str] = []
    for filename in REQUIRED_LAYER_DOCS:
        rel = str(base / filename)
        if not _path_exists(repo_root, rel):
            missing.append(rel)
    return tuple(missing)


def _calculate_score(
    *,
    missing_docs: tuple[str, ...],
    missing_required_paths: tuple[str, ...],
    missing_test_paths: tuple[str, ...],
    checks: tuple[CheckResult, ...],
) -> int:
    total = 1 + len(missing_required_paths) + len(missing_test_paths) + len(checks)
    if total <= 0:
        return 0

    passed = 0
    if not missing_docs:
        passed += 1
    # required/test paths are collapsed into gate signals to avoid biasing by list size.
    if not missing_required_paths:
        passed += 1
    if not missing_test_paths:
        passed += 1
    passed += sum(1 for check in checks if check.passed)
    return int(round((passed / max(1, 3 + len(checks))) * 100))


def _layer_status(score: int, threshold: int) -> str:
    return "PASS" if score >= threshold else "FIX"


def _validate_layer(repo_root: Path, raw_layer: dict[str, Any], threshold: int) -> LayerReport:
    layer_id = str(raw_layer.get("id") or "").strip()
    title = str(raw_layer.get("title") or layer_id)
    owner = str(raw_layer.get("owner") or "unassigned")
    kpis = _as_tuple_of_str(raw_layer.get("kpis"))
    required_paths = _as_tuple_of_str(raw_layer.get("required_paths"))
    test_paths = _as_tuple_of_str(raw_layer.get("tests"))
    raw_checks = raw_layer.get("checks")
    checks = ()
    if isinstance(raw_checks, list):
        checks = tuple(
            _evaluate_check(repo_root, c)
            for c in raw_checks
            if isinstance(c, dict)
        )

    missing_docs = _evaluate_layer_docs(repo_root, layer_id)
    missing_required_paths = _missing_paths(repo_root, required_paths)
    missing_test_paths = _missing_paths(repo_root, test_paths)
    score = _calculate_score(
        missing_docs=missing_docs,
        missing_required_paths=missing_required_paths,
        missing_test_paths=missing_test_paths,
        checks=checks,
    )
    return LayerReport(
        layer_id=layer_id,
        title=title,
        owner=owner,
        kpis=kpis,
        score=score,
        status=_layer_status(score, threshold),
        missing_docs=missing_docs,
        missing_required_paths=missing_required_paths,
        missing_test_paths=missing_test_paths,
        checks=checks,
    )


def _validate_cross_layer(
    repo_root: Path,
    raw_checks: Any,
    threshold: int,
) -> tuple[int, str, tuple[CheckResult, ...]]:
    checks: list[CheckResult] = []
    if isinstance(raw_checks, list):
        for item in raw_checks:
            if isinstance(item, dict):
                checks.append(_evaluate_check(repo_root, item))
    if not checks:
        return 0, "FIX", ()
    passed = sum(1 for check in checks if check.passed)
    score = int(round((passed / len(checks)) * 100))
    return score, _layer_status(score, threshold), tuple(checks)


def load_manifest(path: Path) -> dict[str, Any]:
    """Load layer validation manifest from YAML file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("layer validation manifest root must be a mapping")
    return data


def validate_manifest(manifest: dict[str, Any], repo_root: Path) -> ValidationReport:
    """Validate all layers and cross-layer checks from manifest."""
    scoring = manifest.get("scoring") or {}
    layer_threshold = int(scoring.get("ready_threshold", 80))
    cross_threshold = int(scoring.get("cross_layer_ready_threshold", 85))
    raw_layers = manifest.get("layers")
    if not isinstance(raw_layers, list):
        raise ValueError("manifest.layers must be a list")

    layers = tuple(
        _validate_layer(repo_root, layer, layer_threshold)
        for layer in raw_layers
        if isinstance(layer, dict)
    )
    ready_layers = sum(1 for layer in layers if layer.status == "PASS")
    cross_score, cross_status, cross_checks = _validate_cross_layer(
        repo_root=repo_root,
        raw_checks=manifest.get("cross_layer_checks"),
        threshold=cross_threshold,
    )
    verdict = (
        "PASS"
        if ready_layers == len(layers) and cross_status == "PASS" and len(layers) > 0
        else "PARTIAL"
    )
    return ValidationReport(
        layers=layers,
        cross_layer_score=cross_score,
        cross_layer_status=cross_status,
        cross_layer_checks=cross_checks,
        total_layers=len(layers),
        ready_layers=ready_layers,
        verdict=verdict,
    )
