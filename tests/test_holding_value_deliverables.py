"""Smoke: strategic holding-value plan deliverables exist under docs/."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

HOLDING_MARKDOWN: tuple[Path, ...] = (
    REPO_ROOT / "docs/strategic/HOLDING_OFFER_MATRIX_AR.md",
    REPO_ROOT / "docs/strategic/HOLDING_DOCS_HUB_AR.md",
    REPO_ROOT / "docs/commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md",
    REPO_ROOT / "docs/commercial/RETAINER_PILOT_MINI_AR.md",
    REPO_ROOT / "docs/enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md",
    REPO_ROOT / "docs/40_partners/IP_LICENSE_OUTLINE_AR.md",
    REPO_ROOT / "docs/strategic/DEALIX_EXECUTION_WAVES_AR.md",
)

DOCS_TOP_LEVEL_SNAPSHOT = (
    REPO_ROOT / "docs/strategic/_generated/docs_top_level_snapshot.json"
)


def test_holding_value_markdown_files_exist() -> None:
    for path in HOLDING_MARKDOWN:
        assert path.is_file(), f"expected file at {path.relative_to(REPO_ROOT)}"
        text = path.read_text(encoding="utf-8")
        assert len(text.strip()) > 80, f"unexpected empty doc: {path.name}"


def test_holding_docs_hub_has_anchor_sections() -> None:
    hub = (REPO_ROOT / "docs/strategic/HOLDING_DOCS_HUB_AR.md").read_text(
        encoding="utf-8",
    )
    assert "طبقة 00–25" in hub
    assert "شهادة تشغيل" in hub
    assert "_generated/docs_top_level_snapshot.json" in hub


def test_docs_top_level_snapshot_json() -> None:
    path = DOCS_TOP_LEVEL_SNAPSHOT
    assert path.is_file(), f"expected {path.relative_to(REPO_ROOT)}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data.get("repo_root") == "."
    count = int(data["docs_top_level_dir_count"])
    assert count >= 80, f"expected many docs top-level dirs, got {count}"
    entries = data["entries"]
    assert isinstance(entries, list) and len(entries) == count
    names = {e["name"] for e in entries}
    assert "00_constitution" in names
    assert "26_service_catalog" in names


def test_holding_offer_matrix_lists_scale_doc_folders() -> None:
    matrix = (
        REPO_ROOT / "docs/strategic/HOLDING_OFFER_MATRIX_AR.md"
    ).read_text(encoding="utf-8")
    for n in range(26, 45):
        assert f"docs/{n}_" in matrix, f"matrix should reference docs/{n}_*"


def test_execution_waves_links_holding_section() -> None:
    waves = (
        REPO_ROOT / "docs/strategic/DEALIX_EXECUTION_WAVES_AR.md"
    ).read_text(encoding="utf-8")
    assert "من الملفات إلى قيمة قابضة" in waves
    assert "HOLDING_OFFER_MATRIX_AR.md" in waves
    assert "BU4_TRUST_ACTIVATION_GATE_AR.md" in waves
    assert "IP_LICENSE_OUTLINE_AR.md" in waves
    assert "HOLDING_DOCS_HUB_AR.md" in waves
    assert "DOCS_CANONICAL_REGISTRY_AR.md" in waves
    assert "validate_docs_governance.py" in waves
