#!/usr/bin/env python3
"""Bridge inbound website diagnostics into the canonical Dealix Company OS cycle.

This is an internal/read-only bridge over the existing Revenue Ops Autopilot
store. It does not create a new CRM, scheduler, approval system or proof ledger.
It materializes one daily intake report containing the five canonical agent
work packets and evidence gaps for each real website diagnostic submission.

No external send, publish, payment, merge, deploy, DNS/DB/secret mutation or
binding commercial commitment is performed.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.diagnostic_intake_orchestrator import (  # noqa: E402
    load_company_os_inbound_diagnostics,
)

OUT_DIR = ROOT / "reports" / "self_operating_company_os" / "inbound_diagnostics"

CANONICAL_AGENTS = [
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
]

FORBIDDEN_ENV_FLAGS = {
    "DEALIX_EXTERNAL_SEND": "1",
    "DEALIX_EMAIL_LIVE_SEND": "1",
    "DEALIX_WHATSAPP_OUTBOUND": "1",
    "DEALIX_PUBLIC_PUBLISH": "1",
    "DEALIX_PAID_SPEND": "1",
    "DEALIX_PAYMENT_EXECUTION": "1",
    "DEALIX_PRODUCTION_MUTATION": "1",
    "DEALIX_DNS_MUTATION": "1",
    "DEALIX_DB_MUTATION": "1",
    "DEALIX_SECRET_MUTATION": "1",
}


def _tripwire() -> list[str]:
    violations: list[str] = []
    for key, bad_value in FORBIDDEN_ENV_FLAGS.items():
        if os.getenv(key, "").strip().lower() == bad_value.lower():
            violations.append(f"{key}={bad_value}")
    return violations


def _validate_case(case: dict) -> list[str]:
    errors: list[str] = []
    packets = case.get("work_packets") or []
    agents = [str(packet.get("agent") or "") for packet in packets]
    if agents != CANONICAL_AGENTS:
        errors.append(f"{case.get('lead_id')}:canonical_agents_mismatch")

    authority = case.get("material_authority") or {}
    if not authority or any(bool(value) for value in authority.values()):
        errors.append(f"{case.get('lead_id')}:material_authority_not_all_false")

    if case.get("external_followup_eligible") is False:
        if str(case.get("relationship_state")) == "INBOUND":
            errors.append(f"{case.get('lead_id')}:no_followup_must_not_be_inbound_dispatch_state")
        if str(case.get("consent_state")) == "INBOUND_REQUEST":
            errors.append(f"{case.get('lead_id')}:no_followup_must_not_have_inbound_request_consent")

    if str(case.get("commercial_stage")) != "REAL_INTERACTION":
        errors.append(f"{case.get('lead_id')}:unexpected_commercial_stage")
    if str(case.get("problem_state")) not in {
        "UNPROVEN_NEEDS_EVIDENCE",
        "HYPOTHESIS_WITH_BASELINE_PENDING_VALIDATION",
    }:
        errors.append(f"{case.get('lead_id')}:problem_state_overpromoted")
    return errors


def main() -> int:
    violations = _tripwire()
    if violations:
        print(json.dumps({"ok": False, "tripwire": violations}, ensure_ascii=False, indent=2))
        return 2

    cases = load_company_os_inbound_diagnostics(limit=100)
    errors: list[str] = []
    for case in cases:
        errors.extend(_validate_case(case))
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    path = OUT_DIR / f"{date}.json"
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "source": "canonical_revenue_ops_autopilot",
        "queue_kind": "real_inbound_execution_diagnostics",
        "cases": cases,
        "case_count": len(cases),
        "followup_requested_count": sum(bool(case.get("external_followup_eligible")) for case in cases),
        "material_authority": {
            "external_send": False,
            "public_publish": False,
            "paid_spend": False,
            "payment_execution": False,
            "production_mutation": False,
            "binding_commercial_commitment": False,
        },
        "truth_firewall": [
            "inbound_request_is_not_qualified_problem",
            "customer_reported_context_is_not_verified_customer_proof",
            "followup_request_is_not_direct_marketing_consent",
            "draft_is_not_sent",
            "quote_is_not_invoice",
            "invoice_is_not_payment",
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "report": str(path.relative_to(ROOT)),
                "cases": len(cases),
                "followup_requested": payload["followup_requested_count"],
                "external_action": "none",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
