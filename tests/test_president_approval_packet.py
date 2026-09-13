"""Contracts for the consolidated President Approval Packet (L5, approval-first)."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

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
            "commercial_truth": "PILOT_80_USD_IN_PRINCIPLE_NO_VERIFIED_PAYMENT",
            "evidence_type": "TWO_WAY_EMAIL",
            "observed_at": "2026-09-13",
        }
    ],
    "events": [
        {
            "event": "LEAP x DeepFest 2026",
            "person": "Eman Louzon",
            "company": "KARIZMA",
            "evidence": "one pending connection request only",
        }
    ],
    "verified_revenue_sar": 0,
    "verified_paid_pilots": 0,
    "real_contacts": 1,
}


def explicit_imini_action() -> dict[str, object]:
    return {
        "action_type": "EXTERNAL_SEND",
        "target": "iMini / Jannie",
        "environment": "founder_income_lane",
        "why_now": "Two-way Gmail thread confirms an 80 USD bounded pilot in principle; exact current draft still requires founder action-bound approval before send.",
        "economic_upside": "Founder income only; NOT Dealix company revenue.",
        "risk": "medium",
        "exact_mutation": "send exactly the separately reviewed current Gmail reply once",
        "rollback": "no automated rollback; do not duplicate-send",
        "evidence": ["gmail_thread=19fd08f20e5211d4", "draft_state=DRAFT", "payment_state=NOT_VERIFIED"],
        "payload": "gmail-current-draft-content-hash-placeholder-for-test",
    }


def test_action_hash_is_deterministic_16_hex_and_payload_sensitive() -> None:
    first = packet_builder.action_hash("DEPLOY_RELEASE", "api.dealix.me", "production", "abc123")
    assert first == packet_builder.action_hash("DEPLOY_RELEASE", "api.dealix.me", "production", "abc123")
    assert re.fullmatch(r"[0-9a-f]{16}", first)
    assert first != packet_builder.action_hash("DEPLOY_RELEASE", "api.dealix.me", "production", "abc124")
    assert first != packet_builder.action_hash("EXTERNAL_SEND", "api.dealix.me", "production", "abc123")


def test_relationships_and_events_do_not_auto_create_l5_actions() -> None:
    items = packet_builder.build_items("mainsha", {}, EVIDENCE)
    assert items == []


def test_explicit_pr_heads_create_only_merge_review_item() -> None:
    items = packet_builder.build_items("mainsha", {1867: "exactsha|url|OPEN|draft=false"}, EVIDENCE, "deployedsha")
    assert len(items) == 1
    item = items[0]
    assert item["action_type"] == "MERGE_PROTECTED_MAIN"
    assert item["decision"] == "PENDING_FOUNDER"
    assert "#1867:exactsha" in item["evidence"]
    assert "payload" not in item


def test_explicit_action_manifest_produces_action_bound_hash_only() -> None:
    requested = explicit_imini_action()
    items = packet_builder.build_items("mainsha", {}, EVIDENCE, requested_actions=[requested])
    assert len(items) == 1
    item = items[0]
    for field in packet_builder.REQUIRED_FIELDS:
        assert field in item
    assert item["action_type"] == "EXTERNAL_SEND"
    assert item["target"] == "iMini / Jannie"
    assert item["decision"] == "PENDING_FOUNDER"
    assert re.fullmatch(r"[0-9a-f]{16}", item["action_hash"])
    assert "payload" not in item
    assert "NOT Dealix company revenue" in item["economic_upside"]


def test_external_send_without_direct_evidence_is_rejected() -> None:
    requested = explicit_imini_action()
    requested["evidence"] = ["NO_DIRECT_EVIDENCE_FOUND"]
    with pytest.raises(ValueError, match="direct evidence"):
        packet_builder.build_items("mainsha", {}, EVIDENCE, requested_actions=[requested])


def test_missing_or_unsupported_requested_action_fields_fail_closed() -> None:
    requested = explicit_imini_action()
    requested.pop("payload")
    with pytest.raises(ValueError, match="missing fields"):
        packet_builder.build_items("mainsha", {}, EVIDENCE, requested_actions=[requested])

    unsupported = explicit_imini_action()
    unsupported["action_type"] = "MAGIC_AUTO_SEND"
    with pytest.raises(ValueError, match="unsupported L5 action_type"):
        packet_builder.build_items("mainsha", {}, EVIDENCE, requested_actions=[unsupported])


def test_unknown_pr_head_is_rejected() -> None:
    with pytest.raises(ValueError, match="no exact current head"):
        packet_builder.build_items("mainsha", {1867: "UNKNOWN"}, EVIDENCE)


def test_evidence_for_is_context_only_and_marks_missing_entities() -> None:
    refs = packet_builder.evidence_for("imini", EVIDENCE)
    assert any("PILOT_80_USD_IN_PRINCIPLE_NO_VERIFIED_PAYMENT" in ref for ref in refs)
    assert packet_builder.evidence_for("not-present", EVIDENCE) == ["NO_DIRECT_EVIDENCE_FOUND"]


def test_collect_evidence_reads_tsv_and_truth(tmp_path: Path) -> None:
    (tmp_path / "current").mkdir()
    (tmp_path / "tables").mkdir()
    (tmp_path / "current" / "LATEST_TRUTH.json").write_text(
        json.dumps({"economic_truth": {"verified_revenue_sar": 0, "verified_paid_pilots": 0, "real_contacts": 1}}),
        encoding="utf-8",
    )
    (tmp_path / "tables" / "SCOPED_RELATIONSHIPS.tsv").write_text(
        "relationship_id\tentity\tcommercial_truth\nrel-1\tAcme\tNO_REPLY_PROVEN\n", encoding="utf-8"
    )
    evidence = packet_builder.collect_evidence(tmp_path)
    assert evidence["verified_revenue_sar"] == 0
    assert evidence["real_contacts"] == 1
    assert evidence["relationships"][0]["entity"] == "Acme"


def test_read_action_manifest_accepts_list_or_items_object(tmp_path: Path) -> None:
    action = explicit_imini_action()
    list_path = tmp_path / "list.json"
    list_path.write_text(json.dumps([action]), encoding="utf-8")
    assert packet_builder.read_action_manifest(list_path) == [action]

    object_path = tmp_path / "object.json"
    object_path.write_text(json.dumps({"items": [action]}), encoding="utf-8")
    assert packet_builder.read_action_manifest(object_path) == [action]


def test_render_markdown_contains_only_explicit_items_and_no_secrets() -> None:
    packet = packet_builder.build_packet("mainsha", {}, EVIDENCE, requested_actions=[explicit_imini_action()])
    rendered = packet_builder.render_markdown(packet)
    assert "PRESIDENT APPROVAL PACKET" in rendered
    assert packet["items"][0]["action_hash"] in rendered
    assert "counter_send_150_usd" not in rendered
    assert "#1700" not in rendered
    assert not SECRET_RE.search(rendered)


def test_empty_packet_is_explicitly_fail_closed() -> None:
    packet = packet_builder.build_packet("mainsha", {}, EVIDENCE)
    rendered = packet_builder.render_markdown(packet)
    assert packet["items"] == []
    assert "No current L5 action candidates were explicitly supplied." in rendered
