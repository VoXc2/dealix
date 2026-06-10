"""Wave 8 — Customer-Ready Master Verifier tests."""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFIER_SH = REPO_ROOT / "scripts" / "wave8_customer_ready_verify.sh"


def test_verifier_script_exists():
    assert VERIFIER_SH.exists(), "wave8_customer_ready_verify.sh must exist"


def test_verifier_script_has_required_output_lines():
    """Verify the script contains the required output line format."""
    content = VERIFIER_SH.read_text(encoding="utf-8")
    required_outputs = [
        "WAVE8_CUSTOMER_READY_VERDICT",
        "LOCAL_HEAD",
        "BRANCH",
        "DEPENDENCY_MATRIX",
        "INTEGRATION_REGISTRY",
        "CUSTOMER_CREDENTIALS_CHECK",
        "DATA_BOUNDARY",
        "DPA_CONSENT",
        "LAUNCH_ROOM",
        "ONBOARDING_WIZARD",
        "INTEGRATION_PLAN_QUALITY",
        "PRODUCTION_SMOKE",
        "OBSERVABILITY_ADAPTERS",
        "CUSTOMER_SIGNAL_SYNTHESIS",
        "NO_SECRETS",
        "NO_LIVE_SEND",
        "NO_LIVE_CHARGE",
        "NO_COLD_WHATSAPP",
        "NO_SCRAPING",
        "NO_FAKE_PROOF",
        "NO_FAKE_REVENUE",
    ]
    for line in required_outputs:
        assert line in content, f"Verifier script missing output line: {line}"


def test_verifier_script_has_hard_gates():
    content = VERIFIER_SH.read_text(encoding="utf-8")
    assert "NO_LIVE_SEND" in content
    assert "NO_LIVE_CHARGE" in content
    assert "NO_COLD_WHATSAPP" in content
    assert "NO_SCRAPING" in content
    assert "NO_FAKE_PROOF" in content
    assert "NO_FAKE_REVENUE" in content


def test_verifier_script_checks_all_phases():
    content = VERIFIER_SH.read_text(encoding="utf-8")
    phases = [
        "DEPENDENCY_MATRIX",
        "INTEGRATION_REGISTRY",
        "CUSTOMER_CREDENTIALS_CHECK",
        "DATA_BOUNDARY",
        "DPA_CONSENT",
        "LAUNCH_ROOM",
        "ONBOARDING_WIZARD",
        "INTEGRATION_PLAN_QUALITY",
        "PRODUCTION_SMOKE",
        "OBSERVABILITY_ADAPTERS",
        "CUSTOMER_SIGNAL_SYNTHESIS",
        "EVIDENCE_TABLE",
    ]
    for phase in phases:
        assert phase in content, f"Verifier missing phase check: {phase}"
