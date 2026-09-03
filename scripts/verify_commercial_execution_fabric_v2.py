#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/commercial_execution_fabric_v2.json"
SKILL = ROOT / "skills/dealix-commercial-execution/SKILL.md"
APPROVAL_CONTRACT = ROOT / "docs/ops/APPROVAL_FINGERPRINT_CONTRACT.md"


def main() -> int:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["schema"] == "dealix.commercial-execution-fabric.v2"
    assert payload["runtime_owner"] == "EXISTING_DEALIX_COMPANY_AUTOPILOT_ONLY"
    assert payload["new_scheduler"] is False
    assert payload["new_permanent_agent"] is False
    assert payload["new_crm_or_truth_store"] is False
    assert set(payload["canonical_agents"]) == {
        "dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"
    }
    research = payload["research_admission"]
    assert research["tavily"] == "ADOPT_READ_ONLY_DIRECT_HTTP_NO_NEW_SDK"
    assert research["docling"].startswith("PILOT_ISOLATED")
    assert research["stagehand"].startswith("PILOT_ISOLATED")
    assert research["new_agent_framework"] == "REJECT_DUPLICATE"

    trust = payload["trust_incident_remediation"]
    assert trust["incident_issue"] == 1440
    assert trust["caller_supplied_approval_is_execution_authority"] is False
    assert trust["caller_supplied_runtime_switches_are_execution_authority"] is False

    execution = payload["external_execution"]
    assert execution["provider_adapters_may_execute_only_after_exact_gate_pass"] is True
    assert execution["default_runtime_authority"] == "ALL_FALSE"
    assert execution["canonical_approval_identity"].startswith("ACTION_HASH=sha256(")
    assert execution["recompute_integrity_and_action_hash_before_execution"] is True
    assert execution["fresh_canonical_authority_resolver_required"] is True
    assert execution["durable_idempotency_reservation_before_provider"] is True
    assert execution["idempotency_unknown_or_inflight"] == "RECONCILE_NO_BLIND_RETRY"
    assert execution["gmail_exactly_once_claim"] is False
    assert execution["expired_revoked_suppressed_executes"] is False
    assert execution["provider_receipt_is_customer_outcome"] is False

    assert payload["channel_policy"]["founder_linkedin"] == "MANUAL_NATIVE"
    assert "cached_approval!=fresh_execution_authority" in payload["truth_firewall"]
    assert "caller_supplied_nonempty_ref!=canonical_evidence" in payload["truth_firewall"]

    approval = APPROVAL_CONTRACT.read_text(encoding="utf-8")
    assert "ACTION_HASH = sha256(action_type|target|environment|payload)[0:16]" in approval
    assert "UNKNOWN" in approval and "reconcile" in approval.lower()

    skill = SKILL.read_text(encoding="utf-8")
    assert skill.startswith("---\nname: dealix-commercial-execution\n")
    assert "External Execution Gate" in skill
    assert "ACTION_HASH = sha256" in skill
    assert "durable idempotency" in skill

    print("DEALIX_COMMERCIAL_EXECUTION_FABRIC_V2=PASS")
    print("TRUST_INCIDENT_1440=HARDENED")
    print("CANONICAL_ACTION_HASH=16_HEX")
    print("FRESH_AUTHORITY_RESOLVER=REQUIRED")
    print("DURABLE_IDEMPOTENCY=REQUIRED")
    print("GMAIL_EXACTLY_ONCE_CLAIM=NO")
    print("DEFAULT_EXTERNAL_AUTHORITY=ALL_FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
