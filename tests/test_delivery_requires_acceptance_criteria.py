"""Delivery acceptance-criteria gate tests.

The test workspace is explicitly synthetic. Real workspaces require the full
commercial handoff and must never be created merely to exercise unit tests.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "delivery"))

from client_blueprint import SIGNED_MARKERS, blueprint_status  # noqa: E402
from create_client_workspace import create_workspace  # noqa: E402

TEST_SLUG = "dry-run-test-delivery-ac"


@pytest.fixture()
def workspace():
    path = create_workspace(TEST_SLUG, overwrite=True, synthetic_test=True)
    yield path
    if path.exists():
        shutil.rmtree(path)


def _sign_acceptance_criteria(workspace: Path) -> None:
    ac = workspace / "02_solution" / "acceptance_criteria.md"
    text = ac.read_text(encoding="utf-8")
    text = text.replace("- [ ] Sponsor signature:", "- [x] Sponsor signature: Jane Doe")
    text = text.replace(
        "- [ ] Dealix delivery lead signature:",
        "- [x] Dealix delivery lead signature: Agent",
    )
    ac.write_text(text, encoding="utf-8")


def test_not_ready_when_unsigned(workspace: Path) -> None:
    report = blueprint_status(TEST_SLUG)
    assert report["acceptance_criteria_signed"] is False
    assert report["ready_to_build"] is False


def test_ready_when_signed(workspace: Path) -> None:
    _sign_acceptance_criteria(workspace)
    report = blueprint_status(TEST_SLUG)
    assert report["acceptance_criteria_signed"] is True
    assert report["ready_to_build"] is True


def test_signed_markers_present_in_template(workspace: Path) -> None:
    ac = workspace / "02_solution" / "acceptance_criteria.md"
    text = ac.read_text(encoding="utf-8")
    assert "- [ ] Sponsor signature" in text
    assert "- [ ] Dealix delivery lead signature" in text
    assert all("[x]" in marker for marker in SIGNED_MARKERS)
