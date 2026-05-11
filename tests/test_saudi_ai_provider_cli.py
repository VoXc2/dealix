from __future__ import annotations

import subprocess


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", "-m", "saudi_ai_provider", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_verify_command_passes() -> None:
    result = run_cmd("verify")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SELLABLE_NOW=true" in result.stdout
    assert "DELIVERABLE_NOW=true" in result.stdout


def test_package_command_for_smb() -> None:
    result = run_cmd("package", "--segment", "smb")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Segment package: smb" in result.stdout
    assert "CUSTOMER_PORTAL_BRONZE" in result.stdout


def test_quote_command_for_customer_portal_gold() -> None:
    result = run_cmd(
        "quote",
        "--service",
        "CUSTOMER_PORTAL_GOLD",
        "--employees",
        "120",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Service: CUSTOMER_PORTAL_GOLD" in result.stdout
    assert "SELLABLE_NOW: true" in result.stdout


def test_kpis_and_pitch_commands() -> None:
    kpis = run_cmd("kpis", "--service", "SECURITY_SILVER")
    assert kpis.returncode == 0, kpis.stdout + kpis.stderr
    assert "North Star:" in kpis.stdout

    pitch = run_cmd("pitch", "--service", "OBSERVABILITY_BRONZE", "--lang", "ar")
    assert pitch.returncode == 0, pitch.stdout + pitch.stderr
    assert "OBSERVABILITY_BRONZE" in pitch.stdout
