#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

COMMAND_SCHEMA = "dealix.commercial_autopilot.command.v1"
WORKLOAD_SCHEMA = "dealix.agent-council-growth-workloads.v1"
ROLES = {
    "president",
    "market_intelligence",
    "revenue",
    "content_strategist",
    "creative_director",
    "distribution_manager",
    "lifecycle_agent",
    "experiment_analyst",
    "proof_agent",
    "governance_agent",
}

INTERNAL_ACTIONS = {
    "research",
    "qualify",
    "draft",
    "prepare_diagnostic",
    "prepare_proposal",
    "prepare_negotiation",
    "internal_review",
    "update_internal_queue",
}


def _role_for(item: dict[str, Any]) -> str:
    hint = str(item.get("workload_hint", "")).strip()
    if hint in ROLES:
        return hint

    action_class = str(item.get("action_class", ""))
    action = str(item.get("proposed_action", ""))
    channel = str(item.get("channel", "internal"))
    stage = str(item.get("stage", "ATTENTION"))
    signal = item.get("signal") if isinstance(item.get("signal"), dict) else {}
    signal_type = str(signal.get("signal_type", ""))
    asset_family = str(item.get("asset_family", ""))

    if action_class in {"BLOCKED", "SPECIFIC_APPROVAL_REQUIRED", "EXECUTION_AUTHORIZED"}:
        return "governance_agent"
    if action_class == "MANUAL_NATIVE":
        return "revenue"

    if action in {"prepare_proposal", "prepare_negotiation", "prepare_diagnostic", "qualify"}:
        return "revenue"
    if stage in {"DISCOVERY", "CUSTOMER_SPECIFIC_QUOTE", "PILOT_AGREED"}:
        return "revenue"
    if stage in {"PAYMENT_VERIFIED", "DELIVERY_PROOF", "REFERRAL_OR_EXPANSION"}:
        return "proof_agent"

    if signal_type in {
        "job_change",
        "hiring_or_headcount_change",
        "funding_or_expansion",
        "technology_or_stack_change",
        "competitor_mention",
        "procurement_or_tender_signal",
        "partner_or_referral_signal",
        "event_presence_or_interaction",
    }:
        return "market_intelligence"
    if signal_type in {"inbound_request", "real_reply", "website_or_product_activity"}:
        return "lifecycle_agent"

    if asset_family in {
        "founder_linkedin",
        "dealix_company_post",
        "arabic_english_article",
        "email_sales_snippet",
        "event_talking_point",
        "faq_objection_answer",
    }:
        return "content_strategist"
    if asset_family in {"carousel_document", "short_video", "youtube_seed", "storyboard", "thumbnail"}:
        return "creative_director"
    if channel in {"dealix_linkedin_page", "tiktok", "youtube", "meta_owned_social"}:
        return "distribution_manager"

    if action == "research":
        return "market_intelligence"
    if action == "update_internal_queue":
        return "president"
    return "revenue"


def _packet_class(item: dict[str, Any]) -> str:
    action_class = str(item.get("action_class", ""))
    if action_class == "INTERNAL_EXECUTABLE":
        return "EXECUTE_INTERNAL"
    if action_class == "READY_POLICY_GOVERNED":
        return "PREPARE_AND_HOLD"
    if action_class == "EXECUTION_AUTHORIZED":
        return "REVALIDATE_EXTERNAL_HANDOFF"
    if action_class == "MANUAL_NATIVE":
        return "FOUNDER_MANUAL_NATIVE"
    if action_class == "SPECIFIC_APPROVAL_REQUIRED":
        return "PREPARE_APPROVAL_PACKET"
    return "BLOCK_AND_EXPLAIN"


def _priority_bucket(item: dict[str, Any], primary_id: str | None) -> str:
    if primary_id and str(item.get("id", "")) == primary_id:
        return "P0_PRIMARY_WIP"
    score = float(item.get("priority_score", 0) or 0)
    if score >= 40:
        return "P1_HIGH"
    if score >= 20:
        return "P2_MEDIUM"
    return "P3_BACKLOG"


def _validate_workloads(workloads: dict[str, Any]) -> None:
    if workloads.get("schema") != WORKLOAD_SCHEMA:
        raise ValueError("wrong_workload_schema")
    available = set((workloads.get("roles") or {}).keys())
    missing = ROLES - available
    if missing:
        raise ValueError(f"missing_workload_roles:{','.join(sorted(missing))}")
    if bool((workloads.get("workload_cadence") or {}).get("new_permanent_agent_created")):
        raise ValueError("permanent_agent_creation_not_allowed")
    if bool((workloads.get("workload_cadence") or {}).get("new_timer_created")):
        raise ValueError("new_timer_not_allowed")


