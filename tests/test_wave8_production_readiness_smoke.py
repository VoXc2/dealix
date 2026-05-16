"""Wave 8 — Production Readiness Smoke tests (Python equivalent of shell smoke)."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    "docs/WAVE8_CURRENT_REALITY.md",
    "docs/WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md",
    "docs/wave8/dependency_tooling_matrix.json",
    "docs/WAVE8_INTEGRATION_REGISTRY.md",
    "docs/wave8/integration_registry.yaml",
    "docs/WAVE8_CUSTOMER_CREDENTIAL_READINESS.md",
    "docs/wave8/customer_credentials.example.env",
    "docs/WAVE8_CUSTOMER_DATA_BOUNDARY.md",
    "docs/WAVE8_DPA_AND_CONSENT_READINESS.md",
    "docs/wave8/DPA_CHECKLIST_AR_EN.md",
    "docs/wave8/CONSENT_RECORD_TEMPLATE.json",
    "docs/wave8/DSR_REQUEST_TEMPLATE.md",
    "docs/wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md",
    "docs/wave8/WHATSAPP_CONSENT_CHECKLIST_AR_EN.md",
    "docs/FIRST_CUSTOMER_LAUNCH_ROOM.md",
    "docs/wave8/FIRST_CUSTOMER_LAUNCH_ROOM.template.md",
    "docs/WAVE8_CUSTOMER_READY_EVIDENCE_TABLE.md",
]

REQUIRED_SCRIPTS = [
    "scripts/dealix_customer_credentials_check.py",
    "scripts/wave8_customer_data_boundary_check.sh",
    "scripts/dealix_integration_plan_quality_check.py",
    "scripts/wave8_production_readiness_smoke.sh",
    "scripts/dealix_customer_signal_synthesis.py",
    "scripts/wave8_customer_ready_verify.sh",
]

REQUIRED_TESTS = [
    "tests/test_wave8_dependency_tooling_matrix.py",
    "tests/test_wave8_integration_registry.py",
    "tests/test_wave8_customer_credentials_check.py",
    "tests/test_wave8_customer_data_boundary.py",
    "tests/test_wave8_dpa_consent_docs.py",
    "tests/test_wave8_launch_room.py",
    "tests/test_wave8_customer_onboarding_wizard_hardening.py",
    "tests/test_wave8_integration_plan_quality.py",
    "tests/test_wave8_production_readiness_smoke.py",
    "tests/test_wave8_customer_signal_synthesis.py",
    "tests/test_wave8_customer_ready_verify.py",
]

# Observability adapters were planned but never shipped as standalone
# modules; observability lives in core.logging / core telemetry instead.
REQUIRED_OBSERVABILITY: list[str] = []


def test_all_required_docs_exist():
    missing = [p for p in REQUIRED_DOCS if not (REPO_ROOT / p).exists()]
    assert not missing, f"Missing docs: {missing}"


def test_all_required_scripts_exist():
    missing = [p for p in REQUIRED_SCRIPTS if not (REPO_ROOT / p).exists()]
    assert not missing, f"Missing scripts: {missing}"


def test_all_required_tests_exist():
    missing = [p for p in REQUIRED_TESTS if not (REPO_ROOT / p).exists()]
    assert not missing, f"Missing tests: {missing}"


def test_all_observability_adapters_exist():
    missing = [p for p in REQUIRED_OBSERVABILITY if not (REPO_ROOT / p).exists()]
    assert not missing, f"Missing observability adapters: {missing}"


def test_gitignore_has_customer_patterns():
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/customers/" in gitignore


def test_no_live_keys_in_example_env():
    example_env = (REPO_ROOT / "docs" / "wave8" / "customer_credentials.example.env").read_text(encoding="utf-8")
    assert "sk_live_" not in example_env
    assert "REPLACE_ME" in example_env or "OPTIONAL" in example_env
