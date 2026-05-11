from __future__ import annotations

import subprocess


def run_script(path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", path],
        check=False,
        capture_output=True,
        text=True,
    )


def test_validate_pricing_script_passes() -> None:
    result = run_script("scripts/validate_pricing.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PRICING_VALIDATION=PASS" in result.stdout


def test_validate_catalog_script_passes() -> None:
    result = run_script("scripts/validate_catalog.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CATALOG_VALIDATION=PASS" in result.stdout


def test_validate_kpis_script_passes() -> None:
    result = run_script("scripts/validate_kpis.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "KPI_VALIDATION=PASS" in result.stdout


def test_validate_playbooks_script_passes() -> None:
    result = run_script("scripts/validate_playbooks.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PLAYBOOK_VALIDATION=PASS" in result.stdout


def test_validate_governance_script_passes() -> None:
    result = run_script("scripts/validate_governance.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "GOVERNANCE_VALIDATION=PASS" in result.stdout


def test_validate_runtime_script_passes() -> None:
    result = run_script("scripts/validate_runtime.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RUNTIME_VALIDATION=PASS" in result.stdout


def test_validate_commercialization_script_passes() -> None:
    result = run_script("scripts/validate_commercialization.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "COMMERCIALIZATION_VALIDATION=PASS" in result.stdout
