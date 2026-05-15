"""Tests for enterprise layer validation model."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.enterprise_layer_validation import (
    REQUIRED_LAYER_DOCS,
    load_manifest,
    validate_manifest,
)

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "readiness" / "layer_validation.yaml"


def test_manifest_declares_expected_layers() -> None:
    manifest = load_manifest(MANIFEST)
    layers = manifest.get("layers") or []
    layer_ids = [layer["id"] for layer in layers]
    assert layer_ids == [
        "foundation",
        "agents",
        "workflows",
        "memory",
        "governance",
        "observability",
        "evals",
        "executive",
    ]


def test_real_manifest_validates_cleanly() -> None:
    manifest = load_manifest(MANIFEST)
    report = validate_manifest(manifest, REPO)
    assert report.total_layers == 8
    assert report.ready_layers == 8
    assert report.cross_layer_status == "PASS"
    assert report.verdict == "PASS"


def test_cross_layer_check_fails_when_evidence_missing(tmp_path: Path) -> None:
    layer_dir = tmp_path / "readiness" / "foundation"
    layer_dir.mkdir(parents=True, exist_ok=True)
    for doc in REQUIRED_LAYER_DOCS:
        (layer_dir / doc).write_text("# ok\n", encoding="utf-8")
    (tmp_path / "foundation.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "test_foundation.py").write_text("def test_x():\n    assert True\n", encoding="utf-8")

    manifest = {
        "scoring": {
            "ready_threshold": 80,
            "cross_layer_ready_threshold": 80,
        },
        "layers": [
            {
                "id": "foundation",
                "title": "Foundation",
                "owner": "owner",
                "kpis": ["kpi"],
                "required_paths": ["foundation.py"],
                "tests": ["test_foundation.py"],
                "checks": [
                    {
                        "id": "check_ok",
                        "description": "ok",
                        "evidence_paths": ["foundation.py"],
                    }
                ],
            }
        ],
        "cross_layer_checks": [
            {
                "id": "missing_cross",
                "description": "missing evidence",
                "evidence_paths": ["does_not_exist.py"],
            }
        ],
    }

    report = validate_manifest(manifest, tmp_path)
    assert report.ready_layers == 1
    assert report.cross_layer_status == "FIX"
    assert report.verdict == "PARTIAL"
