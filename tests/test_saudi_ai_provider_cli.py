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


def test_roi_and_generate_offer_commands() -> None:
    roi = run_cmd(
        "roi",
        "--service",
        "CUSTOMER_PORTAL_GOLD",
        "--tickets",
        "50000",
        "--agent-cost",
        "18",
        "--automation-rate",
        "0.42",
    )
    assert roi.returncode == 0, roi.stdout + roi.stderr
    assert "Projected Monthly Savings" in roi.stdout

    generated = run_cmd(
        "generate-offer",
        "--service",
        "SECURITY_GOLD",
        "--segment",
        "enterprise",
        "--industry",
        "banking",
        "--lang",
        "ar",
    )
    assert generated.returncode == 0, generated.stdout + generated.stderr
    assert "offer:" in generated.stdout


def test_proposal_dashboard_and_recurring_commands() -> None:
    proposal = run_cmd(
        "proposal",
        "--service",
        "CUSTOMER_PORTAL_GOLD",
        "--intake-file",
        "intake/demo_customer_intake.json",
        "--lang",
        "ar",
    )
    assert proposal.returncode == 0, proposal.stdout + proposal.stderr
    assert "proposal:" in proposal.stdout
    assert "pricing_sheet:" in proposal.stdout

    dashboard = run_cmd(
        "dashboard-export",
        "--metrics-json",
        "dashboard/sample_metrics.json",
    )
    assert dashboard.returncode == 0, dashboard.stdout + dashboard.stderr
    assert "executive_dashboard:" in dashboard.stdout

    recurring = run_cmd(
        "recurring-model",
        "--setup-fee",
        "45000",
        "--monthly",
        "18000",
        "--months",
        "12",
        "--expansion-rate",
        "0.08",
    )
    assert recurring.returncode == 0, recurring.stdout + recurring.stderr
    assert "Projected Total Revenue" in recurring.stdout
