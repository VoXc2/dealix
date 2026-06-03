"""Data-contract checks must pass: schemas, catalog, need intelligence, packs."""
import pytest

CHECKS = [
    "scripts/checks/check_file_manifest.py",
    "scripts/checks/check_schema_contracts.py",
    "scripts/checks/check_business_os_catalog.py",
    "scripts/checks/check_need_intelligence.py",
    "scripts/checks/check_account_pack_contract.py",
]


@pytest.mark.parametrize("script", CHECKS)
def test_data_contract(run_check, script):
    proc = run_check(script)
    assert proc.returncode == 0, f"{script} failed:\n{proc.stdout}\n{proc.stderr}"
