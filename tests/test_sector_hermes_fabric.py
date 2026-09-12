from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/commercial/run_sector_hermes_fabric.py"


def _load():
    spec = importlib.util.spec_from_file_location("sector_fabric", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


fabric_mod = _load()


def test_fabric_covers_all_twenty_sectors_with_five_agents() -> None:
    fabric = fabric_mod.build_fabric()
    assert fabric["sector_count"] == 20
    assert fabric["permanent_agents"] == fabric_mod.PERMANENT_AGENTS
    assert len(fabric["deep_wip_sectors"]) == 3
    assert len({cell["sector_id"] for cell in fabric["cells"]}) == 20
    for cell in fabric["cells"]:
        assert [row["agent"] for row in cell["agents"]] == fabric_mod.PERMANENT_AGENTS
        assert not any(cell["authority"].values())
        assert cell["counts_as_pipeline"] is False
        assert cell["counts_as_revenue"] is False


def test_top3_are_research_ranked_not_pipeline() -> None:
    fabric = fabric_mod.build_fabric()
    assert fabric["deep_wip_sectors"] == [
        "retail_commerce_ecommerce",
        "logistics_supply_chain",
        "tourism_hospitality",
    ]
    assert fabric["opencode_promotion"] == "DENIED_UNTIL_EXECUTION_PLANE_GREEN"
    assert not any(fabric["material_authority"].values())


def test_patrol_writes_internal_receipt_only(tmp_path: Path) -> None:
    result = fabric_mod.patrol_sector("retail_commerce_ecommerce", tmp_path)
    assert result["ok"] is True
    receipt = (tmp_path / "receipts/retail_commerce_ecommerce.json").read_text(encoding="utf-8")
    assert "INTERNAL_PATROL_READY" in receipt
    assert '"counts_as_pipeline": false' in receipt
    assert '"counts_as_revenue": false' in receipt


def test_canonical_factory_resolution_uses_repo_scheduler(monkeypatch) -> None:
    monkeypatch.delenv(fabric_mod.FACTORY_SCRIPT_ENV, raising=False)
    resolved = fabric_mod.resolve_factory_script()
    assert resolved == fabric_mod.CANONICAL_FACTORY
    assert resolved.is_file()
    assert resolved == ROOT / "scripts/ops/session_factory.py"
    assert "/control/runtime/session-factory-" not in str(resolved)
    assert not hasattr(fabric_mod, "DEFAULT_FACTORY")


def test_factory_resolution_prefers_explicit_then_env(tmp_path: Path, monkeypatch) -> None:
    explicit = tmp_path / "explicit_factory.py"
    explicit.write_text("# stub\n", encoding="utf-8")
    env_path = tmp_path / "env_factory.py"
    env_path.write_text("# stub\n", encoding="utf-8")
    monkeypatch.setenv(fabric_mod.FACTORY_SCRIPT_ENV, str(env_path))
    assert fabric_mod.resolve_factory_script(explicit) == explicit
    assert fabric_mod.resolve_factory_script() == env_path


def test_factory_resolution_fails_closed_when_unavailable(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv(fabric_mod.FACTORY_SCRIPT_ENV, str(tmp_path / "missing.py"))
    monkeypatch.setattr(fabric_mod, "CANONICAL_FACTORY", tmp_path / "also_missing.py")
    with pytest.raises(FileNotFoundError):
        fabric_mod.resolve_factory_script()


def test_submit_due_jobs_uses_canonical_factory(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv(fabric_mod.FACTORY_SCRIPT_ENV, raising=False)
    fabric = fabric_mod.build_fabric()
    result = fabric_mod.submit_due_jobs(fabric, tmp_path / "fabric", tmp_path / "factory", None)
    assert result["submitted_count"] > 0
    assert list((tmp_path / "factory" / "jobs").glob("*.json"))
