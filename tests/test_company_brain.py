"""Phase D — schema-level guarantees for a future company_brain module.

The closure prompts referenced ``tests/test_company_brain.py``. The
module itself is not yet implemented in this repo. This file marks
the gap honestly with ``pytest.skip`` and pins the future contract:
when ``CompanyBrain`` ships, it must respect a small set of
schema-level guarantees that this test will then enforce.

This is a deliberate placeholder. NEVER replace it with fake-green
assertions; it must stay skipped until the real module exists.
"""
from __future__ import annotations

import importlib

import pytest


def _module_exists(dotted_name: str) -> bool:
    try:
        importlib.import_module(dotted_name)
        return True
    except ModuleNotFoundError:
        return False


COMPANY_BRAIN_MODULES = [
    "auto_client_acquisition.company_brain",
    "auto_client_acquisition.self_growth_os.company_brain",
    "core.brain.company_brain",
    "dealix.brain.company_brain",
]


def _find_company_brain_module() -> str | None:
    for name in COMPANY_BRAIN_MODULES:
        if _module_exists(name):
            return name
    return None


def test_company_brain_module_status_recorded():
    """Either the module exists (run schema tests) or it doesn't
    (skip honestly). Never fake-green."""
    module = _find_company_brain_module()
    if module is None:
        pytest.skip(
            "CompanyBrain module is not yet implemented. "
            "Candidates checked: "
            + ", ".join(COMPANY_BRAIN_MODULES)
            + ". When the module ships, this test will run the "
            "schema guarantees below."
        )

    # The contract below applies once the module exists.
    mod = importlib.import_module(module)

    # Required public surface (refine when the module ships):
    #   - a CompanyBrain class or factory
    #   - a query() method that takes a string and returns a result
    #     containing citations
    cls_or_factory = getattr(mod, "CompanyBrain", None) or getattr(
        mod, "build_company_brain", None
    )
    assert cls_or_factory is not None, (
        f"{module} must expose CompanyBrain class or build_company_brain factory"
    )


def test_company_brain_no_external_calls_in_test_path():
    """When the module exists, this test will assert that schema-level
    instantiation does not require network. For now: skip."""
    if _find_company_brain_module() is None:
        pytest.skip("CompanyBrain not yet implemented (see sibling test).")
    # When ready: instantiate with mock provider, assert no httpx calls.