def build_workload_queue(command: dict[str, Any], workloads: dict[str, Any]) -> dict[str, Any]:
    if command.get("schema") != COMMAND_SCHEMA:
        raise ValueError("wrong_command_schema")
    _validate_workloads(workloads)

    truth = command.get("truth_statement") or {}
    required_truth = {
        "ranking_does_not_create_relationship",
        "ranking_does_not_create_revenue",
        "readiness_does_not_equal_execution_authority",
        "planner_never_sends_external",
        "planner_never_issues_execution_authority",
    }
    if not all(bool(truth.get(key)) for key in required_truth):
        raise ValueError("commercial_truth_contract_incomplete")

    primary = command.get("primary_focus") if isinstance(command.get("primary_focus"), dict) else None
    primary_id = str(primary.get("id")) if primary else None

    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    for source_name in (
        "founder_top_5",
        "approval_queue",
        "ready_policy_governed_queue",
        "execution_authorized_queue",
        "manual_native_queue",
        "blocked_queue",
    ):
        source = command.get(source_name, [])
        if not isinstance(source, list):
            continue
        for raw in source:
            if not isinstance(raw, dict):
                continue
            item_id = str(raw.get("id", "")).strip()
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            item = dict(raw)
            role = _role_for(item)
            role_contract = (workloads.get("roles") or {}).get(role) or {}
            packet_class = _packet_class(item)
            safe_internal = packet_class == "EXECUTE_INTERNAL" and str(item.get("proposed_action", "")) in INTERNAL_ACTIONS
            items.append(
                {
                    "work_item_id": item_id,
                    "owner_role": role,
                    "owner_maps_to": role_contract.get("maps_to", []),
                    "priority_bucket": _priority_bucket(item, primary_id),
                    "packet_class": packet_class,
                    "stage": item.get("stage", "ATTENTION"),
                    "proposed_action": item.get("proposed_action", "internal_review"),
                    "channel": item.get("channel", "internal"),
                    "action_class": item.get("action_class"),
                    "authority_reason": item.get("authority_reason"),
                    "objective": item.get("objective") or item.get("next_action") or item.get("proposed_action") or "review",
                    "evidence_refs": item.get("evidence_refs", []),
                    "safe_internal_execute": safe_internal,
                    "external_effect_allowed_by_router": False,
                    "required_output": {
                        "result_summary": True,
                        "evidence_or_source_refs": True,
                        "truth_state_change": "ONLY_IF_CANONICAL_EVIDENCE_ALREADY_SUPPORTS_IT",
                        "next_action": True,
                        "approval_or_block_reason": True,
                    },
                }
            )

    items.sort(key=lambda x: (0 if x["priority_bucket"] == "P0_PRIMARY_WIP" else 1, x["priority_bucket"], x["work_item_id"]))
    per_role: dict[str, list[str]] = {role: [] for role in sorted(ROLES)}
    for item in items:
        per_role[item["owner_role"]].append(item["work_item_id"])

    return {
        "schema": "dealix.commercial_agent_workload_queue.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_command_schema": COMMAND_SCHEMA,
        "source_workload_schema": WORKLOAD_SCHEMA,
        "north_star": "FIRST_VERIFIED_PAID_PILOT",
        "architecture": {
            "new_permanent_agents": 0,
            "new_schedulers": 0,
            "reuse_existing_agent_council": True,
            "reuse_existing_company_brain": True,
            "reuse_existing_opportunity_graph": True,
            "reuse_existing_approval_center": True,
            "reuse_existing_proof_ledger": True,
        },
        "authority": {
            "router_can_execute_internal_only": True,
            "router_can_send_external": False,
            "router_can_publish": False,
            "router_can_merge_main": False,
            "router_can_charge_or_refund": False,
            "execution_authorized_items_are_handoff_only": True,
            "governance_revalidation_required_before_external_effect": True,
        },
        "primary_wip_id": primary_id,
        "work_items": items,
        "per_role_queue": per_role,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a Dealix Commercial Autopilot command into the existing Agent Council workloads.")
    parser.add_argument("--command", required=True, help="Commercial Autopilot command JSON path")
    parser.add_argument(
        "--workloads",
        default=str(Path(__file__).resolve().parents[2] / "data" / "commercial" / "agent_council_growth_workloads.json"),
        help="Existing Agent Council growth workloads JSON path",
    )
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    command = json.loads(Path(args.command).read_text(encoding="utf-8"))
    workloads = json.loads(Path(args.workloads).read_text(encoding="utf-8"))
    result = build_workload_queue(command, workloads)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".tmp")
        tmp.write_text(payload, encoding="utf-8")
        tmp.replace(target)
        print(f"DEALIX_COMMERCIAL_AGENT_WORKLOAD_QUEUE={target}")
    else:
        print(payload, end="")

    print("DEALIX_COMMERCIAL_AGENT_WORKLOAD_ROUTER=PASS")
    print("NEW_PERMANENT_AGENTS=0")
    print("NEW_SCHEDULERS=0")
    print("EXTERNAL_EFFECTS=HANDOFF_ONLY")


if __name__ == "__main__":
    main()
