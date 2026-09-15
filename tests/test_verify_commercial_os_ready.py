from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify_commercial_os_ready.py"


def _module():
    spec = importlib.util.spec_from_file_location("verify_commercial_os_ready", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_verifier_uses_source_contracts_not_mutable_business_state() -> None:
    module = _module()
    assert "data/commercial/pipeline_sample.json" in module.SOURCE_CONTRACTS
    assert "data/outreach/approval_queue.csv" in module.SOURCE_CONTRACTS
    assert "data/commercial/pipeline.csv" not in module.SOURCE_CONTRACTS
    assert "data/outreach/manual_approval_queue.csv" not in module.SOURCE_CONTRACTS
    assert set(module.NON_AUTHORITY_RUNTIME_STATE).isdisjoint(module.SOURCE_CONTRACTS)


def test_verifier_is_cwd_independent_and_passes_current_source(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "COMMERCIAL_OS_READY=PASS" in result.stdout
    assert "authority=IMMUTABLE_SOURCE_CONTRACTS" in result.stdout
    assert "runtime_business_state_required=false" in result.stdout
