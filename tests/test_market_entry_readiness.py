from __future__ import annotations

import csv
from copy import deepcopy
from pathlib import Path

import yaml

from dealix.commercial_ops.market_entry_readiness import (
    audit_pilot_pricing,
    build_market_entry_snapshot,
    load_market_entry_signals,
    write_market_entry_artifacts,
)

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "data/examples/dealix_market_entry_signals.demo.yaml"


def _evidenced_payload() -> dict:
    payload = yaml.safe_load(DEMO.read_text(encoding="utf-8"))
    for row in payload["signals"].values():
        row.update(
            status="pass",
            observed_at="2026-07-15T09:00:00Z",
            evidence_ref="https://example.test/evidence",
        )
    metrics = {
        "warm_permissioned_accounts": 5,
        "paid_pilots_completed": 5,
        "signed_proof_packs": 3,
        "consented_case_studies": 1,
        "active_retainer_customers": 3,
        "gross_margin_samples": 3,
        "pilot_gross_margin_rate": 0.55,
        "delivery_capacity_per_month": 3,
        "on_time_delivery_samples": 5,
        "on_time_delivery_rate": 0.9,
        "median_time_to_first_value_days": 7,
        "retainer_renewal_samples": 3,
        "retainer_renewal_rate": 0.7,
        "cac_samples": 5,
        "cac_payback_months": 3,
    }
    for key, value in metrics.items():
        payload["metrics"][key].update(
            value=value,
            observed_at="2026-07-15T09:00:00Z",
            evidence_ref="https://example.test/metric",
        )
    return payload


def test_demo_snapshot_fails_closed_without_fake_market_readiness() -> None:
    payload = load_market_entry_signals(DEMO)
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    assert snapshot["stage"] == "evidence_required"
    assert snapshot["public_claims_authorized"] is False
    assert snapshot["scale_authorized"] is False
    assert snapshot["external_actions_executed"] == 0


def test_primary_offer_is_governed_and_quote_only_after_discovery() -> None:
    audit = audit_pilot_pricing(ROOT)
    assert audit["ok"] is True
    assert audit["offer_id"] == "revenue_command_pilot_30d"
    assert audit["duration_days"] is None
    assert audit["duration_policy"] == "customer_specific_after_qualified_discovery"
    assert audit["pilot_price"] is None
    assert audit["pricing_status"] == "no_public_amount_until_validation"
    assert audit["publication_status"] == "founder_approval_required"
    assert audit["quote_only_sources_consistent"] is True
    assert audit["legacy_offer_public"] is False
    assert audit["observed"]["finance_catalog"] == {
        "pricing_basis": "quote_only",
        "price_sar": None,
    }
    assert audit["observed"]["product_catalog"]["setup_sar"] is None
    assert audit["observed"]["pricing_rules"]["min"] is None
    assert audit["observed"]["pricing_rules"]["max"] is None


def test_positive_metric_without_evidence_is_not_accepted() -> None:
    payload = _evidenced_payload()
    payload["metrics"]["paid_pilots_completed"] = {
        "value": 99,
        "observed_at": "",
        "evidence_ref": "",
    }
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    assert snapshot["stage"] == "private_pilot_ready"
    gate = next(
        row
        for row in snapshot["gates"]
        if row["gate_id"] == "paid_pilots_completed" and row["stage"] == "limited_launch_ready"
    )
    assert gate["ok"] is False
    assert "غير موثق" in gate["reason_ar"]


def test_invalid_observed_at_is_not_accepted_as_evidence() -> None:
    payload = _evidenced_payload()
    payload["signals"]["founder_offer_approved"]["observed_at"] = "not-a-timestamp"
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    assert snapshot["stage"] == "evidence_required"
    gate = next(
        row for row in snapshot["gates"] if row["gate_id"] == "founder_offer_approved"
    )
    assert gate["ok"] is False
    assert "missing timestamp" in gate["evidence"]


def test_all_evidenced_gates_reach_scale_ready() -> None:
    snapshot = build_market_entry_snapshot(_evidenced_payload(), repo_root=ROOT)
    assert snapshot["stage"] == "scale_ready"
    assert snapshot["public_claims_authorized"] is True
    assert snapshot["scale_authorized"] is True


def test_explicit_external_execution_failure_blocks_all_stages() -> None:
    payload = _evidenced_payload()
    payload["signals"]["external_execution_default_off"]["status"] = "fail"
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    assert snapshot["stage"] == "blocked"
    assert snapshot["public_claims_authorized"] is False
    assert snapshot["external_actions_executed"] == 0
    blocker = snapshot["next_stage_blockers"][0]
    assert blocker["gate_id"] == "external_execution_default_off"
    assert blocker["remediation_ar"]


def test_blocked_snapshot_still_writes_fail_closed_report(tmp_path: Path) -> None:
    payload = _evidenced_payload()
    payload["signals"]["external_execution_default_off"]["status"] = "fail"
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    written = write_market_entry_artifacts(snapshot, tmp_path)
    assert len(written) == 12
    brief = (tmp_path / "founder_market_entry_brief_ar.md").read_text(
        encoding="utf-8"
    )
    assert "external_execution_default_off" in brief
    assert "أوقف التنفيذ الخارجي افتراضيًا" in brief


def test_private_pilot_does_not_require_public_production_gates() -> None:
    payload = _evidenced_payload()
    for key in (
        "production_health",
        "ci_required_checks_green",
        "production_secrets_rotated",
        "payment_path_approved",
    ):
        payload["signals"][key]["status"] = "unknown"
        payload["signals"][key]["evidence_ref"] = ""
        payload["signals"][key]["observed_at"] = ""
    payload["metrics"]["paid_pilots_completed"]["value"] = 0
    payload["metrics"]["signed_proof_packs"]["value"] = 0
    payload["metrics"]["consented_case_studies"]["value"] = 0
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    assert snapshot["stage"] == "private_pilot_ready"


def test_writer_creates_reviewable_boards_without_invented_contacts(tmp_path: Path) -> None:
    snapshot = build_market_entry_snapshot(load_market_entry_signals(DEMO), repo_root=ROOT)
    written = write_market_entry_artifacts(snapshot, tmp_path)
    assert len(written) == 12
    assert all(path.is_file() for path in written)
    with (tmp_path / "contacts_radar.csv").open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == []
    brief = (tmp_path / "founder_market_entry_brief_ar.md").read_text(encoding="utf-8")
    assert "وجود الكود أو الاختبارات لا" in brief


def test_input_payload_is_not_mutated() -> None:
    payload = _evidenced_payload()
    original = deepcopy(payload)
    build_market_entry_snapshot(payload, repo_root=ROOT)
    assert payload == original

def test_market_entry_runbook_matches_founder_offer_decision() -> None:
    runbook = (ROOT / "docs/commercial/FOUNDER_MARKET_ENTRY_EXECUTION_AR.md").read_text(
        encoding="utf-8"
    )
    assert "Revenue Command Pilot" in runbook
    assert "30 يومًا" in runbook
    assert "السعر العام غير معتمد" in runbook
    assert "السعر الكانوني الفعلي في الكود اليوم" not in runbook
