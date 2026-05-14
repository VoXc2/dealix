"""Smoke: documentation governance system (canonical registry, value, policies)."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_STRATEGIC = [
    "docs/strategic/HOLDING_DOCS_HUB_AR.md",
    "docs/strategic/DOCS_CANONICAL_REGISTRY_AR.md",
    "docs/strategic/HOLDING_VALUE_REGISTRY_AR.md",
    "docs/strategic/DOCS_ARCHIVE_POLICY_AR.md",
    "docs/strategic/DOCS_ASSET_LIFECYCLE_AR.md",
    "docs/strategic/DOCS_REVIEW_CADENCE_AR.md",
    "docs/strategic/DOCS_READING_PACKS_AR.md",
    "docs/strategic/DOCS_PUBLICATION_BOUNDARY_AR.md",
    "docs/strategic/EXTERNAL_PACK_REGISTRY_AR.md",
    "docs/strategic/ARCHIVE_REVIEW_QUEUE_AR.md",
    "docs/strategic/DOCS_DECISION_RULES_AR.md",
    "docs/strategic/ASSET_USAGE_GOVERNANCE_AR.md",
    "docs/strategic/ASSET_EVIDENCE_LEVELS_AR.md",
    "docs/strategic/OS_ASSET_OPERATING_MODEL_AR.md",
    "docs/strategic/FULL_MARKET_PROOF_RUN_AR.md",
    "docs/strategic/MONTHLY_ASSET_COUNCIL_AR.md",
    "docs/strategic/QUARTERLY_PRUNING_POLICY_AR.md",
    "docs/strategic/packs/PARTNER_READING_PACK_AR.md",
    "docs/strategic/packs/INVESTOR_READING_PACK_AR.md",
    "docs/strategic/packs/OPERATOR_READING_PACK_AR.md",
    "docs/strategic/packs/PARTNER_MOTION_PACK_AR.md",
    "docs/strategic/packs/INVESTOR_MOTION_PACK_AR.md",
    "docs/strategic/packs/CLIENT_DEMO_PACK_AR.md",
]


def test_docs_governance_core_files_exist() -> None:
    for rel in CORE_STRATEGIC:
        path = REPO_ROOT / rel
        assert path.is_file(), f"missing {rel}"


def test_hub_links_to_governance_files() -> None:
    text = (
        REPO_ROOT / "docs/strategic/HOLDING_DOCS_HUB_AR.md"
    ).read_text(encoding="utf-8")
    for sub in (
        "DOCS_CANONICAL_REGISTRY_AR.md",
        "HOLDING_VALUE_REGISTRY_AR.md",
        "DOCS_ARCHIVE_POLICY_AR.md",
        "DOCS_ASSET_LIFECYCLE_AR.md",
        "DOCS_READING_PACKS_AR.md",
        "EXTERNAL_PACK_REGISTRY_AR.md",
        "ARCHIVE_REVIEW_QUEUE_AR.md",
        "DOCS_DECISION_RULES_AR.md",
        "ASSET_USAGE_GOVERNANCE_AR.md",
        "ASSET_EVIDENCE_LEVELS_AR.md",
        "OS_ASSET_OPERATING_MODEL_AR.md",
        "FULL_MARKET_PROOF_RUN_AR.md",
        "FOUNDER_SIGNAL_ROADMAP_AR.md",
        "MARKET_SIGNAL_OPERATING_LOOP_AR.md",
    ):
        assert sub in text
    assert "تشغيل الأصول بعد الفهرسة" in text
    assert "تشغيل الأصول القابضة" in text
    for motion in (
        "PARTNER_MOTION_PACK_AR.md",
        "INVESTOR_MOTION_PACK_AR.md",
        "CLIENT_DEMO_PACK_AR.md",
    ):
        assert motion in text


def test_snapshot_has_reasonable_doc_count() -> None:
    p = REPO_ROOT / "docs/strategic/_generated/docs_top_level_snapshot.json"
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("docs_top_level_dir_count", 0) >= 80


def test_holding_value_registry_has_core_assets() -> None:
    text = (
        REPO_ROOT / "docs/strategic/HOLDING_VALUE_REGISTRY_AR.md"
    ).read_text(encoding="utf-8")
    for asset in (
        "HOLDING_DOCS_HUB_AR",
        "HOLDING_OFFER_MATRIX_AR",
        "PROOF_DEMO_PACK_5_CLIENTS_AR",
        "RETAINER_PILOT_MINI_AR",
        "BU4_TRUST_ACTIVATION_GATE_AR",
        "IP_LICENSE_OUTLINE_AR",
    ):
        assert asset in text


def test_holding_value_summary_json_valid() -> None:
    p = REPO_ROOT / "docs/strategic/_generated/holding_value_summary.json"
    assert p.is_file(), "run py -3 scripts/generate_holding_value_summary.py"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("asset_count", 0) >= 5
    for key in (
        "top_revenue_assets",
        "top_trust_assets",
        "top_partner_assets",
        "top_investor_assets",
        "top_holding_assets",
        "recommended_for_partner_pack",
        "recommended_for_investor_pack",
        "recommended_for_client_pack",
        "archive_review_candidates",
        "missing_boundary_candidates",
        "assets_missing_status",
        "assets_missing_publication_boundary",
        "assets_recommended_for_partner_pack",
        "assets_recommended_for_archive_review",
    ):
        assert key in data
        assert isinstance(data[key], list)


def test_docs_asset_usage_log_is_json_object() -> None:
    p = REPO_ROOT / "data/docs_asset_usage_log.json"
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert isinstance(data.get("entries"), list)


def test_asset_activation_priorities_json_valid() -> None:
    p = REPO_ROOT / "docs/strategic/_generated/asset_activation_priorities.json"
    assert p.is_file(), "run py -3 scripts/generate_holding_value_summary.py"
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ("activation_priorities", "governance_risks", "archive_candidates"):
        assert key in data
        assert isinstance(data[key], list)


def test_asset_evidence_and_capital_json_valid() -> None:
    evp = REPO_ROOT / "docs/strategic/_generated/asset_evidence_summary.json"
    cap = REPO_ROOT / "docs/strategic/_generated/asset_capital_allocation.json"
    assert evp.is_file(), "run py -3 scripts/generate_holding_value_summary.py"
    assert cap.is_file(), "run py -3 scripts/generate_holding_value_summary.py"
    ev = json.loads(evp.read_text(encoding="utf-8"))
    assert "counts_by_level" in ev and isinstance(ev["counts_by_level"], dict)
    assert "assets_by_level" in ev and isinstance(ev["assets_by_level"], dict)
    c = json.loads(cap.read_text(encoding="utf-8"))
    for key in ("invest", "activate", "maintain", "archive_review"):
        assert key in c
        assert isinstance(c[key], list)


def test_command_center_spine_markers_present() -> None:
    import importlib.util

    script = REPO_ROOT / "scripts" / "validate_docs_governance.py"
    spec = importlib.util.spec_from_file_location("_vdg_cc", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    text = (
        REPO_ROOT / mod.FULL_MARKET_PROOF_RUN_REL
    ).read_text(encoding="utf-8")
    errs = mod.audit_command_center_markers(text)
    assert errs == [], "; ".join(errs)


def test_usage_log_l4_entries_satisfy_audit() -> None:
    import importlib.util

    script = REPO_ROOT / "scripts" / "validate_docs_governance.py"
    spec = importlib.util.spec_from_file_location("_vdg_audit", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = json.loads(
        (REPO_ROOT / "data/docs_asset_usage_log.json").read_text(encoding="utf-8"),
    )
    errs = mod.audit_usage_log_entries(data.get("entries"))
    assert errs == [], "; ".join(errs)
