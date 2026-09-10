from pathlib import Path
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "verify_tenant_boundary_registry_v1.py"
REGISTRY = ROOT / "config" / "saas" / "tenant_boundary_registry_v1.json"


def _load():
    spec = importlib.util.spec_from_file_location("tenant_boundary_registry_v1", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_registry_is_machine_readable_and_pre_activation():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["mode"] == "PRIVATE_SAAS_PRE_ACTIVATION"
    assert data["policy"]["runtime_rls_activation"] is False
    assert data["policy"]["production_db_mutation"] is False


def test_registry_matches_current_orm_and_rls_inventory():
    result = _load().evaluate()
    assert result["inventory_sync"] is True, result["errors"]
    assert result["activation_ready"] is False
    assert result["explicit_tenant_tables"] == 63
    assert result["covered_explicit_tenant_tables"] == 23
    assert len(result["pending_tenant_rls_review"]) == 39
    assert len(result["rls_model_mismatch_review"]) == 8


def test_pending_and_mismatch_sets_do_not_overlap():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    pending = set(data["pending_tenant_rls_review"])
    mismatch = set(data["rls_model_mismatch_review"])
    assert len(pending) == len(data["pending_tenant_rls_review"])
    assert len(mismatch) == len(data["rls_model_mismatch_review"])
    assert pending.isdisjoint(mismatch)
