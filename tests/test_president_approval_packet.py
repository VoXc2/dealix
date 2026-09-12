"""Contracts for the consolidated President Approval Packet (L5, approval-first)."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


packet_builder = _load("build_president_approval_packet")

EVIDENCE = {
    "relationships": [
        {
            "relationship_id": "rel-imini-001",
            "scope": "FOUNDER_INCOME",
            "entity": "iMini / Jannie",
            "commercial_truth": "NEGOTIATION_EXISTS_NO_VERIFIED_PAYMENT",
            "evidence_type": "TWO_WAY_EMAIL",
            "observed_at": "2026-08-24",
        }
    ],
    "events": [
        {
            "event": "LEAP x DeepFest 2026",
            "person": "Eman Louzon",
            "company": "KARIZMA",
            "evidence": "Gmail message confirms one pending connection request",
        }
    ],
    "verified_revenue_sar": 0,
    "verified_paid_pilots": 0,
    "real_contacts": 0,
}


def test_action_hash_is_deterministic_16_hex_and_payload_sensitive() -> None:
    first = packet_builder.action_hash("DEPLOY_RELEASE", "api.dealix.me", "production", "abc123")
    assert first == packet_builder.action_hash("DEPLOY_RELEASE", "api.dealix.me", "production", "abc123")
    assert re.fullmatch(r"[0-9a-f]{16}", first)
    assert first != packet_builder.action_hash("DEPLOY_RELEASE", "api.dealix.me", "production", "abc124")
    assert first != packet_builder.action_hash("EXTERNAL_SEND", "api.dealix.me", "production", "abc123")


def test_build_items_has_required_fields_and_pending_decisions() -> None:
    items = packet_builder.build_items("mainsha", {1700: "sha1700|url"}, EVIDENCE, "deployedsha")
    assert items
    for item in items:
        for field in packet_builder.REQUIRED_FIELDS:
            assert field in item, (item.get("action_type"), field)
        assert item["decision"] == "PENDING_FOUNDER"
        assert item["evidence"]
    action_types = {item["action_type"] for item in items}
    assert {"MERGE_PROTECTED_MAIN", "DEPLOY_RELEASE", "FIX_TLS_SAN", "EXTERNAL_SEND"} <= action_types


def test_packet_keeps_founder_income_scope_out_of_company_revenue() -> None:
    items = packet_builder.build_items("mainsha", {}, EVIDENCE)
    imini = next(item for item in items if "iMini" in item["target"])
    assert "NOT Dealix company revenue" in imini["economic_upside"]
    assert any("NEGOTIATION_EXISTS_NO_VERIFIED_PAYMENT" in ref for ref in imini["evidence"])


def test_event_evidence_is_attached_to_karizma_item() -> None:
    items = packet_builder.build_items("mainsha", {}, EVIDENCE)
    karizma = next(item for item in items if "KARIZMA" in item["target"])
    assert any("LEAP x DeepFest 2026" in ref for ref in karizma["evidence"])


def test_missing_entities_mark_no_direct_evidence() -> None:
    items = packet_builder.build_items("mainsha", {}, {})
    for item in items:
        if item["action_type"] == "EXTERNAL_SEND":
            assert "NO_DIRECT_EVIDENCE_FOUND" in item["evidence"]


def test_collect_evidence_reads_tsv_and_truth(tmp_path: Path) -> None:
    (tmp_path / "current").mkdir()
    (tmp_path / "tables").mkdir()
    (tmp_path / "current" / "LATEST_TRUTH.json").write_text(
        json.dumps({"economic_truth": {"verified_revenue_sar": 0, "verified_paid_pilots": 0, "real_contacts": 0}}),
        encoding="utf-8",
    )
    (tmp_path / "tables" / "SCOPED_RELATIONSHIPS.tsv").write_text(
        "relationship_id\tentity\tcommercial_truth\nrel-1\tAcme\tNO_REPLY_PROVEN\n", encoding="utf-8"
    )
    evidence = packet_builder.collect_evidence(tmp_path)
    assert evidence["verified_revenue_sar"] == 0
    assert evidence["relationships"][0]["entity"] == "Acme"


def test_render_markdown_contains_every_item_and_no_secrets() -> None:
    packet = packet_builder.build_packet("mainsha", {1700: "sha1700|url"}, EVIDENCE)
    rendered = packet_builder.render_markdown(packet)
    assert "PRESIDENT APPROVAL PACKET" in rendered
    for item in packet["items"]:
        assert item["action_hash"] in rendered
    assert not SECRET_RE.search(rendered)
