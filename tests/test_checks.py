"""Every launch check must pass against the committed assets."""
import importlib

import pytest

COMPONENT_CHECKS = [
    "check_file_manifest",
    "check_schema_contracts",
    "check_business_os_catalog",
    "check_need_intelligence",
    "check_account_pack_contract",
    "check_email_quality_gate",
    "check_proposal_gate",
    "check_delivery_gate",
    "check_security_privacy_gates",
    "check_site_routes",
]


@pytest.mark.parametrize("module_name", COMPONENT_CHECKS)
def test_check_passes(module_name):
    mod = importlib.import_module(module_name)
    result = mod.check()
    assert result.passed, f"{module_name} failed: {result.errors}"
