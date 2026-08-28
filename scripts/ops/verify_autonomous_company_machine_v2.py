#!/usr/bin/env python3
"""Verify Dealix Autonomous Company Machine V2 deterministically."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "data" / "ops" / "dealix_autonomous_company_machine_v2.json"
EXPECTED_SYSTEMS = {"command_os","revenue_os","proof_os","client_os","delivery_os","support_os","finance_os","data_os","governance_os","academy_os","partner_os","venture_os"}
EXPECTED_AGENTS = {"dealix-pm","dealix-sales","dealix-delivery","dealix-engineer","dealix-content"}
FAIL_CLOSED = {"customer_send","public_publish","paid_spend","live_payment_or_refund","contract_or_legal_commitment","named_quote_commitment","production_mutation","dns_db_secret_mutation","main_merge"}
EXPECTED_FOUNDER_SURFACE = ["CASH","DECISIONS","RISKS","APPROVALS","NEXT_ACTION"]
EXPECTED_SOURCE = "631585bac79f63859ff2a9116d20d371bc9fb60a"
def verify() -> list[str]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8")); errors=[]
    if data.get("schema_version") != "2.0": errors.append("schema_version")
    if data.get("portfolio_objective") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY": errors.append("portfolio_objective")
    if data.get("source_main_sha") != EXPECTED_SOURCE: errors.append("source_main_sha")
    if (data.get("canonical_scheduler") or {}).get("parallel_company_scheduler_allowed") is not False: errors.append("parallel_scheduler_must_be_false")
    if set(data.get("agent_roster") or {}) != EXPECTED_AGENTS: errors.append("agent_roster")
    systems=data.get("systems") or []; ids=[x.get("id") for x in systems]
    if len(ids)!=len(set(ids)): errors.append("duplicate_system_id")
    if set(ids)!=EXPECTED_SYSTEMS: errors.append("system_set")
    for row in systems:
        sid=row.get("id")
        for key in ("phase","owner","state_machine","workloads","kpis"):
            if not row.get(key): errors.append(f"system_missing_{key}:{sid}")
        if len(row.get("state_machine") or []) < 5: errors.append(f"state_machine_too_small:{sid}")
    effects=data.get("external_effect_defaults") or {}
    for key in FAIL_CLOSED:
        if effects.get(key) is not False: errors.append(f"external_effect_not_fail_closed:{key}")
    firewall=set(data.get("truth_firewall") or [])
    for rule in {"research!=relationship","public_contact_data!=consent","proposal!=revenue","quote!=invoice","invoice!=payment","synthetic!=customer_proof"}:
        if rule not in firewall: errors.append(f"truth_firewall_missing:{rule}")
    dev=data.get("development_factory") or {}
    if dev.get("max_unverified_prs_per_lane") != 1: errors.append("development_wip")
    if dev.get("random_feature_factory_allowed") is not False: errors.append("random_feature_factory")
    if (dev.get("sequence") or [])[-4:] != ["DRAFT_PR","EXACT_HEAD_SOVEREIGN_VERIFICATION","READY_DECISION","LEARNING"]: errors.append("development_factory_tail")
    learning=data.get("learning_factory") or {}
    if learning.get("may_change_authority") is not False: errors.append("learning_authority")
    if learning.get("may_change_legal_or_commercial_truth") is not False: errors.append("learning_governed_truth")
    if learning.get("requires_measurable_before_after") is not True: errors.append("learning_measurement")
    observability=data.get("observability") or {}
    if observability.get("new_observability_database_allowed_by_default") is not False: errors.append("observability_db_duplication")
    if observability.get("capture_prompt_or_customer_content_by_default") is not False: errors.append("sensitive_observability_default")
    if (data.get("runtime_controls") or {}).get("kill_switches_may_only_reduce_authority") is not True: errors.append("kill_switch_authority_ceiling")
    if data.get("founder_surface") != EXPECTED_FOUNDER_SURFACE: errors.append("founder_surface")
    active=data.get("active_wip") or {}
    if active.get("p0") != "MERGED:#1329" or active.get("p1") != "MERGED:#1335_SUPERSEDES_#1330": errors.append("active_wip_contract")
    return errors
def main() -> int:
    errors=verify()
    if errors:
        print("DEALIX_AUTONOMOUS_COMPANY_MACHINE_V2=FAIL")
        for error in errors: print(f"- {error}")
        return 1
    print("DEALIX_AUTONOMOUS_COMPANY_MACHINE_V2=PASS")
    print("systems=12")
    print("portfolio_objective=CASH_READY_AUTONOMOUS_DEALIX_COMPANY")
    print("external_effects=FAIL_CLOSED")
    return 0
if __name__ == "__main__": raise SystemExit(main())
