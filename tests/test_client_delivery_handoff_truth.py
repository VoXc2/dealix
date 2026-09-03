from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "delivery" / "create_client_workspace.py"
MANIFEST = ROOT / "data" / "commercial" / "client_delivery_control_manifest.json"
SNAPSHOT = ROOT / "apps" / "web" / "lib" / "client-delivery-control-snapshot.ts"


def load_module():
    spec = importlib.util.spec_from_file_location("dealix_create_client_workspace", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def populate_template(module, template: Path) -> None:
    for rel in module.expected_files():
        path = template / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("template\n", encoding="utf-8")


def populate_commercial_workspace(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for name in (
        "00_intake.md",
        "02_diagnostic_summary.md",
        "03_command_sprint_scope.md",
        "06_approval_register.md",
        "07_next_action_board.md",
    ):
        (path / name).write_text("governed\n", encoding="utf-8")


def refs(module) -> dict[str, str]:
    return {key: f"evidence:{key}" for key in module.REQUIRED_HANDOFF_REFS}


def configure(module, tmp_path: Path) -> None:
    module.REPO_ROOT = tmp_path
    module.CLIENTS_DIR = tmp_path / "clients"
    module.CUSTOMERS_DIR = tmp_path / "customers"
    module.TEMPLATE_DIR = module.CLIENTS_DIR / "_template"
    populate_template(module, module.TEMPLATE_DIR)


def test_real_delivery_requires_commercial_handoff(tmp_path) -> None:
    module = load_module()
    configure(module, tmp_path)
    with pytest.raises(RuntimeError, match="commercial workspace is required"):
        module.create_workspace("acme", "Acme")


def test_synthetic_test_is_explicitly_isolated(tmp_path) -> None:
    module = load_module()
    configure(module, tmp_path)
    workspace = module.create_workspace("dry-run-acme", "Dry Run", synthetic_test=True)
    payload = json.loads((workspace / "COMMERCIAL_HANDOFF.json").read_text(encoding="utf-8"))
    assert payload["handoff"]["mode"] == module.SYNTHETIC_MARKER
    assert "NOT_CUSTOMER_PROOF" in payload["handoff"]["mode"]


def test_real_handoff_requires_all_evidence_refs(tmp_path) -> None:
    module = load_module()
    configure(module, tmp_path)
    commercial = module.CUSTOMERS_DIR / "acme"
    populate_commercial_workspace(commercial)
    incomplete = refs(module)
    incomplete["payment_or_documented_start_condition_ref"] = ""
    with pytest.raises(RuntimeError, match="commercial handoff missing evidence refs"):
        module.create_workspace(
            "acme",
            "Acme",
            commercial_workspace="customers/acme",
            handoff_refs=incomplete,
        )


def test_real_handoff_creates_delivery_workspace_and_refuses_overwrite(tmp_path) -> None:
    module = load_module()
    configure(module, tmp_path)
    commercial = module.CUSTOMERS_DIR / "acme"
    populate_commercial_workspace(commercial)
    workspace = module.create_workspace(
        "acme",
        "Acme",
        commercial_workspace="customers/acme",
        handoff_refs=refs(module),
    )
    payload = json.loads((workspace / "COMMERCIAL_HANDOFF.json").read_text(encoding="utf-8"))
    assert payload["handoff"]["mode"] == "GOVERNED_REAL_HANDOFF"
    assert payload["delivery_owner"] == "dealix-delivery"
    with pytest.raises(FileExistsError, match="never auto-overwritten"):
        module.create_workspace(
            "acme",
            "Acme",
            overwrite=True,
            commercial_workspace="customers/acme",
            handoff_refs=refs(module),
        )


def test_manifest_and_snapshot_forbid_automatic_renewal_or_upsell() -> None:
    manifest = MANIFEST.read_text(encoding="utf-8")
    snapshot = SNAPSHOT.read_text(encoding="utf-8")
    assert "customers/<slug>/" in manifest
    assert "clients/<slug>/" in manifest
    assert "payment_or_documented_start_condition_ref" in manifest
    assert "no automatic renewal or upsell" in manifest
    assert "no automatic renewal or upsell" in snapshot
