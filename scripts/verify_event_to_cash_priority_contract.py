#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/event_to_cash_priority_contract_v1.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    require(CONTRACT.exists(), "missing event-to-cash contract", errors)
    if errors:
        print("DEALIX_EVENT_TO_CASH_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(contract.get("schema") == "dealix.event-to-cash-priority.v1", "wrong schema", errors)
    require(contract.get("timezone") == "Asia/Riyadh", "event timezone drift", errors)

    window = contract.get("priority_window", {})
    require(window.get("priority_override") is True, "event priority override missing", errors)
    events = window.get("events", [])
    names = {event.get("name") for event in events}
    for required in ("Big 5 Construct Saudi 2026", "LEAP 2026", "DeepFest 2026"):
        require(required in names, f"missing event: {required}", errors)
    require(all(bool(event.get("official_source")) for event in events), "event source reference missing", errors)

    truth = contract.get("truth_invariants", {})
    for key in (
        "research_target_is_relationship",
        "event_attendee_is_relationship",
        "badge_scan_is_relationship",
        "connection_request_is_relationship",
        "message_sent_is_relationship",
        "proposal_is_revenue",
        "invoice_is_payment",
        "synthetic_is_customer_proof",
    ):
        require(truth.get(key) is False, f"truth invariant failed: {key}", errors)

    relationship_requirements = set(contract.get("relationship_promotion_requires", []))
    for required in (
        "real_two_way_interaction_evidence",
        "counterparty_identity_or_bounded_identifier",
        "interaction_timestamp",
        "event_or_channel_source_ref",
    ):
        require(required in relationship_requirements, f"relationship evidence gate missing: {required}", errors)

    receipt_fields = set(contract.get("interaction_receipt_fields", []))
    for required in (
        "person_or_contact_ref",
        "company",
        "event_or_channel",
        "timestamp",
        "what_they_actually_said",
        "followup_permission_state",
        "evidence_ref",
        "next_evidence_required",
        "next_action",
        "owner",
    ):
        require(required in receipt_fields, f"interaction receipt field missing: {required}", errors)

    stage_path = contract.get("stage_path", [])
    required_order = [
        "RESEARCH",
        "REAL_INTERACTION",
        "VERIFIED_RELATIONSHIP",
        "QUALIFIED_PROBLEM",
        "FREE_MINI_DIAGNOSTIC",
        "QUALIFIED_DISCOVERY",
        "CUSTOMER_SPECIFIC_QUOTE",
        "PILOT_DECISION",
        "VERIFIED_PAYMENT",
        "DELIVERY",
        "ACCEPTED_PROOF",
        "EXPANSION_OR_REFERRAL",
    ]
    require(stage_path == required_order, "commercial stage path drift", errors)

    economics = set(contract.get("funnel_economics_required", []))
    for required in (
        "verified_stage_delta",
        "founder_minutes",
        "elapsed_minutes",
        "risk_class",
        "evidence_refs",
        "next_evidence_required",
    ):
        require(required in economics, f"funnel economics field missing: {required}", errors)

    authority = contract.get("authority", {})
    require(authority.get("auto_research") is True, "safe research should remain autonomous", errors)
    require(authority.get("auto_capture_internal_receipt") is True, "internal capture should remain autonomous", errors)
    require(authority.get("auto_prepare_followup_draft") is True, "follow-up drafting should remain autonomous", errors)
    require(authority.get("auto_prepare_diagnostic_seed") is True, "diagnostic preparation should remain autonomous", errors)
    for key in ("external_send", "public_publish", "payment_execution", "quote_or_contract_commitment"):
        require(authority.get(key) is False, f"sensitive authority must stay false: {key}", errors)

    wip = contract.get("daily_wip", {})
    require(wip.get("max_active_company_p0s") == 3, "company P0 WIP drift", errors)
    require(wip.get("max_event_target_accounts") <= 12, "event account WIP too high", errors)
    require(wip.get("max_same_day_followup_drafts") <= 8, "follow-up draft WIP too high", errors)
    require(wip.get("required_next_evidence_per_task") is True, "next-evidence requirement missing", errors)

    if errors:
        print("DEALIX_EVENT_TO_CASH_VERDICT=FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("DEALIX_EVENT_TO_CASH_VERDICT=PASS")
    print("EVENTS=BIG5,LEAP,DEEPFEST")
    print("RELATIONSHIP_PROMOTION=EVIDENCE_GATED")
    print("SAFE_INTERNAL_AUTONOMY=ON")
    print("EXTERNAL_EFFECTS=APPROVAL_GATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
