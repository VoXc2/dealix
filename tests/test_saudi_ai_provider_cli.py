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


def test_p2_monetization_commands() -> None:
    scorecard = run_cmd(
        "proposal-scorecard",
        "--service",
        "CUSTOMER_PORTAL_GOLD",
        "--intake-file",
        "intake/demo_customer_intake.json",
    )
    assert scorecard.returncode in (0, 1)
    assert "Proposal Score:" in scorecard.stdout

    auto_package = run_cmd(
        "auto-package",
        "--intake-file",
        "intake/demo_customer_intake.json",
        "--max-services",
        "4",
    )
    assert auto_package.returncode == 0, auto_package.stdout + auto_package.stderr
    assert "Recommended Services:" in auto_package.stdout

    renewal = run_cmd(
        "renewal-orchestrator",
        "--customer-state-file",
        "revenue/demo_customer_state.json",
    )
    assert renewal.returncode == 0, renewal.stdout + renewal.stderr
    assert "Renewal Risk:" in renewal.stdout

    p2 = run_cmd(
        "p2-monetization",
        "--service",
        "CUSTOMER_PORTAL_GOLD",
        "--intake-file",
        "intake/demo_customer_intake.json",
        "--customer-state-file",
        "revenue/demo_customer_state.json",
    )
    assert p2.returncode == 0, p2.stdout + p2.stderr
    assert "P2_MONETIZATION_SUMMARY" in p2.stdout


def test_offer_stack_and_launch_pack_commands() -> None:
    offer_stack = run_cmd("offer-stack", "--segment", "enterprise", "--lang", "ar")
    assert offer_stack.returncode == 0, offer_stack.stdout + offer_stack.stderr
    assert "حزمة الخدمات التنفيذية" in offer_stack.stdout
    assert "AI_GOVERNANCE_OS" in offer_stack.stdout

    launch_pack = run_cmd(
        "launch-pack",
        "--segment",
        "enterprise",
        "--lang",
        "ar",
        "--output",
        "out/launch/test_final_launch_pack.md",
    )
    assert launch_pack.returncode == 0, launch_pack.stdout + launch_pack.stderr
    assert "launch_pack:" in launch_pack.stdout
