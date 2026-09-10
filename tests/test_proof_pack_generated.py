"""Client proof-pack generation tests using an explicit synthetic workspace."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "delivery"))

from client_proof import PROOF_FILES, proof_pack  # noqa: E402
from create_client_workspace import create_workspace  # noqa: E402

TEST_SLUG = "dry-run-test-delivery-proof"


@pytest.fixture()
def workspace():
    path = create_workspace(TEST_SLUG, overwrite=True, synthetic_test=True)
    yield path
    if path.exists():
        shutil.rmtree(path)


def test_proof_pack_generated(workspace: Path) -> None:
    pack = proof_pack(TEST_SLUG)
    assert pack.exists()
    text = pack.read_text(encoding="utf-8")
    assert "Proof Pack" in text
    for name in PROOF_FILES:
        assert name in text, f"proof pack missing section: {name}"


def test_proof_pack_reports_missing_files(workspace: Path) -> None:
    missing = workspace / "05_proof" / "open_risks.md"
    missing.unlink()
    pack = proof_pack(TEST_SLUG)
    text = pack.read_text(encoding="utf-8")
    assert "Missing proof files" in text
    assert "open_risks.md" in text


def test_proof_pack_doctrine_header(workspace: Path) -> None:
    pack = proof_pack(TEST_SLUG)
    text = pack.read_text(encoding="utf-8")
    assert "Map -> Design -> Build -> Operate -> Scale" in text
