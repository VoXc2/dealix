from __future__ import annotations

import json
import subprocess
from pathlib import Path


CATALOG_PATH = Path("dealix/catalogs/saudi_ai_service_catalog_v2.json")
VERIFIER_PATH = Path("scripts/verify_saudi_ai_service_catalog.py")

REQUIRED_SERVICE_FIELDS = {
    "id",
    "tier",
    "name_ar",
    "problem_ar",
    "decision_ar",
    "execution_ar",
    "proof_ar",
    "expansion_next_ar",
    "action_mode",
    "delivery_window_days",
    "kpis",
}


def test_catalog_has_expected_structure() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    service_lines = catalog["service_lines"]

    assert len(service_lines) == 12
    for line in service_lines:
        services = line["services"]
        assert len(services) >= 3
        for service in services:
            assert REQUIRED_SERVICE_FIELDS.issubset(service.keys())
            assert service["name_ar"].strip()
            assert service["problem_ar"].strip()
            assert service["decision_ar"].strip()
            assert service["execution_ar"]
            assert service["proof_ar"]
            assert service["expansion_next_ar"]
            assert service["kpis"]


def test_catalog_verifier_reports_pass() -> None:
    result = subprocess.run(
        ["python3", str(VERIFIER_PATH)],
        check=False,
        capture_output=True,
        text=True,
    )
    output = result.stdout

    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_SAUDI_REVENUE_COMMAND_CENTER=PASS" in output
    assert "SELLABLE_NOW=yes" in output
    assert "BLOCKERS=none" in output
