#!/usr/bin/env python3
"""Validate docs/registry/ENTERPRISE_ASCENSION_MATRIX.yaml.

Purpose:
- Keep the 12-axis ascension model machine-checkable.
- Block invalid "live" claims.
- Ensure in-progress/live axes have their referenced files on disk.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = REPO_ROOT / "docs" / "registry" / "ENTERPRISE_ASCENSION_MATRIX.yaml"

ALLOWED_STATUSES = {"live", "in_progress", "target", "blocked"}
EXPECTED_AXES = 12
REQUIRED_AXIS_FIELDS = {
    "axis_id",
    "title_ar",
    "title_en",
    "status",
    "objective",
    "required_paths",
    "required_capabilities",
    "gates",
}
REQUIRED_GATES = {
    "architecture_defined",
    "readiness_defined",
    "observability_defined",
    "rollback_defined",
    "metrics_defined",
    "risk_model_defined",
    "tests_defined",
    "evals_defined",
}


@dataclass
class ValidationSummary:
    total: int
    live: int
    in_progress: int
    target: int
    blocked: int
    gate_score_pct: int


def load_matrix(path: Path = MATRIX_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing matrix file: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("Matrix root must be a YAML mapping")
    return data


def _validate_axis(axis: dict[str, Any], errors: list[str], repo_root: Path) -> None:
    axis_id = axis.get("axis_id", "<unknown>")
    missing = sorted(REQUIRED_AXIS_FIELDS - set(axis))
    if missing:
        errors.append(f"{axis_id}: missing required fields {missing}")
        return

    status = axis["status"]
    if status not in ALLOWED_STATUSES:
        errors.append(f"{axis_id}: invalid status={status!r}")

    required_paths = axis.get("required_paths")
    if not isinstance(required_paths, list) or not required_paths:
        errors.append(f"{axis_id}: required_paths must be a non-empty list")
    else:
        # in_progress/live claims must be backed by existing artifacts.
        if status in {"in_progress", "live"}:
            for rel in required_paths:
                if not isinstance(rel, str) or not rel.strip():
                    errors.append(f"{axis_id}: invalid required path entry {rel!r}")
                    continue
                if not (repo_root / rel).exists():
                    errors.append(f"{axis_id}: missing required path {rel!r}")

    capabilities = axis.get("required_capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append(f"{axis_id}: required_capabilities must be a non-empty list")

    gates = axis.get("gates")
    if not isinstance(gates, dict):
        errors.append(f"{axis_id}: gates must be a mapping")
        return
    missing_gates = sorted(REQUIRED_GATES - set(gates))
    if missing_gates:
        errors.append(f"{axis_id}: missing gates {missing_gates}")
        return

    if status == "live":
        for g in REQUIRED_GATES:
            if gates.get(g) is not True:
                errors.append(f"{axis_id}: status=live requires gates.{g}=true")


def validate_matrix(data: dict[str, Any], repo_root: Path = REPO_ROOT) -> tuple[list[str], ValidationSummary]:
    errors: list[str] = []
    axes = data.get("axes")
    if not isinstance(axes, list) or not axes:
        errors.append("axes must be a non-empty list")
        return errors, ValidationSummary(0, 0, 0, 0, 0, 0)

    if len(axes) != EXPECTED_AXES:
        errors.append(f"expected {EXPECTED_AXES} axes, found {len(axes)}")

    seen: set[str] = set()
    gate_true = 0
    gate_total = 0
    live = in_progress = target = blocked = 0

    for axis in axes:
        if not isinstance(axis, dict):
            errors.append("axis entry must be a mapping")
            continue
        axis_id = axis.get("axis_id", "<unknown>")
        if axis_id in seen:
            errors.append(f"duplicate axis_id: {axis_id}")
        seen.add(axis_id)
        _validate_axis(axis, errors, repo_root)

        status = axis.get("status")
        if status == "live":
            live += 1
        elif status == "in_progress":
            in_progress += 1
        elif status == "target":
            target += 1
        elif status == "blocked":
            blocked += 1

        gates = axis.get("gates") or {}
        if isinstance(gates, dict):
            for gate_name in REQUIRED_GATES:
                if gate_name in gates:
                    gate_total += 1
                    if gates.get(gate_name) is True:
                        gate_true += 1

    score = int((gate_true / gate_total) * 100) if gate_total else 0
    summary = ValidationSummary(
        total=len(axes),
        live=live,
        in_progress=in_progress,
        target=target,
        blocked=blocked,
        gate_score_pct=score,
    )
    return errors, summary


def main() -> int:
    data = load_matrix()
    errors, summary = validate_matrix(data)
    print(
        f"ASCENSION_AXES_TOTAL={summary.total} "
        f"LIVE={summary.live} IN_PROGRESS={summary.in_progress} "
        f"TARGET={summary.target} BLOCKED={summary.blocked}"
    )
    print(f"ASCENSION_GATE_SCORE={summary.gate_score_pct}")
    if errors:
        print("FAIL: enterprise ascension matrix violations:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"OK: {MATRIX_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
