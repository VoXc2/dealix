"""Governed client-delivery workspace creation tests.

Real delivery workspaces require a complete commercial handoff. Unit tests use
the explicit synthetic-test lane so they cannot manufacture customer/payment
truth while still exercising the real template and lifecycle code.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "delivery"))

from create_client_workspace import (  # noqa: E402
    PHASES,
    SYNTHETIC_MARKER,
    create_workspace,
    template_complete,
)

TEST_SLUG = "dry-run-test-delivery-demo"


@pytest.fixture()
def workspace():
    """Create and tear down an explicitly synthetic delivery workspace."""
    path = create_workspace(
        TEST_SLUG,
        client_name="Test Delivery Demo",
        overwrite=True,
        synthetic_test=True,
    )
    yield path
    if path.exists():
        shutil.rmtree(path)


def test_template_is_complete() -> None:
    assert template_complete(), "clients/_template is missing expected phase files"


def test_workspace_has_all_phases(workspace: Path) -> None:
    for phase in PHASES:
        assert (workspace / phase).is_dir(), f"missing phase directory: {phase}"


def test_workspace_has_all_phase_files(workspace: Path) -> None:
    for phase, files in PHASES.items():
        for name in files:
            assert (workspace / phase / name).is_file(), f"missing {phase}/{name}"


def test_workspace_readme_and_handoff_are_truthful(workspace: Path) -> None:
    readme = workspace / "README.md"
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "customer-specific delivery workspace" in text
    assert "30-Day Revenue Command Pilot" not in text
    assert f"Handoff mode: {SYNTHETIC_MARKER}" in text

    handoff = (workspace / "COMMERCIAL_HANDOFF.json").read_text(encoding="utf-8")
    assert SYNTHETIC_MARKER in handoff
    assert "quote_is_not_payment" in handoff
    assert "delivery_is_not_customer_value" in handoff
    assert "customer_specific_after_qualified_discovery" in handoff
    assert "30-Day Revenue Command Pilot" not in handoff


def test_create_workspace_refuses_duplicate(workspace: Path) -> None:
    with pytest.raises(FileExistsError):
        create_workspace(TEST_SLUG, synthetic_test=True)


def test_real_workspace_without_commercial_handoff_is_rejected(tmp_path) -> None:
    with pytest.raises(RuntimeError, match="commercial workspace is required"):
        create_workspace("real-client-without-handoff")
