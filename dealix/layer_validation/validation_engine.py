"""Deterministic per-layer validation checks and scoring (no LLM).

Every check returns the readiness-gate shape used across Dealix:
``{"gate": str, "passed": bool, "blockers": list[str]}`` — see
``auto_client_acquisition/delivery_os/readiness_gates.py``.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dealix.layer_validation.loader import load_manifest
from dealix.layer_validation.spec import ENTERPRISE_LAYERS, LayerSpec, layer_by_id

REPO = Path(__file__).resolve().parents[2]

# Score thresholds — 85 matches OFFER_READINESS_MIN in verify_dealix_ready.py.
BUILT_THRESHOLD = 85
PARTIAL_THRESHOLD = 40

# Status values.
READY = "READY"
PARTIAL = "PARTIAL"
MISSING = "MISSING"
BLOCKED = "BLOCKED"

_CODE_SUFFIXES = (".py", ".yaml", ".yml")


@dataclass
class LayerResult:
    """Validation outcome for one enterprise layer."""

    layer_id: str
    order: int
    title: str
    score: int
    status: str
    gates: list[dict[str, Any]] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    capped_by: str | None = None


def _exists(rel: str) -> bool:
    return (REPO / rel).exists()


def _module_populated(rel: str) -> bool:
    """True when a module path is a real file or a directory with content."""
    target = REPO / rel
    if target.is_file():
        return target.stat().st_size > 0
    if not target.is_dir():
        return False
    for suffix in _CODE_SUFFIXES:
        for found in target.rglob(f"*{suffix}"):
            if found.is_file() and found.stat().st_size > 0:
                return True
    return False


def _resolve_test_paths(spec: str) -> list[Path]:
    """Resolve a required-test entry (plain path or glob) to existing files."""
    if any(ch in spec for ch in "*?[]"):
        return [p for p in REPO.glob(spec) if p.is_file()]
    candidate = REPO / spec
    return [candidate] if candidate.is_file() else []


def check_modules(layer: dict[str, Any]) -> dict[str, Any]:
    """Every declared module path must exist and be populated."""
    blockers: list[str] = []
    modules = layer.get("modules") or []
    for mod in modules:
        path = str(mod.get("path") or "").strip()
        if not path:
            continue
        if not _exists(path):
            blockers.append(f"module_missing:{path}")
        elif not _module_populated(path):
            blockers.append(f"module_no_code:{path}")
    return {"gate": "modules", "passed": not blockers, "blockers": blockers}


def check_required_tests(layer: dict[str, Any]) -> dict[str, Any]:
    """Every required test path/glob must resolve to at least one file."""
    blockers: list[str] = []
    for spec in layer.get("required_tests") or []:
        if not _resolve_test_paths(str(spec)):
            blockers.append(f"test_missing:{spec}")
    return {"gate": "required_tests", "passed": not blockers, "blockers": blockers}


def _checklist_evidence_ok(item: dict[str, Any]) -> bool:
    """Independently verify a checklist item's evidence target exists."""
    test_ref = item.get("evidence_test")
    if test_ref and not _resolve_test_paths(str(test_ref)):
        return False
    module_ref = item.get("evidence_module")
    if module_ref and not _module_populated(str(module_ref)):
        return False
    doc_ref = item.get("evidence_doc")
    if doc_ref and not _exists(str(doc_ref)):
        return False
    return bool(test_ref or module_ref or doc_ref)


def check_checklist(layer: dict[str, Any]) -> dict[str, Any]:
    """A ``done: true`` claim is downgraded unless its evidence is verified."""
    blockers: list[str] = []
    for item in layer.get("checklist") or []:
        item_id = str(item.get("id") or "unknown")
        if not item.get("done"):
            blockers.append(f"checklist_incomplete:{item_id}")
        elif not _checklist_evidence_ok(item):
            blockers.append(f"checklist_unverified:{item_id}")
    return {"gate": "checklist", "passed": not blockers, "blockers": blockers}


