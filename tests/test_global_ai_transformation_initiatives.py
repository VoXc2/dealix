"""Per-initiative verification for Global AI Transformation program."""

from __future__ import annotations

import sys
from pathlib import Path
from subprocess import run

import pytest
import yaml

from auto_client_acquisition.governance_os.workflow_control_registry import (
    governed_domain_count,
    governed_workflow_domains,
)

INITIATIVE_IDS = (
    "doctrine-lock",
    "gap-closure",
    "enterprise-package",
    "governance-expansion",
    "data-flywheel",
    "reliability-program",
    "observability-contracts",
    "gtm-system",
    "unit-economics",
    "delivery-control-tower",
    "org-operating-system",
    "category-dominance",
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("initiative_id", INITIATIVE_IDS)
def test_initiative_verify_check(initiative_id: str) -> None:
    proc = run(
        [sys.executable, "scripts/verify_global_ai_transformation.py", "--check", initiative_id],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, f"{initiative_id}:\n{proc.stderr}\n{proc.stdout}"


def test_governance_inventory_matches_registry() -> None:
    inv_path = ROOT / "auto_client_acquisition/governance_os/governance_workflow_inventory.yaml"
    data = yaml.safe_load(inv_path.read_text(encoding="utf-8"))
    inv_domains = {w["domain"] for w in data.get("workflows", [])}
    reg_domains = set(governed_workflow_domains())
    assert inv_domains == reg_domains, f"inventory vs registry mismatch: {inv_domains ^ reg_domains}"


def test_governance_expansion_covers_beyond_legacy_scope() -> None:
    """Blueprint: expand beyond systems 26-35 — require >=10 governed domains."""
    assert governed_domain_count() >= 10


def test_transformation_index_all_implemented() -> None:
    idx = yaml.safe_load(
        (ROOT / "dealix/transformation/global_ai_transformation_index.yaml").read_text(encoding="utf-8")
    )
    for iid, row in (idx.get("initiatives") or {}).items():
        assert row.get("status") == "implemented", iid


def test_global_transformation_bundle_script_exists() -> None:
    path = ROOT / "scripts/run_global_ai_transformation_bundle.sh"
    assert path.exists()
