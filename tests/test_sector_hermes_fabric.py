from __future__ import annotations

import importlib.util
import json
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


def test_fabric_uses_agentic_holding_not_fixed_five_authority() -> None:
    fabric = fabric_mod.build_fabric()
    authority = fabric["agent_authority"]
    assert fabric["sector_count"] == 20
    assert authority["architecture"] == "agentic_holding_sector_company_mesh"
    assert authority["logical_agents"] > len(fabric_mod.LEGACY_EXECUTOR_ALIASES)
    assert authority["legacy_executor_aliases"] == fabric_mod.LEGACY_EXECUTOR_ALIASES
    assert authority["fixed_five_runtime_authority"] is False
    assert authority["runtime_capacity_authority"] == "ResourceGovernor + Session Factory"
    assert fabric["deep_wip_semantics"] == "ECONOMIC_FOCUS_ONLY"
    assert len(fabric["deep_wip_sectors"]) == 3
    assert len({cell["sector_id"] for cell in fabric["cells"]}) == 20
    for cell in fabric["cells"]:
        assert cell["agent_authority"]["fixed_five_runtime_authority"] is False
        assert len(cell["agents"]) == 22
        assert all(row["layer"] == "sector" for row in cell["agents"])
        assert all(row["sector"] == cell["sector_id"] for row in cell["agents"])
        assert not any(cell["authority"].values())
        assert cell["counts_as_relationship"] is False
        assert cell["counts_as_consent"] is False
        assert cell["counts_as_pipeline"] is False
        assert cell["counts_as_revenue"] is False


def test_top3_are_economic_focus_not_runtime_capacity() -> None:
    fabric = fabric_mod.build_fabric()
    assert fabric["deep_wip_sectors"] == [
        "retail_commerce_ecommerce",
        "logistics_supply_chain",
        "tourism_hospitality",
    ]
    assert fabric["deep_wip_semantics"] == "ECONOMIC_FOCUS_ONLY"
    assert fabric["agent_authority"]["runtime_capacity_authority"] == "ResourceGovernor + Session Factory"
    assert fabric["opencode_promotion"] == "GOVERNED_BY_CANONICAL_MODEL_BROKER_AND_SESSION_FACTORY"
    assert not any(fabric["material_authority"].values())


def test_patrol_writes_internal_receipt_only(tmp_path: Path) -> None:
    result = fabric_mod.patrol_sector("retail_commerce_ecommerce", tmp_path)
    assert result["ok"] is True
    receipt = json.loads((tmp_path / "receipts/retail_commerce_ecommerce.json").read_text(encoding="utf-8"))
    assert receipt["verdict"] == "INTERNAL_PATROL_READY"
    assert receipt["counts_as_pipeline"] is False
    assert receipt["counts_as_revenue"] is False
    assert all(row["agent_id"].startswith("dealix.retail_commerce_ecommerce.") for row in receipt["agents"])


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


def test_submit_due_jobs_persists_logical_agent_identity(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv(fabric_mod.FACTORY_SCRIPT_ENV, raising=False)
    fabric = fabric_mod.build_fabric()
    result = fabric_mod.submit_due_jobs(fabric, tmp_path / "fabric", tmp_path / "factory", None)
    assert result["submitted_count"] > 0
    jobs = [json.loads(path.read_text(encoding="utf-8")) for path in (tmp_path / "factory" / "jobs").glob("*.json")]
    assert jobs
    assert all(job.get("LOGICAL_AGENT_ID") for job in jobs)
    assert all(job.get("LOGICAL_AGENT_LAYER") == "sector" for job in jobs)
    assert all(job.get("LOGICAL_AGENT_SECTOR") for job in jobs)
    assert all(job.get("OWNER_AGENT") in fabric_mod.LEGACY_EXECUTOR_ALIASES for job in jobs)


def test_local_ai_jobs_use_internal_sensitivity_and_full_factory_timeout(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv(fabric_mod.FACTORY_SCRIPT_ENV, raising=False)
    fabric = fabric_mod.build_fabric()
    result = fabric_mod.submit_due_jobs(fabric, tmp_path / "fabric", tmp_path / "factory", None)
    assert result["submitted_count"] > 0
    jobs = [json.loads(path.read_text(encoding="utf-8")) for path in (tmp_path / "factory" / "jobs").glob("*.json")]
    local_jobs = [job for job in jobs if job.get("JOB_CLASS") == "LOCAL_AI"]
    assert local_jobs
    assert all(job.get("DATA_SENSITIVITY") == "INTERNAL" for job in local_jobs)
    assert all(job.get("EXECUTOR", {}).get("timeout_seconds") == 120 for job in local_jobs)
    assert all(job.get("EXECUTOR", {}).get("num_predict") == 160 for job in local_jobs)