def run_mapped_tests(layer: dict[str, Any]) -> dict[str, Any]:
    """Execute the layer's required pytest files (opt-in, slow)."""
    paths: list[str] = []
    for spec in layer.get("required_tests") or []:
        paths.extend(str(p.relative_to(REPO)) for p in _resolve_test_paths(str(spec)))
    if not paths:
        return {"gate": "mapped_tests", "passed": False, "blockers": ["no_tests_to_run"]}
    proc = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "pytest", *paths, "-q", "--no-cov"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return {"gate": "mapped_tests", "passed": True, "blockers": []}
    return {"gate": "mapped_tests", "passed": False, "blockers": ["mapped_tests_failed"]}


def _group_score(gate: dict[str, Any], total_items: int) -> float:
    """Sub-score 0-1 for one check group."""
    if total_items <= 0:
        return 1.0
    bad = len(gate.get("blockers") or [])
    return max(0.0, min(1.0, 1.0 - bad / total_items))


def _score_layer(layer: dict[str, Any], gates: list[dict[str, Any]], run_tests: bool) -> int:
    by_gate = {g["gate"]: g for g in gates}
    modules_total = len(layer.get("modules") or [])
    tests_total = len(layer.get("required_tests") or [])
    checklist_total = len(layer.get("checklist") or [])

    modules_s = _group_score(by_gate.get("modules", {}), modules_total)
    tests_s = _group_score(by_gate.get("required_tests", {}), tests_total)
    checklist_s = _group_score(by_gate.get("checklist", {}), checklist_total)

    if run_tests and "mapped_tests" in by_gate:
        mapped_s = 1.0 if by_gate["mapped_tests"].get("passed") else 0.0
        weighted = (
            0.35 * modules_s + 0.25 * tests_s + 0.30 * checklist_s + 0.10 * mapped_s
        )
    else:
        # Redistribute the mapped-tests weight across the other three groups.
        weighted = (35 * modules_s + 25 * tests_s + 30 * checklist_s) / 90.0
    return round(weighted * 100)


def _status_from_score(score: int) -> str:
    if score >= BUILT_THRESHOLD:
        return READY
    if score >= PARTIAL_THRESHOLD:
        return PARTIAL
    return MISSING


def validate_layer(layer_id: str, *, run_tests: bool = False) -> LayerResult:
    """Validate one layer in isolation (no dependency gate applied)."""
    spec = layer_by_id(layer_id)
    if spec is None:
        raise ValueError(f"unknown_layer:{layer_id}")
    manifest = load_manifest(layer_id)
    layer = manifest["layer"]

    gates = [
        check_modules(layer),
        check_required_tests(layer),
        check_checklist(layer),
    ]
    if run_tests:
        gates.append(run_mapped_tests(layer))

    score = _score_layer(layer, gates, run_tests)
    blockers = [b for g in gates for b in (g.get("blockers") or [])]
    return LayerResult(
        layer_id=spec.id,
        order=spec.order,
        title=spec.title,
        score=score,
        status=_status_from_score(score),
        gates=gates,
        blockers=blockers,
    )


def _apply_dependency_gate(results: dict[str, LayerResult]) -> None:
    """A layer is READY only if its score qualifies AND every lower layer is
    READY. Otherwise it is BLOCKED, capped by the first failing dependency."""
    for spec in ENTERPRISE_LAYERS:
        result = results[spec.id]
        if result.status != READY:
            continue
        for dep_id in spec.depends_on:
            if results[dep_id].status != READY:
                result.status = BLOCKED
                result.capped_by = dep_id
                break


def validate_all_layers(*, run_tests: bool = False) -> dict[str, LayerResult]:
    """Validate all 8 layers and apply the strict layer-by-layer gate."""
    results = {
        spec.id: validate_layer(spec.id, run_tests=run_tests) for spec in ENTERPRISE_LAYERS
    }
    _apply_dependency_gate(results)
    return results


def all_ready(results: dict[str, LayerResult]) -> bool:
    """True only when every enterprise layer is READY."""
    return all(r.status == READY for r in results.values())
