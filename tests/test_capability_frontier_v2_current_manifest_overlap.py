from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts/ops/verify_capability_frontier_v2_current_manifest_v1.py"


def _load():
    spec = importlib.util.spec_from_file_location("frontier_current_manifest_guard", VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frontier_does_not_readmit_current_manifest_authority() -> None:
    verifier = _load()
    overlaps = verifier.find_unreconciled_overlaps()
    assert overlaps == [], f"unreconciled current-manifest overlaps: {overlaps}"


def test_reconciled_overlap_decisions_are_fail_closed() -> None:
    verifier = _load()
    assert verifier.ALLOWED_RECONCILED_DECISIONS == {
        "ALREADY_BOUNDED",
        "REJECT_DUPLICATE_DEFAULT",
    }
