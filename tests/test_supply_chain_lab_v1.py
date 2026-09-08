from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ops" / "verify_supply_chain_lab_v1.py"
ACCEPT_PATH = ROOT / "scripts" / "ops" / "accept_supply_chain_lab_v1.sh"
RUNNER_PATH = ROOT / "scripts" / "ops" / "run_supply_chain_evidence_v1.sh"


def _load_module():
    spec = importlib.util.spec_from_file_location("verify_supply_chain_lab_v1", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_supply_chain_manifest_is_fail_closed(capsys):
    module = _load_module()
    module.main()
    out = capsys.readouterr().out
    assert "DEALIX_SUPPLY_CHAIN_LAB_V1=PASS" in out
    assert "production_mutation=false" in out
    assert "customer_effects=false" in out
    assert "auto_remediation=false" in out
    assert "scanner_finding_is_not_exploitability=true" in out
    assert "duplicate_scanner_findings_dedupe_to_one_risk=true" in out


def test_required_tools_are_bounded_to_one_lab():
    module = _load_module()
    assert module.REQUIRED_COMPONENTS == {
        "osv-scanner",
        "syft",
        "grype",
        "github-artifact-attestations",
    }


def test_exact_head_acceptance_uses_process_local_exact_safe_directory_only():
    text = ACCEPT_PATH.read_text(encoding="utf-8")
    assert 'git -c safe.directory="$ROOT"' in text
    assert "safe.directory=*" not in text
    assert "git config --global" not in text
    assert 'ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"' in text
    assert "DEALIX_SUPPLY_CHAIN_LAB_ACCEPTANCE=PASS" in text


def test_runtime_evidence_uses_only_isolated_lab_binaries():
    text = RUNNER_PATH.read_text(encoding="utf-8")
    assert 'LAB_ROOT="${DEALIX_SUPPLY_CHAIN_LAB_ROOT:-/opt/dealix/labs/supply-chain}"' in text
    assert '"$BIN/osv-scanner"' in text
    assert '"$BIN/syft"' in text
    assert '"$BIN/grype"' in text
    assert "command -v syft" not in text
    assert "command -v osv-scanner" not in text
    assert "command -v grype" not in text
