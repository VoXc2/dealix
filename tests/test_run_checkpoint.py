"""Contracts for the durable GitHub run checkpoint (receipts + manifest)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checkpoint = _load("run_checkpoint")


def test_manifest_has_required_fields_and_live_git_identity() -> None:
    manifest = checkpoint.build_manifest(
        run_id="20260911T160000Z",
        objective="test run",
        base="abc123",
        pr="https://github.com/Dealix-sa/dealix/pull/1",
        tests="10 passed",
        go_usage="UNKNOWN",
        l5_required=["merge chain"],
        next_action="verify",
    )
    for field in (
        "run_id",
        "objective",
        "start_head",
        "end_head",
        "branch",
        "origin_main",
        "pr",
        "tests",
        "go_usage_if_observable",
        "l5_required",
        "next_action",
        "secrets_included",
    ):
        assert field in manifest, field
    assert manifest["secrets_included"] is False
    assert manifest["end_head"] != "UNKNOWN"
    assert manifest["branch"]


def test_receipt_renders_run_id_and_l5_items() -> None:
    manifest = checkpoint.build_manifest("RUN1", "obj", "base", "", "tests", "", ["L5-A", "L5-B"], "next")
    rendered = checkpoint.render_receipt(manifest)
    assert "RUN1" in rendered
    assert "L5-A" in rendered
    assert "L5-B" in rendered
    assert "next" in rendered


def test_write_checkpoint_creates_run_dir_and_latest(tmp_path: Path) -> None:
    manifest = checkpoint.build_manifest("RUN2", "obj", "base", "PR1", "tests", "UNKNOWN", [], "next")
    paths = checkpoint.write_checkpoint(manifest, docs_root=tmp_path)
    assert (tmp_path / "runs" / "RUN2" / "RECEIPT.md").exists()
    assert (tmp_path / "runs" / "RUN2" / "MANIFEST.json").exists()
    assert (tmp_path / "LATEST_AUTONOMOUS_RECEIPT.md").exists()
    payload = json.loads(Path(paths["manifest"]).read_text(encoding="utf-8"))
    assert payload["run_id"] == "RUN2"


def test_checkpoint_refuses_secret_like_content(tmp_path: Path) -> None:
    manifest = checkpoint.build_manifest(
        "RUN3", "obj", "base", "", "tests", "sk-" + "a" * 30, [], "next"
    )
    try:
        checkpoint.write_checkpoint(manifest, docs_root=tmp_path)
    except ValueError as error:
        assert "secret" in str(error)
    else:
        raise AssertionError("checkpoint should refuse secret-like content")
