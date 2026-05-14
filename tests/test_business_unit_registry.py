"""Tests for the Business Unit Registry — locking artifacts and discipline."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "data" / "business_units.json"


def _load_register():
    p = REPO_ROOT / "scripts" / "register_business_unit.py"
    spec = importlib.util.spec_from_file_location("register_business_unit_mod", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_registry_file_exists_and_valid_json():
    assert REGISTRY.exists()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert "entries" in data
    assert isinstance(data["entries"], list)


def test_every_registry_entry_has_provenance():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for i, entry in enumerate(data.get("entries") or []):
        for key in ("entry_id", "git_author", "created_at"):
            assert isinstance(entry.get(key), str) and entry[key].strip(), (
                f"entry[{i}] missing {key}"
            )


def test_status_values_in_enum():
    from auto_client_acquisition.holding_os.unit_governance import (
        UnitPortfolioDecision,
    )
    allowed = {s.name for s in UnitPortfolioDecision}
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for entry in data.get("entries") or []:
        assert entry["status"] in allowed


def test_kill_and_hold_entries_have_reason():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for entry in data.get("entries") or []:
        if entry["status"] in ("KILL", "HOLD"):
            assert entry.get("reason"), f"{entry['slug']} status={entry['status']} missing reason"


def test_charter_paths_exist():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for entry in data.get("entries") or []:
        cp = entry.get("charter_path")
        if cp:
            assert (REPO_ROOT / cp).exists(), f"charter_path missing: {cp}"


def test_register_refuses_without_flag(tmp_path, monkeypatch, capsys):
    mod = _load_register()
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "bu.json")
    rc = mod.main([
        "--slug", "test-bu",
        "--name", "Test", "--owner", "test", "--status", "BUILD",
        "--kpi", "x", "--charter-path", "x", "--sector", "x",
    ])
    assert rc == 2
    assert "REFUSED" in capsys.readouterr().err


def test_register_rejects_unknown_status(tmp_path, monkeypatch):
    mod = _load_register()
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "bu.json")
    with pytest.raises(SystemExit):
        mod.register_new(
            slug="x", name="X", owner="o", status="DESTROY",
            kpi="k", charter_path="x", sector="s",
        )


def test_kill_status_requires_reason(tmp_path, monkeypatch):
    mod = _load_register()
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "bu.json")
    with pytest.raises(SystemExit):
        mod.register_new(
            slug="x", name="X", owner="o", status="KILL",
            kpi="k", charter_path="x", sector="s", reason=None,
        )


def test_duplicate_slug_rejected(tmp_path, monkeypatch):
    mod = _load_register()
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "bu.json")
    mod.register_new(slug="dup", name="X", owner="o", status="BUILD",
                     kpi="k", charter_path="x", sector="s")
    with pytest.raises(SystemExit):
        mod.register_new(slug="dup", name="Y", owner="o", status="BUILD",
                         kpi="k", charter_path="x", sector="s")


def test_update_status_changes_existing_entry(tmp_path, monkeypatch):
    mod = _load_register()
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "bu.json")
    mod.register_new(slug="a", name="A", owner="o", status="BUILD",
                     kpi="k", charter_path="x", sector="s")
    updated = mod.update_status(slug="a", new_status="SCALE", reason=None)
    assert updated["status"] == "SCALE"


def test_validator_passes_on_seed():
    """The committed seed registry must pass the validator (locks parity)."""
    import subprocess
    out = subprocess.run(
        ["python", str(REPO_ROOT / "scripts" / "validate_business_units.py")],
        cwd=str(REPO_ROOT), capture_output=True, text=True, check=False,
    )
    assert out.returncode == 0, f"validator failed:\n{out.stdout}\n{out.stderr}"
